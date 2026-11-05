#!/usr/bin/env python
"""ESP32 (MicroPython) UART sniffer for MCU-BLE line — captures into RAM via REPL.

Commands:
  python tools/esp32_sniff.py sniff out.bin [--seconds 60] [--baud 115200]
      starts capture, waits N seconds, dumps buffer to out.bin
  python tools/esp32_sniff.py check
      tests REPL responsiveness and free RAM
"""
import argparse
import sys
import time

try:
    import serial
except ImportError:
    sys.exit("pyserial required: pip install pyserial")

PORT = "COM4"
BAUD_REPL = 115200

START_TMPL = '''import _thread, machine
BUF = bytearray()
def _sniff():
    u = machine.UART(2, baudrate={baud}, tx=17, rx=16)
    while True:
        d = u.read()
        if d:
            BUF.extend(d)
_thread.start_new_thread(_sniff, ())
print("SNIF_OK")
'''


def conn():
    s = serial.Serial(PORT, BAUD_REPL, timeout=2)
    # wait for REPL readiness: newline -> '>>> ' (banner after reset may be delayed)
    deadline = time.time() + 10
    last_nl = 0.0
    while time.time() < deadline:
        d = s.read(65536)
        if b">>>" in d:
            break
        if time.time() - last_nl > 1.5:  # REPL silent — nudge
            s.write(b"\n")
            last_nl = time.time()
    else:
        sys.exit("REPL did not respond within 10 s (no '>>>')")
    time.sleep(0.2)
    s.reset_input_buffer()
    return s


def cmd(s, text, wait=1.0):
    s.write(text.encode() + b"\n")
    time.sleep(wait)
    return s.read(65536).decode(errors="replace")


def wait_prompt(s, marker, timeout=10):
    end = time.time() + timeout
    buf = b""
    while time.time() < end:
        d = s.read(65536)
        if d:
            buf += d
            if marker.encode() in buf:
                return buf.decode(errors="replace")
    return buf.decode(errors="replace")


def check():
    s = conn()
    out = cmd(s, "import gc; print('CHECK', gc.mem_free())", 1.0)
    line = [l for l in out.splitlines() if l.startswith("CHECK")]
    if not line:
        sys.exit(f"REPL not responding:\n{out}")
    print("REPL alive, free RAM:", line[-1].split()[1], "B")
    s.close()


def probe(s):
    """Initial probe command: if REPL was busy (banner/main.py), send Ctrl-C and retry."""
    out = cmd(s, "print('CHECK', 1)", 1.0)
    if "CHECK" not in out:
        s.write(b"\x03")
        time.sleep(1.0)
        s.reset_input_buffer()
        out = cmd(s, "print('CHECK', 1)", 1.0)
    return out


def sniff(out_path, seconds, baud):
    s = conn()
    out = probe(s)
    if "CHECK" not in out:
        sys.exit(f"REPL unavailable (reflash: esptool write-flash --erase-all 0x1000 ...):\n{out}")
    print("starting capture:", seconds, "s @", baud)
    # multiline input in REPL: empty line at the end closes blocks
    out = cmd(s, START_TMPL.format(baud=baud) + "\n", 1.5)
    if "SNIF_OK" not in out:
        sys.exit(f"thread did not start:\n{out}")
    time.sleep(seconds)
    out = cmd(s, "print('SIZE', len(BUF))", 1.0)
    line = [l for l in out.splitlines() if l.startswith("SIZE")]
    size = int(line[-1].split()[1]) if line else -1
    if size < 0:
        sys.exit(f"failed to determine buffer size:\n{out}")
    print(f"buffer: {size} B, downloading...")
    data = bytearray()
    pos = 0
    while pos < size:
        out = cmd(s, f"print('H', BUF[{pos}:{pos+512}].hex())", 0.6)
        hline = [l for l in out.splitlines() if l.startswith("H ")]
        if not hline:
            sys.exit(f"download interrupted at {pos}/{size}:\n{out}")
        data += bytes.fromhex(hline[-1][2:])
        pos += 512
        if pos % 8192 == 0:
            print(f"  {pos}/{size}")
    open(out_path, "wb").write(bytes(data))
    cmd(s, "del BUF", 0.5)
    s.close()
    print(f"saved: {out_path} ({len(data)} B)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p_sniff = sub.add_parser("sniff")
    p_sniff.add_argument("out")
    p_sniff.add_argument("--seconds", type=int, default=60)
    p_sniff.add_argument("--baud", type=int, default=115200)
    sub.add_parser("check")
    a = ap.parse_args()
    if a.cmd == "sniff":
        sniff(a.out, a.seconds, a.baud)
    else:
        check()
