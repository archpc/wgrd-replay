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
