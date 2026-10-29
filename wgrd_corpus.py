"""Read-only replay corpus inventory. Reports can contain private player metadata."""
# Files or directories are accepted; directory walks match .wargamerpl2 case-insensitively
# without following symlinked directories. JSON reports use schema wgrd_corpus/1.
# Exit 0 includes headers-only "not_checked" rows; exit 1 covers incompatible files or
# baseline mismatch; exit 2 covers usage, empty walks, and unreadable/invalid baselines.
# Reports include raw player metadata and paths. Do not publish private inventories.
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
    """Return one inventory row for a single file. Never raises for file-level problems.

    Stages: read -> header -> container -> timeline in full mode. Container includes digest
    validation; headers-only checks the digest separately and can report a "digest" error.
    Failures are isolated to the row. Exceptions other than ReplayFormatError and OSError are
    flagged "unexpected": true, including parser exceptions triggered by malformed input.

    Compatibility values (row["compatibility"]):
      - "structurally_compatible": every command block is complete or framed, no unknown chunks,
        no decode failures. Structural fit only; not a semantic or execution claim.
      - "unsupported": decoded structure has an unresolved/malformed block or unknown chunk.
      - "not_checked": headers_only mode with a valid digest. The whole file was read for hashes,
        but its frame and command stream was not parsed.
      - "error": read, header, digest, container or timeline failure.
    """
    # ASCII WARNING: a "not_checked" row and exit 0 in --headers-only mode both mean the command
    # stream was never parsed. Do not treat a headers-only run as corpus validation.
    #   ,-----.
    #   | ! ! |  headers-only = body unparsed
    #   |  -  |  "not_checked" is not a pass
    #   '-----'
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
        # layout_evidence labels the version match, not semantic validation.
        # Other builds retain "inferred_from_59638" even when their bytes fit.
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
        parsed = parse_replay(data, include_empty=True)
        observed_slots = sorted({record["slot"] for record in parsed["commands"]})
        # Count only nonempty blocks; keep every pact available to the timeline.
        records = [record for record in parsed["commands"] if record["count"]]
        statuses, opcodes = Counter(), Counter()
        failures = []
        declared = decoded_count = 0
        # Each record is one pact (one slot's command block in one frame). Declared counts are
        # summed from pact headers; decoded_count comes from the decoder. Opcode counts cover
        # only the decoded prefix of each block (undecoded tails are not scanned).
        for record in records:
            decoded = record["command_decode"]
            statuses[decoded["status"]] += 1
            declared += record["count"]
            decoded_count += len(decoded["commands"])
            opcodes.update("0x%02x" % c["opcode"] for c in decoded["commands"])
            if decoded["status"] not in ("complete", "framed"):
                tail = bytes.fromhex(decoded["remaining_hex"])
                # Absolute offset = chunk start + 16-byte header + 14-byte pact
                # prefix + consumed bytes. Keep 30 in sync with parse_replay's
                # <IIIH prefix (FORMAT.md section 4).
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
                   observed_slots=observed_slots,
                   declared_commands=declared, decoded_commands=decoded_count,
                   decoded_opcodes=dict(sorted(opcodes.items())),
                   block_statuses=dict(sorted(statuses.items())),
                   unknown_chunks=[{"offset": c["offset"], "tag_hex": c["tag_hex"],
                                    "payload_size": len(c["payload_hex"]) // 2}
                                   for c in parsed["unknown_chunks"]],
                   decode_failures=failures,
                   compatibility=("unsupported" if failures or parsed["unknown_chunks"]
                                  else "structurally_compatible"))
        # Try the timeline even for unsupported structures; attribute its failures
        # to this stage rather than to the container walk.
        stage = "timeline"
        timeline = build_timeline(parsed)
        row["timeline"] = {"events": len(timeline["events"]),
                           "unresolved_spans": len(timeline["unresolved_spans"]),
                           "interpretations": timeline["stats"]["interpretations"]}
    except Exception as error:
        # A parser crash must fail this file, not discard the rest of the corpus. The broad catch
        # is deliberate; "unexpected": true distinguishes non-format exceptions, including
        # bugs triggered by malformed input, from recognized parse failures.
        # Note: row fields set before the failure (e.g. timeline counts) may remain populated.
        row["errors"].append({"stage": stage, "type": type(error).__name__, "reason": str(error),
                              "unexpected": not isinstance(error, (OSError, ReplayFormatError))})
        row["compatibility"] = "error"
    return row


def inventory(paths, *, headers_only=False):
    """Inspect explicit files, deduplicating paths, not identical content.

    Totals: "files" and "bytes" count distinct resolved paths, so byte-identical copies are
    counted once per path. "unique_sha256" counts distinct content. Headers-only rows carry no
    frame/command fields, and totals.compatibility then contains "not_checked" entries.
    """
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
    # Any unreadable directory during the walk aborts the whole run (exit 2 via ap.error). It is
    # not recorded per file, so a partial corpus is never reported as complete.
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
    # --expect is whole-report equality. The baseline includes absolute source_path values and
    # the mode field, so it is machine-path-dependent and must be made with the same mode.
    # A mismatch means "something changed", not which field changed; diff the JSON to locate it.
    mismatch = args.expect is not None and expected != report
    if mismatch:
        print("baseline mismatch: inventory changed", file=sys.stderr)
    failed = any(r["compatibility"] in ("error", "unsupported") for r in report["replays"])
    return 1 if mismatch or failed else 0


if __name__ == "__main__":
    sys.exit(main())
