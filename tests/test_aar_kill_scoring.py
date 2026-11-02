"""Kill-scoring chain checks for revision 131544 (causal chain section 10).

Byte checks pin the static data flow in the original executable. Trace checks
record what the two retained captures establish about it. Neither proves a
scored kill: the score-credit function itself was never observed.
"""
import hashlib
import json
import os
from pathlib import Path
import struct
import unittest

ARTIFACTS = Path(os.environ.get("WGRD_ARTIFACTS_DIR",
                                Path.home() / ".hermes" / "artifacts" / "wgrd-replay"))
EXE = ARTIFACTS / "game" / "win64" / "WarGame3.exe"
EXE_SHA256 = "5eaa6d6168c9570ff9789bffb3b2cc16fd908be61263b12fcc1e8b2f09efc75d"
TRACES = {
    "combat": (ARTIFACTS / "aar-20261102T050816Z" / "wgrd-aar-combat-20261102-01.jsonl",
               "607ee419a674b554051cec998ca8ba619de5c11c8e9de277f071fd7d62f2ba74"),
    "v3": (ARTIFACTS / "aar-v3-20261102T082918Z" / "native-v3b-replay.jsonl",
           "d6a03dc0ca4c4e7400928eb89ce9b05f19739f7e7ca75ca0dffae50bda0d11ec"),
}
# VA -> exact instruction bytes. Section 10 explains each link.
CHAIN = {
    0xc95121: "8b770c",        # esi = entry+0x0c (credited team object)
    0xc95188: "8b4710",        # eax = entry+0x10 (shooter unit descriptor)
    0xc951e6: "ff7544",        # push entry+0x10 as apply arg2
    0xc951fd: "ff5558",        # call vtbl+0x98 (0xc9f910, the impact hook)
    0xc95292: "89b314020000",  # module+0x214 = credited team object
    0xc95298: "898310020000",  # module+0x210 = shooter unit descriptor
    0xc9534b: "8b465c",        # ShooterTeamNumber = team object +0x5c
    0xb9b86c: "8b8714020000",  # score credit reads module+0x214
    0xb9b875: "8b8710020000",  # score credit reads module+0x210
    0xb6a58a: "8d4e70",        # stats +0x70: points by shooter descriptor
    0xb6a5b1: "8d4e64",        # stats +0x64: kills by victim descriptor
    0xb6a5d4: "ff4624",        # stats +0x24: total kills
    0xb7a4a0: "8b8134010000",  # TTeam stats object = team +0x134
    0xa4a337: "83c064",        # GetStatsDescriptorsKilled returns stats +0x64
    0xa75c98: "837e20ff",      # owner destroy: branch on unit +0x20 == -1
    0xa75cb6: "e8358d0800",    # +0x20 != -1: post TIAKillGameplayMessage
    0xa75cfa: "ff5248",        # +0x20 == -1: direct vtbl+0x48 (0xa79680)
}
VTABLES = {0x199440c: (0x3c, 0xb9b680), 0x19b5b08: (0x98, 0xc9f910)}
APPLY_RETURN = "0xc95200"
UNIT_DESCRIPTOR_VTABLE = 0x19a8858  # TUniteAuSolDescriptor


def _pinned(path, sha):
    if not path.exists():
        raise unittest.SkipTest("private artifact unavailable: %s" % path.name)
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != sha:
        raise AssertionError("private artifact integrity mismatch: %s" % path)
    return data


class StaticKillScoringChain(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.exe = _pinned(EXE, EXE_SHA256)
        pe = struct.unpack_from("<I", cls.exe, 0x3c)[0]
        count = struct.unpack_from("<H", cls.exe, pe + 6)[0]
        optional = struct.unpack_from("<H", cls.exe, pe + 20)[0]
        cls.sections = []
        for index in range(count):
            offset = pe + 24 + optional + 40 * index
            _, va, raw_size, raw = struct.unpack_from("<IIII", cls.exe, offset + 8)
            cls.sections.append((0x400000 + va, raw_size, raw))

    def read(self, va, size):
        for base, raw_size, raw in self.sections:
            if base <= va < base + raw_size:
                return self.exe[raw + va - base:raw + va - base + size]
        raise KeyError(hex(va))

    def test_instruction_bytes(self):
        for va, expected in CHAIN.items():
            with self.subTest(va=hex(va)):
                self.assertEqual(self.read(va, len(expected) // 2).hex(), expected)

    def test_virtual_slots(self):
        for vtable, (slot, target) in VTABLES.items():
            with self.subTest(vtable=hex(vtable)):
                self.assertEqual(struct.unpack("<I", self.read(vtable + slot, 4))[0], target)


class RetainedTraceBoundary(unittest.TestCase):
    def records(self, name):
        path, sha = TRACES[name]
        return [json.loads(line) for line in _pinned(path, sha).splitlines()]

    def test_impact_hook_is_the_c95040_apply_call(self):
        for name in TRACES:
            enters = [r for r in self.records(name)
                      if r.get("hook") == "impact_apply_candidate" and r["event"] == "enter"]
            with self.subTest(trace=name):
                self.assertEqual(len(enters), 28)
                self.assertEqual({r["return_address"] for r in enters}, {APPLY_RETURN})
                for record in enters:
                    arg2 = next(x["result"]["hex"] for x in record["reads"]
                                if x["source"] == "arg2" and x["offset"] == 0)
                    vtable = struct.unpack("<I", bytes.fromhex(arg2[:8]))[0]
                    self.assertEqual(vtable, UNIT_DESCRIPTOR_VTABLE)

    def test_observed_destroys_took_the_message_branch(self):
        # Every observed owner destroy has unit +0x20 != -1, so 0xa75c70 posted
        # TIAKillGameplayMessage instead of calling vtbl+0x48 directly. The
        # message-to-score-credit edge is unresolved.
        for name in TRACES:
            fields = []
            for record in self.records(name):
                if record.get("hook") == "owner_destroy_candidate" and record["event"] == "enter":
                    block = next(x["result"]["hex"] for x in record["reads"]
                                 if x["source"] == "ecx" and x["offset"] == 0)
                    fields.append(struct.unpack_from("<i", bytes.fromhex(block), 0x20)[0])
            with self.subTest(trace=name):
                self.assertEqual(len(fields), 6)
                self.assertNotIn(-1, fields)


if __name__ == "__main__":
    unittest.main()
