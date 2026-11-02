"""Bounded read-only revision-131544 engine state observer.

Facts used here are build-specific to the pinned PE32 and are documented in
``research/current-build/2026-11-02-engine-state.md``. The observer only reads
memory: no engine calls, no interceptors, no writes. Every read is a fixed
offset from a fixed base and is bounded by one readable mapping.
"""
import argparse
import hashlib
import json
import math
import struct
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

EXE_SHA256 = "5eaa6d6168c9570ff9789bffb3b2cc16fd908be61263b12fcc1e8b2f09efc75d"
# Default pin for the authenticated replay used by the existing runtime captures.
REPLAY_SHA256 = "abf6a5e909ec976a30d16e043f25220bfb7d7a149cfbf828de992be8e69da121"
REVISION_MARKER = b"####SVNREVISION####0000131544####SVNREVISION####"

IMAGE_BASE = 0x400000
MAX_READ_BYTES = 0x100
MAX_TOTAL_BYTES = 0x200
MAX_SAMPLES = 150
MAX_SECONDS = 30.0
MAX_TS_PREFIX = 0x100
MAX_PATH_BYTES = 1024        # 512 UTF-16 units, never crossing one mapping

# --- verified static addresses (module VAs, evidence in the research note) ---
TS_SLOT = 0x201D318          # TGameplayServices* global slot (.data)
TS_PREFIX_SIZE = 0x100       # preserve the v1 +0x00..+0xff raw prefix
CLOCK_OBJECT = 0x1FCE0D0     # static clock/speed object, used as `ecx` directly
CLOCK_SPAN_OFFSET = 0x68
CLOCK_SPAN_SIZE = 0x08       # f32 speed factor at +0x68, i32 step at +0x6c

CLOCK_CONSTANTS = {
    "speed_factor_max": 0x1932738,   # 100.0
    "speed_factor_min": 0x19326D8,   # 0.01
    "speed_factor_plus_one": 0x19326E8,   # 1.0
    "speed_factor_minus_one": 0x1932748,  # -1.0
}
# Named Lua bindings for the deterministic clock (parent-confirmed .data table entries).
# a406b0 -> [[0x201d318]+0xd0] * 0.2 ; a40780 -> [[0x201d318]+0xd0] ; a41710 -> [[0x201d318]+0x98]
ENGINE_NAMED_TIME_BINDINGS = (
    {"name": "DeterministicCurrentTimeInSeconds", "table_entry": 0x1D9CD68, "fn": 0xA406B0,
     "reads": "[[0x201d318]+0xd0] * 0.2f via 0xaaedf0"},
    {"name": "DeterministicCurrentTimeInTicks", "table_entry": 0x1D9CD78, "fn": 0xA40780,
     "reads": "[[0x201d318]+0xd0] (u32)"},
    {"name": "SetDeterministicCurrentTimeInTicks", "table_entry": 0x1D9CD88, "fn": 0xA41BC0,
     "reads": "setter; not exercised by this read-only observer"},
    {"name": "RealtimeCurrentTime", "table_entry": 0x1D9CD98, "fn": 0xA41710,
     "reads": "[[0x201d318]+0x98] (f32)"},
)
TICK_SECONDS = 0.2

MANAGER_IA = 0x2024A40       # TManagerIA singleton pointer slot
MANAGER_CHAPTER_OFFSET = 0x74
UI_BINDING_CONTEXT = 0x2022844  # dword passed to the Lua-arg resolver; meaning unresolved

# TS field map. `offset` is relative to TGameplayServices.
TS_FIELDS = {
    "game_started": (0x20, "u8"),
    "end_game_asked": (0x21, "u8"),
    "game_ended": (0x22, "u8"),
    "replay_controller_ptr": (0x34, "u32"),
    "phase_manager_ptr": (0x38, "u32"),
    "speed_header_ptr": (0x3C, "u32"),
    "network_ptr": (0x5C, "u32"),
    "realtime_current_time": (0x98, "f32"),
    "tick_counter": (0xD0, "u32"),
}
# Dereference targets.
PHASE_MANAGER_PHASE_ID = 0x0C
SPEED_HEADER_SPAN = (0x08, 0x0C)     # +0x08 direction code, +0x0c dword, +0x10 f32
NET_SPAN = (0xA0, 0x2C)              # +0xa1 pending, +0xa4 dedicated, +0xa5 replay cand, +0xc8 loading
LOADING_PHASE_INDEX = 0x0C

# Every planned read: (name, static VA or None when pointer-derived, size).
# Sum of sizes is asserted against MAX_TOTAL_BYTES by the tests.
READ_PLAN = (
    ("slot", TS_SLOT, 4),
    ("ts", None, TS_PREFIX_SIZE),
    ("clock", CLOCK_OBJECT, CLOCK_SPAN_SIZE),
    ("clock_tick_scale", 0x195D768, 4),
    ("constant_speed_factor_max", CLOCK_CONSTANTS["speed_factor_max"], 4),
    ("constant_speed_factor_min", CLOCK_CONSTANTS["speed_factor_min"], 4),
    ("constant_speed_factor_plus_one", CLOCK_CONSTANTS["speed_factor_plus_one"], 4),
    ("constant_speed_factor_minus_one", CLOCK_CONSTANTS["speed_factor_minus_one"], 4),
    ("phase_manager", None, 4),
    ("speed_header", None, SPEED_HEADER_SPAN[1]),
    ("network", None, NET_SPAN[1]),
    ("loading", None, 4),
    ("manager_ia_slot", MANAGER_IA, 4),
    ("manager_chapter", None, 4),
    ("ui_binding_context", UI_BINDING_CONTEXT, 4),
)
PLANNED_BYTES = sum(size for _, _, size in READ_PLAN)

SCRIPT = r"""
'use strict';
const m = Process.getModuleByName('wargame3.exe');
const BASE = 0x400000;
const MAX_READ = 0x100;
const MAX_TOTAL = 0x200;
const MAX_PATH_BYTES = 1024;
let total = 0;
function addr(va) { return m.base.add(va - BASE); }
function sane(p) { return p && !p.isNull() && p.compare(ptr('0x10000')) > 0; }
function span(p, n) {
  if (!sane(p)) return {ok: false, error: 'null or implausible pointer'};
  if (!(n > 0) || n > MAX_READ) return {ok: false, error: 'read size out of bounds'};
  if (total + n > MAX_TOTAL) return {ok: false, error: 'read budget exceeded'};
  const r = Process.findRangeByAddress(p);
  if (!r) return {ok: false, error: 'unmapped'};
  if (!r.protection || !r.protection.includes('r')) return {ok: false, error: 'not readable'};
  const end = p.add(n);
  if (end.compare(p) < 0 || end.compare(r.base.add(r.size)) > 0)
    return {ok: false, error: 'span crosses mapping'};
  try {
    const bytes = new Uint8Array(p.readByteArray(n));
    total += n;
    let hex = '';
    for (let i = 0; i < bytes.length; i++) hex += bytes[i].toString(16).padStart(2, '0');
    return {ok: true, hex: hex, address: p.toString(), size: n};
  } catch (e) {
    return {ok: false, error: 'read failed: ' + e};
  }
}
function deref(read) {
  if (!read.ok) return null;
  const h = read.hex;
  return ptr('0x' + h.slice(6, 8) + h.slice(4, 6) + h.slice(2, 4) + h.slice(0, 2));
}
function child(parent, offset, size) {
  if (!parent.ok) return {ok: false, error: 'parent unreadable'};
  const p = deref(parent);
  if (!sane(p)) return {ok: false, error: 'null pointer'};
  return span(p.add(offset), size);
}
rpc.exports = {
  inspect() {
    const p = m.base.add(0x3c).readU32();
    return {name: m.name, path: m.path, base: m.base.toString(), size: m.size, arch: Process.arch,
            pointer_size: Process.pointerSize, mz: m.base.readU16(), machine: m.base.add(p + 4).readU16(),
            entries: []};
  },
  state() {
    total = 0;
    const out = {reads: {}, counter_hex: null,
      read_budget: {max_read: MAX_READ, max_total: MAX_TOTAL, used: 0}};
    const scale = span(addr(0x195d768), 4);
    out.reads.clock_tick_scale = scale;
    if (!scale.ok || scale.hex !== 'cdcc4c3e') throw new Error('clock scale byte mismatch');
    out.scale_hex = scale.hex;
    // Absolute-address reads: attempted even when the services object is absent,
    // so a null global still yields raw clock/manager evidence instead of a throw.
    out.reads.clock = span(addr(0x1fce0d0 + 0x68), 8);
    out.reads.constant_speed_factor_max = span(addr(0x1932738), 4);
    out.reads.constant_speed_factor_min = span(addr(0x19326d8), 4);
    out.reads.constant_speed_factor_plus_one = span(addr(0x19326e8), 4);
    out.reads.constant_speed_factor_minus_one = span(addr(0x1932748), 4);
    const slot = span(addr(0x201d318), 4);
    out.reads.slot = slot;
    out.pointer_slot_hex = slot.ok ? slot.hex : null;
    out.container = '0x0';
    out.counter = null;
    out.clock_ticks_i32 = null;
    out.container_prefix_hex = null;
    out.ts_present = null;          // tri-state: null = slot not read, never guessed
    out.slot_state = 'unreadable';
    const mgrSlot = span(addr(0x2024a40), 4);
    out.reads.manager_ia_slot = mgrSlot;
    const mgr = deref(mgrSlot);
    out.reads.manager_chapter = sane(mgr) ? span(mgr.add(0x74), 4) : {ok: false, error: 'null pointer'};
    out.reads.ui_binding_context = span(addr(0x2022844), 4);
    const tsPtr = slot.ok ? deref(slot) : null;
    if (!slot.ok) { out.slot_state = 'unreadable'; out.read_budget.used = total; return out; }
    if (tsPtr.isNull()) { out.slot_state = 'null'; out.ts_present = false; out.read_budget.used = total; return out; }
    if (!sane(tsPtr)) { out.slot_state = 'implausible'; out.read_budget.used = total; return out; }
    out.slot_state = 'present';
    out.container = tsPtr.toString();
    const ts = span(tsPtr, 0x100);
    out.reads.ts = ts;
    out.ts_present = ts.ok ? true : null;
    out.container_prefix_hex = ts.ok ? ts.hex : null;
    if (!ts.ok) { out.read_budget.used = total; return out; }
    const word = function (offset) {
      const o = offset * 2;
      return ts.hex.slice(o, o + 8);
    };
    out.counter_hex = word(0xd0);
    out.counter = (function () {
      const s = word(0xd0);
      const value = parseInt(s.slice(6, 8) + s.slice(4, 6) + s.slice(2, 4) + s.slice(0, 2), 16);
      return value > 0x7fffffff ? value - 0x100000000 : value;
    })();
    // The named bindings move the same dword with movd/cvtdq2ps, i.e. signed i32.
    out.clock_ticks_i32 = out.counter > 0x7fffffff ? out.counter - 0x100000000 : out.counter;
    const phasePtr = deref({ok: true, hex: word(0x38)});
    const speedPtr = deref({ok: true, hex: word(0x3c)});
    const netPtr = deref({ok: true, hex: word(0x5c)});
    out.reads.phase_manager = sane(phasePtr) ? span(phasePtr.add(0x0c), 4) : {ok: false, error: 'null pointer'};
    out.reads.speed_header = sane(speedPtr) ? span(speedPtr.add(0x08), 0x0c) : {ok: false, error: 'null pointer'};
    out.reads.network = sane(netPtr) ? span(netPtr.add(0xa0), 0x2c) : {ok: false, error: 'null pointer'};
    let loading = {ok: false, error: 'null pointer'};
    if (out.reads.network.ok) {
      const h = out.reads.network.hex, o = (0xc8 - 0xa0) * 2;
      const lp = deref({ok: true, hex: h.slice(o, o + 8)});
      if (sane(lp)) loading = span(lp.add(0x0c), 4);
    }
    out.reads.loading = loading;
    out.read_budget.used = total;
    return out;
  }
};

// --- optional read-only replay-open watch (CreateFileW only) -----------------
const MAX_EVENTS = 32;
const MAX_TRACE = 8;
let watch = null, watchEvents = [], otherOpens = 0, pathErrors = 0, watchError = null, watchInstalled = false;
let matchingOpens = 0, droppedEvents = 0, invalidHandles = 0;
function normPath(value) {
  if (typeof value !== 'string') return '';
  let v = value.replace(/\//g, '\\');
  while (v.indexOf('\\\\') !== -1) v = v.replace(/\\\\/g, '\\');
  return v.toLowerCase();
}
function safeTrace(context) {
  try { return Thread.backtrace(context, Backtracer.FUZZY).slice(0, MAX_TRACE).map(a => a.toString()); }
  catch (e) { return null; }
}
// Bound one wide-string read to the tail of the single mapping that holds the
// pointer, require a NUL inside that span and stop there. The length is never
// guessed and the read never crosses a mapping edge.
function readWidePath(p) {
  if (!sane(p)) return {ok: false, error: 'null or implausible path pointer'};
  const r = Process.findRangeByAddress(p);
  if (!r) return {ok: false, error: 'path unmapped'};
  if (!r.protection || !r.protection.includes('r')) return {ok: false, error: 'path not readable'};
  const room = parseInt(r.base.add(r.size).toString(), 16) - parseInt(p.toString(), 16);
  let n = Math.min(MAX_PATH_BYTES, room);
  n -= n % 2;
  if (n < 2) return {ok: false, error: 'no path span inside mapping'};
  let bytes;
  try { bytes = new Uint8Array(p.readByteArray(n)); } catch (e) { return {ok: false, error: 'path read failed: ' + e}; }
  let end = -1;
  for (let i = 0; i + 1 < bytes.length; i += 2) {
    if (bytes[i] === 0 && bytes[i + 1] === 0) { end = i; break; }
  }
  if (end < 0) return {ok: false, error: 'path not NUL-terminated inside mapping span'};
  let text = '';
  for (let i = 0; i < end; i += 2) text += String.fromCharCode(bytes[i] | (bytes[i + 1] << 8));
  return {ok: true, value: text, bytes: end};
}
rpc.exports.install_replay_watch = function (config) {
  if (watchInstalled || watch) return {installed: watchInstalled, error: watchError};
  const target = normPath(config.path);
  if (!target) return {installed: false, error: 'no exact target path supplied'};
  watch = {target: target, backtrace: !!config.backtrace};
  let address = null;
  try { address = Module.getExportByName(null, 'CreateFileW'); }
  catch (e) { watchError = 'CreateFileW export unavailable: ' + e; }
  if (!address) {
    try {
      address = Process.getModuleByName('kernel32.dll').getExportByName('CreateFileW');
      watchError = null;
    } catch (e) { watchError = watchError || ('kernel32 CreateFileW unavailable: ' + e); }
  }
  if (!address) return {installed: false, error: watchError};
  try {
    Interceptor.attach(address, {
      onEnter(args) {
        // Win32 CreateFileW ABI: 0 lpFileName, 1 dwDesiredAccess, 2 dwShareMode,
        // 3 lpSecurityAttributes, 4 dwCreationDisposition, 5 dwFlagsAndAttributes.
        try {
          const read = readWidePath(args[0]);
          if (!read.ok) { pathErrors++; return; }
          if (normPath(read.value) !== watch.target) { otherOpens++; return; }
          matchingOpens++;
          // Recorded per invocation: no module-global is shared between calls.
          this.pendingOpen = {path: read.value, access: args[1].toUInt32(), share: args[2].toUInt32(),
                              disposition: args[4].toUInt32(), match: 'path',
                              thread_id: Process.getCurrentThreadId(), timestamp_ns: Date.now() * 1e6,
                              caller: this.returnAddress ? this.returnAddress.toString() : null,
                              backtrace: watch.backtrace ? safeTrace(this.context) : null};
        } catch (e) { pathErrors++; }
      },
      onLeave(retval) {
        const record = this.pendingOpen;
        this.pendingOpen = null;
        if (!record) return;
        const handle = retval.toString();
        const valid = !retval.isNull() && handle !== '0xffffffff';
        if (!valid) invalidHandles++;
        if (watchEvents.length >= MAX_EVENTS) { droppedEvents++; return; }
        record.handle = handle;
        record.valid_handle = valid;
        watchEvents.push(record);
      }
    });
    watchInstalled = true;
    return {installed: true, target: address.toString()};
  } catch (e) {
    watchError = String(e);
    return {installed: false, error: watchError};
  }
};
rpc.exports.replay_watch = function () {
  return {installed: watchInstalled, error: watchError, other_open_count: otherOpens,
          path_read_errors: pathErrors, max_events: MAX_EVENTS, matching_open_attempts: matchingOpens,
          dropped_events: droppedEvents, invalid_handle_count: invalidHandles,
          truncated: droppedEvents > 0, events: watchEvents.slice()};
};
"""

# --------------------------------------------------------------------------- #
# decoding (pure functions, exercised by tests without a live target)
# --------------------------------------------------------------------------- #
def _u(hexstr, offset, size, signed=False):
    start = offset * 2
    raw = hexstr[start:start + size * 2]
    if len(raw) != size * 2:
        raise ValueError("short field at offset %#x" % offset)
    return int.from_bytes(bytes.fromhex(raw), "little", signed=signed)


def _finite(value, out, name):
    """Non-finite floats are unreadable evidence, not JSON-encodable numbers."""
    if value is None or math.isfinite(value):
        return value
    out["errors"][name] = "non-finite float"
    return None


def _f32(hexstr, offset):
    raw = bytes.fromhex(hexstr[offset * 2:offset * 2 + 8])
    if len(raw) != 4:
        raise ValueError("short float at offset %#x" % offset)
    return struct.unpack("<f", raw)[0]


def decode_sample(sample):
    """Turn one raw JSONL sample into decoded, individually-guarded fields."""
    reads = sample.get("reads") or {}
    out = {"errors": {}, "present": {}, "values": {}, "no_services": False, "slot_state": None}

    def note(name, read):
        if not read or not read.get("ok"):
            out["errors"][name] = (read or {}).get("error", "missing")
            out["present"][name] = False
        else:
            out["present"][name] = True

    ts = reads.get("ts")
    note("ts", ts)
    if ts and ts.get("ok"):
        prefix = ts["hex"]
        for name, (offset, kind) in TS_FIELDS.items():
            try:
                value = _f32(prefix, offset) if kind == "f32" else _u(
                    prefix, offset, 1 if kind == "u8" else 4)
                out["values"][name] = _finite(value, out, name) if kind == "f32" else value
            except ValueError as error:
                out["errors"][name] = str(error)
    else:
        # Legacy samples only carried container_prefix_hex.
        prefix = sample.get("container_prefix_hex")
        if prefix:
            try:
                for name, (offset, kind) in TS_FIELDS.items():
                    if offset + (1 if kind == "u8" else 4) <= len(prefix) // 2:
                        value = _f32(prefix, offset) if kind == "f32" else _u(
                            prefix, offset, 1 if kind == "u8" else 4)
                        out["values"][name] = _finite(value, out, name) if kind == "f32" else value
            except ValueError as error:
                out["errors"]["prefix"] = str(error)

    clock = reads.get("clock")
    note("clock", clock)
    if clock and clock.get("ok"):
        out["values"]["speed_factor"] = _finite(_f32(clock["hex"], 0), out, "speed_factor")
        out["values"]["speed_step"] = _u(clock["hex"], 4, 4, signed=True)
    else:
        # Fall back to the legacy scale/counter record only for the counter.
        out["values"]["speed_factor"] = None
        out["values"]["speed_step"] = None

    for name in ("constant_speed_factor_max", "constant_speed_factor_min",
                 "constant_speed_factor_plus_one", "constant_speed_factor_minus_one"):
        read = reads.get(name)
        note(name, read)
        out["values"][name] = _finite(_f32(read["hex"], 0), out, name) if read and read.get("ok") else None

    phase = reads.get("phase_manager")
    note("phase_manager", phase)
    out["values"]["phase_id"] = _u(phase["hex"], 0, 4) if phase and phase.get("ok") else None

    header = reads.get("speed_header")
    note("speed_header", header)
    if header and header.get("ok"):
        # The span starts at +0x08, so offsets here are relative to the span.
        out["values"]["speed_header_direction"] = _u(header["hex"], 0x00, 4)
        out["values"]["speed_header_dword_c"] = _u(header["hex"], 0x04, 4)
        out["values"]["speed_header_float_10"] = _finite(_f32(header["hex"], 0x08), out,
                                                         "speed_header_float_10")
    else:
        out["values"].update(speed_header_direction=None, speed_header_dword_c=None,
                             speed_header_float_10=None)

    net = reads.get("network")
    note("network", net)
    if net and net.get("ok"):
        # The span starts at +0xa0, so offsets here are relative to the span.
        out["values"]["net_pending_a1"] = _u(net["hex"], 0x01, 1)
        out["values"]["net_dedicated_a4"] = _u(net["hex"], 0x04, 1)
        out["values"]["net_replay_candidate_a5"] = _u(net["hex"], 0x05, 1)
        out["values"]["net_loading_obj_c8"] = _u(net["hex"], 0x28, 4)
    else:
        for name in ("net_pending_a1", "net_dedicated_a4", "net_replay_candidate_a5",
                     "net_loading_obj_c8"):
            out["values"][name] = None

    loading = reads.get("loading")
    note("loading", loading)
    out["values"]["loading_phase_index"] = _u(loading["hex"], 0, 4) if loading and loading.get("ok") else None

    mgr = reads.get("manager_chapter")
    note("manager_chapter", mgr)
    out["values"]["chapter_id"] = _u(mgr["hex"], 0, 4) if mgr and mgr.get("ok") else None

    ui = reads.get("ui_binding_context")
    note("ui_binding_context", ui)
    out["values"]["ui_binding_context"] = _u(ui["hex"], 0, 4) if ui and ui.get("ok") else None

    ticks = out["values"].get("tick_counter")
    if ticks is not None:
        out["values"]["tick_counter_i32"] = ticks - 0x100000000 if ticks > 0x7FFFFFFF else ticks

    # "No services" is an explicit, read-proven null slot. An unreadable or
    # implausible slot proves nothing and must stay unreadable.
    out["slot_state"] = sample.get("slot_state")
    out["no_services"] = bool(sample.get("ts_present") is False
                              and sample.get("slot_state") == "null")
    return out


def _f32_round(value):
    """Round a Python double to the nearest IEEE-754 binary32."""
    return struct.unpack("<f", struct.pack("<f", value))[0]


F32_TICK_SECONDS = _f32_round(TICK_SECONDS)


def deterministic_seconds_from_ticks(ticks):
    """Reproduce 0xaaedf0 exactly: f32(int32(ticks) * f32(0.2)).

    ``ticks`` is the raw u32 dword; the named binding moves it with
    ``movd``/``cvtdq2ps``, so the engine sees a signed i32. The product is
    rounded to f32, which is why 4165 yields 833.0 and not 833.0000124.
    """
    if ticks is None:
        return None
    signed = ticks - 0x100000000 if ticks > 0x7FFFFFFF else ticks
    return _f32_round(_f32_round(float(signed)) * F32_TICK_SECONDS)


def _expected_factor(step):
    """Step -> factor per 0x519490 (parent-verified): >=0 -> step+1, else -1/(step-1)."""
    if step is None:
        return None
    return float(step) + 1.0 if step >= 0 else -1.0 / (step - 1.0)


def classify(decoded, replay_field=None):
    """Conservative classification. Unknown is a first-class answer."""
    values = decoded["values"]
    errors = decoded["errors"]
    uncertainties = []
    started = values.get("game_started")
    ended = values.get("game_ended")
    asked = values.get("end_game_asked")

    state, confident = "unreadable", False
    reason = errors.get("ts", "gameplay-services prefix unavailable")

    if decoded.get("no_services"):
        # An explicit null global is an answer, not an exception and not a menu.
        state, confident, reason = "no_gameplay_services", True, "TGameplayServices pointer slot is null"
    else:
        flags = [started, asked, ended]
        if any(flag is None for flag in flags):
            state, reason = "unreadable", "engine flag bytes unavailable"
        elif any(flag not in (0, 1) for flag in flags):
            state, reason = "invalid_flags", "engine flag bytes are not boolean"
            uncertainties.append("engine flags outside {0,1}")
        elif ended == 1 and started == 0:
            state, reason = "contradictory_flags", "GameEnded set while GameStarted clear"
            uncertainties.append("outgame/GameEnded contradiction")
        elif ended == 1:
            # Independent completion: never derived from counter motion.
            state, confident, reason = "game_ended", True, "GameEnded byte is set"
        elif started == 0:
            state, confident, reason = "not_started", True, "GameStarted byte is clear; UI state unknown"
        elif started == 1:
            state, confident, reason = "ingame", True, "GameStarted byte is set"
    if state == "unreadable" and decoded.get("slot_state") in ("unreadable", "implausible"):
        reason = "TGameplayServices slot %s; no state claim" % decoded["slot_state"]

    speed_factor = values.get("speed_factor")
    speed_step = values.get("speed_step")
    implied = _expected_factor(speed_step)
    speed_consistent = None
    if speed_factor is not None and implied is not None and math.isfinite(speed_factor):
        speed_consistent = abs(speed_factor - implied) <= 1e-4 * max(1.0, abs(implied))
        if not speed_consistent:
            uncertainties.append("speed factor disagrees with step-index model")
        low = values.get("constant_speed_factor_min")
        high = values.get("constant_speed_factor_max")
        if low is not None and high is not None and not (low <= speed_factor <= high):
            uncertainties.append("speed factor outside verified clamp constants")
            speed_consistent = False
    elif speed_step is not None:
        uncertainties.append("speed factor unavailable")

    loading_present = values.get("net_loading_obj_c8")
    loading = None if loading_present is None else loading_present != 0

    replay_candidate = values.get("net_replay_candidate_a5")
    replay_validated = False
    replay_active = None
    selected_candidate = None
    if replay_field == "net_a5" and replay_candidate in (0, 1):
        selected_candidate = replay_candidate == 1
    elif replay_field == "controller" and values.get("replay_controller_ptr") is not None:
        selected_candidate = values["replay_controller_ptr"] != 0
    if replay_field in ("net_a5", "controller"):
        uncertainties.append("caller-selected replay candidate is not runtime-validated")

    ticks = values.get("tick_counter")
    deterministic_seconds = deterministic_seconds_from_ticks(ticks)
    return {
        "engine_named_time": {
            "deterministic_ticks": ticks,
            "deterministic_ticks_signed": values.get("tick_counter_i32"),
            "deterministic_seconds": deterministic_seconds,
            "deterministic_seconds_source": "f32(int32(TS+0xd0) * f32(0.2)) via 0xaaedf0; the "
                                            "stored dword is u32, the binding reads it as i32",
            "realtime_seconds": values.get("realtime_current_time"),
            "tick_seconds_scale": F32_TICK_SECONDS,
            "unit": "engine deterministic clock (name-verified binding)",
            "origin": "unknown",
            "epoch_validated": False,
            "replay_frame_mapping": None,
            "bindings": [dict(entry) for entry in ENGINE_NAMED_TIME_BINDINGS],
        },
        "engine_state": state,
        "engine_state_confident": confident,
        "engine_state_reason": reason,
        "engine_game_started": bool(started) if started in (0, 1) else None,
        "engine_end_game_asked": bool(asked) if asked in (0, 1) else None,
        "engine_game_ended": bool(ended) if ended in (0, 1) else None,
        "independent_completion": ended == 1,
        "speed_factor": speed_factor,
        "speed_step": speed_step,
        "speed_step_implied_factor": implied,
        "speed_consistent": speed_consistent,
        "replay_controller_present": (values.get("replay_controller_ptr") or 0) != 0
        if values.get("replay_controller_ptr") is not None else None,
        "replay_net_flag_candidate": replay_candidate,
        "replay_validated": replay_validated,
        "replay_active": replay_active,
        "selected_replay_candidate": selected_candidate,
        "loading_object_present": loading,
        "loading_phase_index": values.get("loading_phase_index"),
        "phase_id": values.get("phase_id"),
        "chapter_id": values.get("chapter_id"),
        "ui_binding_context_present": (values.get("ui_binding_context") or 0) != 0
        if values.get("ui_binding_context") is not None else None,
        "ui_outgame_substate": None,
        "ui_outgame_substate_basis": None,
        "ui_state": None,
        "pause_state": "not_determined",
        "speed_header_direction": values.get("speed_header_direction"),
        "speed_header_dword_c": values.get("speed_header_dword_c"),
        "speed_header_float_10": values.get("speed_header_float_10"),
        "net_pending_a1": values.get("net_pending_a1"),
        "net_dedicated_a4": values.get("net_dedicated_a4"),
        "uncertainties": uncertainties,
        "errors": errors,
    }


_FINGERPRINT_FIELDS = {"chapter_id": int, "phase_id": int, "ui_binding_context_present": bool}


def apply_fingerprint(state, fingerprint):
    """Map an outgame observation to menu/browser only from an observed config."""
    if not fingerprint or state["engine_state"] != "not_started":
        return state
    for entry in fingerprint.get("outgame", []):
        if not isinstance(entry, dict) or any(
                type(entry.get(key)) is not kind or type(state.get(key)) is not kind
                for key, kind in _FINGERPRINT_FIELDS.items()):
            continue
        if (state["chapter_id"] == entry.get("chapter_id")
                and state["phase_id"] == entry.get("phase_id")
                and state["ui_binding_context_present"] == entry.get("ui_binding_context_present")):
            state["ui_outgame_substate"] = entry["name"]
            state["ui_outgame_substate_basis"] = "caller_supplied_raw_fingerprint"
            return state
    state["uncertainties"].append("outgame fingerprint did not match any observed entry")
    return state


def expect_matches(predicate, summary):
    """Return True/False, or None when the predicate cannot be decided.

    Unknown is never coerced to a verdict: a missing or discontinuous counter
    comparison, or an uncalibrated loading field, returns None.
    """
    observation = summary.get("observation")
    if predicate in ("stable_counter", "advancing_counter"):
        if (summary.get("samples") or 0) < 2 or observation not in ("stable_counter",
                                                                    "advancing_counter"):
            return None
        delta = summary.get("counter_delta")
        if delta is None:
            return None
        return delta == 0 if predicate == "stable_counter" else delta != 0
    if predicate == "engine_game_ended":
        return summary.get("engine_game_ended")
    if predicate == "engine_game_started":
        return summary.get("engine_game_started")
    if predicate == "no_gameplay_services":
        return summary.get("engine_state") == "no_gameplay_services"
    if predicate == "outgame":
        return None  # A clear GameStarted flag does not establish a frontend screen.
    if predicate == "ingame":
        return summary.get("engine_state") == "ingame"
    if predicate == "loading":
        # A non-null [net+0xc8] pointer is presence evidence only; the loading
        # *state* needs a calibration flag that no capture has produced yet.
        if not summary.get("loading_calibrated"):
            return None
        return summary.get("loading_active")
    if predicate == "replay_active":
        return summary.get("replay_active")
    return None


def summarize(samples, replay_field=None, fingerprint=None):
    if len(samples) < 2:
        raise ValueError("at least two samples required")
    pairs = list(zip(samples, samples[1:]))
    discontinuity = any(
        _container(a) != _container(b) or _counter(b) is not None and _counter(b) < (_counter(a) or 0)
        for a, b in pairs)
    elapsed = (samples[-1]["monotonic_ns"] - samples[0]["monotonic_ns"]) / 1e9
    first, last = _counter(samples[0]), _counter(samples[-1])
    delta = None if first is None or last is None else last - first
    decoded = decode_sample(samples[-1])
    state = classify(decoded, replay_field=replay_field)
    state = apply_fingerprint(state, fingerprint)
    observation = "discontinuity" if discontinuity else (
        "stable_counter" if delta == 0 else "advancing_counter" if delta is not None else "unreadable"
    )
    stationary = None if observation not in ("stable_counter", "advancing_counter") \
        else observation == "stable_counter"
    if stationary:
        pause_reason = "stationary counter is not evidence of pause without a witnessed input and repeat"
    else:
        pause_reason = "pause state is not exposed by any verified field"
    result = {
        "observation": observation,
        "counter_delta": delta,
        "wall_seconds": elapsed,
        "counter_per_wall_second": delta / elapsed if delta is not None and elapsed > 0 and not discontinuity else None,
        "simulation_time_validated": False,
        "stationary_counter": stationary,
        "loading_calibrated": False,
        "container": _container(samples[-1]),
        "samples": len(samples),
        **state,
        "pause_state": "not_determined",
        "pause_state_reason": pause_reason,
    }
    return result


def _container(sample):
    return sample.get("container")


def _counter(sample):
    value = sample.get("counter")
    return value if isinstance(value, int) else None


def normalize_windows_path(value):
    """Case-insensitive comparison form for a Win32 path; separators collapsed."""
    if not isinstance(value, str):
        return ""
    text = value.replace("/", "\\")
    while "\\\\" in text:
        text = text.replace("\\\\", "\\")
    return text.lower()


def sha256_file(path):
    digest = hashlib.sha256()
    size = 0
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
            size += len(chunk)
    return {"sha256": digest.hexdigest(), "size": size}


def evaluate_replay_open(watch, expected_sha256, before, after):
    """Purely local evaluation of the optional CreateFileW watch.

    Evidence is file-content identity; a matching UI selection or a context
    pointer is not evidence about which file the engine opened.
    """
    watch = watch or {}
    events = watch.get("events") or []
    valid = [event for event in events if event.get("valid_handle")]
    truncated = watch.get("truncated")
    invalid = any(not event.get("valid_handle") for event in events)
    invalid_count = watch.get("invalid_handle_count")
    invalid_observed = (invalid_count > 0 if isinstance(invalid_count, int)
                        else True if invalid else None)
    return {
        "watch_installed": bool(watch.get("installed")),
        "watch_error": watch.get("error"),
        "observed": bool(events),
        "open_attempts": watch.get("matching_open_attempts"),
        "retained_open_results": len(events),
        "path_read_errors": watch.get("path_read_errors"),
        "max_events": watch.get("max_events"),
        "dropped_events": watch.get("dropped_events"),
        "truncated": truncated,
        "invalid_handle_observed": invalid_observed,
        "observation_complete": (bool(watch.get("installed")) and watch.get("path_read_errors") == 0
                                 and truncated is False and watch.get("matching_open_attempts") == len(events)),
        "valid_handle": bool(valid),
        "matched_by": sorted({event.get("match") for event in events if event.get("match")}),
        "other_open_count": watch.get("other_open_count"),
        "expected_sha256": expected_sha256,
        "sha256_before": before["sha256"] if before else None,
        "sha256_after": after["sha256"] if after else None,
        "size": before["size"] if before else None,
        "content_stable": bool(before and after and before["sha256"] == after["sha256"]),
        "verified": bool(watch.get("installed")) and bool(valid) and bool(
            before and after and before["sha256"] == expected_sha256 == after["sha256"]),
        "scope": "file content identity only; UI selection is not evidence",
    }


def load_fingerprint(path):
    if not path:
        return None
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    entries = data.get("outgame")
    if not isinstance(entries, list) or not entries:
        raise ValueError("fingerprint requires a non-empty outgame list")
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("name"), str) or any(
                type(entry.get(key)) is not kind for key, kind in _FINGERPRINT_FIELDS.items()):
            raise ValueError("fingerprint requires name, integer chapter_id/phase_id and boolean UI context")
    return data


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pid", type=int, required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--samples", type=int, default=12)
    parser.add_argument("--interval", type=float, default=0.2)
    parser.add_argument("--timeout", type=float, default=10.0,
                        help="bounded condition-wait budget in seconds (max 30)")
    parser.add_argument("--expect", choices=[
        "stable_counter", "advancing_counter", "engine_game_ended", "engine_game_started",
        "no_gameplay_services", "outgame", "ingame", "loading", "replay_active"])
    parser.add_argument("--replay-field", choices=["none", "net_a5", "controller"], default="none",
                        help="select a raw candidate to report; does not validate replay state")
    parser.add_argument("--fingerprint", help="observed outgame fingerprint JSON (menu/browser)")
    parser.add_argument("--replay", help="authenticated replay file whose open should be observed")
    parser.add_argument("--replay-sha256", default=REPLAY_SHA256,
                        help="expected replay content hash (defaults to the pinned capture)")
    parser.add_argument("--require-replay-open", action="store_true",
                        help="exit 3 unless a matching open with a valid handle is verified")
    parser.add_argument("--backtrace", action="store_true", help="record caller backtrace for matches")
    args = parser.parse_args(argv)
    if args.require_replay_open and not args.replay:
        parser.error("--require-replay-open requires --replay")
    if not 2 <= args.samples <= MAX_SAMPLES or not 0.05 <= args.interval <= 1 \
            or args.samples * args.interval > MAX_SECONDS or not 0 < args.timeout <= MAX_SECONDS:
        parser.error("bound samples to 2..150, interval to 0.05..1, total and timeout to 30 seconds")
    if sys.platform != "win32":
        parser.error("observer must run in the authorized Windows guest")
    fingerprint = load_fingerprint(args.fingerprint)
    if args.replay and len(args.replay_sha256) != 64:
        parser.error("--replay-sha256 must be a 64-character hex digest")
    import frida
    from wgrd_frida import process_identity, verify_loaded
    path, created = process_identity(args.pid)
    image = Path(path).read_bytes()
    if hashlib.sha256(image).hexdigest() != EXE_SHA256:
        raise ValueError("executable SHA-256 mismatch")
    if REVISION_MARKER not in image:
        raise ValueError("revision marker mismatch")
    before = sha256_file(args.replay) if args.replay else None
    if args.replay and before["sha256"] != args.replay_sha256:
        raise ValueError("replay SHA-256 mismatch")
    deadline = time.monotonic() + args.timeout
    exit_code = 0
    with open(args.output, "x", encoding="utf-8") as output:
        def write(record):
            output.write(json.dumps(record, allow_nan=False, separators=(",", ":")) + "\n")
            output.flush()
        write({"event": "start", "pid": args.pid, "created_filetime": created,
               "exe_sha256": EXE_SHA256, "script_sha256": hashlib.sha256(SCRIPT.encode()).hexdigest(),
               "expect": args.expect, "replay_field": args.replay_field,
               "planned_read_bytes": PLANNED_BYTES,
               "timestamp_utc": datetime.now(timezone.utc).isoformat()})
        session = script = None
        samples = []
        result = None
        try:
            session = frida.get_local_device().attach(args.pid)
            if process_identity(args.pid) != (path, created):
                raise ValueError("process changed during attach")
            script = session.create_script(SCRIPT)
            script.load()
            info = script.exports_sync.inspect()
            verify_loaded({"sha256": EXE_SHA256, "module": "wargame3.exe",
                           "ghidra_base": "0x400000", "hooks": []}, image, info, path)
            write({"event": "identity_verified", "module": info})
            if args.replay:
                watch_status = script.exports_sync.install_replay_watch({
                    "path": str(Path(args.replay).resolve()),
                    "backtrace": args.backtrace,
                })
                write({"event": "replay_watch", **watch_status,
                       "replay_sha256": args.replay_sha256})
            next_poll = time.monotonic()
            limit = MAX_SAMPLES if args.expect else args.samples
            uncertain = False
            earlier = []
            while True:
                remaining = next_poll - time.monotonic()
                if remaining > 0:
                    time.sleep(remaining)  # Explicit bounded sampling interval.
                read_started = time.monotonic_ns()
                sample = script.exports_sync.state()
                sample.update(event="counter_sample", monotonic_ns=time.monotonic_ns(),
                              read_started_ns=read_started,
                              timestamp_utc=datetime.now(timezone.utc).isoformat())
                samples.append(sample)
                write(sample)
                next_poll += args.interval
                if len(samples) >= 2:
                    result = summarize(samples, replay_field=args.replay_field,
                                       fingerprint=fingerprint)
                    if result["engine_state"] in ("unreadable", "invalid_flags",
                                                  "contradictory_flags"):
                        # Earlier uncertainty is recorded, never carried into the verdict.
                        earlier.append({"sample": len(samples),
                                        "engine_state": result["engine_state"],
                                        "reason": result["engine_state_reason"]})
                if args.expect:
                    if len(samples) >= 2 and expect_matches(args.expect, result) is True:
                        break
                    if time.monotonic() >= deadline or len(samples) >= limit:
                        break
                elif len(samples) >= limit:
                    break
                if time.monotonic() >= deadline:
                    break
            if len(samples) < 2:
                write({"event": "summary", "observation": "insufficient_samples",
                       "engine_state": "unreadable", "samples": len(samples)})
                write({"event": "end", "cleanup_errors": 0})
                return 3
            result = summarize(samples, replay_field=args.replay_field, fingerprint=fingerprint)
            if process_identity(args.pid) != (path, created):
                raise ValueError("process changed during observation")
            if hashlib.sha256(Path(path).read_bytes()).hexdigest() != EXE_SHA256:
                raise ValueError("image changed during observation")
            if args.replay:
                watch = script.exports_sync.replay_watch()
                for event in watch.get("events", []):
                    write({"event": "replay_open", **event})
                after = sha256_file(args.replay)
                result["replay_open"] = evaluate_replay_open(
                    watch, args.replay_sha256, before, after)
                write({"event": "replay_verification", **result["replay_open"]})
                if args.require_replay_open and not result["replay_open"]["verified"]:
                    uncertain = True
            result["earlier_uncertain_states"] = earlier
            write({"event": "summary", **result})
            verdict = expect_matches(args.expect, result) if args.expect else None
            if result["engine_state"] in ("unreadable", "invalid_flags", "contradictory_flags"):
                uncertain = True
            if args.expect and verdict is None:
                uncertain = True
            if uncertain:
                exit_code = 3
            elif args.expect and verdict is False:
                exit_code = 2
        except BaseException as error:
            write({"event": "failure", "error": str(error)})
            raise
        finally:
            if script is not None:
                script.unload()
            if session is not None:
                session.detach()
        write({"event": "end", "cleanup_errors": 0})
    print(json.dumps(result, allow_nan=False))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
