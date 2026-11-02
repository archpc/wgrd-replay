"""Read-only revision-131544 counter observations; not validated simulation time."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import time
from datetime import datetime, timezone

EXE_SHA256 = "5eaa6d6168c9570ff9789bffb3b2cc16fd908be61263b12fcc1e8b2f09efc75d"
SCRIPT = r"""
'use strict';
const m=Process.getModuleByName('wargame3.exe');
function bytes(p,n) {
 const r=Process.findRangeByAddress(p);
 if(p.isNull() || !r || !r.protection.includes('r') || p.add(n).compare(p)<0 ||
    p.add(n).compare(r.base.add(r.size))>0) throw new Error('unreadable state span');
 return Array.from(new Uint8Array(p.readByteArray(n)),x=>x.toString(16).padStart(2,'0')).join('');
}
rpc.exports={
 inspect() {
  const p=m.base.add(0x3c).readU32();
  return {name:m.name,path:m.path,base:m.base.toString(),size:m.size,arch:Process.arch,
   pointer_size:Process.pointerSize,mz:m.base.readU16(),machine:m.base.add(p+4).readU16(),entries:[]};
 },
 state() {
  const scale=m.base.add(0x195d768-0x400000);
  if(bytes(scale,4)!=='cdcc4c3e') throw new Error('clock scale byte mismatch');
  const slot=m.base.add(0x201d318-0x400000);
  const slotHex=bytes(slot,4), object=slot.readPointer();
  const prefix=bytes(object,256), raw=bytes(object.add(0xd0),4);
  return {container:object.toString(),pointer_slot_hex:slotHex,counter:object.add(0xd0).readS32(),
   counter_hex:raw,container_prefix_hex:prefix,scale_hex:'cdcc4c3e'};
 }
};
"""


def summarize(samples):
    if len(samples) < 2:
        raise ValueError("at least two samples required")
    pairs = list(zip(samples, samples[1:]))
    discontinuity = any(a["container"] != b["container"] or b["counter"] < a["counter"] for a, b in pairs)
    elapsed = (samples[-1]["monotonic_ns"] - samples[0]["monotonic_ns"]) / 1e9
    delta = samples[-1]["counter"] - samples[0]["counter"]
    prefix = samples[-1].get("container_prefix_hex")
    flags = bytes.fromhex(prefix)[0x20:0x23] if prefix else b""
    if flags and (len(flags) != 3 or any(value not in (0, 1) for value in flags)):
        raise ValueError("invalid GameplayServices boolean flags")
    return {"observation": "discontinuity" if discontinuity else "stable_counter" if delta == 0 else "advancing_counter",
            "engine_game_started": bool(flags[0]) if flags else None,
            "engine_end_game_asked": bool(flags[1]) if flags else None,
            "engine_game_ended": bool(flags[2]) if flags else None,
            "counter_delta": delta, "wall_seconds": elapsed,
            "counter_per_wall_second": delta / elapsed if elapsed > 0 and not discontinuity else None,
            "simulation_time_validated": False, "ui_state": None}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pid", type=int, required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--samples", type=int, default=12)
    parser.add_argument("--interval", type=float, default=0.2)
    parser.add_argument("--expect", choices=["stable_counter", "advancing_counter"])
    args = parser.parse_args(argv)
    if not 2 <= args.samples <= 150 or not 0.05 <= args.interval <= 1 or args.samples * args.interval > 30:
        parser.error("bound samples to 2..150, interval to 0.05..1, and total to 30 seconds")
    if sys.platform != "win32":
        parser.error("observer must run in the authorized Windows guest")
    import frida
    from wgrd_frida import process_identity, verify_loaded
    path, created = process_identity(args.pid)
    image = Path(path).read_bytes()
    if hashlib.sha256(image).hexdigest() != EXE_SHA256:
        raise ValueError("executable SHA-256 mismatch")
    if b"####SVNREVISION####0000131544####SVNREVISION####" not in image:
        raise ValueError("revision marker mismatch")
    with open(args.output, "x", encoding="utf-8") as output:
        def write(record):
            output.write(json.dumps(record, allow_nan=False, separators=(",", ":")) + "\n")
            output.flush()
        write({"event": "start", "pid": args.pid, "created_filetime": created,
               "exe_sha256": EXE_SHA256, "script_sha256": hashlib.sha256(SCRIPT.encode()).hexdigest(),
               "timestamp_utc": datetime.now(timezone.utc).isoformat()})
        session = script = None
        samples = []
        try:
            session = frida.get_local_device().attach(args.pid)
            if process_identity(args.pid) != (path, created):
                raise ValueError("process changed during attach")
            script = session.create_script(SCRIPT)
            script.load()
            info = script.exports_sync.inspect()
            verify_loaded({"sha256": EXE_SHA256, "module": "wargame3.exe", "ghidra_base": "0x400000", "hooks": []}, image, info, path)
            write({"event": "identity_verified", "module": info})
            next_poll = time.monotonic()
            for _ in range(args.samples):
                remaining = next_poll - time.monotonic()
                if remaining > 0:
                    time.sleep(remaining)  # Explicit bounded sampling interval.
                before = time.monotonic_ns()
                sample = script.exports_sync.state()
                sample.update(event="counter_sample", monotonic_ns=time.monotonic_ns(), read_started_ns=before,
                              timestamp_utc=datetime.now(timezone.utc).isoformat())
                samples.append(sample)
                write(sample)
                next_poll += args.interval
            result = summarize(samples)
            if process_identity(args.pid) != (path, created):
                raise ValueError("process changed during observation")
            if hashlib.sha256(Path(path).read_bytes()).hexdigest() != EXE_SHA256:
                raise ValueError("image changed during observation")
            write({"event": "summary", **result})
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
    if args.expect and result["observation"] != args.expect:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
