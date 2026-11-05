#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Offline verification of Xiaomi/Mijia FOTA packages (MCU and BLE).

Format (found in §42, root added in §44):
    package = [content...] + [PEM chain: Mijia Open CA, leaf "cert"] + [ECDSA-SHA256 DER]
    signature = ECDSA P-256 (key leaf "cert") over SHA-256(everything before first
    '-----BEGIN CERTIFICATE-----')

Trust chain (§44): Mijia Root (assets/MijiaRootCert.der from Mi Home APK,
self-signed, 2016..2066) -> Mijia Open (c0) -> cert (c1). Public key of root
is extracted manually (Python cryptography 50.0 does not parse this DER due to
ExtraData; OpenSSL 3.5 parses and verifies without issues).

Usage:
    python verify_fota.py <package_file> [<file2> ...]
    python verify_fota.py --self   # verify known images from repo
"""
import sys, os

from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes

HERE = os.path.dirname(os.path.abspath(__file__))
MCU_IMG = os.path.join(HERE, '..', '..', 'images', 'mcu_0007.bin')
BLE_PKG = os.path.join(HERE, '..', '..', '..', 'firmware_ota',
                       '0d41b4df91f8d37b5f1355484e2b93c3_upd_xiaomi.scooter.5pro_v2.7.0_0015.bin')
CERT_DIR = os.path.join(HERE, 'tmp_certs')


def _root_pubkey():
    """Mijia Root public key from DER (manually: cryptography does not parse certificate)."""
    der = open(os.path.join(CERT_DIR, 'mijia_root.der'), 'rb').read()
    i = der.find(b'\x03\x42\x00\x04')  # BITSTR 66 B, uncompressed P-256
    if i < 0:
        raise ValueError('BITSTR of root public key not found')
    xy = der[i+4:i+4+64]  # X(32) + Y(32), without 0x04 marker
    return ec.EllipticCurvePublicNumbers(
        int.from_bytes(xy[:32], 'big'), int.from_bytes(xy[32:], 'big'),
        ec.SECP256R1()).public_key()


def load_chain():
    c0 = x509.load_der_x509_certificate(open(os.path.join(CERT_DIR, 'c0.der'), 'rb').read())
    c1 = x509.load_der_x509_certificate(open(os.path.join(CERT_DIR, 'c1.der'), 'rb').read())
    # validity of chain to root: c1 <- c0 <- Mijia Root
    c0.public_key().verify(c1.signature, c1.tbs_certificate_bytes,
                           ec.ECDSA(c1.signature_hash_algorithm))
    _root_pubkey().verify(c0.signature, c0.tbs_certificate_bytes,
                          ec.ECDSA(hashes.SHA256()))
    return c0, c1


def verify(path):
    """Verifies FOTA package. Returns (ok, info)."""
    d = open(path, 'rb').read()
    pem_start = d.find(b'-----BEGIN CERTIFICATE-----')
    if pem_start < 0:
        return False, 'PEM chain not found'
    sig = d[pem_start:]
    # DER SEQUENCE begins after last '-----END CERTIFICATE-----\n'
    end = sig.rfind(b'-----END CERTIFICATE-----\n')
    if end < 0:
        return False, 'END CERTIFICATE not found'
    der_off = pem_start + end + len(b'-----END CERTIFICATE-----\n')
    der = d[der_off:]
    if der[:1] != b'\x30':
        return False, f'no DER SEQUENCE after PEM (byte {der[0]:#x})'

    c0, c1 = load_chain()
    msg = d[:pem_start]
    for name, key in (('leaf "cert" (c1)', c1.public_key()), ('Mijia Open CA (c0)', c0.public_key())):
        try:
            key.verify(der, msg, ec.ECDSA(hashes.SHA256()))
            return True, f'signature VALID: {name} x SHA-256(d[:{pem_start:#x}]), ' \
                         f'chain c1<-c0<-MijiaRoot valid'
        except Exception:
            pass
    return False, 'signature invalid with all chain keys'


def main():
    files = sys.argv[1:]
    if not files or files == ['--self']:
        files = [f for f in (MCU_IMG, BLE_PKG) if os.path.exists(f)]
        print('mode --self: known images in repo')
    rc = 0
    for f in files:
        ok, info = verify(f)
        print(f'{"OK " if ok else "FAIL"} {os.path.basename(f)}: {info}')
        rc |= 0 if ok else 1
    return rc


if __name__ == '__main__':
    sys.exit(main())
