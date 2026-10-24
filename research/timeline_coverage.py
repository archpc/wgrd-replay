"""Recompute authenticated timeline census. No sample bytes emitted."""
import hashlib
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from wgrd_replay import parse_replay
from wgrd_timeline import build_timeline


def census():
    samples = Path(os.environ.get("WGRD_SAMPLES_DIR", str(Path.home() / ".hermes/artifacts/wgrd-replay/samples/raw")))
    manifest = json.loads((ROOT / "samples/manifest.json").read_text())
    rows = []
    for sample in manifest["samples"]:
        data = (samples / sample["file"]).read_bytes()
        if hashlib.sha256(data).hexdigest() != sample["sha256"]:
            raise ValueError("Sample hash mismatch: " + sample["file"])
        parsed = parse_replay(data)
        timeline = build_timeline(parsed)
        from collections import Counter
        rows.append({"sample": sample["file"], "sha256": parsed["sha256"],
                     "version": parsed["header"]["game_version"],
                     "stats": timeline["stats"],
                     "opcodes": dict(sorted(Counter("%02x" % e["opcode"] for e in timeline["events"]).items()))})
    return {"schema": "wgrd_timeline_census/1", "samples": rows}


if __name__ == "__main__":
    print(json.dumps(census(), indent=1, sort_keys=True))
