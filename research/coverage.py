"""Reproduce the authenticated replay boundary census; no sample bytes emitted.

Run from any directory: python3 -B research/coverage.py > research/coverage.json
"""
import collections
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import wgrd_replay as w


def census():
    result = {"layout_build": "59638", "samples": []}
    for sample in json.loads((ROOT / "samples/manifest.json").read_text())["samples"]:
        data = Path(sample["stored_at"]).expanduser().read_bytes()
        if len(data) != sample["size"] or hashlib.sha256(data).hexdigest() != sample["sha256"]:
            raise ValueError("sample identity mismatch: " + sample["file"])
        replay = w.parse_replay(data)
        statuses, multi, opcodes, unresolved = (collections.Counter() for _ in range(4))
        opaque = collections.Counter()
        for record in replay["commands"]:
            decoded = record["command_decode"]
            status = decoded["status"]
            if status == "malformed":
                raise ValueError((sample["file"], record["offset"], decoded["reason"]))
            statuses[status] += 1
            if record["count"] > 1:
                multi[status] += 1
            if status in ("complete", "framed"):
                commands = decoded["commands"]
                if (len(commands) != record["count"]
                        or "".join(c["raw_hex"] for c in commands) != record["block_hex"]
                        or decoded["consumed_bytes"] != record["block_length"]
                        or decoded["remaining_hex"]):
                    raise ValueError("boundary/reassembly mismatch")
                offset = 0
                for command in commands:
                    if command["offset"] != offset:
                        raise ValueError("command offset mismatch")
                    offset += command["length"]
                    key = "0x%02x" % command["opcode"]
                    opcodes[key] += 1
                    if command["field_decode_status"] == "opaque":
                        opaque[key] += 1
            else:
                unresolved["0x%02x" % bytes.fromhex(decoded["remaining_hex"])[0]] += 1
        result["samples"].append({
            "file": sample["file"], "sha256": sample["sha256"],
            "game_version": replay["header"]["game_version"],
            "nonempty_blocks": len(replay["commands"]), "block_statuses": dict(statuses),
            "multi_block_statuses": dict(multi), "commands_in_split_blocks": dict(opcodes),
            "opaque_commands": dict(opaque), "unresolved_opcodes": dict(unresolved)})
    samples = result["samples"]
    result["totals"] = {
        "multi_blocks": sum(sum(s["multi_block_statuses"].values()) for s in samples),
        "fully_split_multi_blocks": sum(sum(s["multi_block_statuses"].get(k, 0)
                                            for k in ("complete", "framed")) for s in samples),
        "layout_decoded_multi_blocks": sum(s["multi_block_statuses"].get("complete", 0) for s in samples),
        "opaque_framed_multi_blocks": sum(s["multi_block_statuses"].get("framed", 0) for s in samples),
        "nonempty_blocks": sum(s["nonempty_blocks"] for s in samples),
        "fully_split_nonempty_blocks": sum(sum(s["block_statuses"].get(k, 0)
                                               for k in ("complete", "framed")) for s in samples)}
    return result


if __name__ == "__main__":
    print(json.dumps(census(), indent=2, sort_keys=True))
