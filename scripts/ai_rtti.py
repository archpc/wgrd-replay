#!/usr/bin/env python3
"""Resolve MSVC RTTI type descriptors to vtables in a PE32 image.

Read-only, file-only. Never executes or loads the target.

Why this exists: WarGame3.exe (build 131544) ships no usable PDB, and its COFF
symbol table covers only a small slice of the image. MSVC RTTI descriptors are
intact, so class names, vtables and virtual methods can still be recovered
deterministically from the file bytes alone.

Layout assumed (MSVC, x86/PE32):
  TypeDescriptor        +0x0 vftable, +0x4 spare, +0x8 name (".?AV...@@")
  RTTICompleteObjectLocator
                        +0x0 signature (0 or 1), +0x4 offset, +0x8 cdOffset,
                        +0xC pTypeDescriptor, +0x10 pClassDescriptor
  vftable               slot -1 = pCOL, slot 0.. = method pointers

Address math: a section header's VirtualAddress is an RVA. Absolute VA is
ImageBase + RVA. Pointers stored in the image and in RTTI records are absolute
VAs, so every comparison happens in VA space.
"""

from __future__ import annotations

import argparse
import json
import struct
import sys
from dataclasses import dataclass, field

IMAGE_SCN_MEM_EXECUTE = 0x20000000


class ImageError(ValueError):
    """The image or a requested structure is not present/valid."""


@dataclass
class Section:
    name: str
    va: int
    vsize: int
    data: bytes
    characteristics: int = 0

    @property
    def executable(self) -> bool:
        return bool(self.characteristics & IMAGE_SCN_MEM_EXECUTE)

    @property
    def end_va(self) -> int:
        return self.va + max(self.vsize, len(self.data))


@dataclass
class Image:
    """A flat VA-addressable view of an image with a prebuilt pointer index."""

    imagebase: int
    size_of_image: int
    sections: list[Section] = field(default_factory=list)
    _index: dict[int, list[int]] | None = None

    def section_of(self, va: int) -> Section | None:
        """Section containing *va* whose file bytes actually cover it."""
        for s in self.sections:
            if s.va <= va < s.va + len(s.data):
                return s
        return None

    def read(self, va: int, size: int) -> bytes:
        s = self.section_of(va)
        if s is None:
            raise ImageError(f"0x{va:08x} is not mapped to file bytes")
        off = va - s.va
        if off + size > len(s.data):
            raise ImageError(f"0x{va:08x}+{size} crosses the end of {s.name}")
        return s.data[off:off + size]

    def u32(self, va: int) -> int:
        return struct.unpack("<I", self.read(va, 4))[0]

    def is_va(self, value: int) -> bool:
        return self.imagebase <= value < self.imagebase + self.size_of_image

    def build_pointer_index(self) -> dict[int, list[int]]:
        """Map pointer value -> every VA that stores it, in one pass.

        Only sections that can hold pointers participate (code and read-only
        data), and only values that fall inside the image are indexed. This
        replaces repeated whole-section scans with a single O(bytes) pass.
        """
        index: dict[int, list[int]] = {}
        for s in self.sections:
            if s.executable or not s.data:
                continue
            usable = len(s.data) - (len(s.data) % 4)
            for off in range(0, usable, 4):
                value = struct.unpack_from("<I", s.data, off)[0]
                if self.imagebase <= value < self.imagebase + self.size_of_image:
                    index.setdefault(value, []).append(s.va + off)
        self._index = index
        return index

    def pointers_to(self, target: int) -> list[int]:
        if self._index is None:
            self.build_pointer_index()
        assert self._index is not None
        return self._index.get(target, [])

    def find_bytes(self, needle: bytes) -> list[int]:
        hits: list[int] = []
        for s in self.sections:
            i = s.data.find(needle)
            while i != -1:
                hits.append(s.va + i)
                i = s.data.find(needle, i + 1)
        return hits


def load_pe32(path: str) -> Image:
    with open(path, "rb") as fh:
        d = fh.read()
    if d[:2] != b"MZ":
        raise ImageError("missing MZ header")
    e_lfanew = struct.unpack_from("<I", d, 0x3C)[0]
    if d[e_lfanew:e_lfanew + 4] != b"PE\0\0":
        raise ImageError("missing PE signature")
    coff = e_lfanew + 4
    nsec = struct.unpack_from("<H", d, coff + 2)[0]
    opt_size = struct.unpack_from("<H", d, coff + 16)[0]
    opt = coff + 20
    magic = struct.unpack_from("<H", d, opt)[0]
    if magic != 0x10B:
        raise ImageError(f"not PE32 (magic 0x{magic:04x})")
    imagebase = struct.unpack_from("<I", d, opt + 28)[0]
    size_of_image = struct.unpack_from("<I", d, opt + 56)[0]
    sections: list[Section] = []
    sec = opt + opt_size
    for i in range(nsec):
        o = sec + i * 40
        name = d[o:o + 8].rstrip(b"\0").decode("latin1")
        vsize, rva, rawsize, rawptr = struct.unpack_from("<IIII", d, o + 8)
        chars = struct.unpack_from("<I", d, o + 36)[0]
        body = d[rawptr:rawptr + rawsize] if rawsize else b""
        sections.append(Section(name=name, va=imagebase + rva, vsize=vsize,
                                data=body, characteristics=chars))
    return Image(imagebase=imagebase, size_of_image=size_of_image, sections=sections)


def _plausible_td(image: Image, td: int) -> bool:
    """A TypeDescriptor begins with a vftable pointer and has a spare dword."""
    if td % 4 or not image.is_va(td):
        return False
    try:
        vtbl, _spare = image.u32(td), image.u32(td + 4)
    except ImageError:
        return False
    sec = image.section_of(vtbl)
    return sec is not None


def resolve_class(image: Image, class_name: str) -> dict:
    """Resolve one decorated MSVC name to TD -> COL -> vtables.

    Raises ImageError when the name is absent or the chain does not validate.
    """
    needle = class_name.encode("latin1")
    # TypeDescriptor stores its name at +8, so the name bytes *are* the field;
    # nothing points at them separately. The TD base is what COL references.
    descriptors = [name_va - 8 for name_va in image.find_bytes(needle)]
    descriptors = [td for td in descriptors if _plausible_td(image, td)]
    if not descriptors:
        raise ImageError(f"{class_name}: no TypeDescriptor")

    locators: list[int] = []
    for td in descriptors:
        for ref in image.pointers_to(td):
            col = ref - 12
            try:
                signature = image.u32(col)
            except ImageError:
                continue
            if signature in (0, 1):
                locators.append(col)
    if not locators:
        raise ImageError(f"{class_name}: no RTTICompleteObjectLocator")

    vtables: list[int] = []
    for col in locators:
        for ref in image.pointers_to(col):
            vt = ref + 4
            try:
                first = image.u32(vt)
            except ImageError:
                continue
            sec = image.section_of(first)
            if sec is not None and sec.executable:
                vtables.append(vt)
    if not vtables:
        raise ImageError(f"{class_name}: no vftable references its COL")

    return {
        "class": class_name,
        "type_descriptor": descriptors[0],
        "locators": sorted(set(locators)),
        "vtables": sorted(set(vtables)),
    }


def vtable_slots(image: Image, vt_va: int, limit: int = 256) -> list[int]:
    """Method pointers from slot 0 until a non-code or repeated entry."""
    slots: list[int] = []
    seen: set[int] = set()
    for k in range(limit):
        try:
            value = image.u32(vt_va + 4 * k)
        except ImageError:
            break
        sec = image.section_of(value)
        if value == 0 or sec is None or not sec.executable or value in seen:
            break
        slots.append(value)
        seen.add(value)
    return slots


def describe(image: Image, class_name: str, slot_limit: int = 12) -> dict:
    out = resolve_class(image, class_name)
    out["slots"] = [
        {"slot": k, "va": v}
        for vt in out["vtables"]
        for k, v in enumerate(vtable_slots(image, vt))
    ]
    out["slot_count"] = len(out["slots"])
    out["first_slots"] = out["slots"][:slot_limit]
    return out


def _iter_ia_names(image: Image):
    """Yield every RTTI class name in an IA-ish Eugen namespace."""
    needles = [b".?AV", b".?AU"]
    for needle in needles:
        for va in image.find_bytes(needle):
            try:
                s = image.read(va, 400)
            except ImageError:
                continue
            end = s.find(b"\0")
            if end < 4:
                continue
            name = s[:end].decode("latin1")
            if "@Eugen@@" in name and ("@IA@" in name or "IAStrat@" in name):
                yield name.encode("latin1")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--exe", required=True, help="path to a PE32 image (read-only)")
    ap.add_argument("--class", dest="classes", action="append",
                    help="decorated MSVC name, e.g. .?AVTFoo@Eugen@@ (repeatable)")
    ap.add_argument("--json", help="write full results to this path")
    ap.add_argument("--slots", type=int, default=8, help="slots to print (default 8)")
    ap.add_argument("--slot-map", action="store_true",
                    help="resolve every .?AV*@IA*@Eugen@@ class and emit slot->class")
    ap.add_argument("--lookup", action="append", default=[],
                    help="with --slot-map, report the class owning this VA (hex)")
    args = ap.parse_args(argv)

    image = load_pe32(args.exe)
    image.build_pointer_index()

    if args.slot_map:
        names = sorted({n.decode("latin1") for n in _iter_ia_names(image)})
        slot_map: dict[int, list[str]] = {}
        resolved = 0
        for name in names:
            try:
                res = resolve_class(image, name)
            except ImageError:
                continue
            resolved += 1
            for vt in res["vtables"]:
                for k, va in enumerate(vtable_slots(image, vt)):
                    slot_map.setdefault(va, []).append(f"{name}[{k}]")
        print(f"classes={len(names)} resolved={resolved} slots={len(slot_map)}")
        for raw in args.lookup:
            va = int(raw, 16)
            owners = slot_map.get(va, [])
            # also report the nearest preceding slot in the same function range
            print(f"0x{va:08x}: {owners if owners else 'no vtable slot starts here'}")
        if args.json:
            with open(args.json, "w") as fh:
                json.dump({"slot_map": {f"0x{k:08x}": v for k, v in slot_map.items()},
                           "classes": names}, fh, indent=0)
        return 0

    if not args.classes:
        ap.error("--class is required unless --slot-map is given")
    results = []
    failed = 0
    for name in args.classes:
        try:
            res = describe(image, name, slot_limit=args.slots)
        except ImageError as exc:
            failed += 1
            print(f"FAIL {exc}")
            results.append({"class": name, "error": str(exc)})
            continue
        print(f"OK   {name}")
        print(f"     td=0x{res['type_descriptor']:08x} "
              f"col={[hex(c) for c in res['locators']]} "
              f"vtable={[hex(v) for v in res['vtables']]} slots={res['slot_count']}")
        for slot in res["first_slots"]:
            print(f"     [{slot['slot']:2d}] 0x{slot['va']:08x}")
        results.append(res)
    if args.json:
        with open(args.json, "w") as fh:
            json.dump({"exe": args.exe, "results": results}, fh, indent=2)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
