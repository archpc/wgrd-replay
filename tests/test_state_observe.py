"""Bounded multi-field engine-state observer: decoding, classification, fail-closed gates.

Engine semantics are not asserted here beyond the fields the pinned binary proves;
these tests pin the *observer contract* (bounds, error handling, conservative state).
"""
import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import re
import shutil
import struct
import subprocess
import tempfile
import unittest
import unittest.mock

ROOT = Path(__file__).resolve().parents[1]

# Frida read-API simulation, embedded so the repository scope stays at
# instrumentation/state_observe.py + this test file.
SIM_JS = r"""'use strict';
// Simulates the Frida read API surface used by instrumentation/state_observe.py so
// the observer's bounds/classification contract is testable without a target.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');

const scriptPath = process.argv[2];
assert.ok(scriptPath, 'usage: node frida_state_sim.js <state_observe.py> <out.json>');

class Pointer {
  constructor(n) { this.n = n >>> 0; }
  add(n) { return new Pointer((this.n + n) >>> 0); }
  compare(p) { return Math.sign(this.n - p.n); }
  isNull() { return this.n === 0; }
  toUInt32() { return this.n >>> 0; }
  toString() { return '0x' + this.n.toString(16); }
  readUtf16String(max) {
    const range = lookup(this.n);
    if (!range) throw new Error('access violation');
    const bytes = range.data.subarray(this.n - range.base);
    let out = '';
    for (let i = 0; i + 1 < bytes.length && out.length < max; i += 2) {
      const code = bytes[i] | (bytes[i + 1] << 8);
      if (code === 0) break;
      out += String.fromCharCode(code);
    }
    return out;
  }
  readByteArray(n) {
    const range = lookup(this.n);
    if (!range) throw new Error('access violation');
    const off = this.n - range.base;
    if (off + n > range.data.length) throw new Error('access violation');
    return range.data.slice(off, off + n).buffer;
  }
}
const ranges = [];
function map(base, size) { const r = {base, size, data: new Uint8Array(size)}; ranges.push(r); return r; }
function lookup(address) { return ranges.find(r => address >= r.base && address < r.base + r.size) || null; }
function rangeAt(address) {
  const r = lookup(address);
  if (!r) return null;
  return {base: new Pointer(r.base), size: r.size, protection: 'rw-'};
}
function write(base, offset, bytes) {
  const r = lookup(base);
  assert.ok(r, 'fixture address 0x' + base.toString(16) + ' is not mapped');
  r.data.set(bytes, offset);
}
function u32(value) { const b = Buffer.alloc(4); b.writeUInt32LE(value >>> 0); return b; }
function f32(value) { const b = Buffer.alloc(4); b.writeFloatLE(value); return b; }

// Module image holds the static clock object and the four clamp/offset constants.
map(0x400000, 0x2000000);
write(0x400000, 0x1fce0d0 - 0x400000 + 0x68, Buffer.concat([f32(1.0), Buffer.alloc(4)]));
write(0x400000, 0x1932738 - 0x400000, f32(100.0));
write(0x400000, 0x19326d8 - 0x400000, f32(0.01));
write(0x400000, 0x19326e8 - 0x400000, f32(1.0));
write(0x400000, 0x1932748 - 0x400000, f32(-1.0));

const TS = 0x21100000, PHASE = 0x21200000, HEADER = 0x21300000;
const NET = 0x21400000, LOADING = 0x21500000, MANAGER = 0x21600000;
for (const base of [TS, PHASE, HEADER, NET, LOADING, MANAGER]) map(base, 0x1000);

const hooks = [];

// Real resolver shape: kernel32 and KERNELBASE export different CreateFileW
// addresses, and the unnamed module search lands on yet another address. A
// regression that watches the wrong resolution point is therefore visible.
function buildSandbox(opts, sink) {
  opts = opts || {};
  const localHooks = sink || [];
  const modules = {
    'wargame3.exe': {
      name: 'wargame3.exe', path: 'C:/fixture/wargame3.exe', base: new Pointer(0x400000),
      size: 0x2000000, readU16: () => 0x5a4d, readU32: () => 0
    },
    'kernel32.dll': {
      name: 'kernel32.dll', base: new Pointer(0x76d00000),
      getExportByName: name => {
        if (name === 'CreateFileW') return new Pointer(0x76dc1c70);
        throw new Error('unresolved export ' + name);
      }
    }
  };
  if (opts.kernelBase !== false) {
    modules['KERNELBASE.dll'] = {
      name: 'KERNELBASE.dll', base: new Pointer(0x77100000),
      getExportByName: name => {
        if (name === 'CreateFileW') return new Pointer(0x77141ce0);
        throw new Error('unresolved export ' + name);
      }
    };
  }
  const scope = {
    rpc: {exports: {}},
    Date,
    Module: {getExportByName: (mod, name) => {
      if (name === 'CreateFileW') return new Pointer(0x76dc1c00);
      throw new Error('unresolved export ' + name);
    }},
    Interceptor: {attach: (address, callbacks) => { localHooks.push({address, callbacks}); return {detach() {}}; }},
    Thread: {backtrace: () => [new Pointer(0x401000), new Pointer(0x402000)]},
    Backtracer: {FUZZY: 'fuzzy'},
    ptr: value => new Pointer(typeof value === 'string' ? Number(value) : value),
    Process: {
      pointerSize: 4,
      arch: 'ia32',
      getModuleByName: name => {
        if (!Object.prototype.hasOwnProperty.call(modules, name))
          throw new Error('module not found: ' + name);
        return modules[name];
      },
      getCurrentThreadId: () => 4242,
      findRangeByAddress: p => (p ? rangeAt(p.n) : null)
    },
    Uint8Array, Number, parseInt, Math, Error, Buffer: undefined
  };
  vm.runInNewContext(fs.readFileSync(scriptPath, 'utf8'), scope);
  return {api: scope.rpc.exports, hooks: localHooks, sandbox: scope};
}

const env = buildSandbox({}, hooks);
const api = env.api;
const sandbox = env.sandbox;

function tsFixture({started = 1, asked = 0, ended = 0, phase = PHASE, header = HEADER,
                    net = NET, seconds = 1234.5, ticks = 4165, replay = 0, loading = 0} = {}) {
  const ts = new Uint8Array(0xd4);
  ts[0x20] = started; ts[0x21] = asked; ts[0x22] = ended;
  ts.set(u32(phase), 0x38); ts.set(u32(header), 0x3c); ts.set(u32(net), 0x5c);
  ts.set(f32(seconds), 0x98); ts.set(u32(ticks), 0xd0);
  return ts;
}

function reset() {
  write(TS, 0, new Uint8Array(0x1000));
  write(PHASE, 0, new Uint8Array(0x1000));
  write(HEADER, 0, new Uint8Array(0x1000));
  write(NET, 0, new Uint8Array(0x1000));
  write(LOADING, 0, new Uint8Array(0x1000));
  write(MANAGER, 0, new Uint8Array(0x1000));
  write(0x400000, 0x201d318 - 0x400000, u32(TS));
  write(0x400000, 0x2024a40 - 0x400000, u32(MANAGER));
  write(0x400000, 0x2022844 - 0x400000, u32(0));
  write(0x400000, 0x195d768 - 0x400000, f32(0.2));
}

const scenarios = {};

reset();
write(TS, 0, tsFixture());
write(PHASE, 0x0c, u32(3));
write(HEADER, 0x08, Buffer.concat([u32(1), u32(2), f32(1.5)]));
write(MANAGER, 0x74, u32(7));
scenarios.ingame = api.state();
assert.equal(scenarios.ingame.counter, 4165, 'raw tick counter is preserved');
assert.equal(scenarios.ingame.reads.ts.ok, true);
assert.equal(scenarios.ingame.counter_hex, Buffer.from(u32(4165)).toString('hex'));
assert.equal(scenarios.ingame.scale_hex, 'cdcc4c3e');
assert.equal(scenarios.ingame.container_prefix_hex.length, 0x100 * 2);
write(0x400000, 0x195d768 - 0x400000, f32(0.1));
assert.throws(() => api.state(), /clock scale byte mismatch/);
reset();
write(TS, 0, tsFixture({ticks: 0xffffffff}));
assert.equal(api.state().counter, -1, 'legacy counter remains a signed i32');

reset();
write(TS, 0, tsFixture({replay: 1, loading: 1, ticks: 0}));
write(NET, 0xa5, Uint8Array.of(1));
write(NET, 0xa4, Uint8Array.of(0));
write(NET, 0xa1, Uint8Array.of(1));
write(NET, 0xc8, u32(LOADING));
write(LOADING, 0x0c, u32(9));
scenarios.replay_loading = api.state();
assert.equal(scenarios.replay_loading.reads.loading.ok, true);

reset();
write(TS, 0, tsFixture({started: 0, ended: 1}));
scenarios.contradiction = api.state();

reset();
write(TS, 0, tsFixture());
write(0x400000, 0x1fce0d0 - 0x400000 + 0x68, Buffer.concat([f32(0.5), u32(0xffffffff)]));
scenarios.negative_step = api.state();

reset();
write(TS, 0, tsFixture({started: 2}));
scenarios.invalid_flag = api.state();

reset();
write(0x400000, 0x201d318 - 0x400000, u32(0));
scenarios.null_slot = api.state();
assert.equal(scenarios.null_slot.ts_present, false);

reset();
write(0x400000, 0x201d318 - 0x400000, u32(0x21900000));  // unmapped object
scenarios.unmapped_ts = api.state();
assert.equal(scenarios.unmapped_ts.reads.ts.ok, false);
assert.ok(scenarios.unmapped_ts.reads.clock, 'independent reads still attempted');

// Span crossing a mapping edge must be refused, not silently truncated.
map(0x21800000, 0x40);
write(0x400000, 0x201d318 - 0x400000, u32(0x21800020));
scenarios.crossing_span = api.state();
assert.equal(scenarios.crossing_span.reads.ts.ok, false);
assert.match(scenarios.crossing_span.reads.ts.error, /crosses mapping/);

// Implausible but non-null slot: not a read-proven null, so not "no services".
reset();
write(0x400000, 0x201d318 - 0x400000, u32(0x8000));
scenarios.implausible_slot = api.state();
assert.equal(scenarios.implausible_slot.ts_present, null);
assert.equal(scenarios.implausible_slot.slot_state, 'implausible');

// Optional CreateFileW watch: real Win32 ABI, bounded per-invocation state.
scenarios.rpc_export_names = Object.keys(api);
map(0x50a00000, 0x1000);
function wide(address, text, opts) {
  const nul = !opts || opts.nul !== false;
  const bytes = Buffer.alloc(text.length * 2 + (nul ? 2 : 0));
  for (let i = 0; i < text.length; i++) bytes.writeUInt16LE(text.charCodeAt(i), i * 2);
  write(0x50a00000, address - 0x50a00000, bytes);
}
reset();
const install = api.installReplayWatch({
  path: 'C:/Replays/match.wrpl', backtrace: true
});
assert.equal(install.installed, true);
assert.equal(hooks.length, 1);
wide(0x50a00100, 'C:\\Windows\\other.dll');
wide(0x50a00200, 'c:\\replays\\MATCH.wrpl');
wide(0x50a00300, 'D:\\copies\\match.wrpl');
wide(0x50a00400, 'C:\\Replays\\match.wrpl.bak');

// Win32 CreateFileW: 0 lpFileName, 1 dwDesiredAccess, 2 dwShareMode,
// 3 lpSecurityAttributes, 4 dwCreationDisposition, 5 dwFlagsAndAttributes.
function argsFor(namePointer, access, share, disposition) {
  return [namePointer, new Pointer(access >>> 0), new Pointer(share), new Pointer(0),
    new Pointer(disposition), new Pointer(0x80)];
}
function context(caller) {
  return {returnAddress: new Pointer(caller), context: {esp: new Pointer(0x8000)}};
}
function enter(ctx, namePointer, access, share, disposition) {
  hooks[0].callbacks.onEnter.call(ctx, argsFor(namePointer, access, share, disposition));
}
function leave(ctx, handle) { hooks[0].callbacks.onLeave.call(ctx, handle); }
function full(ctx, namePointer, handle, access, share, disposition) {
  enter(ctx, namePointer, access, share, disposition);
  leave(ctx, handle);
}
const ctx0 = context(0x401234);
full(ctx0, new Pointer(0x50a00100), new Pointer(0x1a4), 0x80000000, 3, 3);
full(ctx0, new Pointer(0x50a00200), new Pointer(0x1a8), 0x80000000, 3, 3);
full(ctx0, new Pointer(0x50a00300), new Pointer(0xffffffff), 1, 0, 2);
full(ctx0, new Pointer(0x50a00400), new Pointer(0x1ac), 1, 0, 2);
const watchA = api.replayWatch();
scenarios.replay_watch = {install, ...watchA, hooks: hooks.length};
assert.equal(watchA.other_open_count, 3, 'non-matching opens are counted, never retained');
assert.equal(watchA.events.length, 1);
assert.equal(watchA.events[0].match, 'path');
assert.equal(watchA.events[0].valid_handle, true);
assert.equal(watchA.events[0].access, 0x80000000, 'args[1] is dwDesiredAccess');
assert.equal(watchA.events[0].share, 3, 'args[2] is dwShareMode');
assert.equal(watchA.events[0].disposition, 3, 'args[4] is dwCreationDisposition');
assert.equal(watchA.events[0].backtrace.length, 2);
assert.equal(JSON.stringify(watchA).includes('other.dll'), false);
assert.equal(JSON.stringify(watchA).includes('copies'), false);

// Two interleaved opens on different contexts must not share a pending record.
const ctxA = context(0x401111), ctxB = context(0x402222);
enter(ctxA, new Pointer(0x50a00200), 1, 0, 3);
enter(ctxB, new Pointer(0x50a00200), 2, 1, 4);
leave(ctxB, new Pointer(0x1b0));
leave(ctxA, new Pointer(0x1b4));
const watchB = api.replayWatch();
scenarios.replay_watch_interleaved = {events: watchB.events, other_open_count: watchB.other_open_count,
  path_read_errors: watchB.path_read_errors};
assert.equal(watchB.events.length, 3);
assert.equal(watchB.events[1].handle, '0x1b0');
assert.equal(watchB.events[1].access, 2);
assert.equal(watchB.events[1].caller, '0x402222');
assert.equal(watchB.events[2].handle, '0x1b4');
assert.equal(watchB.events[2].access, 1);
assert.equal(watchB.events[2].caller, '0x401111');

// A wide path that is not NUL-terminated inside its mapping is refused, not truncated.
map(0x50b00000, 0x20);
write(0x50b00000, 0x1c, Buffer.from('41004200', 'hex'));
full(context(0x401234), new Pointer(0x50b0001e), new Pointer(0x1c0), 1, 0, 3);
map(0x50c00000, 0x800);
const longText = 'A'.repeat(512);
write(0x50c00000, 0, Buffer.from(longText.split('').map(c => c + '\u0000').join(''), 'binary'));
full(context(0x401234), new Pointer(0x50c00000), new Pointer(0x1c4), 1, 0, 3);
const watchC = api.replayWatch();
scenarios.replay_watch_bounded = {events: watchC.events.length - 3,
  other_open_count: watchC.other_open_count, path_read_errors: watchC.path_read_errors};
assert.equal(watchC.events.length, 3, 'refused path reads never become events');
assert.equal(watchC.path_read_errors, 2);
assert.equal(watchC.other_open_count, 3, 'refused reads are not counted as non-matching opens');
assert.equal(JSON.stringify(watchC).includes('AAAAAAAA'), false);
// Retention saturation must not erase a later failed matching open.
for (let i = 0; i < 40; i++)
  full(context(0x401234), new Pointer(0x50a00200), new Pointer(0x2000 + i), 1, 0, 3);
full(context(0x401234), new Pointer(0x50a00200), new Pointer(0xffffffff), 1, 0, 3);
scenarios.replay_watch_saturated = api.replayWatch();

// Resolver selection: the live module exports differ, so the watched address
// identifies which resolver the script actually chose.
const preferred = buildSandbox({}, []);
const preferredInstall = preferred.api.installReplayWatch({path: 'C:\\Replays\\match.wrpl'});
scenarios.replay_watch_resolver_preferred = {
  install: preferredInstall,
  watch: preferred.api.replayWatch(),
  attach_address: preferred.hooks.length ? preferred.hooks[0].address.toString() : null
};
assert.equal(preferredInstall.installed, true);
assert.equal(preferredInstall.module, 'KERNELBASE.dll', 'KERNELBASE export is preferred');
assert.equal(preferred.hooks[0].address.toString(), '0x77141ce0');

const fallback = buildSandbox({kernelBase: false}, []);
const fallbackInstall = fallback.api.installReplayWatch({path: 'C:\\Replays\\match.wrpl'});
scenarios.replay_watch_resolver_fallback = {
  install: fallbackInstall,
  watch: fallback.api.replayWatch(),
  attach_address: fallback.hooks.length ? fallback.hooks[0].address.toString() : null
};
assert.equal(fallbackInstall.installed, true);
assert.equal(fallbackInstall.module, 'kernel32.dll', 'kernel32 remains the fallback');
assert.equal(fallback.hooks[0].address.toString(), '0x76dc1c70');

fs.writeFileSync(process.argv[3], JSON.stringify(scenarios));
console.log('WGRD_STATE_SIM_OK');
"""
spec = importlib.util.spec_from_file_location("state_observe", ROOT / "instrumentation/state_observe.py")
assert spec is not None and spec.loader is not None
state = importlib.util.module_from_spec(spec)
spec.loader.exec_module(state)


def load_sim():
    """Run the Frida read-API simulation once; returns decoded scenario records."""
    if not shutil.which("node"):
        raise unittest.SkipTest("Node is unavailable for the Frida read simulation")
    with tempfile.TemporaryDirectory() as tmp:
        script = Path(tmp) / "observer.js"
        sim = Path(tmp) / "sim.js"
        out = Path(tmp) / "out.json"
        script.write_text(state.SCRIPT, encoding="utf-8")
        sim.write_text(SIM_JS, encoding="utf-8")
        result = subprocess.run(["node", str(sim), str(script), str(out)],
                                capture_output=True, text=True)
        assert result.returncode == 0, result.stdout + result.stderr
        assert "WGRD_STATE_SIM_OK" in result.stdout
        return json.loads(out.read_text(encoding="utf-8"))


SIM = load_sim()


def sample(record, ns):
    return {**record, "monotonic_ns": ns}


class CounterMechanics(unittest.TestCase):
    """Legacy behaviour that must survive the extension."""

    def test_advancing_counter_reports_raw_rate_without_time_semantics(self):
        out = state.summarize([{"counter": 10, "monotonic_ns": 0, "container": "0x1"},
                               {"counter": 20, "monotonic_ns": 1000000000, "container": "0x1"}])
        self.assertEqual(out["counter_delta"], 10)
        self.assertEqual(out["counter_per_wall_second"], 10)
        self.assertEqual(out["observation"], "advancing_counter")
        self.assertFalse(out["simulation_time_validated"])

    def test_stable_counter_is_not_called_paused(self):
        out = state.summarize([{"counter": 10, "monotonic_ns": 0, "container": "0x1"},
                               {"counter": 10, "monotonic_ns": 1000000000, "container": "0x1"}])
        self.assertEqual(out["observation"], "stable_counter")
        self.assertTrue(out["stationary_counter"])
        self.assertEqual(out["pause_state"], "not_determined")
        self.assertIsNone(out["ui_state"])

    def test_game_ended_flag_is_independent_of_stationary_counter(self):
        samples = [{"counter": 4165, "monotonic_ns": 0, "container": "0x1",
                    "container_prefix_hex": (bytes(0x22) + b"\x01" + bytes(221)).hex()},
                   {"counter": 4165, "monotonic_ns": 1000000000, "container": "0x1",
                    "container_prefix_hex": (bytes(0x22) + b"\x01" + bytes(221)).hex()}]
        out = state.summarize(samples)
        self.assertTrue(out["engine_game_ended"])
        self.assertTrue(out["stationary_counter"], "completion must not be inferred from motion")
        samples[-1]["container_prefix_hex"] = bytes(256).hex()
        self.assertFalse(state.summarize(samples)["engine_game_ended"])

    def test_reset_or_container_change_is_discontinuity(self):
        for end in [{"counter": 1, "monotonic_ns": 1, "container": "0x1"},
                    {"counter": 11, "monotonic_ns": 1, "container": "0x2"}]:
            out = state.summarize([{"counter": 10, "monotonic_ns": 0, "container": "0x1"}, end])
            self.assertEqual(out["observation"], "discontinuity")


class FieldDecoding(unittest.TestCase):
    def test_nonfinite_legacy_and_constant_values_remain_strict_json(self):
        prefix = bytearray.fromhex(SIM["ingame"]["container_prefix_hex"])
        struct.pack_into("<f", prefix, 0x98, float("nan"))
        decoded = state.decode_sample({"container_prefix_hex": prefix.hex()})
        self.assertIsNone(decoded["values"]["realtime_current_time"])
        json.dumps(state.classify(decoded), allow_nan=False)
        current = json.loads(json.dumps(SIM["ingame"]))
        current["reads"]["constant_speed_factor_max"]["hex"] = struct.pack("<f", float("inf")).hex()
        decoded = state.decode_sample(current)
        self.assertIsNone(decoded["values"]["constant_speed_factor_max"])
        json.dumps(decoded, allow_nan=False)

    def test_all_planned_fields_decode_from_a_live_shaped_record(self):
        decoded = state.decode_sample(SIM["ingame"])
        self.assertEqual(decoded["values"]["game_started"], 1)
        self.assertEqual(decoded["values"]["game_ended"], 0)
        self.assertEqual(decoded["values"]["tick_counter"], 4165)
        self.assertEqual(decoded["values"]["phase_id"], 3)
        self.assertEqual(decoded["values"]["chapter_id"], 7)
        self.assertAlmostEqual(decoded["values"]["speed_header_float_10"], 1.5, places=6)
        self.assertEqual(decoded["values"]["speed_header_dword_c"], 2)
        self.assertEqual(decoded["values"]["speed_header_direction"], 1)

    def test_speed_factor_and_step_are_distinct_from_any_time_field(self):
        decoded = state.decode_sample(SIM["ingame"])
        self.assertAlmostEqual(decoded["values"]["speed_factor"], 1.0, places=6)
        self.assertEqual(decoded["values"]["speed_step"], 0)
        self.assertNotIn("simulation_time", decoded["values"])

    def test_negative_speed_step_decodes_and_matches_the_verified_formula(self):
        decoded = state.decode_sample(SIM["negative_step"])
        self.assertEqual(decoded["values"]["speed_step"], -1)
        self.assertAlmostEqual(decoded["values"]["speed_factor"], 0.5, places=6)
        out = state.classify(decoded)
        self.assertAlmostEqual(out["speed_step_implied_factor"], 0.5, places=6)
        self.assertTrue(out["speed_consistent"])
        self.assertEqual(out["speed_factor"], 0.5)

    def test_unreadable_subobject_records_an_error_without_throwing(self):
        decoded = state.decode_sample(SIM["unmapped_ts"])
        self.assertFalse(decoded["present"]["ts"])
        self.assertIn("unmapped", decoded["errors"]["ts"])
        self.assertIsNone(decoded["values"]["phase_id"])


class ConservativeClassification(unittest.TestCase):
    def test_main_menu_started_flag_does_not_prove_ingame(self):
        # Live baseline: baseline-screen.png SHA3d7d9c47..., PID4844, main-menu
        # Solo/Profile/Options/Quit labels while these raw lifecycle flags were set.
        decoded = state.decode_sample(SIM["ingame"])
        decoded["values"].update(game_started=1, end_game_asked=0, game_ended=0,
                                 phase_id=0, chapter_id=0xFFFFFFFF, ui_binding_context=1)
        out = state.classify(decoded)
        self.assertTrue(out["engine_game_started"])
        self.assertEqual(out["engine_state"], "game_started")
        self.assertIsNone(state.expect_matches("ingame", out))
        self.assertIsNone(out["ui_state"])

    def test_ingame_state_does_not_promote_replay_candidates(self):
        out = state.classify(state.decode_sample(SIM["replay_loading"]))
        self.assertEqual(out["engine_state"], "game_started")
        self.assertEqual(out["replay_net_flag_candidate"], 1)
        self.assertFalse(out["replay_validated"])
        self.assertIsNone(out["replay_active"])
        self.assertEqual(out["ui_state"], None)
        self.assertEqual(out["ui_outgame_substate"], None)

    def test_selecting_a_candidate_does_not_validate_replay_state(self):
        decoded = state.decode_sample(SIM["replay_loading"])
        for candidate in ("net_a5", "controller"):
            selected = state.classify(decoded, replay_field=candidate)
            self.assertIsNone(selected["replay_active"])
            self.assertFalse(selected["replay_validated"])
        self.assertTrue(state.classify(decoded, replay_field="net_a5")["selected_replay_candidate"])

    def test_loading_object_and_phase_are_reported(self):
        out = state.classify(state.decode_sample(SIM["replay_loading"]))
        self.assertTrue(out["loading_object_present"])
        self.assertEqual(out["loading_phase_index"], 9)

    def test_loading_gate_stays_unknown_until_calibrated(self):
        out = state.summarize([sample(SIM["replay_loading"], 0),
                               sample(SIM["replay_loading"], 1000000000)])
        self.assertTrue(out["loading_object_present"], "raw presence is preserved")
        self.assertFalse(out["loading_calibrated"])
        self.assertIsNone(state.expect_matches("loading", out),
                          "pointer presence is not a loading-state verdict")

    def test_implausible_slot_is_unreadable_not_no_services(self):
        decoded = state.decode_sample(SIM["implausible_slot"])
        self.assertIsNone(SIM["implausible_slot"]["ts_present"], "tri-state, never false")
        self.assertEqual(decoded["slot_state"], "implausible")
        self.assertFalse(decoded["no_services"])
        out = state.classify(decoded)
        self.assertEqual(out["engine_state"], "unreadable")
        self.assertFalse(out["engine_state_confident"])
        self.assertIn("implausible", out["engine_state_reason"])

    def test_unreadable_slot_read_is_not_an_explicit_null(self):
        record = json.loads(json.dumps(SIM["ingame"]))
        record["reads"]["slot"] = {"ok": False, "error": "unmapped"}
        record["reads"].pop("ts", None)
        record["slot_state"] = "unreadable"
        record["ts_present"] = None
        record["container_prefix_hex"] = None
        out = state.classify(state.decode_sample(record))
        self.assertEqual(out["engine_state"], "unreadable")
        self.assertNotEqual(out["engine_state"], "no_gameplay_services")
        self.assertFalse(state.expect_matches("no_gameplay_services", out))

    def test_null_global_is_no_gameplay_services_not_a_menu(self):
        out = state.classify(state.decode_sample(SIM["null_slot"]))
        self.assertEqual(out["engine_state"], "no_gameplay_services")
        self.assertTrue(out["engine_state_confident"])
        self.assertIsNone(out["engine_game_started"])
        self.assertIsNone(out["ui_outgame_substate"])
        self.assertNotEqual(out["engine_state"], "outgame")

    def test_invalid_flag_byte_fails_closed(self):
        out = state.classify(state.decode_sample(SIM["invalid_flag"]))
        self.assertEqual(out["engine_state"], "invalid_flags")
        self.assertFalse(out["engine_state_confident"])
        self.assertIsNone(out["engine_game_started"])

    def test_contradictory_flags_are_uncertain(self):
        out = state.classify(state.decode_sample(SIM["contradiction"]))
        self.assertEqual(out["engine_state"], "contradictory_flags")
        self.assertFalse(out["engine_state_confident"])

    def test_not_started_does_not_prove_outgame_or_menu(self):
        decoded = state.decode_sample(SIM["ingame"])
        decoded["values"].update(game_started=0, game_ended=0)
        out = state.classify(decoded)
        self.assertEqual(out["engine_state"], "not_started")
        self.assertIsNone(state.expect_matches("outgame", out))
        self.assertIsNone(out["ui_outgame_substate"], "menu/browser must stay unresolved without data")

    def test_speed_factor_outside_clamps_is_flagged(self):
        decoded = state.decode_sample(SIM["ingame"])
        decoded["values"]["speed_factor"] = 1000.0
        out = state.classify(decoded)
        self.assertFalse(out["speed_consistent"])
        self.assertTrue(any("clamp" in item for item in out["uncertainties"]))


class NamedClock(unittest.TestCase):
    def test_deterministic_seconds_reproduces_f32_product(self):
        self.assertEqual(state.deterministic_seconds_from_ticks(4165), 833.0)
        self.assertEqual(repr(state.deterministic_seconds_from_ticks(4165)), "833.0",
                         "the f32 product is exact, not 833.0000124")
        negative = state.deterministic_seconds_from_ticks(0xFFFFFFFF)
        self.assertEqual(negative, state._f32_round(-1.0 * state.F32_TICK_SECONDS))
        self.assertLess(negative, 0)
        self.assertIsNone(state.deterministic_seconds_from_ticks(None))

    def test_engine_named_time_reports_ticks_seconds_and_unknown_origin(self):
        out = state.summarize([sample(SIM["ingame"], 0), sample(SIM["ingame"], 1000000000)])
        named = out["engine_named_time"]
        self.assertEqual(named["deterministic_ticks"], 4165)
        self.assertAlmostEqual(named["deterministic_seconds"], 4165 * 0.2, places=4)
        self.assertEqual(named["tick_seconds_scale"], state.F32_TICK_SECONDS)
        self.assertAlmostEqual(named["tick_seconds_scale"], 0.2, places=7)
        self.assertEqual(named["origin"], "unknown")
        self.assertFalse(named["epoch_validated"])
        self.assertIsNone(named["replay_frame_mapping"])
        names = {binding["name"] for binding in named["bindings"]}
        self.assertIn("DeterministicCurrentTimeInSeconds", names)
        self.assertIn("DeterministicCurrentTimeInTicks", names)
        self.assertIn("RealtimeCurrentTime", names)

    def test_speed_object_is_never_reported_as_simulation_time(self):
        out = state.summarize([sample(SIM["ingame"], 0), sample(SIM["ingame"], 1000000000)])
        self.assertFalse(out["simulation_time_validated"])
        self.assertIn("speed_factor", out)
        self.assertNotIn("simulation_time", out)


class ReplayOpenWatch(unittest.TestCase):
    def test_rpc_names_match_python_frida_camelcase_conversion(self):
        self.assertIn("installReplayWatch", SIM["rpc_export_names"])
        self.assertIn("replayWatch", SIM["rpc_export_names"])

    def test_watch_errors_and_dropped_invalid_results_are_persisted(self):
        watch = SIM["replay_watch_saturated"]
        result = state.evaluate_replay_open(watch, "ab" * 32, None, None)
        self.assertEqual(result["path_read_errors"], 2)
        self.assertEqual(result["max_events"], 32)
        self.assertTrue(result["truncated"])
        self.assertGreater(result["open_attempts"], result["retained_open_results"])
        self.assertGreater(result["dropped_events"], 0)
        self.assertTrue(result["invalid_handle_observed"], "the final invalid result was dropped")
        self.assertFalse(result["observation_complete"])

    def test_path_normalization_matches_windows_semantics(self):
        self.assertEqual(state.normalize_windows_path("C:/Games//Foo/REPLAY.wrpl"),
                         state.normalize_windows_path("c:\\games\\foo\\replay.wrpl"))

    def test_watch_retains_only_the_exact_full_target_path(self):
        watch = SIM["replay_watch"]
        self.assertTrue(watch["installed"])
        self.assertEqual(watch["other_open_count"], 3,
                         "same-basename and prefix paths are non-matches, not weak matches")
        self.assertEqual(len(watch["events"]), 1)
        self.assertEqual(watch["events"][0]["match"], "path")
        self.assertTrue(watch["events"][0]["valid_handle"])
        self.assertNotIn("other.dll", json.dumps(watch))
        self.assertNotIn("copies", json.dumps(watch))

    def test_real_create_file_w_abi_fields_are_decoded_from_args_0_1_2_4(self):
        event = SIM["replay_watch"]["events"][0]
        self.assertEqual(event["access"], 0x80000000)
        self.assertEqual(event["share"], 3)
        self.assertEqual(event["disposition"], 3)

    def test_interleaved_opens_keep_their_own_pending_records(self):
        events = SIM["replay_watch_interleaved"]["events"]
        self.assertEqual(len(events), 3, "two interleaved opens append two events")
        self.assertEqual((events[1]["handle"], events[1]["access"]), ("0x1b0", 2))
        self.assertEqual((events[2]["handle"], events[2]["access"]), ("0x1b4", 1))
        self.assertNotEqual(events[1]["caller"], events[2]["caller"])

    def test_unterminated_or_overlong_paths_are_refused_not_truncated(self):
        bounded = SIM["replay_watch_bounded"]
        self.assertEqual(bounded["events"], 0, "refused reads never become events")
        self.assertEqual(bounded["path_read_errors"], 2)
        self.assertNotIn("AAAA", json.dumps(bounded))

    def test_resolver_prefers_kernelbase_export_over_unnamed_search(self):
        record = SIM["replay_watch_resolver_preferred"]
        self.assertEqual(record["attach_address"], "0x77141ce0",
                         "KERNELBASE!CreateFileW is the live open path")
        self.assertEqual(record["install"]["module"], "KERNELBASE.dll")
        self.assertEqual(record["watch"]["resolver_module"], "KERNELBASE.dll")

    def test_resolver_falls_back_to_kernel32_when_kernelbase_is_absent(self):
        record = SIM["replay_watch_resolver_fallback"]
        self.assertEqual(record["attach_address"], "0x76dc1c70")
        self.assertEqual(record["install"]["module"], "kernel32.dll")
        self.assertEqual(record["watch"]["resolver_module"], "kernel32.dll")

    def test_verified_requires_stable_content_and_a_valid_handle(self):
        watch = SIM["replay_watch"]
        digest = "ab" * 32
        record = {"sha256": digest, "size": 10}
        out = state.evaluate_replay_open(watch, digest, record, record)
        self.assertTrue(out["verified"])
        self.assertTrue(out["content_stable"])
        self.assertEqual(out["matched_by"], ["path"])

    def test_invalid_handle_or_changed_content_is_not_verified(self):
        watch = SIM["replay_watch"]
        digest = "ab" * 32
        record = {"sha256": digest, "size": 10}
        changed = {"sha256": "cd" * 32, "size": 11}
        out = state.evaluate_replay_open(watch, digest, record, changed)
        self.assertFalse(out["verified"])
        self.assertFalse(out["content_stable"])
        self.assertFalse(out["invalid_handle_observed"])
        only_bad = {"installed": True, "events": [{"valid_handle": False, "match": "path"}],
                    "other_open_count": 0}
        bad = state.evaluate_replay_open(only_bad, digest, record, record)
        self.assertFalse(bad["verified"])
        self.assertTrue(bad["invalid_handle_observed"])
        absent = {"installed": True, "events": [], "other_open_count": 4}
        out = state.evaluate_replay_open(absent, digest, record, record)
        self.assertFalse(out["observed"])
        self.assertFalse(out["verified"])


class ControllerFlow(unittest.TestCase):
    def test_required_replay_open_cannot_omit_the_path(self):
        error = io.StringIO()
        with unittest.mock.patch.object(state.sys, "platform", "darwin"), \
                contextlib.redirect_stderr(error), self.assertRaises(SystemExit) as raised:
            state.main(["--pid", "1444", "--output", "unused.jsonl", "--require-replay-open"])
        self.assertEqual(raised.exception.code, 2)
        self.assertIn("--require-replay-open requires --replay", error.getvalue())

    """End-to-end controller path with a stubbed Frida device (no Windows required)."""

    def run_main(self, extra, records, watch):
        import sys as _sys
        import types

        class Exports:
            def __init__(self):
                self.pos = 0

            def inspect(self):
                return {"name": "wargame3.exe", "path": "C:/fixture/wargame3.exe", "base": "0x400000",
                        "size": 1, "arch": "ia32", "pointer_size": 4, "mz": 23117, "machine": 332}

            def state(self):
                record = records[min(self.pos, len(records) - 1)]
                self.pos += 1
                return json.loads(json.dumps(record))

            def install_replay_watch(self, config):
                return {"installed": True, "target": "0x76000000"}

            def replay_watch(self):
                return watch

        class Script:
            def __init__(self):
                self.exports_sync = Exports()

            def load(self):
                pass

            def unload(self):
                pass

        class Session:
            def create_script(self, source):
                return Script()

            def detach(self):
                pass

        frida = types.SimpleNamespace(get_local_device=lambda: types.SimpleNamespace(attach=lambda pid: Session()))
        helper = types.SimpleNamespace(process_identity=lambda pid: (str(self.exe), 12345),
                                       verify_loaded=lambda *args: None)
        out = Path(self.tmp.name) / ("out%d.jsonl" % self.counter)
        self.counter += 1
        with unittest.mock.patch.dict(_sys.modules, {"frida": frida, "wgrd_frida": helper}), \
                unittest.mock.patch.object(state, "EXE_SHA256", self.exe_sha), \
                unittest.mock.patch.object(_sys, "platform", "win32"):
            with contextlib.redirect_stdout(io.StringIO()):
                code = state.main(["--pid", "1", "--output", str(out), "--samples", "2",
                                   "--interval", "0.05"] + extra)
        return code, [json.loads(line) for line in out.read_text(encoding="utf-8").splitlines()]

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.counter = 0
        self.exe = Path(self.tmp.name) / "WarGame3.exe"
        self.exe.write_bytes(b"MZ" + b"####SVNREVISION####0000131544####SVNREVISION####")
        self.exe_sha = hashlib.sha256(self.exe.read_bytes()).hexdigest()
        self.replay = Path(self.tmp.name) / "match.wrpl"
        self.replay.write_bytes(b"replay-bytes")
        self.digest = hashlib.sha256(self.replay.read_bytes()).hexdigest()

    def tearDown(self):
        self.tmp.cleanup()

    def test_state_gate_succeeds_and_records_replay_verification(self):
        watch = {**SIM["replay_watch"], "events": [dict(SIM["replay_watch"]["events"][0])]}
        code, records = self.run_main(["--expect", "engine_game_started", "--replay", str(self.replay),
                                       "--replay-sha256", self.digest], [SIM["ingame"]], watch)
        self.assertEqual(code, 0)
        verification = [r for r in records if r["event"] == "replay_verification"][0]
        self.assertTrue(verification["verified"])
        self.assertEqual([r["event"] for r in records].count("replay_open"), 1)
        self.assertEqual([r for r in records if r["event"] == "summary"][0]["engine_state"], "game_started")

    def test_early_uncertainty_does_not_override_a_valid_final_verdict(self):
        code, records = self.run_main(["--expect", "engine_game_started"],
                                      [SIM["invalid_flag"], SIM["invalid_flag"], SIM["ingame"]],
                                      SIM["replay_watch"])
        self.assertEqual(code, 0)
        summary = [r for r in records if r["event"] == "summary"][0]
        self.assertEqual(summary["engine_state"], "game_started")
        self.assertEqual(len(summary["earlier_uncertain_states"]), 1)
        self.assertEqual(summary["earlier_uncertain_states"][0]["engine_state"], "invalid_flags")

    def test_missing_open_fails_closed_when_required(self):
        watch = {"installed": True, "error": None, "other_open_count": 3,
                 "max_events": 32, "events": []}
        code, records = self.run_main(["--expect", "engine_game_started", "--replay", str(self.replay),
                                       "--replay-sha256", self.digest, "--require-replay-open"],
                                      [SIM["ingame"]], watch)
        self.assertEqual(code, 3)
        self.assertFalse([r for r in records if r["event"] == "replay_verification"][0]["verified"])

    def test_replay_hash_mismatch_is_rejected_before_attach(self):
        with self.assertRaises(ValueError):
            self.run_main(["--replay", str(self.replay), "--replay-sha256", "00" * 32],
                          [SIM["ingame"]], SIM["replay_watch"])


class CounterVerdicts(unittest.TestCase):
    def test_unknown_or_discontinuous_counter_is_not_a_verdict(self):
        unknown = state.summarize([{"counter": None, "monotonic_ns": 0, "container": "0x1"},
                                   {"counter": 10, "monotonic_ns": 1, "container": "0x1"}])
        self.assertIsNone(unknown["counter_delta"])
        self.assertIsNone(state.expect_matches("advancing_counter", unknown))
        self.assertIsNone(state.expect_matches("stable_counter", unknown))
        jump = state.summarize([{"counter": 10, "monotonic_ns": 0, "container": "0x1"},
                                {"counter": 20, "monotonic_ns": 1, "container": "0x2"}])
        self.assertEqual(jump["observation"], "discontinuity")
        self.assertIsNone(state.expect_matches("advancing_counter", jump))
        self.assertIsNone(jump["stationary_counter"])
        one = state.summarize([{"counter": 5, "monotonic_ns": 0, "container": "0x1"},
                               {"counter": 5, "monotonic_ns": 1, "container": "0x1"}])
        self.assertIs(state.expect_matches("stable_counter", one), True)


class Gates(unittest.TestCase):
    def test_fingerprint_rejects_missing_observation_fields(self):
        for missing in ("phase_id", "ui_binding_context_present"):
            current = {"engine_state": "not_started", "chapter_id": 7, "phase_id": 3,
                       "ui_binding_context_present": False, "ui_outgame_substate": None,
                       "uncertainties": []}
            entry = {"name": "menu", "chapter_id": 7, "phase_id": 3,
                     "ui_binding_context_present": False}
            current[missing] = entry[missing] = None
            self.assertIsNone(state.apply_fingerprint(current, {"outgame": [entry]})[
                "ui_outgame_substate"])
            with tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / "incomplete-fingerprint.json"
                path.write_text(json.dumps({"outgame": [entry]}))
                with self.assertRaises(ValueError):
                    state.load_fingerprint(path)

    def test_expectation_predicates_fail_closed(self):
        out = state.summarize([sample(SIM["ingame"], 0), sample(SIM["ingame"], 1)])
        self.assertIsNone(state.expect_matches("replay_active", out))
        self.assertFalse(state.expect_matches("engine_game_ended", out))
        null = state.summarize([sample(SIM["null_slot"], 0), sample(SIM["null_slot"], 1)])
        self.assertTrue(state.expect_matches("no_gameplay_services", null))
        self.assertIsNone(state.expect_matches("engine_game_started", null))

    def test_fingerprint_is_required_for_outgame_substates(self):
        fingerprint = {"outgame": [{"name": "menu", "chapter_id": 7, "phase_id": 3,
                                    "ui_binding_context_present": False}]}
        decoded = state.decode_sample(SIM["ingame"])
        decoded["values"].update(game_started=0, game_ended=0)
        matched = state.apply_fingerprint(state.classify(decoded), fingerprint)
        self.assertEqual(matched["ui_outgame_substate"], "menu")
        self.assertEqual(matched["ui_outgame_substate_basis"], "caller_supplied_raw_fingerprint")
        other = {"outgame": [{"name": "browser", "chapter_id": 9, "phase_id": 4,
                              "ui_binding_context_present": True}]}
        missed = state.apply_fingerprint(state.classify(decoded), other)
        self.assertIsNone(missed["ui_outgame_substate"])
        self.assertTrue(any("fingerprint" in item for item in missed["uncertainties"]))

    def test_fingerprint_validation_rejects_guesses(self):
        with self.assertRaises((ValueError, OSError)):
            state.load_fingerprint(str(ROOT / "tests/nonexistent.json"))
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "fp.json"
            path.write_text('{"outgame": []}', encoding="utf-8")
            with self.assertRaises(ValueError):
                state.load_fingerprint(str(path))


class ObserverBounds(unittest.TestCase):
    def test_planned_reads_fit_the_budget(self):
        self.assertLessEqual(state.PLANNED_BYTES, state.MAX_TOTAL_BYTES)
        self.assertLessEqual(state.MAX_TOTAL_BYTES, 0x300)
        for name, _, size in state.READ_PLAN:
            with self.subTest(name=name):
                self.assertLessEqual(size, state.MAX_READ_BYTES)

    def test_simulated_reads_stay_inside_the_budget(self):
        for name, record in SIM.items():
            if "read_budget" not in record:
                continue
            budget = record["read_budget"]
            with self.subTest(scenario=name):
                self.assertLessEqual(budget["used"], budget["max_total"])

    def test_script_is_read_only(self):
        forbidden = [r"\bNativeFunction\b", r"\bMemory\.write", r"\.write\(",
                     r"\bApiResolver\b", r"\bStalker\b", r"\bModule\.load\b"]
        for pattern in forbidden:
            with self.subTest(pattern=pattern):
                self.assertIsNone(re.search(pattern, state.SCRIPT))
        self.assertIn("readByteArray", state.SCRIPT)
        # The only permitted native observation is one CreateFileW open watch.
        self.assertEqual(state.SCRIPT.count("Interceptor.attach"), 1)
        self.assertIn("'CreateFileW'", state.SCRIPT)
        self.assertNotRegex(state.SCRIPT, r'''["']CreateFileA["']''',
                            "No ANSI API string literal may be implemented; comments may discuss it")
        self.assertNotIn("sync.call", state.SCRIPT)

    def test_mapping_edge_is_refused(self):
        record = SIM["crossing_span"]
        self.assertFalse(record["reads"]["ts"]["ok"])
        self.assertIn("crosses mapping", record["reads"]["ts"]["error"])

    def test_cli_keeps_legacy_arguments(self):
        parser_args = ["--pid", "1", "--output", "x", "--expect", "stable_counter"]
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as caught:
            state.main(parser_args)  # rejected by the platform guard, not by argparse
        self.assertEqual(caught.exception.code, 2)
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            state.main(["--pid", "1", "--output", "x", "--samples", "200"])
        self.assertIn("stable_counter", state.__doc__ + str(parser_args))


if __name__ == "__main__":
    unittest.main()
