import importlib.util
import pathlib
import unittest

MODULE_PATH = pathlib.Path(__file__).resolve().parents[1] / "instrumentation" / "wgrd_frida.py"
SPEC = importlib.util.spec_from_file_location("wgrd_frida", MODULE_PATH)
wgrd_frida = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(wgrd_frida)


class AddressTranslationTests(unittest.TestCase):
    def test_rebased_function(self):
        self.assertEqual(wgrd_frida.runtime_address(0x500000, 0x400000, 0xB2BE30, 0x2000000), 0xC2BE30)

    def test_address_outside_image_is_rejected(self):
        for address in (0x3FFFFF, 0x2400000):
            with self.subTest(address=address), self.assertRaises(ValueError):
                wgrd_frida.runtime_address(0x500000, 0x400000, address, 0x2000000)


class PeMappingTests(unittest.TestCase):
    def image(self):
        import struct
        image = bytearray(1024)
        image[0:2] = b"MZ"
        struct.pack_into("<I", image, 0x3C, 0x80)
        image[0x80:0x84] = b"PE\0\0"
        struct.pack_into("<HH", image, 0x84, 0x14C, 1)
        struct.pack_into("<H", image, 0x94, 0xE0)
        struct.pack_into("<H", image, 0x98, 0x10B)
        struct.pack_into("<IIII", image, 0x178 + 8, 0x300, 0x1000, 0x200, 0x200)
        image[0x210:0x214] = b"test"
        return bytes(image)

    def test_maps_file_backed_rva(self):
        self.assertEqual(wgrd_frida.pe_bytes_at_rva(self.image(), 0x1010, 4), b"test")

    def test_rejects_unbacked_and_non_pe(self):
        for image, rva in ((self.image(), 0x1200), (b"bad", 0)):
            with self.subTest(rva=rva), self.assertRaises(ValueError):
                wgrd_frida.pe_bytes_at_rva(image, rva, 4)


class LoadedIdentityTests(PeMappingTests):
    def data(self):
        import hashlib
        image = self.image()
        config = {"sha256": hashlib.sha256(image).hexdigest(), "module": "wargame3.exe",
                  "ghidra_base": "0x400000", "hooks": [{"name": "one", "va": "0x401010"}]}
        info = {"name": "wargame3.exe", "path": "C:\\Game\\wargame3.exe", "arch": "ia32",
                "pointer_size": 4, "mz": 0x5A4D, "machine": 0x14C, "base": "0x500000", "size": 0x3000,
                "entries": [{"name": "one", "address": "0x501010", "executable": True,
                             "bytes": {"ok": True, "hex": image[0x210:0x220].hex()}}]}
        return config, image, info

    def test_validates_rebased_image_and_entry(self):
        config, image, info = self.data()
        self.assertIsNone(wgrd_frida.verify_loaded(config, image, info, info["path"]))

    def test_rejects_mismatches(self):
        for field in ("path", "machine", "bytes", "address", "executable", "disk"):
            config, image, info = self.data()
            if field == "path": info["path"] = "C:\\Other\\wargame3.exe"
            elif field == "machine": info["machine"] = 0xAA64
            elif field == "bytes": info["entries"][0]["bytes"]["hex"] = "00" * 16
            elif field == "address": info["entries"][0]["address"] = "0x501011"
            elif field == "executable": info["entries"][0]["executable"] = False
            else: image = image + b"x"
            with self.subTest(field=field), self.assertRaises(ValueError):
                wgrd_frida.verify_loaded(config, image, info, "C:\\Game\\wargame3.exe")


class TraceSequenceTests(unittest.TestCase):
    def sender(self, last=1):
        return {"loss_accounting": {"last_sequence": last, "send_failures": 0},
                "suppressed": 0, "callback_errors": 0, "stale_frames": 0,
                "stack_mismatches": 0, "outstanding_threads": 0}

    def test_finalization_rejects_missing_tail_and_any_incomplete_sender_state(self):
        import copy
        variants = []
        for key in ("suppressed", "callback_errors", "stale_frames",
                    "stack_mismatches", "outstanding_threads"):
            for value in (1, None, False):
                summary = self.sender()
                summary[key] = value
                variants.append(summary)
        for key, value in (("last_sequence", 2), ("last_sequence", True),
                           ("send_failures", 1), ("send_failures", None)):
            summary = self.sender()
            summary["loss_accounting"][key] = value
            variants.append(summary)
        variants.extend(({}, {"loss_accounting": None}))
        for summary in variants:
            audit = wgrd_frida.TraceSequenceAudit()
            audit.observe({"sequence": 1})
            with self.subTest(summary=summary), self.assertRaises(ValueError):
                audit.finish(copy.deepcopy(summary))

    def test_no_completion_after_discontinuity_or_late_records(self):
        audit = wgrd_frida.TraceSequenceAudit()
        audit.observe({"sequence": 1})
        with self.assertRaises(ValueError):
            audit.observe({"sequence": 3})
        audit.observe({"sequence": 2})
        with self.assertRaises(ValueError):
            audit.finish(self.sender(last=2))
        closed = wgrd_frida.TraceSequenceAudit()
        closed.observe({"sequence": 1})
        closed.finish(self.sender())
        with self.assertRaises(ValueError):
            closed.observe({"sequence": 2})

    def test_rejects_missing_duplicate_out_of_order_and_noninteger_sequences(self):
        for value in (None, True, 2.0, "2", 0, -1, 1, 3):
            audit = wgrd_frida.TraceSequenceAudit()
            audit.observe({"sequence": 1})
            with self.subTest(sequence=value), self.assertRaises(ValueError):
                audit.observe({"sequence": value})
            self.assertEqual(audit.last_sequence, 1)

    def test_contiguous_stream_reconciles_with_sender(self):
        audit = wgrd_frida.TraceSequenceAudit()
        audit.observe({"sequence": 1})
        audit.observe({"sequence": 2})
        result = audit.finish({"loss_accounting": {"last_sequence": 2, "send_failures": 0},
                               "suppressed": 0, "callback_errors": 0, "stale_frames": 0,
                               "stack_mismatches": 0, "outstanding_threads": 0})
        self.assertEqual(result, {"received_records": 2, "last_sequence": 2, "complete": True})


class LossAllowanceTests(unittest.TestCase):
    """The documented v4 detach allowance (one unpaired tick enter) must be
    explicit, bounded to outstanding_threads, and never stretch to 2."""

    def sender(self, last=1, **over):
        base = {"loss_accounting": {"last_sequence": last, "send_failures": 0},
                "suppressed": 0, "callback_errors": 0, "stale_frames": 0,
                "stack_mismatches": 0, "outstanding_threads": 0}
        base.update(over)
        return base

    def audit(self):
        audit = wgrd_frida.TraceSequenceAudit()
        audit.observe({"sequence": 1})
        return audit

    def test_explicit_allowance_accepts_exactly_one_outstanding_thread(self):
        result = self.audit().finish(self.sender(outstanding_threads=1),
                                     {"outstanding_threads": 1})
        self.assertTrue(result["complete"])

    def test_default_stays_strict(self):
        with self.assertRaises(ValueError):
            self.audit().finish(self.sender(outstanding_threads=1))

    def test_allowance_does_not_stretch_to_two_or_other_counters(self):
        with self.assertRaises(ValueError):
            self.audit().finish(self.sender(outstanding_threads=2),
                                {"outstanding_threads": 1})
        with self.assertRaises(ValueError):
            self.audit().finish(self.sender(suppressed=1),
                                {"outstanding_threads": 1})
        with self.assertRaises(ValueError):
            self.audit().finish(self.sender(outstanding_threads=-1),
                                {"outstanding_threads": 1})
        with self.assertRaises(ValueError):
            self.audit().finish(self.sender(outstanding_threads=True),
                                {"outstanding_threads": 1})

    def test_unknown_allowance_keys_are_rejected(self):
        with self.assertRaises(ValueError):
            self.audit().finish(self.sender(), {"suppressed": 1})


class LossAccountingRecorderTests(unittest.TestCase):
    """Receiver-side glue used by the controller message loop and finalizer."""

    def sender(self, last=1, **over):
        base = {"loss_accounting": {"last_sequence": last, "send_failures": 0},
                "suppressed": 0, "callback_errors": 0, "stale_frames": 0,
                "stack_mismatches": 0, "outstanding_threads": 0}
        base.update(over)
        return base

    def test_disabled_recorder_is_transparent(self):
        rec = wgrd_frida.LossAccountingRecorder(False)
        self.assertEqual(rec.observe({"event": "enter"}), [])
        self.assertEqual(rec.observe({"sequence": 5}), [])
        records, error = rec.finalize({})
        self.assertEqual(records, [])
        self.assertIsNone(error)

    def test_contiguous_stream_finalizes_complete(self):
        rec = wgrd_frida.LossAccountingRecorder(True)
        self.assertEqual(rec.observe({"sequence": 1}), [])
        self.assertEqual(rec.observe({"sequence": 2}), [])
        records, error = rec.finalize(self.sender(last=2))
        self.assertIsNone(error)
        self.assertEqual(records, [{"event": "loss_accounting", "received_records": 2,
                                    "last_sequence": 2, "complete": True}])

    def test_gap_emits_one_failure_and_blocks_completion(self):
        rec = wgrd_frida.LossAccountingRecorder(True)
        rec.observe({"sequence": 1})
        records = rec.observe({"sequence": 3})
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["event"], "loss_accounting_failure")
        self.assertIn("sequence", records[0]["error"])
        # No cascading failures after the first discontinuity.
        self.assertEqual(rec.observe({"sequence": 9}), [])
        records, error = rec.finalize(self.sender(last=3))
        self.assertIsNotNone(error)
        self.assertEqual(records[0]["event"], "loss_accounting_failure")

    def test_late_record_after_completion_fails(self):
        rec = wgrd_frida.LossAccountingRecorder(True)
        rec.observe({"sequence": 1})
        rec.finalize(self.sender())
        records = rec.observe({"sequence": 2})
        self.assertEqual(records[0]["event"], "loss_accounting_failure")

    def test_allowance_flag_flows_to_finalizer(self):
        rec = wgrd_frida.LossAccountingRecorder(True, allow_outstanding_threads=True)
        rec.observe({"sequence": 1})
        records, error = rec.finalize(self.sender(outstanding_threads=1))
        self.assertIsNone(error)
        self.assertTrue(records[0]["complete"])
        strict = wgrd_frida.LossAccountingRecorder(True)
        strict.observe({"sequence": 1})
        records, error = strict.finalize(self.sender(outstanding_threads=1))
        self.assertIsNotNone(error)

    def test_missing_sender_accounting_fails_closed(self):
        rec = wgrd_frida.LossAccountingRecorder(True)
        rec.observe({"sequence": 1})
        records, error = rec.finalize({"suppressed": 0})
        self.assertIsNotNone(error)
        self.assertEqual(records[0]["event"], "loss_accounting_failure")


class LossConfigValidationTests(unittest.TestCase):
    def config(self, **over):
        base = {"revision": "131544", "sha256": "a" * 64,
                "module": "wargame3.exe", "ghidra_base": "0x400000",
                "hooks": [{"name": "wrapper", "va": "0xb2be30", "args": 2, "sample_every": 1}]}
        base.update(over)
        return base

    def test_loss_accounting_must_be_boolean(self):
        for value in (1, "true", None, [], {}):
            with self.subTest(value=value), self.assertRaises(ValueError):
                wgrd_frida.validate_config(self.config(loss_accounting=value))

    def test_allowance_flag_must_be_boolean_and_requires_loss_accounting(self):
        with self.assertRaises(ValueError):
            wgrd_frida.validate_config(self.config(loss_allow_outstanding_threads=True))
        for value in (1, "yes", None):
            with self.subTest(value=value), self.assertRaises(ValueError):
                wgrd_frida.validate_config(
                    self.config(loss_accounting=True, loss_allow_outstanding_threads=value))

    def test_valid_loss_configurations_accepted(self):
        wgrd_frida.validate_config(self.config(loss_accounting=True))
        wgrd_frida.validate_config(self.config(loss_accounting=False))
        wgrd_frida.validate_config(
            self.config(loss_accounting=True, loss_allow_outstanding_threads=True))
        wgrd_frida.validate_config(self.config())


class ConfigurationTests(unittest.TestCase):
    def config(self):
        return {
            "revision": "131544", "sha256": "a" * 64,
            "module": "wargame3.exe", "ghidra_base": "0x400000",
            "hooks": [{"name": "wrapper", "va": "0xb2be30", "args": 2, "sample_every": 1}],
        }

    def test_valid_configuration(self):
        self.assertIsNone(wgrd_frida.validate_config(self.config()))

    def test_rejects_duplicate_hooks_and_unbounded_capture(self):
        for alteration in ("duplicate", "sample", "read", "phase", "indirect", "chain", "hash"):
            config = self.config()
            if alteration == "duplicate":
                config["hooks"].append(dict(config["hooks"][0]))
            elif alteration == "sample":
                config["hooks"][0]["sample_every"] = 0
            elif alteration == "read":
                config["hooks"][0]["reads"] = [{"source": "ecx", "offset": 0, "size": 129}]
            elif alteration == "phase":
                config["hooks"][0]["reads"] = [{"source": "ecx", "offset": 0, "size": 4, "phase": "after"}]
            elif alteration == "indirect":
                config["hooks"][0]["reads"] = [{"source": "ecx", "offset": 0, "size": 4, "indirect": "yes"}]
            elif alteration == "chain":
                config["hooks"][0]["reads"] = [{"source": "ecx", "offset": 0, "size": 4, "second_indirect": True}]
            else:
                config["sha256"] = "bad"
            with self.subTest(alteration=alteration), self.assertRaises(ValueError):
                wgrd_frida.validate_config(config)


if __name__ == "__main__":
    unittest.main()
