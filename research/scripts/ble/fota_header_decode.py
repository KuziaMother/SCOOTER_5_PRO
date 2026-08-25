#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
§62 — Декодер FOTA-хедеров BLE-образа (Realtek RTL8762C) по SDK-структурам.

Структуры взяты из zip_archives/rtl8762c-sdk-full/inc/platform/patch_header_check.h
(#pragma pack(1)). Пакет = два 1KB-хедера (ic_type=5, общий uuid) + payload'ы + cert-trailer.

Запуск:  python -X utf8 scripts/ble/fota_header_decode.py [path-to-ble.bin]
"""
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_IMG = os.path.join(HERE, "..", "..", "images", "ble_2.7.0_0015.bin")
FLASH_BASE = 0x01800000


def ctrl_flag_bits(v):
    return dict(
        xip=(v >> 0) & 1, enc=(v >> 1) & 1, load_when_boot=(v >> 2) & 1,
        enc_load=(v >> 3) & 1, enc_key_select=(v >> 4) & 7, not_ready=(v >> 7) & 1,
        not_obsolete=(v >> 8) & 1, integrity_check_en_in_boot=(v >> 9) & 1,
        rsvd=(v >> 10) & 0x3F,
    )


def decode_ctrl(img, off):
    """T_IMG_CTRL_HEADER_FORMAT (12 Б)."""
    return dict(
        ic_type=img[off], secure_version=img[off + 1],
        ctrl_flag=struct.unpack_from('<H', img, off + 2)[0],
        image_id=struct.unpack_from('<H', img, off + 4)[0],
        crc16=struct.unpack_from('<H', img, off + 6)[0],
        payload_len=struct.unpack_from('<I', img, off + 8)[0],
    )


def decode_img_header(img, off):
    """T_IMG_HEADER_FORMAT (ключевые поля; magic@0x30, dec_key@0x34)."""
    c = decode_ctrl(img, off)
    d = dict(c)
    d['ctrl_flag_bits'] = ctrl_flag_bits(c['ctrl_flag'])
    d['uuid'] = img[off + 0x0C:off + 0x1C]
    d['exe_base'] = struct.unpack_from('<I', img, off + 0x1C)[0]
    d['load_base'] = struct.unpack_from('<I', img, off + 0x20)[0]
    d['load_len'] = struct.unpack_from('<I', img, off + 0x24)[0]
    d['img_base'] = struct.unpack_from('<I', img, off + 0x28)[0]
    d['magic_pattern'] = struct.unpack_from('<I', img, off + 0x30)[0]
    d['dec_key'] = img[off + 0x34:off + 0x44]
    return d


def find_headers(img):
    """1KB-выровненные хедеры с ic_type==5."""
    out = []
    for off in range(0, max(0, len(img) - 0x400), 0x400):
        if img[off] == 5:
            out.append(off)
    return out


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_IMG
    with open(path, 'rb') as f:
        img = f.read()
    print(f"Образ: {os.path.basename(path)} ({len(img)} Б = {len(img):#x}), flash base {FLASH_BASE:#x}")
    hdrs = find_headers(img)
    print(f"Хедеры (ic_type=5, 1KB-aligned): {[hex(h) for h in hdrs]}")
    uuids = set()
    for i, off in enumerate(hdrs, 1):
        d = decode_img_header(img, off)
        uuids.add(d['uuid'].hex())
        print(f"\n=== HDR #{i} @file {off:#x} (vaddr {FLASH_BASE + off:#x}) ===")
        print(f"  ic_type={d['ic_type']} sec_ver={d['secure_version']} image_id={d['image_id']:#x} "
              f"crc16={d['crc16']:#x} payload_len={d['payload_len']} ({d['payload_len']:#x})")
        print(f"  ctrl_flag={d['ctrl_flag']:#06x}: {d['ctrl_flag_bits']}")
        print(f"  uuid[16]={d['uuid'].hex()}")
        print(f"  exe_base={d['exe_base']:#x} load_base={d['load_base']:#x} "
              f"load_len={d['load_len']} ({d['load_len']:#x}) img_base={d['img_base']:#x}")
        print(f"  magic_pattern={d['magic_pattern']:#x} dec_key[16]={d['dec_key'].hex()}")
    print(f"\nУникальных uuid: {len(uuids)} -> {[u for u in uuids]}")


if __name__ == '__main__':
    main()
