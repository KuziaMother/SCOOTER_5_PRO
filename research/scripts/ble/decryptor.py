#!/usr/bin/env python3
"""
Attempt to decrypt the encrypted APP region of BLE firmware (RTL8762C) without SWD dump
of OTP. See docs/FACTS.md: `xip=1, enc=1, enc_key_select=7` -> key is stored in OTP,
normally decrypted only by hardware (XIP) -> cannot be recovered from .bin via software WITHOUT key.
This is the statically last chance: try publicly known/default demo SDK keys.

Region (docs/FACTS.md): ENC = 0x0a200..0x25400 (111104 B), IV candidate = header
bytes [0x0c:0x1c] (16 B, see research/analyze_crypto.py).

Key candidates:
  * `OTA_AES_KEY` from rtl8762c-gcc-examples/config/oem_config.c — 32 B placeholder
    from demo SDK config (00 01 02 ... 1F), does NOT necessarily match Dreame key
    (BT_MAC there is also placeholder aa:bb:cc:dd:ee:ff) — but it is the only
    documented "default OTA key of RTL8762x" available statically.
    Tested as AES-128 (first 16 B) and AES-256 (full 32 B).
  * all-zero / all-0xff — typical "forgot to configure" defaults.

Modes: CBC and CTR (in CTR, candidate IV is used as nonce||counter=0, evaluated
as big-endian 128-bit counter, as exact RTL8762x XIP counter format is unknown).

Result verification — HEURISTICS, not proof:
  * entropy (low = resembles code/data, ~8.0 = still ciphertext/garbage);
  * proportion of plausible Thumb 16-bit instructions (align, top bits of frequent opcodes);
  * readable ASCII strings longer than 6 chars.
If no candidate yields a recognizable result — outcome is negative and expected:
key is in OTP, statically unreachable (SWD dump required, see todo.md §B).
"""
import collections
import math
import os
import struct
import sys

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

IMG = os.path.join(os.path.dirname(__file__), "..", "..", "images", "ble_2.7.0_0015.bin")
FW = sys.argv[1] if len(sys.argv) > 1 else IMG
ENC = (0x0A200, 0x25400)

OEM_CONFIG_KEY32 = bytes(range(0x00, 0x20))  # oem_config.c OTA_AES_KEY (demo placeholder)

CANDIDATE_KEYS = {
    "oem_config_aes128 (first 16B of OTA_AES_KEY)": OEM_CONFIG_KEY32[:16],
    "oem_config_aes256 (full 32B of OTA_AES_KEY)": OEM_CONFIG_KEY32,
    "zero128": bytes(16),
    "zero256": bytes(32),
    "ff128": bytes([0xFF] * 16),
    "ff256": bytes([0xFF] * 32),
}


def entropy(b):
    if not b:
        return 0.0
    c = collections.Counter(b)
    n = len(b)
    return -sum((x / n) * math.log2(x / n) for x in c.values())


def ascii_strings(b, min_len=8):
    out, cur = [], bytearray()
    for byte in b:
        if 32 <= byte < 127:
            cur.append(byte)
        else:
            if len(cur) >= min_len:
                out.append(bytes(cur).decode())
            cur = bytearray()
    if len(cur) >= min_len:
        out.append(bytes(cur).decode())
    return out


def thumb_plausibility(b):
    """Rough heuristic: proportion of 16-bit halfwords matching frequent Thumb opcodes
    (push/pop/mov/bl-upper half, etc. by high bits). NOT a disassembler."""
    if len(b) < 2:
        return 0.0
    n = len(b) // 2
    hits = 0
    for i in range(0, n * 2, 2):
        hw = struct.unpack_from("<H", b, i)[0]
        top5 = hw >> 11
        # frequent Thumb16 prefixes: 000xx(shift) 010001(hi-reg) 0100(alu) 1011(misc/push-pop)
        # 11100(uncond b) 1101(cond b) 10110/10111(push/pop) — coarsely check top 5 bits
        if top5 in (0b00000, 0b00001, 0b00010, 0b10110, 0b10111, 0b11100, 0b01000, 0b01001):
            hits += 1
    return hits / n


def try_one(name, key, data, iv):
    results = []
    for mode_name in ("CBC", "CTR"):
        try:
            if mode_name == "CBC":
                if len(data) % 16 != 0:
                    continue
                cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
            else:
                cipher = Cipher(algorithms.AES(key), modes.CTR(iv))
            dec = cipher.decryptor()
            pt = dec.update(data) + dec.finalize()
        except Exception as e:
            results.append((mode_name, None, str(e)))
            continue
        results.append((mode_name, pt, None))
    return results


def main():
    d = open(FW, "rb").read()
    enc = d[ENC[0]:ENC[1]]
    iv = d[0x0C:0x1C]

    # Heuristic calibration: known PLAINTEXT code region (0x6000..0xa200, from
    # analyze_crypto.py) as positive baseline and raw ciphertext itself (undecrypted)
    # as negative control — otherwise eyeball thresholds catch random ASCII
    # substrings in noise (verified: without calibration ALL candidates are FALSELY flagged).
    plain_sample = d[0x6000:0x6000 + 4096]
    plain_strs = len(ascii_strings(d[0x6000:0x6000 + 65536]))
    plain_e = entropy(plain_sample)
    plain_plaus = thumb_plausibility(plain_sample)
    neg_e = entropy(enc[:4096])
    neg_strs = len(ascii_strings(enc[:65536]))
    neg_plaus = thumb_plausibility(enc[:4096])

    print(f"[decryptor] file={FW}  enc-region=0x{ENC[0]:x}..0x{ENC[1]:x} ({len(enc)} B)")
    print(f"[decryptor] IV candidate (header[0x0c:0x1c]) = {iv.hex()}")
    print(f"[decryptor] calibration: plaintext-code(0x6000) entropy={plain_e:.3f} "
          f"Thumb={plain_plaus:.2f} strings={plain_strs}  |  "
          f"raw-ciphertext entropy={neg_e:.3f} Thumb={neg_plaus:.2f} strings={neg_strs}\n")

    # Threshold: noticeably closer to plaintext profile than ciphertext.
    e_thresh = (plain_e + neg_e) / 2
    strs_thresh = max(plain_strs * 0.3, neg_strs * 3)

    best = []
    for name, key in CANDIDATE_KEYS.items():
        for mode_name, pt, err in try_one(name, key, enc, iv):
            if err:
                print(f"  [{name:45}] {mode_name}: error ({err})")
                continue
            e = entropy(pt[:4096])
            strs = ascii_strings(pt[:65536])
            plaus = thumb_plausibility(pt[:4096])
            flag = "  <-- resembles plaintext?" if (e < e_thresh and len(strs) > strs_thresh) else ""
            print(f"  [{name:45}] {mode_name}: entropy={e:.3f}  Thumb={plaus:.2f}  "
                  f"strings(>=8)={len(strs)}{flag}")
            best.append((e, plaus, name, mode_name))

    best.sort(key=lambda x: (x[0], -x[1]))
    print("\n[decryptor] best candidate by minimum entropy:",
          best[0][2], best[0][3], f"entropy={best[0][0]:.3f}" if best else "(none)")
    print(f"[decryptor] cutoff threshold: entropy<{e_thresh:.3f} AND strings>{strs_thresh:.0f}")
    print("[decryptor] if no candidate is marked '<-- resembles plaintext?' -")
    print("            result is NEGATIVE: key is in OTP, statically unrecoverable")
    print("            (see todo.md §B - SWD dump of XIP region required).")


if __name__ == "__main__":
    main()
