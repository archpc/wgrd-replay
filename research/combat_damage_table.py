"""Table-backed adapter over the Phase 2a damage kernel (Phase 2b).

Loads the private, hash-pinned extraction of the ``TGameplayArmeArmureContainer``
object at NDF record offset ``0x104f2f7`` for build 131544. The object holds a
65-row MAPLIST keyed 0..64; each value is a LIST of FLOAT32. Rows have 30 values
except key 2, which has 25. The engine indexes ``data[family * 35 + armor]``, so
columns 30..34 are always zero and the short row is zero beyond column 24.

This module validates the extraction and pads every row to 35 columns. It does
not embed the table in Git, resolve the Arme encoding, or compute range, crit,
accuracy or falloff. The full table stays in the private evidence directory.
"""
import hashlib
import json
import math
import os
import struct
import sys
from dataclasses import dataclass
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from combat_damage import f32  # noqa: E402

FIXTURE_SHA256 = "9004d7765a201027171eacad15d176010347e3471767654399202985c7d12834"
PACKED_SHA256 = "6b829a65c485346a03117f9074b1772198acc3fc28195abe923513b8799dc2c8"
DECOMPRESSED_SHA256 = "640c66c2336f6e54bb1e0183a76eecd2d1defe7fafe67ed56e7f82a5021ed032"
RECORD_OFFSET = "0x104f2f7"
CLASS_ID = 236
PROPERTY_ID = 1419

FAMILY_COUNT = 65
ARMOR_COLUMNS = 35
ROW_VALUES = 30
SHORT_FAMILY = 2
SHORT_ROW_VALUES = 25

DEFAULT_PATH = (Path.home() / ".hermes/artifacts/wgrd-replay"
                / "combat-damage-static-20261109/arme-armure-table.json")

_F32 = struct.Struct("<f")


class CombatDamageTableError(ValueError):
    """The extraction failed hash, shape, type or metadata validation."""


@dataclass(frozen=True)
class ArmeArmureTable:
    rows: tuple
    packed_sha256: str
    decompressed_sha256: str
    record_offset: str
    class_id: int
    property_id: int

    @property
    def family_count(self):
        return len(self.rows)

    @property
    def armor_count(self):
        return len(self.rows[0]) if self.rows else 0

    def lookup(self, family, armor):
        """Return ``T[family][armor]``, including zero-filled columns."""
        if isinstance(family, bool) or not isinstance(family, int):
            raise TypeError("family must be an int, not " + type(family).__name__)
        if isinstance(armor, bool) or not isinstance(armor, int):
            raise TypeError("armor must be an int, not " + type(armor).__name__)
        if not 0 <= family < self.family_count:
            raise IndexError("family out of range: " + str(family))
        if not 0 <= armor < self.armor_count:
            raise IndexError("armor out of range: " + str(armor))
        return self.rows[family][armor]


def parse_arme_armure_table(payload, *, expected_sha256=FIXTURE_SHA256):
    """Validate a raw extraction payload and return the padded table."""
    digest = hashlib.sha256(payload).hexdigest()
    if digest != expected_sha256:
        raise CombatDamageTableError(
            "table SHA-256 mismatch: " + digest + " != " + expected_sha256)
    try:
        document = json.loads(payload)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CombatDamageTableError("table is not valid JSON: " + str(exc)) from exc
    if not isinstance(document, dict):
        raise CombatDamageTableError("table document must be a JSON object")

    for key, expected in (
            ("packed_sha256", PACKED_SHA256),
            ("decompressed_sha256", DECOMPRESSED_SHA256),
            ("record_offset", RECORD_OFFSET),
            ("class_id", CLASS_ID),
            ("property_id", PROPERTY_ID)):
        if document.get(key) != expected:
            raise CombatDamageTableError(
                "record metadata mismatch for " + key + ": " + repr(document.get(key)))

    rows = document.get("rows")
    if not isinstance(rows, dict):
        raise CombatDamageTableError("rows must be a JSON object")
    expected_keys = {str(family) for family in range(FAMILY_COUNT)}
    if set(rows) != expected_keys:
        missing = sorted(expected_keys - set(rows), key=int)
        extra = sorted(set(rows) - expected_keys)
        raise CombatDamageTableError(
            "family keys must be 0..64; missing=" + repr(missing) + " extra=" + repr(extra))

    padded = []
    for family in range(FAMILY_COUNT):
        key = str(family)
        row = rows[key]
        if not isinstance(row, list):
            raise CombatDamageTableError("row " + key + " must be a JSON list")
        expected_length = SHORT_ROW_VALUES if family == SHORT_FAMILY else ROW_VALUES
        if len(row) != expected_length:
            raise CombatDamageTableError(
                "row " + key + " has " + str(len(row)) + " values, expected "
                + str(expected_length))
        values = []
        for column, value in enumerate(row):
            if isinstance(value, bool) or not isinstance(value, float):
                raise CombatDamageTableError(
                    "row " + key + " column " + str(column)
                    + " is not a JSON float: " + repr(value))
            if not math.isfinite(value):
                raise CombatDamageTableError(
                    "row " + key + " column " + str(column) + " is not finite")
            if f32(value) != value:
                raise CombatDamageTableError(
                    "row " + key + " column " + str(column)
                    + " is not exactly representable as float32: " + repr(value))
            values.append(value)
        padded.append(tuple(values) + (0.0,) * (ARMOR_COLUMNS - len(values)))

    return ArmeArmureTable(
        rows=tuple(padded),
        packed_sha256=document["packed_sha256"],
        decompressed_sha256=document["decompressed_sha256"],
        record_offset=document["record_offset"],
        class_id=document["class_id"],
        property_id=document["property_id"],
    )


def load_arme_armure_table(path=None, *, expected_sha256=FIXTURE_SHA256):
    """Read and validate the private extraction; missing files raise."""
    if path is None:
        path = Path(os.environ.get("WGRD_ARME_ARMURE_TABLE", DEFAULT_PATH))
    payload = Path(path).read_bytes()
    return parse_arme_armure_table(payload, expected_sha256=expected_sha256)
