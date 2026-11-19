#!/usr/bin/env python3
"""Authoritative fixed-width record specification for WGRD-CICS.

This module is the single definition of the three external formats. The COBOL
program, the differential oracle, the fixture builders and the tests all refer
to it; no other document version may redefine offsets.

BATCH (176 bytes, one transaction per record, ASCII, zero-filled implied
decimals, no decimal point on the wire)::

    1       type        X    "D" detail, "Z" control card
    2-11    id          X(10)
    12      mode        9    1 or 2
    13-24   h           9(4)V9(8)
    25-36   p           9(4)V9(8)
    37-48   k           9(4)V9(8)
    49-60   c           9(4)V9(8)
    61-72   f           9(4)V9(8)
    73-74   armor       9(2)
    75-76   family      9(2)   used only when the range gate is closed
    77-78   proj        9(2)   ProjectileType (+0xec)
    79-80   arme        9(2)   Arme (+0xe8)
    81      eff         9     EfficaciteSelonPortee (+0xf0), nonzero = true
    82      class       9     target class 1..6 (0xda5b90)
    83-93   dist        9(6)V9(5)   R+0x44 two-dimensional distance
    94-104  r_bateaux   9(6)V9(5)   PorteeMaximaleBateaux (+0x8c)
    105-115 r_max       9(6)V9(5)   PorteeMaximale (+0x6c)
    116-126 r_tba       9(6)V9(5)   PorteeMaximaleTBA (+0x74)
    127-137 r_ha        9(6)V9(5)   PorteeMaximaleHA (+0x7c)
    138-148 r_proj      9(6)V9(5)   PorteeMaximaleProjectile (+0x84)
    149-156 maxhp       9(5)V9(3)   MaxDamages (+0x194), mode 2
    157-164 curhp       9(5)V9(3)   current HP (+0x19c), mode 2
    165-176 filler      X(12)  spaces

Control card: byte 1 "Z", bytes 2-8 decimal count of detail records.

JOURNAL (72 bytes)::

    1       "D" accepted, "R" rejected
    2-11    id
    12-13   status "OK" / "RJ"
    14-17   reject code, "0000" when accepted
    18-20   family ("---" on reject)
    21-23   armor ("---" on reject)
    24-31   amount IEEE-754 binary32 bits, uppercase hex
    32-39   applied bits, "--------" for mode 1 and rejects
    40-47   new HP bits, "--------" for mode 1 and rejects
    48-65   amount text, 9(9).9(8), truncated
    66-72   filler spaces

Trailer record (last journal line)::

    1       "T"
    2-8     accepted count 9(7)
    9-15    rejected count 9(7)
    16-23   float32 total amount bits, uppercase hex
    24-72   spaces

TABLE DECK (80-byte cards)::

    H + name X(16) + build X(6) + rows 9(3) + cols 9(3)
      + control total in thousandths 9(11) + tag X(24) + filler X(16)
    R + family 9(3) + sequence 99 + 3 x [value 9(3)V9(18) + filler X(3)]
      + filler X(2)

Values carry the exact decimal expansion of the binary32 cell, so the COBOL
numeric MOVE reconstructs the same bit pattern with no rounding.
"""
import struct
from decimal import Decimal

BATCH_LEN = 176
JOURNAL_LEN = 72
TABLE_CARD_LEN = 80

# name, start (1-based), length, decimals
BATCH_FIELDS = (
    ("type", 1, 1, None),
    ("id", 2, 10, None),
    ("mode", 12, 1, 0),
    ("h", 13, 12, 8),
    ("p", 25, 12, 8),
    ("k", 37, 12, 8),
    ("c", 49, 12, 8),
    ("f", 61, 12, 8),
    ("armor", 73, 2, 0),
    ("family", 75, 2, 0),
    ("proj", 77, 2, 0),
    ("arme", 79, 2, 0),
    ("eff", 81, 1, 0),
    ("tclass", 82, 1, 0),
    ("dist", 83, 11, 5),
    ("r_bateaux", 94, 11, 5),
    ("r_max", 105, 11, 5),
    ("r_tba", 116, 11, 5),
    ("r_ha", 127, 11, 5),
    ("r_proj", 138, 11, 5),
    ("maxhp", 149, 8, 3),
    ("curhp", 157, 8, 3),
)

FIELD_INDEX = {field[0]: field for field in BATCH_FIELDS}

JOURNAL_FIELDS = (
    ("type", 1, 1),
    ("id", 2, 10),
    ("status", 12, 2),
    ("code", 14, 4),
    ("family", 18, 3),
    ("armor", 21, 3),
    ("amt_bits", 24, 8),
    ("applied_bits", 32, 8),
    ("cur_bits", 40, 8),
    ("amt_text", 48, 18),
)

_F32 = struct.Struct("<f")
_U32 = struct.Struct("<I")


def f32(value):
    return _F32.unpack(_F32.pack(value))[0]


def bits(value):
    return "%08X" % _U32.unpack(_F32.pack(f32(value)))[0]


def exact_float32(value):
    """Return the decimal text that transports this binary32 exactly."""
    scaled = Decimal(repr(f32(value))) * (10 ** 18)
    if scaled != scaled.to_integral_value():
        raise ValueError("value needs more than 18 decimals: %r" % value)
    return "%021d" % int(scaled)


def _digits(name, value, decimals):
    """Render an implied-decimal integer, zero filled, no sign."""
    if isinstance(value, Decimal):
        scaled = int(value.scaleb(decimals).to_integral_value())
    else:
        scaled = int(round(float(value) * 10 ** decimals))
    if scaled < 0:
        raise ValueError("%s must be non-negative" % name)
    return str(scaled)


def encode_detail(values):
    """Return one 176-byte batch record. ``values`` maps field name to value."""
    line = [" "] * BATCH_LEN

    def put(name, text, numeric=True):
        start, length = FIELD_INDEX[name][1], FIELD_INDEX[name][2]
        if len(text) > length:
            raise ValueError("%s overflows %d columns" % (name, length))
        if numeric:
            line[start - 1:start - 1 + length] = text.rjust(length,
                                                            "0")
        else:
            line[start - 1:start - 1 + length] = text.ljust(length)

    put("type", values.get("type", "D"), numeric=False)
    put("id", values["id"], numeric=False)
    for name, _, _, decimals in BATCH_FIELDS:
        if decimals is None or name in ("type", "id"):
            continue
        put(name, _digits(name, values[name], decimals))
    return "".join(line)


def encode_control(count):
    line = [" "] * BATCH_LEN
    line[0] = "Z"
    line[1:8] = ("%07d" % count)
    return "".join(line)


def decode(line):
    """Decode a batch record into raw strings and Decimal values."""
    line = line.ljust(BATCH_LEN)[:BATCH_LEN]
    out = {}
    for name, start, length, decimals in BATCH_FIELDS:
        raw = line[start - 1:start - 1 + length]
        out[name] = raw
        if decimals is not None:
            if raw.isdigit():
                out[name + "_value"] = Decimal(raw).scaleb(-decimals)
            else:
                out[name + "_value"] = None
    return out


def journal_line(record):
    line = [" "] * JOURNAL_LEN
    for name, start, length in JOURNAL_FIELDS:
        text = record[name]
        if len(text) > length:
            raise ValueError("%s overflows journal field" % name)
        if name == "amt_text":
            text = text.rjust(length, "0")
        line[start - 1:start - 1 + length] = text.ljust(length)
    return "".join(line).rstrip()
