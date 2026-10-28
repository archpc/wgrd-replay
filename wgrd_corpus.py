"""Read-only replay corpus inventory. Reports can contain private player metadata."""
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import sys

from wgrd_replay import ReplayFormatError, parse_header, parse_replay
from wgrd_timeline import build_timeline


def _inspect(path, headers_only):
    row = {"filename": path.name, "source_path": str(path), "size": None,
           "sha256": None, "game_version": None, "compatibility": "error",
           "duration_seconds": None, "slot_to_player_identity": None,
           "errors": []}
    stage = "read"
    try:
        data = path.read_bytes()
        row.update(size=len(data), sha256=hashlib.sha256(data).hexdigest())
        stage = "header"
        header, metadata = parse_header(data)
        try:
            json.dumps(metadata, allow_nan=False)
        except ValueError as error:
            raise ReplayFormatError("non-finite metadata value cannot be inventoried") from error
        game = metadata.get("game", {})
        row.update(game_version=header["game_version"],
                   container_version=header["container_version"],
                   map=game.get("Map"), game_mode_raw=game.get("GameMode"),
                   game_type_raw=game.get("GameType"),
                   victory_condition_raw=game.get("VictoryCond"),
                   configured_time_limit_raw=game.get("TimeLimit"),
                   players={k: v for k, v in metadata.items() if k.startswith("player_")},
                   layout_evidence=("build_59638" if header["game_version"] == "59638"
                                    else "inferred_from_59638"))
        row["digest_valid"] = hashlib.sha224(data[0x28:]).hexdigest() == header["sha224_hex"]
        if headers_only:
            row["compatibility"] = "not_checked" if row["digest_valid"] else "error"
            if not row["digest_valid"]:
                row["errors"].append({"stage": "digest", "reason": "SHA-224 mismatch"})
            return row
        stage = "container"
        parsed = parse_replay(data)
        records = parsed["commands"]
        statuses, opcodes = Counter(), Counter()
        failures = []
        declared = decoded_count = 0
        for record in records:
            decoded = record["command_decode"]
            statuses[decoded["status"]] += 1
            declared += record["count"]
            decoded_count += len(decoded["commands"])
            opcodes.update("0x%02x" % c["opcode"] for c in decoded["commands"])
            if decoded["status"] not in ("complete", "framed"):
                tail = bytes.fromhex(decoded["remaining_hex"])
                failures.append({"frame": record["frame"], "slot": record["slot"],
                                 "chunk_offset": record["offset"],
                                 "command_offset": decoded["consumed_bytes"],
                                 "file_offset": record["offset"] + 30 + decoded["consumed_bytes"],
                                 "status": decoded["status"], "reason": decoded.get("reason"),
                                 "next_byte_hex": tail[:1].hex() or None,
                                 "unconsumed_bytes": len(tail),
                                 "undecoded_commands": record["count"] - len(decoded["commands"])})
        row.update(frames=parsed["stats"]["frames"],
                   slots_per_frame=parsed["stats"].get("slots_per_frame"),
                   observed_slots=list(range(parsed["stats"].get("slots_per_frame", 0))),
                   declared_commands=declared, decoded_commands=decoded_count,
                   decoded_opcodes=dict(sorted(opcodes.items())),
                   block_statuses=dict(sorted(statuses.items())),
                   unknown_chunks=[{"offset": c["offset"], "tag_hex": c["tag_hex"],
                                    "payload_size": len(c["payload_hex"]) // 2}
                                   for c in parsed["unknown_chunks"]],
                   decode_failures=failures,
                   compatibility=("unsupported" if failures or parsed["unknown_chunks"]
                                  else "structurally_compatible"))
        stage = "timeline"
        timeline = build_timeline(parsed)
        row["timeline"] = {"events": len(timeline["events"]),
                           "unresolved_spans": len(timeline["unresolved_spans"]),
                           "interpretations": timeline["stats"]["interpretations"]}
    except Exception as error:
        # A parser crash must fail this file, not discard the rest of the corpus.
        row["errors"].append({"stage": stage, "type": type(error).__name__, "reason": str(error),
                              "unexpected": not isinstance(error, (OSError, ReplayFormatError))})
        row["compatibility"] = "error"
    return row


def inventory(paths, *, headers_only=False):
    """Inspect explicit files, deduplicating paths, not identical content."""
    rows = [_inspect(p, headers_only) for p in sorted({Path(p).expanduser().resolve() for p in paths})]
    return {"schema": "wgrd_corpus/1", "mode": "headers" if headers_only else "full",
            "limitations": ["Structural fit does not verify semantics or execution outcomes.",
                            "Frame duration and slot-to-player identity remain unresolved.",
                            "TimeLimit is configuration, not observed match duration.",
                            "Opcode counts include decoded prefixes only; undecoded tails are not scanned."],
            "replays": rows,
            "totals": {"files": len(rows), "bytes": sum(r["size"] or 0 for r in rows),
                       "unique_sha256": len({r["sha256"] for r in rows if r["sha256"]}),
                       "versions": dict(sorted(Counter(str(r["game_version"]) for r in rows).items())),
                       "compatibility": dict(sorted(Counter(r["compatibility"] for r in rows).items()))}}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("paths", nargs="+", help="files or directories (recursive, no symlink-directory traversal)")
    ap.add_argument("--headers-only", action="store_true", help="hash and inspect metadata, skip frame/command decoding")
    ap.add_argument("--expect", type=Path, help="compare against a previously emitted JSON inventory")
    args = ap.parse_args(argv)
    paths = []
    def walk_error(error):
        raise error
    try:
        for source in args.paths:
            path = Path(source).expanduser()
            if path.is_dir():
                for root, _, files in os.walk(path, onerror=walk_error, followlinks=False):
                    paths.extend(Path(root) / f for f in files if f.lower().endswith(".wargamerpl2"))
            else:
                paths.append(path)
        if not paths:
            ap.error("no replay files found")
        expected = json.loads(args.expect.read_text()) if args.expect else None
    except (OSError, ValueError) as error:
        ap.error(str(error))
    report = inventory(paths, headers_only=args.headers_only)
    json.dump(report, sys.stdout, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False)
    sys.stdout.write("\n")
    mismatch = args.expect is not None and expected != report
    if mismatch:
        print("baseline mismatch: inventory changed", file=sys.stderr)
    failed = any(r["compatibility"] in ("error", "unsupported") for r in report["replays"])
    return 1 if mismatch or failed else 0


if __name__ == "__main__":
    sys.exit(main())
