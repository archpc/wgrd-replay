#!/usr/bin/env python3
"""Windows Frida controller for revision-pinned WGRD investigations."""

import argparse
import ctypes
import hashlib
import json
import os
from pathlib import Path
import sys
import threading
from datetime import datetime, timezone


def runtime_address(image_base, ghidra_base, ghidra_va, image_size):
    """Translate a Ghidra VA to a loaded-image address."""
    rva = ghidra_va - ghidra_base
    if not 0 <= rva < image_size:
        raise ValueError("address is outside the loaded image")
    return image_base + rva


def pe_bytes_at_rva(image, rva, length):
    """Read file-backed PE32 bytes at a relative virtual address."""
    import struct

    try:
        if image[:2] != b"MZ" or rva < 0 or not 1 <= length <= 128:
            raise ValueError("invalid PE or byte range")
        pe = struct.unpack_from("<I", image, 0x3C)[0]
        if image[pe:pe + 4] != b"PE\0\0":
            raise ValueError("invalid PE signature")
        machine, sections = struct.unpack_from("<HH", image, pe + 4)
        optional_size = struct.unpack_from("<H", image, pe + 20)[0]
        magic = struct.unpack_from("<H", image, pe + 24)[0]
        if machine != 0x14C or magic != 0x10B:
            raise ValueError("expected x86 PE32")
        table = pe + 24 + optional_size
        for i in range(sections):
            _, section_rva, raw_size, raw_offset = struct.unpack_from("<IIII", image, table + i * 40 + 8)
            offset = rva - section_rva
            if 0 <= offset and offset + length <= raw_size and raw_offset + offset + length <= len(image):
                return image[raw_offset + offset:raw_offset + offset + length]
    except struct.error as exc:
        raise ValueError("truncated PE") from exc
    raise ValueError("RVA not backed by file bytes")


def verify_loaded(config, image, info, process_path):
    """Verify the selected loaded module and entry bytes before attaching hooks."""
    import hashlib
    import ntpath

    if hashlib.sha256(image).hexdigest() != config["sha256"]:
        raise ValueError("executable SHA-256 mismatch")
    if (info["name"].lower() != config["module"].lower() or
            ntpath.normcase(ntpath.normpath(info["path"])) != ntpath.normcase(ntpath.normpath(process_path))):
        raise ValueError("loaded module path does not match process image")
    if (info["arch"] != "ia32" or info["pointer_size"] != 4 or
            info["mz"] != 0x5A4D or info["machine"] != 0x14C):
        raise ValueError("loaded module is not x86 PE32")
    base, size = int(info["base"], 0), info["size"]
    ghidra_base = int(config["ghidra_base"], 0)
    entries = {entry["name"]: entry for entry in info["entries"]}
    if len(entries) != len(config["hooks"]):
        raise ValueError("loaded hook entry count mismatch")
    for hook in config["hooks"]:
        entry = entries[hook["name"]]
        va = int(hook["va"], 0)
        expected = runtime_address(base, ghidra_base, va, size)
        disk = pe_bytes_at_rva(image, va - ghidra_base, 16).hex()
        if (int(entry["address"], 0) != expected or not entry["executable"] or
                not entry["bytes"]["ok"] or entry["bytes"].get("hex") != disk):
            raise ValueError(f"loaded entry mismatch: {hook['name']}")


def validate_config(config):
    """Reject ambiguous or unsafe hook configurations."""
    import re

    if not re.fullmatch(r"[0-9a-f]{64}", config.get("sha256", "")):
        raise ValueError("sha256 must be lowercase hexadecimal")
    if not config.get("revision") or config.get("module", "").lower() != "wargame3.exe":
        raise ValueError("revision and explicit wargame3.exe module are required")
    base = int(config["ghidra_base"], 0)
    hooks = config.get("hooks")
    if not isinstance(hooks, list) or not hooks or len(hooks) > 16:
        raise ValueError("configure 1 to 16 hooks")
    names, addresses = set(), set()
    for hook in hooks:
        name = hook.get("name")
        va = int(hook["va"], 0)
        if not name or name in names or va in addresses or va < base:
            raise ValueError("hook names and addresses must be unique, within image")
        names.add(name)
        addresses.add(va)
        if not 0 <= hook.get("args", 0) <= 12 or not 1 <= hook.get("sample_every", 1) <= 1000000:
            raise ValueError("invalid argument count or sample rate")
        for read in hook.get("reads", []):
            if not isinstance(read.get("indirect", False), bool):
                raise ValueError("invalid indirect-read flag")
            if (not isinstance(read.get("second_indirect", False), bool) or
                    read.get("second_indirect", False) and not read.get("indirect", False)):
                raise ValueError("invalid second pointer dereference")
            if read.get("phase", "enter") not in {"enter", "leave", "both"}:
                raise ValueError("invalid read phase")
            if read.get("source") not in {"ecx", "edx", *[f"arg{i}" for i in range(hook.get("args", 0))]}:
                raise ValueError("invalid read source")
            if not isinstance(read.get("offset"), int) or not 0 <= read["offset"] <= 4096:
                raise ValueError("invalid read offset")
            if not isinstance(read.get("size"), int) or not 1 <= read["size"] <= 128:
                raise ValueError("invalid read size")


def process_identity(pid):
    """Read the image path and creation FILETIME of one Windows process."""
    from ctypes import wintypes

    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.OpenProcess.argtypes = (wintypes.DWORD, wintypes.BOOL, wintypes.DWORD)
    kernel.OpenProcess.restype = wintypes.HANDLE
    kernel.QueryFullProcessImageNameW.argtypes = (wintypes.HANDLE, wintypes.DWORD, wintypes.LPWSTR,
                                                  ctypes.POINTER(wintypes.DWORD))
    kernel.GetProcessTimes.argtypes = (wintypes.HANDLE, ctypes.POINTER(wintypes.FILETIME),
                                       ctypes.POINTER(wintypes.FILETIME), ctypes.POINTER(wintypes.FILETIME),
                                       ctypes.POINTER(wintypes.FILETIME))
    kernel.CloseHandle.argtypes = (wintypes.HANDLE,)
    handle = kernel.OpenProcess(0x1000, False, pid)
    if not handle:
        raise ctypes.WinError(ctypes.get_last_error())
    try:
        buffer = ctypes.create_unicode_buffer(32768)
        size = wintypes.DWORD(len(buffer))
        if not kernel.QueryFullProcessImageNameW(handle, 0, buffer, ctypes.byref(size)):
            raise ctypes.WinError(ctypes.get_last_error())
        times = [wintypes.FILETIME() for _ in range(4)]
        if not kernel.GetProcessTimes(handle, *(ctypes.byref(t) for t in times)):
            raise ctypes.WinError(ctypes.get_last_error())
        created = (times[0].dwHighDateTime << 32) | times[0].dwLowDateTime
        return buffer.value, created
    finally:
        kernel.CloseHandle(handle)


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def run_trace(args):
    if os.name != "nt":
        raise RuntimeError("controller must run on Windows")
    import frida

    config = json.loads(Path(args.config).read_text(encoding="utf-8"))
    validate_config(config)
    if args.hook:
        requested = set(args.hook)
        known = {hook["name"] for hook in config["hooks"]}
        if not requested <= known:
            raise ValueError(f"unknown hook(s): {sorted(requested - known)}")
        config["hooks"] = [hook for hook in config["hooks"] if hook["name"] in requested]
    if not 1 <= args.seconds <= 600 or not 1 <= args.event_limit <= 100000:
        raise ValueError("seconds must be 1..600; event limit must be 1..100000")
    if not Path(args.output).is_absolute():
        raise ValueError("output must be an absolute path outside the repository")
    output_path = Path(args.output).resolve()
    for parent in Path(__file__).resolve().parents:
        if (parent / ".git").exists() and output_path.is_relative_to(parent):
            raise ValueError("trace output must be outside the repository")
    device = frida.get_local_device()
    if args.pid is None:
        matches = [p.pid for p in device.enumerate_processes() if p.name.lower() == config["module"].lower()]
        if len(matches) != 1:
            raise RuntimeError(f"expected one {config['module']} process, found {matches}")
        pid = matches[0]
    else:
        pid = args.pid
    path, created = process_identity(pid)
    image = Path(path).read_bytes()
    if hashlib.sha256(image).hexdigest() != config["sha256"]:
        raise ValueError("process image SHA-256 mismatch before attach")
    marker = f"####SVNREVISION####{int(config['revision']):010d}####SVNREVISION####".encode()
    if marker not in image:
        raise ValueError("revision marker not found in executable")
    ghidra_base = int(config["ghidra_base"], 0)
    js_config = {"module": config["module"], "event_limit": args.event_limit,
                 "hooks": [{**h, "rva": int(h["va"], 0) - ghidra_base,
                            "args": h.get("args", 0), "sample_every": h.get("sample_every", 1)}
                           for h in config["hooks"]]}
    source = Path(__file__).with_name("hooks.js").read_text(encoding="utf-8").replace(
        "__CONFIG__", json.dumps(js_config, separators=(",", ":")), 1)
    session = script = None
    installed = False
    detached = threading.Event()
    wake = threading.Event()
    errors = []
    lock = threading.Lock()
    with open(args.output, "x", encoding="utf-8", newline="\n") as output:
        def write(event):
            try:
                with lock:
                    output.write(json.dumps(event, separators=(",", ":"), ensure_ascii=True) + "\n")
                    output.flush()
            except Exception as exc:
                errors.append(f"trace write failed: {exc}")
                wake.set()
                print(f"trace write failed: {exc}", file=sys.stderr)

        def message(msg, data):
            if msg.get("type") == "send":
                write(msg["payload"])
                if msg["payload"].get("event") == "callback_error":
                    errors.append(msg["payload"])
                    wake.set()
            else:
                errors.append(msg)
                write({"event": "script_error", "timestamp_utc": utc_now(), "message": msg})
                wake.set()

        def on_detached(reason, *extra):
            write({"event": "detached", "timestamp_utc": utc_now(), "reason": str(reason)})
            detached.set()
            wake.set()

        write({"event": "start", "timestamp_utc": utc_now(), "pid": pid, "created_filetime": created,
               "revision": config["revision"], "sha256": config["sha256"], "path": path,
               "frida_version": frida.__version__, "seconds": args.seconds, "event_limit": args.event_limit,
               "hooks": config["hooks"]})
        try:
            if errors:
                raise RuntimeError("cannot write trace header")
            session = device.attach(pid)
            session.on("detached", on_detached)
            if process_identity(pid) != (path, created):
                raise RuntimeError("process identity changed during attach")
            script = session.create_script(source)
            script.on("message", message)
            script.load()
            info = script.exports_sync.inspect()
            verify_loaded(config, image, info, path)
            if hashlib.sha256(Path(path).read_bytes()).hexdigest() != config["sha256"]:
                raise RuntimeError("image changed during validation")
            write({"event": "identity_verified", "timestamp_utc": utc_now(), "module": info})
            if errors:
                raise RuntimeError("cannot write identity verification")
            # Set before RPC: stop() also unwinds a partially installed hook set.
            installed = True
            installed_result = script.exports_sync.install()
            if installed_result.get("installed") != len(config["hooks"]):
                raise RuntimeError("partial hook installation")
            write({"event": "hooks_installed", "timestamp_utc": utc_now(), **installed_result})
            wake.wait(args.seconds)
            if errors:
                raise RuntimeError("injected script reported an error")
            if detached.is_set():
                raise RuntimeError("target detached before planned completion")
        except BaseException as exc:
            write({"event": "failure", "timestamp_utc": utc_now(), "error": f"{type(exc).__name__}: {exc}"})
            raise
        finally:
            if installed and script is not None and not detached.is_set():
                try:
                    result = script.exports_sync.stop()
                    write({"event": "summary", "timestamp_utc": utc_now(), **result})
                    if result.get("callback_errors", 0):
                        errors.append("instrumentation callback failed")
                except Exception as exc:
                    errors.append(str(exc))
                    write({"event": "cleanup_error", "timestamp_utc": utc_now(), "error": str(exc)})
            if script is not None and not detached.is_set():
                try:
                    script.unload()
                except Exception as exc:
                    errors.append(str(exc))
                    write({"event": "cleanup_error", "timestamp_utc": utc_now(), "error": str(exc)})
            if session is not None and not detached.is_set():
                try:
                    session.detach()
                except Exception as exc:
                    errors.append(str(exc))
                    write({"event": "cleanup_error", "timestamp_utc": utc_now(), "error": str(exc)})
            write({"event": "end", "timestamp_utc": utc_now(), "cleanup_errors": len(errors)})
    if errors:
        raise RuntimeError("script or cleanup errors occurred")
    print(f"HERMES_DONE_WGRD_TRACE {args.output}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--pid", type=int)
    parser.add_argument("--seconds", type=int, default=30)
    parser.add_argument("--event-limit", type=int, default=1000)
    parser.add_argument("--hook", action="append", help="trace only named hooks; repeatable")
    try:
        run_trace(parser.parse_args())
    except Exception as exc:
        print(f"WGRD trace failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
