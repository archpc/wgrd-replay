'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
class Pointer {
  constructor(n) { this.n = n >>> 0; }
  add(n) { return new Pointer(this.n + n); }
  and(n) { return new Pointer(this.n & n); }
  compare(p) { return Math.sign(this.n - p.n); }
  isNull() { return this.n === 0; }
  toString() { return '0x' + this.n.toString(16); }
  readByteArray(n) { return Uint8Array.from({length:n}, (_,i)=>i+1).buffer; }
  readPointer() {
    // Minimal pointer map: 0x1000 -> tagged block 0x2003, 0x1010 -> low tag only.
    const map = {0x1000: 0x2003, 0x1010: 0x1};
    if (!(this.n in map)) throw new Error('unmapped pointer read');
    return new Pointer(map[this.n]);
  }
}
const events = [], listeners = [];
const config = {module:'wargame3.exe',event_limit:100,hooks:[
  {name:'impact',rva:0,args:0,sample_every:1,reads:[]},
  {name:'owner',rva:16,args:0,sample_every:1,within:['impact'],
   reads:[{source:'retval',offset:0x20,size:4,phase:'leave'}]},
  {name:'masked',rva:32,args:0,sample_every:1,
   reads:[{source:'retval',offset:0x20,size:8,phase:'leave',indirect:true,
           indirect_mask:'FFFFFFFC',indirect_offset:4}]},
  {name:'masked_null',rva:48,args:0,sample_every:1,
   reads:[{source:'retval',offset:0x20,size:8,phase:'leave',indirect:true,
           indirect_mask:'FFFFFFFC',indirect_offset:4}]}
]};
const sandbox={rpc:{exports:{}},send:e=>events.push(e),
 Process:{pointerSize:4,getModuleByName:()=>({base:new Pointer(0x4000)}),
 findRangeByAddress:()=>({base:new Pointer(0),size:0x10000,protection:'r'})},
 Interceptor:{attach:(_,callbacks)=>{listeners.push(callbacks);return{detach(){}};}},
 Thread:{},Backtracer:{},Uint8Array,Date};
vm.runInNewContext(fs.readFileSync(path.join(__dirname,'..','instrumentation','hooks.js'),'utf8')
 .replace('__CONFIG__',JSON.stringify(config)),sandbox);
sandbox.rpc.exports.install();
function ctx(sp,thread=1){return{threadId:thread,context:{esp:new Pointer(sp),ecx:new Pointer(0),edx:new Pointer(0)},returnAddress:new Pointer(0x1234)};}
const outside=ctx(0x9000);
listeners[1].onEnter.call(outside,[]);
listeners[1].onLeave.call(outside,new Pointer(0x2000));
assert.equal(events.length,0,'out-of-scope lookup must emit no events');
const root=ctx(0x9000), child=ctx(0x8ff0);
listeners[0].onEnter.call(root,[]);
const otherThread=ctx(0x8ff0,2);
listeners[1].onEnter.call(otherThread,[]);
listeners[1].onLeave.call(otherThread,new Pointer(0x2000));
listeners[1].onEnter.call(child,[]);
listeners[1].onLeave.call(child,new Pointer(0x2000));
listeners[0].onLeave.call(root,new Pointer(0));
assert.equal(events.length,4);
assert.equal(events[1].parent_call_id,events[0].call_id);
assert.equal(events[2].reads[0].address,'0x2020');
assert.equal(events[2].reads[0].result.hex,'01020304');
assert.equal('raw_pointer' in events[2].reads[0],false,'unmasked reads keep the old record shape');
const prior=ctx(0x9000), notNested=ctx(0x9000);
listeners[0].onEnter.call(prior,[]);
listeners[1].onEnter.call(notNested,[]);
listeners[1].onLeave.call(notNested,new Pointer(0x2000));
assert.equal(events.length,5,'equal stack pointers must not admit an apparent parent');
listeners[0].onLeave.call(prior,new Pointer(0));
// masked chain: retval+0x20 -> 0x1000 -> 0x2003, mask FFFFFFFC -> 0x2000, +4 -> 0x2004
const tagged=ctx(0x9000);
listeners[2].onEnter.call(tagged,[]);
listeners[2].onLeave.call(tagged,new Pointer(0xfe0));
const masked=events[events.length-1];
assert.equal(masked.event,'leave');
const m=masked.reads[0];
assert.equal(m.indirect,true);
assert.deepEqual(Array.from(m.chain),['0x2003']);
assert.equal(m.raw_pointer,'0x2003');
assert.equal(m.applied_mask,'0xfffffffc');
assert.equal(m.target_offset,4);
assert.equal(m.final_target,'0x2004');
assert.equal(m.target,'0x2004');
assert.equal(m.result.hex,'0102030405060708');
// a mask that clears the whole pointer must fail closed, not read address 0
const clear=ctx(0x9000);
listeners[3].onEnter.call(clear,[]);
listeners[3].onLeave.call(clear,new Pointer(0xff0));
const nulled=events[events.length-1].reads[0];
assert.equal(nulled.ok,undefined);
assert.equal(nulled.result.ok,false);
assert.equal(nulled.result.reason,'masked target is null');
assert.equal(nulled.final_target,null);
const summary=sandbox.rpc.exports.stop();
assert.equal(summary.filtered.owner,3);
assert.equal(summary.counts.owner,1);
assert.equal(summary.stack_mismatches,0);
assert.equal(summary.outstanding_threads,0);
console.log('WGRD_SCOPE_SIM_OK');
