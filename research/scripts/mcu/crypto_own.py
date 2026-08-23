# -*- coding: utf-8 -*-
"""Модель криптографии MCU: конфиг #3 (expand) + шифроблок «own» (0x1a7ac).

Статический разбор (2026-08-23), сверено исполнением (Unicorn):

  0x1bfa0(dst, src)   — расшифровщик/экспандер конфига #3:
                        dst[0..15] = src[0..15]; далее 160 байт генерации:
                        B_r2 = B_{r2-4} ^ S(B_{r2-1}), r2=4..43 (итого 176 Б),
                        где S — тождество, кроме r2%4==0:
                        S(st) = [S1[st1]^S2[r2/4], S1[st2], S1[st3], S1[st0]]
                        (S1 = S-box @0xa907, S2 = @0xab07).
  0x1a5fa(win, buf, ctx) — buf ^= ctx[16*win .. 16*win+15] (16 Б).
  0x1dd8c(buf)        — T: по каждому 4-байтовому блоку b:
                        P = b0^b1^b2^b3; new[i] = b[i] ^ L(b[i]^b[i+1]) ^ P,
                        индексы циклически; L(x) = ((x<<1)&0xFF) ^ (0x1B*(x>>7)).
  0x1a7ac(buf, ctx)   — шифроблок «own»: buf ^= C_0; for r in 1..10:
                        buf = S1[buf]; buf = permute(buf);
                        if r < 10: buf = T(buf);  buf ^= C_r.
                        C_r = ctx[16r..16r+15]; ctx = таблица @0x16aa (176 Б).

Ключевые выводы (сверено исполнением, 2026-08-23):
  * «S-box'ы» @0xa907/@0xab07 — НЕ перестановки: это 256-байтные срезы КОДА
    образа (func_0x0a910 и соседние функции/пулы). Подстановка необратима.
  * T (0x1dd8c) обратим (ранг 32/32), НО весь own_cipher — ОДНОНАПРАВЛЕННАЯ
    функция (lossy на каждом раунде): 65536 входов -> ~11k уникальных выходов.
    Это keyed-hash/MAC, не блочный шифр: расшифровать ответ нельзя,
    но при известном сееде можно ВЫЧИСЛИТЬ любой ответ MCU офлайн.
  * Ключ = первые 176 Б таблицы @0x16aa (расшифровка конфига #3). Сид (16 Б)
    приходит из Mi Home при бинде (кадр 0x1a), хранится в NVRAM
    (flash @0x0801F400-регион, RAM @0x871), восстанавливается и
    пере-расшифровывается при старте (0x1ca08).
  * Используется ровно в двух местах (оба статические):
      'b'  (0x200e4): ответ = "ok " + f(полученный блок) + "\r";
      'm'+'k' (0x20212): после совпадения с маской @0x1565 — f(маска)
      (ротация/сжигание маски; ответ содержит маску ДО шифра).

Запуск:
  python crypto_own.py model      # модель: ранг T, коллизии, sanity
  python crypto_own.py verify     # сверка с исполнением реального кода (Unicorn)
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
    """0x1dd8c на одном 4-байтовом блоке."""
    P = b[0] ^ b[1] ^ b[2] ^ b[3]
    out = []
    for i in range(4):
        d = b[i] ^ b[(i + 1) % 4]
        out.append(b[i] ^ L(d) ^ P)
    return bytes(out)


def T(buf16):
    """0x1dd8c на 16-байтовом буфере (4 независимых блока)."""
    return b"".join(T_block(buf16[i:i + 4]) for i in (0, 4, 8, 12))


# перестановка из 0x1a7de..0x1a80c:
#   цикл [1->5->9->D], swap [2,A], swap [6,E], цикл [3->F->B->7]
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
    """0x1a7ac: 10-раундовый блочный шифр, ключ = окна ctx C_0..C_10."""
    assert len(ctx) >= 176
    buf = bytearray(buf16)
    for i in range(16):
        buf[i] ^= ctx[i]                       # C_0 (через 0x1a5fa win=0)
    for r in range(1, 11):
        buf = bytearray(S1[x] for x in buf)    # S-box по всем 16 Б
        buf = bytearray(permute(bytes(buf)))   # фиксированная перестановка
        if r < 10:
            buf = bytearray(T(bytes(buf)))     # 0x1dd8c
        base = 16 * r
        for i in range(16):
            buf[i] ^= ctx[base + i]            # C_r
    return bytes(buf)


def expand(seed16):
    """0x1bfa0: 16-байтовый сид -> 176-байтовая таблица.

    ВАЖНО: «S-box'ы» @0xa907/@0xab07 — НЕ перестановки, а произвольные 256 Б
    среза кода образа (включая func_0x0a910 и пулы) -> подстановка необратима,
    шифр — однонаправленный (lossy)."""
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


# ---------------------------------------------------------------- инверсии

def gf2_matrix_of_T():
    """Матрица T (32x32) над GF(2): M[r][c] = бит r образа T(e_c)."""
    M = [[0] * 32 for _ in range(32)]
    for c in range(32):
        blk = bytearray(4)
        blk[c // 8] = 1 << (c % 8)
        out = T_block(bytes(blk))
        for r in range(32):
            M[r][c] = (out[r // 8] >> (r % 8)) & 1
    return M


def gf2_invert(M):
    """Инверсия квадратной матрицы над GF(2) (Gauss). None, если вырождена."""
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
    """Обратное применение T к блоку через инверсную матрицу."""
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


# прямая перестановка: out[j] = in[PI(j)]
PI = [0, 5, 0xA, 0xF, 4, 9, 0xE, 3, 8, 0xD, 2, 7, 0xC, 1, 6, 0xB]


def permute_inv(out16):
    """in[i] = out[PI^{-1}(i)] — обратная перестановка."""
    pinv = [0] * 16
    for i, j in enumerate(PI):
        pinv[j] = i
    return bytes(out16[pinv[i]] for i in range(16))


def own_cipher_inv(ct16, ctx, Tinv):
    """Обратный шифр «own» (если T обратим)."""
    # S1 — не перестановка: берём произвольный предобраз; корректность
    # проверяется повторным шифрованием (round-trip через own_cipher).
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
    print(f"S1(@0xa907) перестановка: {is_perm(S1)}")
    print(f"S2(@0xab07) перестановка: {is_perm(S2)}")
    seed = bytes(range(16))
    tbl = expand(seed)
    print(f"expand: 16 -> {len(tbl)} Б")
    print(f"  seed  : {seed.hex()}")
    print(f"  tbl[0:16] == seed: {tbl[:16] == seed}")
    print(f"  tbl[16:48]: {tbl[16:48].hex()}")

    M, rank, Minv = build_T_inv()
    print(f"T (0x1dd8c): ранг над GF(2) = {rank}/32 -> {'ОБРАТИМ' if Minv else 'НЕОБРАТИМ'}")
    # проверка T_inv(T(x)) == x на всём пространстве блоков (4^4*... — перебор 256^4 невозможен;
    # линейность: достаточно базиса)
    if Minv:
        ok = True
        for col in range(32):
            blk = bytearray(4)
            blk[col // 8] = 1 << (col % 8)
            back = T_block_inv(T_block(bytes(blk)), Minv)
            if back != bytes(blk):
                ok = False
        print(f"  T_inv(T(basis)) == basis: {ok}")

    # Однонаправленность: S1 не биективна -> функция не инъективна.
    # Доказательство: коллизии в 2-байтном подпространстве (65536 входов).
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
    print(f"own_cipher: коллизий в 2-Б подпространстве: {coll} "
          f"(уникальных выходов {len(seen)}/65536) -> ОДНОНАПРАВЛЕННАЯ функция")


def verify():
    sys.path.insert(0, os.path.join(os.path.dirname(HERE), "..", "..", "emulator"))
    from mcu_emu import McuEmu, RAM

    seed = bytes([0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88,
                  0x99, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF, 0x0F])
    SRC = RAM + 0x4000
    DST = RAM + 0x4100          # 176 Б
    BUF = RAM + 0x4200          # 16 Б
    CTX = RAM + 0x4300          # 176 Б

    emu = McuEmu(max_insn=200000)
    emu.uc.mem_write(SRC, seed)
    emu.uc.mem_write(DST, bytes(176))

    # --- 0x1bfa0: expand
    emu.run_func(0x1bfa0, args=(DST, SRC))
    got = bytes(emu.uc.mem_read(DST, 176))
    exp = expand(seed)
    print(f"[verify] expand (0x1bfa0): модель == исполнение: {got == exp}")
    if got != exp:
        for i in range(176):
            if got[i] != exp[i]:
                print(f"  первый расхождение @{i}: got={got[i]:02x} exp={exp[i]:02x}")
                break

    # --- 0x1dd8c: T
    blk = bytes.fromhex("de ad be ef 01 23 45 67 89 ab cd ef fe ed fa 5a")
    emu.uc.mem_write(BUF, blk)
    emu.run_func(0x1dd8c, args=(BUF,))
    got = bytes(emu.uc.mem_read(BUF, 16))
    exp = T(blk)
    print(f"[verify] T (0x1dd8c):      модель == исполнение: {got == exp}")
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
            print(f"[verify] xor win={win}: РАСХОЖДЕНИЕ")

    # --- 0x1a7ac: own_cipher
    emu.uc.mem_write(BUF, blk)
    emu.run_func(0x1a7ac, args=(BUF, CTX))
    got = bytes(emu.uc.mem_read(BUF, 16))
    exp = own_cipher(blk, ctx)
    print(f"[verify] own (0x1a7ac):    модель == исполнение: {got == exp}")
    if got != exp:
        print(f"  got: {got.hex()}")
        print(f"  exp: {exp.hex()}")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "model"
    if mode == "verify":
        verify()
    else:
        model()
