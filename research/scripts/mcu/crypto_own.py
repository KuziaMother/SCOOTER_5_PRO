# -*- coding: utf-8 -*-
"""MCU cryptography model: config #3 (expand) + "own" cipher block (0x1a7ac).

Static analysis (2026-08-23), verified by execution (Unicorn):

  0x1bfa0(dst, src)   - config #3 decryptor/expander:
                        dst[0..15] = src[0..15]; then 160 bytes generated:
                        B_r2 = B_{r2-4} ^ S(B_{r2-1}), r2=4..43 (total 176 B),
                        where S is identity except when r2%4==0:
                        S(st) = [S1[st1]^S2[r2/4], S1[st2], S1[st3], S1[st0]]
                        (S1 = S-box @0xa907, S2 = @0xab07).
  0x1a5fa(win, buf, ctx) - buf ^= ctx[16*win .. 16*win+15] (16 B).
  0x1dd8c(buf)        - T: for each 4-byte block b:
                        P = b0^b1^b2^b3; new[i] = b[i] ^ L(b[i]^b[i+1]) ^ P,
                        cyclic indices; L(x) = ((x<<1)&0xFF) ^ (0x1B*(x>>7)).
  0x1a7ac(buf, ctx)   - "own" cipher block: buf ^= C_0; for r in 1..10:
                        buf = S1[buf]; buf = permute(buf);
                        if r < 10: buf = T(buf);  buf ^= C_r.
                        C_r = ctx[16r..16r+15]; ctx = table @0x16aa (176 B).

Key conclusions (verified by execution, 2026-08-23):
  * "S-boxes" @0xa907/@0xab07 are NOT permutations: these are 256-byte slices of image CODE
    (func_0x0a910 and neighboring functions/pools). Substitution is irreversible.
  * T (0x1dd8c) is invertible (rank 32/32), BUT full own_cipher is a ONE-WAY
    function (lossy at each round): 65536 inputs -> ~11k unique outputs.
    This is a keyed-hash/MAC, not a block cipher: response cannot be decrypted,
    but with known seed one can COMPUTE any MCU response offline.
  * Key = first 176 B of table @0x16aa (decrypted config #3). Seed (16 B)
    comes from Mi Home upon bind (frame 0x1a), stored in NVRAM
    (flash @0x0801F400-region, RAM @0x871), restored and
    re-decrypted at boot (0x1ca08).
  * Used in exactly two places (both static):
      'b'  (0x200e4): response = "ok " + f(received block) + "\r";
      'm'+'k' (0x20212): after matching mask @0x1565 - f(mask)
      (mask rotation/burning; response contains mask BEFORE cipher).

Usage:
  python crypto_own.py model      # model: rank T, collisions, sanity
  python crypto_own.py verify     # verification against real code execution (Unicorn)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.dirname(os.path.dirname(HERE))
FW = os.path.join(RES, "images", "mcu_0007.bin")

FW_DATA = open(FW, "rb").read()
S1 = FW_DATA[0xa907:0xaa07]   # S-box 1 (256 B)
S2 = FW_DATA[0xab07:0xac07]   # S-box 2 (256 B)


def is_perm(box):
    return len(set(box)) == 256


def L(x):
    return ((x << 1) & 0xFF) ^ (0x1B * ((x >> 7) & 1))


def T_block(b):
    """0x1dd8c on a single 4-byte block."""
    P = b[0] ^ b[1] ^ b[2] ^ b[3]
    out = []
    for i in range(4):
        d = b[i] ^ b[(i + 1) % 4]
        out.append(b[i] ^ L(d) ^ P)
    return bytes(out)


def T(buf16):
    """0x1dd8c on a 16-byte buffer (4 independent blocks)."""
    return b"".join(T_block(buf16[i:i + 4]) for i in (0, 4, 8, 12))


# permutation from 0x1a7de..0x1a80c:
#   cycle [1->5->9->D], swap [2,A], swap [6,E], cycle [3->F->B->7]
def permute(buf16):
    o = bytearray(buf16)
    # [1,5,9,D]: tmp=o[1]; o[1]=o[5]; o[5]=o[9]; o[9]=o[0xD]; o[0xD]=tmp
    t = o[1]
    o[1], o[5], o[9], o[0xD] = o[5], o[9], o[0xD], t
    o[2], o[0xA] = o[0xA], o[2]
    o[6], o[0xE] = o[0xE], o[6]
    # [3,F,B,7]: tmp=o[3]; o[3]=o[0xF]; o[0xF]=o[0xB]; o[0xB]=o[7]; o[7]=tmp
    t = o[3]
    o[3], o[0xF], o[0xB], o[7] = o[0xF], o[0xB], o[7], t
    return bytes(o)


def own_cipher(buf16, ctx):
    """0x1a7ac: 10-round block cipher, key = ctx windows C_0..C_10."""
    assert len(ctx) >= 176
    buf = bytearray(buf16)
    for i in range(16):
        buf[i] ^= ctx[i]                       # C_0 (via 0x1a5fa win=0)
    for r in range(1, 11):
        buf = bytearray(S1[x] for x in buf)    # S-box across all 16 B
        buf = bytearray(permute(bytes(buf)))   # fixed permutation
        if r < 10:
            buf = bytearray(T(bytes(buf)))     # 0x1dd8c
        base = 16 * r
        for i in range(16):
            buf[i] ^= ctx[base + i]            # C_r
    return bytes(buf)


def expand(seed16):
    """0x1bfa0: 16-byte seed -> 176-byte table.

    IMPORTANT: "S-boxes" @0xa907/@0xab07 are NOT permutations, but arbitrary 256 B
    slices of image code (including func_0x0a910 and pools) -> substitution is irreversible,
    cipher is one-way (lossy)."""
    B = [bytearray(4) for _ in range(44)]
    for k in range(4):
        B[k] = bytearray(seed16[4 * k:4 * k + 4])
    for r2 in range(4, 44):
        st = bytes(B[r2 - 1])
        if r2 % 4 == 0:
            k = r2 // 4
            st = bytes([S1[st[1]] ^ S2[k], S1[st[2]], S1[st[3]], S1[st[0]]])
        B[r2] = bytearray(B[r2 - 4][i] ^ st[i] for i in range(4))
    return b"".join(bytes(b) for b in B)


# ---------------------------------------------------------------- inversions

def gf2_matrix_of_T():
    """Matrix T (32x32) over GF(2): M[r][c] = bit r of image T(e_c)."""
    M = [[0] * 32 for _ in range(32)]
    for c in range(32):
        blk = bytearray(4)
        blk[c // 8] = 1 << (c % 8)
        out = T_block(bytes(blk))
        for r in range(32):
            M[r][c] = (out[r // 8] >> (r % 8)) & 1
    return M


def gf2_invert(M):
    """Inversion of square matrix over GF(2) (Gauss). None if singular."""
    n = len(M)
    A = [row[:] + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(M)]
    for c in range(n):
        piv = next((r for r in range(c, n) if A[r][c]), None)
        if piv is None:
            return None
        A[c], A[piv] = A[piv], A[c]
        for r in range(n):
            if r != c and A[r][c]:
                A[r] = [a ^ b for a, b in zip(A[r], A[c])]
    return [row[n:] for row in A]


def gf2_rank(M):
    n = len(M)
    A = [row[:] for row in M]
    rank = 0
    for c in range(n):
        piv = next((r for r in range(rank, n) if A[r][c]), None)
        if piv is None:
            continue
        A[rank], A[piv] = A[piv], A[rank]
        for r in range(n):
            if r != rank and A[r][c]:
                A[r] = [a ^ b for a, b in zip(A[r], A[rank])]
        rank += 1
    return rank


def T_block_inv(out4, Minv):
    """Inverse application of T to block via inverse matrix."""
    col_in = [ (out4[i] >> j) & 1 for i in range(4) for j in range(8) ]
    out = bytearray(4)
    for r in range(32):
        v = 0
        for c in range(32):
            v ^= Minv[r][c] * col_in[c]
        out[r // 8] |= (v & 1) << (r % 8)
    return bytes(out)


def build_T_inv():
    M = gf2_matrix_of_T()
    rank = gf2_rank(M)
    Minv = gf2_invert(M) if rank == 32 else None
    return M, rank, Minv


# forward permutation: out[j] = in[PI(j)]
PI = [0, 5, 0xA, 0xF, 4, 9, 0xE, 3, 8, 0xD, 2, 7, 0xC, 1, 6, 0xB]


def permute_inv(out16):
    """in[i] = out[PI^{-1}(i)] - inverse permutation."""
    pinv = [0] * 16
    for i, j in enumerate(PI):
        pinv[j] = i
    return bytes(out16[pinv[i]] for i in range(16))


def own_cipher_inv(ct16, ctx, Tinv):
    """Inverse "own" cipher (if T is invertible)."""
    # S1 is not a permutation: take an arbitrary preimage; correctness
    # is verified by re-encrypting (round-trip via own_cipher).
    S1inv = bytearray(256)
    for i, v in enumerate(S1):
        S1inv[v] = i
    buf = bytearray(ct16)
    for r in range(10, 0, -1):
        base = 16 * r
        for i in range(16):
            buf[i] ^= ctx[base + i]
        if r < 10:
            buf = b"".join(T_block_inv(buf[i:i + 4], Tinv) for i in (0, 4, 8, 12))
        buf = permute_inv(bytes(buf))
        buf = bytearray(S1inv[x] for x in buf)
    for i in range(16):
        buf[i] ^= ctx[i]
    return bytes(buf)


def model():
    print(f"S1(@0xa907) permutation: {is_perm(S1)}")
    print(f"S2(@0xab07) permutation: {is_perm(S2)}")
    seed = bytes(range(16))
    tbl = expand(seed)
    print(f"expand: 16 -> {len(tbl)} B")
    print(f"  seed  : {seed.hex()}")
    print(f"  tbl[0:16] == seed: {tbl[:16] == seed}")
    print(f"  tbl[16:48]: {tbl[16:48].hex()}")

    M, rank, Minv = build_T_inv()
    print(f"T (0x1dd8c): rank over GF(2) = {rank}/32 -> {'INVERTIBLE' if Minv else 'NOT INVERTIBLE'}")
    # check T_inv(T(x)) == x across entire block space (256^4 brute force impossible;
    # linearity: basis is sufficient)
    if Minv:
        ok = True
        for col in range(32):
            blk = bytearray(4)
            blk[col // 8] = 1 << (col % 8)
            back = T_block_inv(T_block(bytes(blk)), Minv)
            if back != bytes(blk):
                ok = False
        print(f"  T_inv(T(basis)) == basis: {ok}")

    # One-way property: S1 is not bijective -> function is not injective.
    # Proof: collisions in 2-byte subspace (65536 inputs).
    ctx = expand(bytes(range(16)))
    base = bytes(16)
    seen = {}
    coll = 0
    for hi in range(256):
        for lo in range(256):
            pt = bytearray(base)
            pt[0], pt[1] = hi, lo
            ct = own_cipher(bytes(pt), ctx)
            if ct in seen:
                coll += 1
            else:
                seen[ct] = (hi, lo)
    print(f"own_cipher: collisions in 2-B subspace: {coll} "
          f"(unique outputs {len(seen)}/65536) -> ONE-WAY function")


def verify():
    sys.path.insert(0, os.path.join(os.path.dirname(HERE), "..", "..", "emulator"))
    from mcu_emu import McuEmu, RAM

    seed = bytes([0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88,
                  0x99, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF, 0x0F])
    SRC = RAM + 0x4000
    DST = RAM + 0x4100          # 176 B
    BUF = RAM + 0x4200          # 16 B
    CTX = RAM + 0x4300          # 176 B

    emu = McuEmu(max_insn=200000)
    emu.uc.mem_write(SRC, seed)
    emu.uc.mem_write(DST, bytes(176))

    # --- 0x1bfa0: expand
    emu.run_func(0x1bfa0, args=(DST, SRC))
    got = bytes(emu.uc.mem_read(DST, 176))
    exp = expand(seed)
    print(f"[verify] expand (0x1bfa0): model == execution: {got == exp}")
    if got != exp:
        for i in range(176):
            if got[i] != exp[i]:
                print(f"  first mismatch @{i}: got={got[i]:02x} exp={exp[i]:02x}")
                break

    # --- 0x1dd8c: T
    blk = bytes.fromhex("de ad be ef 01 23 45 67 89 ab cd ef fe ed fa 5a")
    emu.uc.mem_write(BUF, blk)
    emu.run_func(0x1dd8c, args=(BUF,))
    got = bytes(emu.uc.mem_read(BUF, 16))
    exp = T(blk)
    print(f"[verify] T (0x1dd8c):      model == execution: {got == exp}")
    if got != exp:
        print(f"  got: {got.hex()}")
        print(f"  exp: {exp.hex()}")

    # --- 0x1a5fa: xor window
    ctx = expand(seed)
    emu.uc.mem_write(CTX, ctx)
    emu.uc.mem_write(BUF, blk)
    for win in (0, 3, 7, 10):
        emu.uc.mem_write(BUF, blk)
        emu.run_func(0x1a5fa, args=(win, BUF, CTX))
        got = bytes(emu.uc.mem_read(BUF, 16))
        exp = bytes(blk[i] ^ ctx[16 * win + i] for i in range(16))
        if got != exp:
            print(f"[verify] xor win={win}: MISMATCH")

    # --- 0x1a7ac: own_cipher
    emu.uc.mem_write(BUF, blk)
    emu.run_func(0x1a7ac, args=(BUF, CTX))
    got = bytes(emu.uc.mem_read(BUF, 16))
    exp = own_cipher(blk, ctx)
    print(f"[verify] own (0x1a7ac):    model == execution: {got == exp}")
    if got != exp:
        print(f"  got: {got.hex()}")
        print(f"  exp: {exp.hex()}")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "model"
    if mode == "verify":
        verify()
    else:
        model()
