"""Pure-Python direct-fire damage kernel for build 131544 (Phase 2a).

Scope is exactly two verified arithmetic fragments:

* ``damage_amount`` reproduces the scalar SSE product at ``0xcfa2ae``..
  ``0xcfa2e6``: ``((((H * P) * T) * K) * C) * F``, left to right, with a
  float32 rounding after every multiply. Each input is a float32 value read
  from memory (T, P, C and F arrive as x87 returns stored as ``fstp dword``),
  so inputs are rounded before use.
* ``apply_mode2`` reproduces the mode-2 HP clamp at ``0xc9fa4f``..``0xc9fc37``:
  ``applied = min(amount, max_damages - current)`` then
  ``current = max(current + applied, 0)``, rounded to float32 per operation.

The kernel takes every term explicitly. It does not determine H, P, T, K, C or F,
and it contains no weapon identity, facing label, accuracy term or falloff
table. Mode 1 (additive suppression at ``+0x190``) is not modelled.
"""
import struct

_F32 = struct.Struct("<f")


def f32(value):
    """Round a Python float to the nearest IEEE-754 binary32 value."""
    return _F32.unpack(_F32.pack(value))[0]


def damage_amount(h, p, t, k, c, f):
    """Return the amount term with verified float32 operation order."""
    value = f32(h)
    for factor in (p, t, k, c, f):
        value = f32(value * f32(factor))
    return value


def apply_mode2(amount, max_damages, current):
    """Return ``(applied, new_current)`` for one mode-2 HP application."""
    amount = f32(amount)
    room = f32(f32(max_damages) - f32(current))
    applied = amount if amount < room else room
    new_current = f32(f32(current) + applied)
    if new_current < 0.0:
        new_current = 0.0
    return applied, new_current
