#!/usr/bin/env python3
"""Research preservation manifest: create or verify.

    python3 -B research/maintenance/preservation_manifest.py create > research/maintenance/preservation-manifest.json
    python3 -B research/maintenance/preservation_manifest.py verify research/maintenance/preservation-manifest.json

`create` lists every tracked file under research/, plus the root research
documents (FORMAT.md, REA-NOTES-59638.md, REPLAY-RESEARCH.md, NEXT-STEPS.md),
with size, SHA-256 and a category. `verify` recomputes hashes for every entry:
an entry is OK when its file exists at `path` (or at `moved_to` if set) with the
same SHA-256; entries listed under `allowed_changes` may differ (active docs
edited intentionally). Any other mismatch or missing file -> exit 1.

The manifest is the baseline for the 2026-10-26 maintenance milestone; it is not
a backup. Git history holds the content; this file proves nothing was lost.
"""
# Verify checks listed entries only, not unlisted additions or entry_count. It exempts
# allowed_changes from hash comparison, and does not validate disposition or category.
# Missing/unreadable manifests raise; verify returns 1 when listed entries fail.
import hashlib
import json
import os
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
ROOT_DOCS = ["FORMAT.md", "REA-NOTES-59638.md", "REPLAY-RESEARCH.md", "NEXT-STEPS.md", "README.md"]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def category(rel):
    if rel.startswith("research/evidence/"):
        return "evidence"
    if rel.startswith("research/chatgpt-session-"):
        return "historical-session-archive"
    if rel.startswith("research/unit-data/"):
        return "static-data-index"
    if rel.startswith("research/reports/"):
        return "generated-report"
    if rel.startswith("research/maintenance/"):
        return "maintenance"
    if rel.endswith("-PLAN.md") or rel.endswith("/PLAN.md"):
        return "historical-plan"
    if rel.endswith(".py"):
        return "research-script"
    if rel.endswith(".json"):
        return "generated-or-validation-data"
    if rel.endswith(".md"):
        return "research-note" if rel.startswith("research/") else "root-doc"
    return "other"


def tracked_files():
    # Uses `git ls-files`, so untracked files under research/ are excluded at create time.
    # Hashes are taken from the working tree, not the index.
    out = subprocess.check_output(["git", "-C", ROOT, "ls-files", "-z", "research", *ROOT_DOCS])
    return sorted(p.decode() for p in out.split(b"\0") if p)


def create():
    entries = []
    for rel in tracked_files():
        full = os.path.join(ROOT, rel)
        entries.append({"path": rel, "size": os.path.getsize(full), "sha256": sha256(full),
                        "category": category(rel), "disposition": "unchanged", "moved_to": None})
    head = subprocess.check_output(["git", "-C", ROOT, "rev-parse", "HEAD"]).decode().strip()
    return {"baseline_commit": head, "entry_count": len(entries), "allowed_changes": [], "entries": entries}


def verify(manifest):
    # ASCII WARNING: "problems=0" covers only listed entries. Additions and changes
    # to unlisted files pass silently; allowed_changes bypasses the hash check.
    #    _____
    #   |     |  <- new files? not here.
    #   | o o |
    #   |  ^  |  allowed_changes = hash exempt
    #   |_____|
    bad = []
    for e in manifest["entries"]:
        rel = e.get("moved_to") or e["path"]
        full = os.path.join(ROOT, rel)
        if not os.path.exists(full):
            bad.append(("missing", e["path"], rel))
            continue
        # allowed_changes exempts by original path even when moved_to is set.
        if sha256(full) != e["sha256"] and e["path"] not in manifest.get("allowed_changes", []):
            bad.append(("changed", e["path"], rel))
    ok = len(manifest["entries"]) - len(bad)
    print("entries=%d ok=%d problems=%d allowed_changes=%d" % (
        len(manifest["entries"]), ok, len(bad), len(manifest.get("allowed_changes", []))))
    for b in bad:
        print("  %-8s %s -> %s" % b)
    return 1 if bad else 0


def main(argv):
    if len(argv) >= 2 and argv[1] == "create":
        json.dump(create(), sys.stdout, indent=1, sort_keys=True)
        sys.stdout.write("\n")
        return 0
    if len(argv) >= 3 and argv[1] == "verify":
        # Note: the file handle is not closed explicitly (behaviour kept; CLI is short-lived).
        return verify(json.load(open(argv[2])))
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
