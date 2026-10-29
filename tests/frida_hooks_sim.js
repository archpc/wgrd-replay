// Run with Node; this simulates Interceptor callbacks, not the Frida runtime.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');

function fixture(limit = 20, sample = 1, badRead = false, overflow = false, leaveRead = false, indirect = false, nullBase = false, secondIndirect = false, invalidSecond = false) {
  class Pointer {
    constructor(value) { this.value = value; }
    add(n) { return new Pointer((this.value + n) >>> 0); }
    compare(other) { return Math.sign(this.value - other.value); }
    isNull() { return this.value === 0; }
    toString() { return '0x' + this.value.toString(16); }
    readByteArray(size) { return new Uint8Array(size).buffer; }
    readPointer() { return new Pointer(this.value === 0x2000 ? 0x3000 : 0x4000); }
  }
  const listeners = [];
  const events = [];
  const config = {module: 'wargame3.exe', event_limit: limit, hooks: [
    {name: 'outer', rva: 0x100, args: leaveRead || indirect ? 1 : 0, sample_every: sample,
      reads: indirect ? [{source: 'arg0', offset: 0, size: 4, indirect: true, second_indirect: secondIndirect}] :
        (leaveRead ? [{source: 'arg0', offset: 4, size: 4, phase: 'leave'}] :
          (badRead || overflow || nullBase ? [{source: 'ecx', offset: overflow || nullBase ? 32 : 0, size: 4}] : []))},
    {name: 'inner', rva: 0x200, args: 0, sample_every: 1}
  ]};
  const sandbox = {
    rpc: {exports: {}}, send: event => events.push(event),
    Process: {pointerSize: 4, getModuleByName: () => ({base: new Pointer(0x400000)}),
      findRangeByAddress: p => invalidSecond && p.value === 0x3000 ? null :
        ({base: new Pointer(0), size: 0x10000000, protection: 'r-x'})},
    Interceptor: {attach: (address, callbacks) => { listeners.push(callbacks); return {detach() {}}; }},
    Thread: {}, Backtracer: {}, Uint8Array, Date
  };
  const source = fs.readFileSync(path.join(__dirname, '..', 'instrumentation', 'hooks.js'), 'utf8')
    .replace('__CONFIG__', JSON.stringify(config));
  vm.runInNewContext(source, sandbox);
  sandbox.rpc.exports.install();
  function enter(index, tid, sp) {
    const ctx = {threadId: tid, context: {esp: new Pointer(sp), ecx: badRead ? undefined : new Pointer(overflow ? 0xfffffff0 : 0), edx: new Pointer(0)},
      returnAddress: new Pointer(0x1234)};
    listeners[index].onEnter.call(ctx, leaveRead || indirect ? [new Pointer(0x2000)] : []);
    return ctx;
  }
  function leave(index, ctx) { listeners[index].onLeave.call(ctx, new Pointer(0)); }
  return {enter, leave, events, stop: sandbox.rpc.exports.stop};
}

{
  const f = fixture();
  const a = f.enter(0, 1, 0x9000);
  const b = f.enter(1, 1, 0x8ff0);
  const other = f.enter(1, 2, 0x8ff0);
  assert.equal(f.events[1].parent_call_id, f.events[0].call_id);
  assert.equal(f.events[1].parent_recorded, true);
  assert.equal(f.events[2].parent_call_id, null);
  f.leave(1, b); f.leave(0, a); f.leave(1, other);
  assert.equal(f.stop().outstanding_threads, 0);
}
{
  const f = fixture(20, 2);
  const first = f.enter(0, 1, 0x9000); f.leave(0, first);
  const sampledOut = f.enter(0, 1, 0x9000);
  const nested = f.enter(1, 1, 0x8ff0);
  const e = f.events.find(x => x.hook === 'inner');
  assert.equal(e.parent_recorded, false);
  f.leave(1, nested); f.leave(0, sampledOut);
}
{
  const f = fixture();
  f.enter(0, 1, 0x9000); // simulated exception/nonlocal unwind, no onLeave
  const next = f.enter(1, 1, 0x9000);
  assert.equal(f.events[1].parent_call_id, null);
  assert.equal(f.events[1].stale_frames_discarded, 1);
  f.leave(1, next);
  assert.equal(f.stop().outstanding_threads, 0);
}
{
  const f = fixture(1);
  const a = f.enter(0, 1, 0x9000); f.leave(0, a);
  const summary = f.stop();
  assert.equal(summary.emitted, 1);
  assert.equal(summary.suppressed, 1);
}
{
  const f = fixture(20, 1, true);
  f.enter(0, 1, 0x9000);
  assert.equal(f.events[0].event, 'callback_error');
  assert.equal(f.stop().callback_errors, 1);
  assert.equal(f.stop().outstanding_threads, 0);
}
{
  const f = fixture();
  const a = f.enter(0, 1, 0x9000);
  f.enter(1, 1, 0x8ff0);
  f.leave(0, a); // impossible ordering is flagged and invalidates the stack
  assert.equal(f.events.at(-1).stack_match, false);
  assert.equal(f.stop().stack_mismatches, 1);
}
{
  const f = fixture(20, 1, false, true);
  f.enter(0, 1, 0x9000);
  assert.equal(f.events[0].reads[0].result.ok, false);
  assert.equal(f.events[0].reads[0].result.reason, 'pointer overflow');
}
{
  const f = fixture(20, 1, false, false, true);
  const frame = f.enter(0, 1, 0x9000);
  assert.equal(f.events[0].reads.length, 0);
  f.leave(0, frame);
  assert.equal(f.events[1].reads.length, 1);
  assert.equal(f.events[1].reads[0].address, '0x2004');
  assert.equal(f.events[1].reads[0].result.ok, true);
}
{
  const f = fixture(20, 1, false, false, false, true);
  f.enter(0, 1, 0x9000);
  assert.equal(f.events[0].reads[0].address, '0x2000');
  assert.equal(f.events[0].reads[0].target, '0x3000');
  assert.equal(f.events[0].reads[0].result.ok, true);
}
{
  const f = fixture(20, 1, false, false, false, false, true);
  f.enter(0, 1, 0x9000);
  assert.equal(f.events[0].reads[0].result.ok, false);
  assert.equal(f.events[0].reads[0].result.reason, 'null source');
}
{
  const f = fixture(20, 1, false, false, false, true, false, true);
  f.enter(0, 1, 0x9000);
  assert.equal(f.events[0].reads[0].target, '0x4000');
  assert.deepEqual(Array.from(f.events[0].reads[0].chain), ['0x3000', '0x4000']);
  assert.equal(f.events[0].reads[0].result.ok, true);
}
{
  const f = fixture(20, 1, false, false, false, true, false, true, true);
  f.enter(0, 1, 0x9000);
  assert.equal(f.events[0].reads[0].result.ok, false);
  assert.equal(f.events[0].reads[0].result.reason, 'pointer slot not readable');
  assert.deepEqual(Array.from(f.events[0].reads[0].chain), ['0x3000']);
}
console.log('WGRD_JS_SIMULATION_OK');
