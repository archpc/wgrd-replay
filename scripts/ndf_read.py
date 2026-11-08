#!/usr/bin/env python3
"""Read Eugen Systems compiled NDF (`.ndfbin`) files, read-only.

The format is not ours: it is implemented from the open-source modding suite
(TK3600/moddingSuite, `model/Ndfbin` + `BL/Ndf/NdfbinReader.cs`). We only port
the subset needed to read values so shipped data can be cited by name and
value, rather than by guessed identifier hashes.

Container layout (little-endian):

    header   "EUG0", 0, "CNDF", u32 compressed(0x80), u64 footer, u64 header_size,
             u64 full_size_uncompressed            (44 bytes)
    footer   "TOC0", u32 count, then count * (8s name, u64 offset, u64 size)
    OBJE     object instances
    CLAS     u32 len + name, repeated
    PROP     u32 len + name + u32 class_id, repeated
    STRG     u32 len + string, repeated (TableString payloads)
    TRAN     u32 len + string, repeated
    CHNK     two u32; the second is the instance count
    TOPO/IMPR/EXPR   u32 lists

Object record: i32 class_id, then (u32 property_id, value)* until 0xABABABAB.
Value: u32 type tag, then payload. A Reference tag (9) is followed by a second
type tag before the payload. List/MapList/WideString/Blob/ZipBlob carry a u32
count first; Map is exactly two values.

Read-only: nothing is executed, and no file in the game directory is written.
"""

from __future__ import annotations

import argparse
import json
import struct
import sys
import zlib
from dataclasses import dataclass, field

# NdfType values (moddingSuite model/Ndfbin/Types/NdfType.cs)
BOOL, INT8 = 0x00, 0x01
INT16, UINT16 = 0x18, 0x19
INT32, UINT32, FLOAT32, FLOAT64 = 0x02, 0x03, 0x05, 0x06
LONG, TIME64 = 0x13, 0x04
VECTOR, COLOR128, COLOR32, TRIPPLEINT = 0x0B, 0x0C, 0x0D, 0x0E
TABLESTRING, TABLESTRINGFILE, WIDESTRING = 0x07, 0x1C, 0x08
LOCALISATIONHASH, HASH = 29, 0x25
REFERENCE, OBJECTREF, TRANSTABLE = 0x09, 0xBBBBBBBB, 0xAAAAAAAA
MAP, BLOB, ZIPBLOB, LIST, MAPLIST = 0x22, 0x14, 0x1E, 0x11, 0x12
GUID, EUGINT2, EUGFLOAT2 = 26, 0x1F, 0x21

FIXED = {
    BOOL: 1, INT8: 1, INT16: 2, UINT16: 2,
    INT32: 4, UINT32: 4, FLOAT32: 4, TABLESTRING: 4, TABLESTRINGFILE: 4,
    COLOR32: 4, WIDESTRING: 4,
    FLOAT64: 8, LONG: 8, LOCALISATIONHASH: 8, OBJECTREF: 8, EUGINT2: 8,
    EUGFLOAT2: 8, TIME64: 8, TRANSTABLE: 4,
    TRIPPLEINT: 12, VECTOR: 12,
    COLOR128: 16, GUID: 16, HASH: 16,
}


class NdfError(ValueError):
    pass


@dataclass
class Value:
    type: str
    value: object


@dataclass
class NdfClass:
    id: int
    name: str
    property_ids: list[int] = field(default_factory=list)


@dataclass
class NdfProperty:
    id: int
    name: str
    class_id: int


@dataclass
class NdfObject:
    id: int
    class_id: int
    values: dict[int, Value] = field(default_factory=dict)


class NdfFile:
    def __init__(self, data: bytes):
        self.raw = data
        self.classes: list[NdfClass] = []
        self.properties: dict[int, NdfProperty] = {}
        self.strings: list[str] = []
        self.objects: list[NdfObject] = []
        self.top_objects: list[int] = []
        self._parse()

    # -- container ---------------------------------------------------------
    def _u32(self, off: int) -> int:
        return struct.unpack_from("<I", self.raw, off)[0]

    def _u64(self, off: int) -> int:
        return struct.unpack_from("<Q", self.raw, off)[0]

    def _str_at(self, off: int) -> tuple[str, int]:
        n = self._u32(off)
        end = off + 4 + n
        return self.raw[off + 4:end].decode("latin-1"), end

    def _parse(self) -> None:
        d = self.raw
        if d[:4] != b"EUG0" or d[8:12] != b"CNDF":
            raise NdfError("not an ndfbin (EUG0/CNDF)")
        compressed = self._u32(12) == 0x80
        footer_off = self._u64(16)
        header_size = self._u64(24)
        if compressed:
            # Body is zlib after a 4-byte block length. Decompressed copies can
            # keep the flag set (the reference decompressor does not rewrite the
            # header), so fall back to the plain body if inflate is not applicable.
            try:
                d = d[:header_size] + zlib.decompress(d[header_size + 4:])
                self.raw = d
            except zlib.error:
                compressed = False
        if d[footer_off:footer_off + 4] != b"TOC0":
            raise NdfError("missing TOC0 footer")
        count = self._u32(footer_off + 4)
        sections: dict[str, tuple[int, int]] = {}
        off = footer_off + 8
        for _ in range(count):
            name = d[off:off + 8].rstrip(b"\0").decode("ascii")
            sections[name] = (self._u64(off + 8), self._u64(off + 16))
            off += 24
        self._parse_classes(sections["CLAS"])
        self._parse_properties(sections["PROP"])
        if "STRG" in sections:
            self._parse_strings(sections["STRG"])
        self._parse_uint_list(sections.get("TOPO"), self.top_objects)
        self._parse_objects(sections["OBJE"], sections["CHNK"])

    def _parse_classes(self, sec: tuple[int, int]) -> None:
        off, end = sec[0], sec[0] + sec[1]
        while off < end:
            name, off = self._str_at(off)
            self.classes.append(NdfClass(id=len(self.classes), name=name))

    def _parse_properties(self, sec: tuple[int, int]) -> None:
        off, end = sec[0], sec[0] + sec[1]
        pid = 0
        while off < end:
            name, off = self._str_at(off)
            class_id = self._u32(off)
            off += 4
            prop = NdfProperty(id=pid, name=name, class_id=class_id)
            self.properties[pid] = prop
            if class_id < len(self.classes):
                self.classes[class_id].property_ids.append(pid)
            pid += 1

    def _parse_strings(self, sec: tuple[int, int]) -> None:
        off, end = sec[0], sec[0] + sec[1]
        while off < end:
            s, off = self._str_at(off)
            self.strings.append(s)

    def _parse_uint_list(self, sec, out: list[int]) -> None:
        if not sec:
            return
        off, end = sec[0], sec[0] + sec[1]
        while off + 4 <= end:
            out.append(self._u32(off))
            off += 4

    def _parse_objects(self, obj_sec, chnk_sec) -> None:
        chnk_off = chnk_sec[0]
        n_objects = self._u32(chnk_off + 4)
        off = obj_sec[0]
        for i in range(n_objects):
            obj = NdfObject(id=i, class_id=struct.unpack_from("<i", self.raw, off)[0])
            off += 4
            while True:
                pid = self._u32(off)
                off += 4
                if pid == 0xABABABAB:
                    break
                value, off = self._read_value(off)
                obj.values[pid] = value
            self.objects.append(obj)

    # -- values ------------------------------------------------------------
    def _read_value(self, off: int) -> tuple[Value, int]:
        tag = self._u32(off)
        off += 4
        if tag == REFERENCE:
            tag = self._u32(off)
            off += 4
        if tag in (LIST, MAPLIST):
            n = self._u32(off)
            off += 4
            items = []
            for _ in range(n):
                if tag == LIST:
                    v, off = self._read_value(off)
                    items.append(v.value)
                else:
                    k, off = self._read_value(off)
                    v, off = self._read_value(off)
                    items.append([k.value, v.value])
            return Value("list" if tag == LIST else "maplist", items), off
        if tag == MAP:
            k, off = self._read_value(off)
            v, off = self._read_value(off)
            return Value("map", {str(k.value): v.value}), off
        if tag == ZIPBLOB:
            n = self._u32(off)
            off += 4
            if self.raw[off] != 1:
                raise NdfError("zip blob marker != 1")
            off += 1
            return Value("zipblob", n), off
        if tag in FIXED:
            size = FIXED[tag]
            blob = self.raw[off:off + size]
            off += size
            return Value(_name(tag), _decode(tag, blob)), off
        raise NdfError(f"unsupported value tag 0x{tag:08x} at 0x{off - 4:x}")


def _name(tag: int) -> str:
    return {
        BOOL: "bool", INT8: "i8", INT16: "i16", UINT16: "u16", INT32: "i32",
        UINT32: "u32", FLOAT32: "f32", FLOAT64: "f64", LONG: "i64", TIME64: "time64",
        VECTOR: "vector", COLOR128: "color128", COLOR32: "color32",
        TRIPPLEINT: "trippleint", TABLESTRING: "string", TABLESTRINGFILE: "filestring",
        WIDESTRING: "widestring", HASH: "hash", GUID: "guid",
        OBJECTREF: "objectref", EUGINT2: "eugint2", EUGFLOAT2: "eugfloat2",
    }.get(tag, f"type{tag:#x}")


def _decode(tag: int, b: bytes):
    if tag == BOOL:
        return b[0] != 0
    if tag == INT8:
        return struct.unpack("<b", b)[0]
    if tag == INT16:
        return struct.unpack("<h", b)[0]
    if tag == UINT16:
        return struct.unpack("<H", b)[0]
    if tag == INT32:
        return struct.unpack("<i", b)[0]
    if tag == UINT32:
        return struct.unpack("<I", b)[0]
    if tag == FLOAT32:
        return struct.unpack("<f", b)[0]
    if tag == FLOAT64:
        return struct.unpack("<d", b)[0]
    if tag == TRANSTABLE:
        return struct.unpack("<I", b)[0]
    if tag in (LONG, TIME64):
        return struct.unpack("<q", b)[0]
    return list(b)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--class-name", help="only objects of this class")
    ap.add_argument("--prop", action="append", default=[],
                    help="only these property names (repeatable)")
    ap.add_argument("--json")
    ap.add_argument("--list-classes", action="store_true")
    args = ap.parse_args(argv)

    ndf = NdfFile(open(args.file, "rb").read())
    if args.list_classes:
        for c in ndf.classes:
            print(f"{c.id}: {c.name} ({len(c.property_ids)} properties)")
        print(f"objects: {len(ndf.objects)}")
        return 0

    wanted = set(args.prop)
    out = []
    for obj in ndf.objects:
        cls = ndf.classes[obj.class_id].name if obj.class_id < len(ndf.classes) else "?"
        if args.class_name and cls != args.class_name:
            continue
        rows = {}
        for pid, val in obj.values.items():
            prop = ndf.properties.get(pid)
            if prop is None:
                continue
            if wanted and prop.name not in wanted:
                continue
            rows[prop.name] = {"type": val.type, "value": val.value}
        out.append({"object": obj.id, "class": cls, "properties": rows})
    print(json.dumps(out, indent=2)[:20000])
    if args.json:
        with open(args.json, "w") as fh:
            json.dump(out, fh, indent=2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
