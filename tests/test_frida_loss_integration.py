"""Controller wiring under a fake Frida device: exit paths and trace evidence.

Offline integration coverage for the loss-accounting wiring in run_trace:
transport loss, late/duplicate delivery, install/stop RPC failures, legacy
shape preservation. No game, no live attach, no private evidence. The fake
device delivers scripted records through the real message handler and stop
summary through the real finalizer, so the audit, drain and exit decision are
executed, not mocked away.
"""
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import threading
import time
import types
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "instrumentation"))
import wgrd_frida  # noqa: E402

REVISION_MARKER = b"####SVNREVISION####0000131544####SVNREVISION####"


class FakeScript:
    def __init__(self, mode):
        self.mode = mode
        self._message = None
        self.exports_sync = types.SimpleNamespace(
            inspect=self._inspect, install=self._install, stop=self._stop)

    def on(self, name, cb):
        if name == "message":
            self._message = cb

    def load(self):
        pass

    def unload(self):
        pass

    def _inspect(self):
        return {"name": "wargame3.exe", "path": "fake", "base": "0x400000",
                "size": 1, "arch": "ia32", "pointer_size": 4, "mz": 0x5A4D,
                "machine": 0x14C, "entries": []}

    def _install(self):
        if self.mode.get("install_raises"):
            raise RuntimeError("simulated install RPC failure")
        return {"installed": 1}

    def _stop(self):
        if self.mode.get("stop_raises"):
            raise RuntimeError("simulated stop RPC failure")
        summary = {"counts": {"wrapper": 2}, "filtered": {}, "emitted": 2,
                   "suppressed": 0, "callback_errors": 0, "stale_frames": 0,
                   "stack_mismatches": 0,
                   "outstanding_threads": self.mode.get("outstanding", 0)}
        if self.mode["accounting"]:
            summary["loss_accounting"] = {
                "last_sequence": self.mode.get("sender_last", 2),
                "send_failures": self.mode.get("send_failures", 0)}
        return summary

    def deliver(self, payload):
        self._message({"type": "send", "payload": payload}, None)


class FakeSession:
    def __init__(self, script):
        self.script = script
        self.source = None

    def on(self, name, cb):
        pass

    def create_script(self, source):
        self.source = source
        return self.script

    def detach(self):
        pass


class FakeFridaTraceTests(unittest.TestCase):
    def run_case(self, mode):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        directory = Path(tmp.name)
        image = directory / "fake-wargame3.exe"
        image.write_bytes(b"MZ" + b"0" * 32 + REVISION_MARKER + b"0" * 64)
        script = FakeScript(mode)
        session = FakeSession(script)
        fake = types.ModuleType("frida")
        fake.__version__ = "17.0.0-sim"
        fake.get_local_device = lambda: types.SimpleNamespace(
            enumerate_processes=lambda: [types.SimpleNamespace(pid=4242, name="wargame3.exe")],
            attach=lambda pid: session)

        state = {"delivered": False}

        def wait(_self, timeout=None):
            if not state["delivered"]:
                state["delivered"] = True
                for seq in range(1, mode.get("records", 1) + 1):
                    if seq in mode.get("drop", set()):
                        continue
                    payload = {"event": "enter", "call_id": seq}
                    if mode["accounting"]:
                        payload["sequence"] = seq
                    script.deliver(payload)
            return False

        dup_after = mode.get("dup_after_finalize")
        if dup_after is not None:
            original_stop = script.exports_sync.stop

            def stop_then_late_dup():
                summary = original_stop()

                def late():
                    time.sleep(mode.get("late_delay", 0.05))
                    script.deliver({"sequence": dup_after, "event": "enter", "call_id": 99})

                threading.Thread(target=late, daemon=True).start()
                return summary

            script.exports_sync.stop = stop_then_late_dup

        config = {"revision": "131544",
                  "sha256": hashlib.sha256(image.read_bytes()).hexdigest(),
                  "module": "wargame3.exe", "ghidra_base": "0x400000",
                  "hooks": [{"name": "wrapper", "va": "0xb2be30", "args": 0,
                             "sample_every": 1}]}
        if mode["accounting"]:
            config["loss_accounting"] = True
        if mode.get("allow_outstanding"):
            config["loss_allow_outstanding_threads"] = True
        config_path = directory / "config.json"
        config_path.write_text(json.dumps(config))
        output = directory / "trace.jsonl"
        args = types.SimpleNamespace(config=str(config_path), output=str(output),
                                     pid=4242, seconds=1, event_limit=1000, hook=None)
        exit_code = 0
        with contextlib.ExitStack() as stack:
            stack.enter_context(mock.patch.object(wgrd_frida, "os", types.SimpleNamespace(name="nt")))
            stack.enter_context(mock.patch.object(wgrd_frida, "verify_loaded", lambda *a, **k: None))
            stack.enter_context(mock.patch.object(
                wgrd_frida, "process_identity", lambda pid: (str(image), 12345)))
            stack.enter_context(mock.patch.dict(sys.modules, {"frida": fake}))
            stack.enter_context(mock.patch.object(threading.Event, "wait", wait))
            stack.enter_context(contextlib.redirect_stdout(io.StringIO()))
            try:
                wgrd_frida.run_trace(args)
            except Exception:
                exit_code = 1
        events = [json.loads(line) for line in output.read_text().splitlines() if line.strip()]
        return {"exit": exit_code, "events": events,
                "kinds": [e["event"] for e in events],
                "loss": [e for e in events if e["event"].startswith("loss_accounting")],
                "js_source": session.source}

    def complete(self, result):
        return [e for e in result["loss"]
                if e["event"] == "loss_accounting" and e.get("complete")]

    def test_clean_accounting_completes(self):
        result = self.run_case(dict(accounting=True, records=3, sender_last=3))
        self.assertEqual(result["exit"], 0)
        self.assertEqual(len(self.complete(result)), 1)
        self.assertEqual(self.complete(result)[0]["received_records"], 3)
        self.assertIn('"loss_accounting":true', result["js_source"])

    def test_dropped_middle_record_fails(self):
        result = self.run_case(dict(accounting=True, records=3, sender_last=3, drop={2}))
        self.assertEqual(result["exit"], 1)
        self.assertFalse(self.complete(result))
        self.assertTrue(any(e["event"] == "loss_accounting_failure" for e in result["loss"]))

    def test_dropped_tail_record_fails_on_totals(self):
        result = self.run_case(dict(accounting=True, records=3, sender_last=3, drop={3}))
        self.assertEqual(result["exit"], 1)
        self.assertFalse(self.complete(result))

    def test_sender_send_failure_counter_fails(self):
        result = self.run_case(dict(accounting=True, records=3, sender_last=3, send_failures=1))
        self.assertEqual(result["exit"], 1)
        self.assertFalse(self.complete(result))

    def test_legacy_shape_is_preserved(self):
        result = self.run_case(dict(accounting=False, records=2))
        self.assertEqual(result["exit"], 0)
        self.assertEqual(result["loss"], [])
        self.assertFalse(any("sequence" in e for e in result["events"]))
        # The script source always contains the opt-in code paths; the injected
        # CONFIG must not carry the key in legacy mode.
        config_line = next(line for line in result["js_source"].splitlines()
                           if line.startswith("const config = "))
        self.assertNotIn("loss_accounting", config_line)

    def test_stop_rpc_failure_writes_no_complete_audit(self):
        result = self.run_case(dict(accounting=True, records=2, sender_last=2, stop_raises=True))
        self.assertEqual(result["exit"], 1)
        self.assertFalse(self.complete(result))

    def test_install_failure_skips_audit(self):
        # R2 regression: a capture that failed before any records flowed must
        # not carry a vacuous loss_accounting complete:true (0 == 0 passes).
        result = self.run_case(dict(accounting=True, records=0, sender_last=0,
                                    install_raises=True))
        self.assertEqual(result["exit"], 1)
        self.assertFalse(self.complete(result))
        self.assertTrue(any(e["event"] == "loss_accounting_skipped" for e in result["loss"]))

    def test_late_duplicate_after_finalize_fails(self):
        # R1 regression: a duplicate delivered after the audit closed must
        # still reach the exit decision via the bounded drain.
        result = self.run_case(dict(accounting=True, records=2, sender_last=2,
                                    dup_after_finalize=2, late_delay=0.05))
        self.assertEqual(result["exit"], 1)
        self.assertTrue(any(e["event"] == "loss_accounting_failure" for e in result["loss"]))

    def test_explicit_allowance_accepts_one_outstanding_thread(self):
        result = self.run_case(dict(accounting=True, records=2, sender_last=2,
                                    outstanding=1, allow_outstanding=True))
        self.assertEqual(result["exit"], 0)
        self.assertEqual(len(self.complete(result)), 1)

    def test_outstanding_thread_without_allowance_fails(self):
        result = self.run_case(dict(accounting=True, records=2, sender_last=2, outstanding=1))
        self.assertEqual(result["exit"], 1)
        self.assertFalse(self.complete(result))


if __name__ == "__main__":
    unittest.main()