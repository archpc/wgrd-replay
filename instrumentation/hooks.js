'use strict';

// CONFIG is supplied by the Python controller, never by the target process.
const config = __CONFIG__;
const target = Process.getModuleByName(config.module);
const listeners = [];
const counts = {};
const stacks = {};
let nextCall = 1;
let emitted = 0;
let suppressed = 0;
let callbackErrors = 0;
let staleFrames = 0;
let stackMismatches = 0;

function hexBytes(address, size) {
  const range = Process.findRangeByAddress(address);
  if (address.isNull() || range === null || !range.protection.includes('r') ||
      address.add(size).compare(address) < 0 ||
      address.add(size).compare(range.base.add(range.size)) > 0) {
    return {ok: false, reason: 'not fully readable'};
  }
  try {
    return {ok: true, hex: Array.from(new Uint8Array(address.readByteArray(size)),
      b => b.toString(16).padStart(2, '0')).join('')};
  } catch (error) {
    return {ok: false, reason: String(error)};
  }
}

function emit(event) {
  if (emitted >= config.event_limit) { suppressed++; return false; }
  emitted++;
  event.timestamp_utc = new Date().toISOString();
  send(event);
  return true;
}

function captureReads(hook, args, ecx, edx, phase) {
  const snapshots = [];
  for (const read of hook.reads || []) {
    const configuredPhase = read.phase || 'enter';
    if (configuredPhase !== phase && configuredPhase !== 'both') continue;
    const pointer = read.source === 'ecx' ? ecx :
      read.source === 'edx' ? edx : args[Number(read.source.slice(3))];
    const address = pointer.add(read.offset);
    let result, target = null;
    const chain = [];
    if (pointer.isNull()) {
      result = {ok: false, reason: 'null source'};
    } else if (address.compare(pointer) < 0) {
      result = {ok: false, reason: 'pointer overflow'};
    } else if (read.indirect) {
      let cursor = address;
      const depth = read.second_indirect ? 2 : 1;
      try {
        for (let i = 0; i < depth; i++) {
          const slot = hexBytes(cursor, Process.pointerSize);
          if (!slot.ok) { result = {ok: false, reason: 'pointer slot not readable'}; break; }
          cursor = cursor.readPointer();
          chain.push(cursor.toString());
        }
        if (result === undefined) {
          target = cursor.toString();
          result = hexBytes(cursor, read.size);
        }
      } catch (error) { result = {ok: false, reason: String(error)}; }
    } else result = hexBytes(address, read.size);
    snapshots.push({source: read.source, phase, offset: read.offset, size: read.size,
      address: address.toString(), indirect: !!read.indirect, chain, target, result});
  }
  return snapshots;
}

function callbackFailure(phase, hook, error, thread) {
  callbackErrors++;
  send({event: 'callback_error', phase, hook, thread_id: thread,
    timestamp_utc: new Date().toISOString(), error: String(error)});
}

rpc.exports = {
  inspect() {
    const base = target.base;
    const peOffset = base.add(0x3c).readU32();
    const entries = config.hooks.map(h => {
      const address = base.add(h.rva);
      const range = Process.findRangeByAddress(address);
      return {name: h.name, address: address.toString(), executable: !!range && range.protection.includes('x'),
        bytes: hexBytes(address, 16)};
    });
    return {name: target.name, path: target.path, base: base.toString(), size: target.size,
      arch: Process.arch, pointer_size: Process.pointerSize, mz: base.readU16(),
      machine: base.add(peOffset + 4).readU16(), entries};
  },
  install() {
    for (const hook of config.hooks) {
      counts[hook.name] = 0;
      listeners.push(Interceptor.attach(target.base.add(hook.rva), {
        onEnter(args) {
          const thread = this.threadId;
          this.traceThread = thread;
          this.traceSampled = false;
          this.traceFrame = null;
          try {
            const stack = stacks[thread] || (stacks[thread] = []);
            let discarded = 0;
            // x86 stack grows down. Equal/higher ESP indicates a returned or
            // unwound frame, not a nested call. Fiber switches remain ambiguous.
            while (stack.length && stack[stack.length - 1].sp.compare(this.context.esp) <= 0) {
              stack.pop(); discarded++; staleFrames++;
            }
            const parent = stack.length ? stack[stack.length - 1] : null;
            const frame = {id: nextCall++, sp: this.context.esp, recorded: false};
            stack.push(frame);
            this.traceFrame = frame;
            const ordinal = ++counts[hook.name];
            this.traceSampled = (ordinal - 1) % hook.sample_every === 0;
            if (!this.traceSampled) return;
            const values = [];
            this.traceArgs = [];
            this.traceEcx = this.context.ecx;
            this.traceEdx = this.context.edx;
            for (let i = 0; i < hook.args; i++) {
              this.traceArgs.push(args[i]);
              values.push(args[i].toString());
            }
            const snapshots = captureReads(hook, this.traceArgs, this.traceEcx, this.traceEdx, 'enter');
            let backtrace = null;
            if (hook.backtrace) {
              try { backtrace = Thread.backtrace(this.context, Backtracer.ACCURATE).slice(0, 16).map(p => p.toString()); }
              catch (error) { backtrace = {error: String(error)}; }
            }
            frame.recorded = emit({event: 'enter', hook: hook.name, call_id: frame.id,
              parent_call_id: parent ? parent.id : null, parent_recorded: parent ? parent.recorded : null,
              stale_frames_discarded: discarded, stack_pointer: frame.sp.toString(),
              ordinal, thread_id: thread, return_address: this.returnAddress.toString(),
              ecx: this.context.ecx.toString(), edx: this.context.edx.toString(),
              args: values, reads: snapshots, backtrace});
          } catch (error) {
            this.traceSampled = false;
            delete stacks[thread];
            callbackFailure('enter', hook.name, error, thread);
          }
        },
        onLeave(retval) {
          try {
            const stack = stacks[this.traceThread] || [];
            const index = stack.indexOf(this.traceFrame);
            const valid = index !== -1 && index === stack.length - 1;
            if (!valid) { stackMismatches++; delete stacks[this.traceThread]; }
            else {
              stack.pop();
              if (stack.length === 0) delete stacks[this.traceThread];
            }
            if (this.traceSampled) emit({event: 'leave', hook: hook.name,
              call_id: this.traceFrame ? this.traceFrame.id : null, thread_id: this.traceThread,
              stack_match: valid, retval: retval.toString(),
              reads: captureReads(hook, this.traceArgs, this.traceEcx, this.traceEdx, 'leave')});
          } catch (error) {
            delete stacks[this.traceThread];
            callbackFailure('leave', hook.name, error, this.traceThread);
          }
        }
      }));
    }
    return {installed: listeners.length};
  },
  stop() {
    for (const listener of listeners) listener.detach();
    listeners.length = 0;
    return {counts, emitted, suppressed, callback_errors: callbackErrors, stale_frames: staleFrames,
      stack_mismatches: stackMismatches, outstanding_threads: Object.keys(stacks).length};
  }
};
