"""Kinetic range family-index kernel for build 131544 (Phase 2c).

Implements the calculation at ``0xda3410`` and its two dependencies:

* ``0xc2ce00`` gate: ``ProjectileType (+0xec) == 0`` and ``5 <= Arme <= 64``.
  The call site additionally requires ``EfficaciteSelonPortee (+0xf0) != 0``.
* ``0xda5b90`` target class 1..6 and ``0xc2ba70`` range-field selection.

Verified instruction order at ``0xda3410``: the selected range is loaded
through x87 and stored as float32; the 2-D distance ``R+0x44`` is float32; then
``subss``, ``maxss`` with 0, ``divss`` by ``[0x203dd00]`` (13000.0),
``cvtps2pd`` + ``cvttsd2si`` (truncate toward zero), add ``Arme``, signed
``min`` with the cap, and signed ``max`` with 5.

The result is a damage-table row index only. It is not named here as AP or as
any weapon family. Range units are not established; the divisor is the shipped
``DistanceStepToGain1APLevel`` value, used as a raw number.

The third argument at the call site is the armour index; ``0xda3410`` never
reads it (verified: no operand after the two pushes), so no armour input is
accepted here.
"""
import math
import struct
import sys
from collections.abc import Mapping
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from combat_damage import f32  # noqa: E402

RANGE_STEP = 13000.0
FAMILY_FLOOR = 5
LOW_CAP = 34
HIGH_CAP = 64
ARME_MIN = 5
ARME_MAX = 64

# 0xc2ba70 jump table at 0xc2baa8, indexed by target_class-1.
RANGE_PROPERTY_BY_CLASS = {
    1: "PorteeMaximaleBateaux",   # +0x8c
    2: "PorteeMaximale",          # +0x6c
    3: "PorteeMaximaleTBA",       # +0x74
    4: "PorteeMaximaleTBA",       # +0x74
    5: "PorteeMaximaleHA",        # +0x7c
    6: "PorteeMaximaleProjectile",  # +0x84
}

_F32 = struct.Struct("<f")


def _require_int(value, name):
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(name + " must be an int, not " + type(value).__name__)


def _require_number(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(name + " must be a number, not " + type(value).__name__)
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(name + " must be finite")
    return value


def range_family_applies(projectile_type, arme, efficacite_selon_portee):
    """Return whether the range family-index path is enabled for this ammo."""
    _require_int(projectile_type, "projectile_type")
    _require_int(arme, "arme")
    if isinstance(efficacite_selon_portee, bool):
        flag = int(efficacite_selon_portee)
    elif isinstance(efficacite_selon_portee, int):
        flag = efficacite_selon_portee
    else:
        raise TypeError("efficacite_selon_portee must be an int flag, not "
                        + type(efficacite_selon_portee).__name__)
    return projectile_type == 0 and ARME_MIN <= arme <= ARME_MAX and flag != 0


def range_max_for_class(properties, target_class):
    """Select the raw range field for a 0xda5b90 target class.

    ``properties`` is a mapping of NDF property names to numeric values. An
    absent or null field raises; this adapter does not invent a zero default.
    """
    if not isinstance(properties, Mapping):
        raise TypeError("properties must be a mapping")
    _require_int(target_class, "target_class")
    if target_class not in RANGE_PROPERTY_BY_CLASS:
        raise ValueError("target_class must be 1..6: " + str(target_class))
    name = RANGE_PROPERTY_BY_CLASS[target_class]
    if name not in properties or properties[name] is None:
        raise KeyError(name)
    return _require_number(properties[name], name)


def kinetic_family_index(arme, rmax, distance):
    """Return the table row index; inputs are explicit, no gate is applied."""
    _require_int(arme, "arme")
    rmax = _require_number(rmax, "rmax")
    distance = _require_number(distance, "distance")

    remaining = f32(f32(rmax) - f32(distance))
    if remaining < 0.0:
        remaining = 0.0
    steps = math.trunc(f32(remaining / f32(RANGE_STEP)))

    cap = LOW_CAP if arme < LOW_CAP else HIGH_CAP
    return max(FAMILY_FLOOR, min(cap, arme + steps))
