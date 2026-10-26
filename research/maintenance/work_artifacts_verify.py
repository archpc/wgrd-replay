#!/usr/bin/env python3
"""Verify git-ignored work/ research artifacts against the tracked manifest.

    python3 -B research/maintenance/work_artifacts_verify.py [manifest]

Recomputes SHA-256 for every entry in
research/maintenance/work-artifacts-manifest.json and reports missing or
changed files, plus files present under work/ that are not in the manifest.
Exit 1 if anything is missing or changed. Read-only; never modifies work/.
"""
import hashlib
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
DEFAULT = os.path.join(ROOT, "research", "maintenance", "work-artifacts-manifest.json")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main(argv):
    manifest = json.load(open(argv[1] if len(argv) > 1 else DEFAULT))
    missing, changed, seen = [], [], set()
    for e in manifest["entries"]:
        full = os.path.join(ROOT, e["path"])
        seen.add(os.path.normpath(e["path"]))
        if not os.path.exists(full):
            missing.append(e["path"])
        elif sha256(full) != e["sha256"]:
            changed.append(e["path"])
    extra = []
    for dp, dn, fn in os.walk(os.path.join(ROOT, "work")):
        dn[:] = [d for d in dn if d not in ("node_modules", ".git")]
        for f in fn:
            rel = os.path.normpath(os.path.relpath(os.path.join(dp, f), ROOT))
            if rel not in seen:
                extra.append(rel)
    print("entries=%d missing=%d changed=%d untracked_new=%d" % (len(manifest["entries"]), len(missing), len(changed), len(extra)))
    for label, items in (("missing", missing), ("changed", changed), ("new", extra)):
        for p in items[:20]:
            print("  %-8s %s" % (label, p))
    return 1 if (missing or changed) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
