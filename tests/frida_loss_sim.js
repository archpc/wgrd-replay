'use strict';
// Collector mechanics under a simulated Frida API, not engine evidence.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const source = fs.readFileSync(path.join(__dirname, '..', 'instrumentation', 'hooks.js'), 'utf8');
class Pointer {
  constructor(n) { this.n = n; }
  add(n) { return new Pointer(this.n + n); }
  compare(p) { return Math.sign(this.n - p.n); }
  toString() { return '0x' + this.n.toString(16); }
}
function capture(accounting, failOn = 0) {
  const events = [], listeners = [];
  let sendCalls = 0;
  const config = {module:'wargame3.exe', event_limit:10, loss_accounting:accounting,
    hooks:[{name:'input', rva:0, args:0, sample_every:1, reads:[]}]};
  const sandbox = {rpc:{exports:{}}, send:event=>{
      if (++sendCalls === failOn) throw new Error('simulated send failure');
      events.push(event);
    },
    Process:{getModuleByName:()=>({base:new Pointer(0x400000)})},
    Interceptor:{attach:(_, callbacks)=>{listeners.push(callbacks);return {detach(){}};}},
    Date};
  vm.runInNewContext(source.replace('__CONFIG__', JSON.stringify(config)), sandbox);
  sandbox.rpc.exports.install();
  const invocation = {threadId:1, context:{esp:new Pointer(0x9000),
    ecx:new Pointer(0), edx:new Pointer(0)}, returnAddress:new Pointer(0x1234)};
  listeners[0].onEnter.call(invocation, []);
  listeners[0].onLeave.call(invocation, new Pointer(0));
  return {events, summary:sandbox.rpc.exports.stop()};
}
const tracked = capture(true);
assert.deepEqual(tracked.events.map(event=>event.sequence), [1, 2]);
assert.equal(tracked.summary.loss_accounting.last_sequence, 2);
assert.equal(tracked.summary.loss_accounting.send_failures, 0);
const legacy = capture(false);
assert.equal(legacy.events.some(event=>'sequence' in event), false);
assert.equal('loss_accounting' in legacy.summary, false);
// A failed send leaves a sequence hole: the enter record is numbered but not
// delivered, the catch path emits a callback_error with the next sequence,
// and the sender reports the failure. The receiver audit must fail on this.
const failed = capture(true, 1);
assert.equal(failed.events.length, 1);
assert.equal(failed.events[0].event, 'callback_error');
assert.equal(failed.events[0].sequence, 2);
assert.equal(failed.summary.loss_accounting.last_sequence, 2);
assert.equal(failed.summary.loss_accounting.send_failures, 1);
assert.equal(failed.summary.stack_mismatches, 1);
console.log('WGRD_LOSS_SIM_OK');
