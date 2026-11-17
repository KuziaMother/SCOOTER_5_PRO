# -*- coding: utf-8 -*-
# ruff: noqa: F405  (имена из star-import от fv_core)
"""E2-batch54..56 (6566-7176)."""
from fv_core import *  # noqa: F401,F403
from fv_core import _fresh_call, _intercept  # noqa: F401
# --- E2-batch54: семейство Q16-интерполяторов + валидатор (reference-model, возврат через LR-sentinel) ---
_M32 = 0xFFFFFFFF

def _sxth(x):
    x &= 0xFFFF
    return x - 0x10000 if x >= 0x8000 else x

def _asr16(x):
    v = x & _M32
    v -= 0x100000000 if v >= 0x80000000 else 0
    return v >> 16

def _div16328(num, den):
    """0x16328: signed-деление (udiv |a|/|b|, trunc); den==0 -> +0x7fffffff/-0x80000000; overflow -> clamp."""
    if den == 0:
        return 0x7FFFFFFF if num >= 0 else -0x80000000
    sign = ((num ^ den) >> 31) & 1
    q = abs(num) // abs(den)
    if sign:
        return -q if q < 0x80000000 else -0x80000000
    return q if q < 0x7FFFFFFF else 0x7FFFFFFF

def _floor_idx(key, arr, hi):
    """последний i в [0,hi) с arr[i] <= key (сравнение — как в вызывающем: signed/unsigned)."""
    return max(i for i in range(hi) if arr[i] <= key)

def _s32(x):
    x &= _M32
    return x - 0x100000000 if x >= 0x80000000 else x

def _ref_e36c(a0, a1):
    # проверено эмпирически (b54): min/max — unsigned; diff — unsigned;
    # "max < 0x2710" — SIGNED (blt); min<0 — signed; div-ветка: num=min*0x2710 (u32),
    # den=0x2710-diff, res=div16328(num,den) с clamp в [-0x8000, 0x7FFF]; *out=sxth(res).
    # min/max — SIGNED (blt на 0xe376 проверено эмпирически: (1640,-335)->sxth(min))
    x, y = a0 & _M32, a1 & _M32
    xs, ys = _s32(x), _s32(y)
    mx, mn = (x, y) if xs >= ys else (y, x)
    diff = (mx - mn) & _M32
    if diff >= 0x2710:
        return 0
    if _s32(mx) < 0x2710:
        if _s32(mn) < 0:
            return _sxth(mn)
        res = _div16328((mn * 0x2710) & _M32, (0x2710 - diff) & _M32)
        if res > 0x7FFF:
            res = 0x7FFF
        elif res < -0x8000:
            res = -0x8000
        return _sxth(res)
    return _sxth(mx)

def _t_e36c(run, rng):
    from emulator.mcu_emu import RAM as _R
    out = 0x600
    for _ in range(25):
        a0 = rng.randint(-0x4000, 0x4000)
        a1 = rng.randint(-0x4000, 0x4000)
        run.call(0xE36C, args=(a0 & _M32, a1 & _M32, _R + out), max_insn=50000)
        exp = _ref_e36c(a0, a1)
        got = int.from_bytes(run.ram_read(out, 2), 'little')
        assert got == (exp & 0xFFFF), f'({a0},{a1}): *out={got:#x} want {exp & 0xFFFF:#x}'
t(0xE36C, 'E2-b54: 0xe36c fixed-point lerp с насыщением: diff>=0x2710->0; max(signed)>=0x2710->sxth(max); min<0->sxth(min); иначе div16328(min*0x2710, 0x2710-diff) clamp[-0x8000,0x7fff]')(_t_e36c)

def _ref_17306(key, arr, hi):
    if key < arr[0]:
        return 0, 0
    if arr[hi] <= key:
        return hi - 1, 0x10000
    idx = _floor_idx(key, arr, hi)
    diff = arr[idx + 1] - arr[idx]
    frac = 0 if diff == 0 else (((key - arr[idx]) << 16) & _M32) // diff & _M32
    return idx, frac

def _t_17306(run, rng):
    import struct as _st
    from emulator.mcu_emu import RAM as _R
    base, out = 0x400, 0xC00
    for _ in range(25):
        n = rng.randint(3, 12)
        arr = sorted(rng.randint(-20000, 20000) for _ in range(n))
        while len(set(arr)) < n:
            arr = sorted(rng.randint(-20000, 20000) for _ in range(n))
        hi = n - 1
        key = rng.randint(-32768, 32767)
        run.ram_write(base, _st.pack('<%dh' % n, *arr))
        r0, _ = run.call(0x17306, args=(key & _M32, _R + base, hi, _R + out), max_insn=50000)
        exp_idx, exp_frac = _ref_17306(key, arr, hi)
        assert r0 == exp_idx, f'key={key}: idx={r0} want {exp_idx}'
        got = int.from_bytes(run.ram_read(out, 4), 'little')
        assert got == exp_frac, f'key={key}: *out={got:#x} want {exp_frac:#x}'
t(0x17306, 'E2-b54: 0x17306 i16-интерполятор: r0=idx (bsearch floor), *u32=Q15.16 frac; key<arr[0]->(0,0); key>=arr[hi]->(hi-1,0x10000)')(_t_17306)

def _ref_1736a(key, arr, hi):
    if key < arr[0]:
        return 0, 0
    if arr[hi] <= key:
        return hi - 1, 0x10000
    idx = _floor_idx(key, arr, hi)
    diff = (arr[idx + 1] - arr[idx]) & _M32
    frac = 0 if diff == 0 else ((key - arr[idx]) * 0x10000 // diff) & _M32   # 0x161ea(num, den, 16)
    return idx, frac

def _t_1736a(run, rng):
    import struct as _st
    from emulator.mcu_emu import RAM as _R
    base, out = 0x400, 0xC00
    for _ in range(25):
        n = rng.randint(3, 12)
        arr = sorted(rng.randint(0, 0x40000) for _ in range(n))
        while len(set(arr)) < n:
            arr = sorted(rng.randint(0, 0x40000) for _ in range(n))
        hi = n - 1
        key = rng.randint(0, 0x50000)
        run.ram_write(base, _st.pack('<%dI' % n, *arr))
        r0, _ = run.call(0x1736A, args=(key, _R + base, hi, _R + out), max_insn=50000)
        exp_idx, exp_frac = _ref_1736a(key, arr, hi)
        assert r0 == exp_idx, f'key={key:#x}: idx={r0} want {exp_idx}'
        got = int.from_bytes(run.ram_read(out, 4), 'little')
        assert got == exp_frac, f'key={key:#x}: *out={got:#x} want {exp_frac:#x}'
t(0x1736A, 'E2-b54: 0x1736a u32-интерполятор (twin 0x17306): bsearch 0x1619e + frac=0x161ea(key-x0, dx, 16)')(_t_1736a)

def _ref_16aa2(key, arr, table, hi):
    # x-таблица: u16 (ldrh), ключ: u32 — сравнения unsigned; y-таблица: s16 (ldrsh).
    if not arr[0] < key:
        idx, frac = 0, 0
    elif arr[hi] <= key:
        idx, frac = hi - 1, 0x10000
    else:
        idx = _floor_idx(key, arr, hi)
        diff = arr[idx + 1] - arr[idx]
        frac = 0 if diff == 0 else ((key - arr[idx]) * 0x10000 // diff) & _M32   # udiv — точно
    t0, t1 = _sxth(table[idx]), _sxth(table[idx + 1])
    prod = (frac * (t1 - t0)) & _M32          # muls: signed low-32
    return _sxth((table[idx] & 0xFFFF) + _asr16(prod))

def _t_16aa2(run, rng):
    import struct as _st
    from emulator.mcu_emu import RAM as _R
    xbase, ybase = 0x400, 0x800
    for _ in range(25):
        n = rng.randint(3, 12)
        arr = sorted(rng.randint(0, 0xFFFF) for _ in range(n))
        while len(set(arr)) < n:
            arr = sorted(rng.randint(0, 0xFFFF) for _ in range(n))
        table = [rng.randint(-32768, 32767) for _ in range(n + 1)]
        hi = n - 1
        key = rng.randint(0, 0xFFFF)
        run.ram_write(xbase, _st.pack('<%dH' % n, *arr))
        run.ram_write(ybase, _st.pack('<%dh' % (n + 1), *table))
        r0, _ = run.call(0x16AA2, args=(key & _M32, _R + xbase, _R + ybase, hi), max_insn=50000)
        exp = _ref_16aa2(key, arr, table, hi)
        got = _sxth(r0)
        assert got == exp, f'key={key}: r0={got} want {exp}'
t(0x16AA2, 'E2-b54: 0x16aa2 u16-ключ/u16-x-таблица -> s16-таблица: bsearch(unsigned) + lerp frac*(t1-t0) asr16, sxth')(_t_16aa2)

def _ref_table_interp(key, arr, table, hi, signed):
    if signed:
        below = key < arr[0]
        above = arr[hi] <= key
        idx = _floor_idx(key, arr, hi) if not (below or above) else (0 if below else hi - 1)
        num = (key - arr[idx]) & _M32
    else:
        below = key < arr[0]
        above = arr[hi] <= key
        idx = _floor_idx(key, arr, hi) if not (below or above) else (0 if below else hi - 1)
        num = (key - arr[idx]) & _M32
    if below:
        idx, frac = 0, 0
    elif above:
        idx, frac = hi - 1, 0x10000
    else:
        diff = (arr[idx + 1] - arr[idx]) & _M32
        # 0x161ea — shift-and-subtract: ТОЧНЫЙ floor((key-arr[idx])*2^16/dx) без u32-wrap числителя
        frac = 0 if diff == 0 else ((key - arr[idx]) * 0x10000 // diff) & _M32
    t0, t1 = table[idx] & 0xFFFF, table[idx + 1] & 0xFFFF
    if t0 <= t1:
        return (t0 + ((frac * (t1 - t0)) >> 16)) & 0xFFFF
    return (t0 - ((frac * (t0 - t1)) >> 16)) & 0xFFFF

def _mk_table_interp(off, signed):
    def _test(run, rng):
        import struct as _st
        from emulator.mcu_emu import RAM as _R
        xbase, ybase = 0x400, 0x800
        for _ in range(25):
            n = rng.randint(3, 12)
            lo, hi_v = (-20000, 20000) if signed else (0, 0x40000)
            arr = sorted(rng.randint(lo, hi_v) for _ in range(n))
            while len(set(arr)) < n:
                arr = sorted(rng.randint(lo, hi_v) for _ in range(n))
            table = [rng.randint(0, 0xFFFF) for _ in range(n + 1)]
            hi = n - 1
            krange = (-32768, 32767) if signed else (0, 0x50000)
            key = rng.randint(*krange)
            fmt = 'i' if signed else 'I'
            run.ram_write(xbase, _st.pack('<%d%s' % (n, fmt), *arr))
            run.ram_write(ybase, _st.pack('<%dH' % (n + 1), *table))
            r0, _ = run.call(off, args=(key & _M32, _R + xbase, _R + ybase, hi), max_insn=50000)
            exp = _ref_table_interp(key, arr, table, hi, signed)
            got = r0 & 0xFFFF
            assert got == exp, f'key={key:#x}: r0={got:#x} want {exp:#x}'
    return _test

_t_169f0 = _mk_table_interp(0x169F0, False)
t(0x169F0, 'E2-b54: 0x169f0 u32-ключ -> u16-таблица: bsearch + Q16-lerp (ветки asc/desc), r0=u16')(_t_169f0)
def _t_16b22(run, rng):
    # «signed twin» по каталогу, НО эмпирически сравнения — unsigned (проверено:
    # arr=[-5000,5000]: key=-4999/-1000 -> t1, key=-12418/0/5000/5001 -> t0) —
    # контракт идентичен 0x169f0. Тестируем весь u32-диапазон ключей (включая >0x80000000).
    import struct as _st
    from emulator.mcu_emu import RAM as _R
    xbase, ybase = 0x400, 0x800
    for _ in range(25):
        n = rng.randint(3, 12)
        arr = sorted(rng.randint(0, 0x400000) for _ in range(n))
        while len(set(arr)) < n:
            arr = sorted(rng.randint(0, 0x400000) for _ in range(n))
        table = [rng.randint(0, 0xFFFF) for _ in range(n + 1)]
        hi = n - 1
        key = rng.randint(0, 0xFFFFFFFF)
        run.ram_write(xbase, _st.pack('<%dI' % n, *arr))
        run.ram_write(ybase, _st.pack('<%dH' % (n + 1), *table))
        r0, _ = run.call(0x16B22, args=(key, _R + xbase, _R + ybase, hi), max_insn=50000)
        exp = _ref_table_interp(key, arr, table, hi, False)
        got = r0 & 0xFFFF
        assert got == exp, f'key={key:#x}: r0={got:#x} want {exp:#x}'
t(0x16B22, 'E2-b54: 0x16b22 u32-ключ -> u16-таблица (twin 0x169f0; эмпирически unsigned-контракт на всём u32), r0=u16')(_t_16b22)

def _t_1647c(run, rng):
    # валидатор: a∈[1,0xc] && b∈[1,0x1f] && c<=0x17 -> bl 0x16410(id,a,b)
    # (id проверок не ограничивает — эмпирически ни один id из [0..0xbbb], 0x1000,
    #  0x10000, 0x80000000, 0xffffffff не отклонён; r3 в bl не передаётся)
    cap, _ = _intercept(0x1647C, 0x16410, max_insn=30000, args=(0xC00, 5, 0x10, 3))
    assert cap and cap.get('r0') == 0xC00 and cap.get('r1') == 5 and cap.get('r2') == 0x10, \
        f'args={cap} want (0xc00,5,0x10)'
    for good in ((0, 1, 1, 0), (0xBB8, 0xC, 0x1F, 0x17), (0xFFFFFFFF, 5, 0x10, 3)):
        cap, _ = _intercept(0x1647C, 0x16410, max_insn=30000, args=good)
        assert cap, f'{good}: bl 0x16410 not reached'
    for bad in ((0xC00, 0, 0x10, 3), (0xC00, 0xD, 0x10, 3),
                (0xC00, 5, 0, 3), (0xC00, 5, 0x20, 3), (0xC00, 5, 0x10, 0x18)):
        cap, _ = _intercept(0x1647C, 0x16410, max_insn=30000, args=bad)
        assert not cap, f'{bad}: bl 0x16410 reached with invalid args'
t(0x1647C, 'E2-b54: 0x1647c валидатор: a∈[1,0xc] && b∈[1,0x1f] && c<=0x17 -> bl 0x16410(id,a,b); id не ограничивает (эмпирически)')(_t_1647c)

# --- E2-batch55: чистые compute-функции (reference-model) + табличные поиски ---
def _sdiv(a, b):
    """ARM SDIV: signed-деление с усечением к нулю."""
    q = abs(a) // abs(b)
    return -q if (a < 0) != (b < 0) else q

def _t_506a(run, rng):
    # bubble sort u16: n проходов, i от n-k-1 вниз до 0, swap если buf[i] > buf[i+1] (unsigned);
    # ЧИТАЕТ buf[n] (один элемент за концом!) — caller обязан дать n+1 слотов (эмпирически).
    import struct as _st
    from emulator.mcu_emu import RAM as _R
    for _ in range(20):
        n = rng.randint(2, 12)
        data = [rng.randint(0, 0xFFFF) for _ in range(n + 1)]
        run.ram_write(0x400, _st.pack('<%dH' % (n + 1), *data))
        run.call(0x506A, args=(_R + 0x400, n), max_insn=30000)
        buf = data[:]
        for k in range(n):
            for i in range(n - k - 1, -1, -1):
                if buf[i] > buf[i + 1]:
                    buf[i], buf[i + 1] = buf[i + 1], buf[i]
        got = list(_st.unpack('<%dH' % (n + 1), run.ram_read(0x400, 2 * (n + 1))))
        assert got == buf, f'n={n}: {got} want {buf}'
t(0x506A, 'E2-b55: 0x506a bubble sort u16 (n проходов, читает buf[n] — нужен n+1 слот)')(_t_506a)

def _ref_50b0(buf, data, n):
    # 0x50b0 (эмпирически): СРАВНЕНИЯ min/max — по байтам БУФ-АРГУМЕНТА (s8);
    # значения при обновлении + суммирование — из ФИКСИРОВАННОГО буфера RAM+0x44 (pool-литерал).
    # mn=mx=s8(buf[0]); r8=ip=1; sum=0 (sxth-накопление s8(data[i]));
    # if s8(buf[i]) > mx: mx=s8(data[i]), ip=i+1;  if s8(buf[i]) < mn: mn=s8(data[i]), r8=i+1
    # out = {s8(sdiv(sum,n)), mn, mx, r8, ip}
    def _s8(b):
        return b - 0x100 if b >= 0x80 else b
    mn = mx = _s8(buf[0])
    r8 = ip = 1
    s = 0
    for i in range(n):
        cv, dv = _s8(buf[i]), _s8(data[i])
        if cv > mx:
            mx, ip = dv, (i + 1) & 0xFF
        if cv < mn:
            mn, r8 = dv, (i + 1) & 0xFF
        s = _sxth(s + dv)
    return [(_sdiv(s, n) & 0xFF), mn & 0xFF, mx & 0xFF, r8, ip]

def _t_50b0(run, rng):
    from emulator.mcu_emu import RAM as _R
    for _ in range(20):
        n = rng.randint(1, 40)
        buf = bytes(rng.randint(0, 0xFF) for _ in range(n))
        data = bytes(rng.randint(0, 0xFF) for _ in range(n))
        run.ram_write(0x44, data)
        run.ram_write(0x500, buf)
        run.call(0x50B0, args=(_R + 0x500, n, _R + 0x600), max_insn=30000)
        got = list(run.ram_read(0x600, 5))
        exp = _ref_50b0(buf, data, n)
        assert got == exp, f'n={n} buf0={buf[0]:#x}: {got} want {exp}'
t(0x50B0, 'E2-b55: 0x50b0 byte-stats: сравнения по s8(buf[i]), значения/сумма из фикс. RAM+0x44; out={s8(sdiv(sum,n)),min,max,last_min+1,last_max+1}, init=s8(buf[0])')(_t_50b0)

def _ref_rle(src, max_out):
    # RLE-токен (эмпирически, оба декодера идентичны по формату):
    # h: lit = h&7 (0 -> extended-байт), КОПИРУЕТСЯ lit-1 литералов (pre-decrement цикл);
    # lf = h>>4 логически (0 -> extended); bit3(h): backward (offset-байт, count=lf+2 от dst-offset)
    # иначе lf нулей. Порядок: h, [lit-ext], [lf-ext], литералы, [off].
    out = bytearray()
    p = 0
    while len(out) < max_out:
        h = src[p]; p += 1
        lit = h & 7
        if lit == 0:
            lit = src[p]; p += 1
        lf = h >> 4
        if lf == 0:
            lf = src[p]; p += 1
        for _ in range(lit - 1):
            out.append(src[p]); p += 1
        if (h >> 3) & 1:
            offv = src[p]; p += 1
            back = len(out) - offv
            for _ in range(lf + 2):
                out.append(out[back]); back += 1
        else:
            out.extend(b'\x00' * lf)
    return bytes(out[:max_out])

def _mk_rle(off):
    def _test(run, rng):
        from emulator.mcu_emu import RAM as _R
        for _ in range(15):
            max_out = rng.randint(8, 64)
            src = bytearray()
            out = bytearray()
            while len(out) < max_out:
                L = rng.randint(0, 20)      # желаемое число литералов
                LF = rng.randint(0, 20)     # len-поле (нули или backward count-2)
                B = rng.getrandbits(1)
                if L == 0 and LF == 0:      # гарантия прогресса токена
                    LF = 2
                if B and len(out) == 0:     # backward требует >=1 байт в out
                    L = 1
                # lit-поле: 3 бита = L+1 (1..7), 0 -> extended-байт = L+1
                if L <= 6:
                    lit_field, lit_ext = L + 1, None
                else:
                    lit_field, lit_ext = 0, L + 1
                # len-поле: 4 бита = LF (1..15), 0 -> extended-байт = LF
                if 1 <= LF <= 15:
                    lf_field, lf_ext = LF, None
                else:
                    lf_field, lf_ext = 0, LF
                h = (B << 3) | (lf_field << 4) | lit_field
                src.append(h)
                if lit_ext is not None:
                    src.append(lit_ext)
                if lf_ext is not None:
                    src.append(lf_ext)
                for _ in range(L):
                    out.append(rng.randint(0, 0xFF))
                    src.append(out[-1])
                if B:
                    offv = rng.randint(1, max(1, len(out)))
                    src.append(offv)
                    back = len(out) - offv
                    for _ in range(LF + 2):
                        out.append(out[back]); back += 1
                else:
                    out.extend(b'\x00' * LF)
            run.ram_write(0x400, bytes(src))
            run.ram_write(0xC00, bytes(max_out))
            run.call(off, args=(_R + 0x400, _R + 0xC00, max_out), max_insn=50000)
            got = run.ram_read(0xC00, max_out)
            exp = _ref_rle(bytes(src), max_out)
            assert got == exp, f'max_out={max_out}: {got.hex()} want {exp.hex()}'
    return _test

_t_152a = _mk_rle(0x152A)
t(0x152A, 'E2-b55: 0x152a RLE-декодер: lit=h&7 (0->ext), count=lit-1; lf=h>>4 (0->ext); bit3=backward(off,count=lf+2) иначе lf нулей')(_t_152a)
_t_1a24c = _mk_rle(0x1A24C)
t(0x1A24C, 'E2-b55: 0x1a24c RLE-декодер #2 (твин 0x152a, формат токена идентичен)')(_t_1a24c)

def _mk_tbl_search(off, tbl_off, n_entries, out_off):
    def _test(run, rng):
        import struct as _st
        from emulator.mcu_emu import RAM as _R
        for _ in range(15):
            keys = [rng.randint(0, 0xFF) for _ in range(n_entries)]
            entries = b''.join(_st.pack('<IB3x', rng.randint(0, 0x10000), k) for k in keys)
            run.ram_write(tbl_off, entries)
            key = rng.choice(keys + [rng.randint(0, 0xFF)])
            r0, _ = run.call(off, args=(key, _R + out_off), max_insn=30000)
            exp_i = next((i for i in range(n_entries) if keys[i] == key), None)
            exp_r0 = (_R + tbl_off + exp_i * 8) if exp_i is not None else 0
            assert r0 == exp_r0, f'key={key:#x}: r0={r0:#x} want {exp_r0:#x}'
            assert run.ram_read(out_off, 1)[0] == (1 if exp_i is not None else 0), \
                f'key={key:#x}: *out flag'
    return _test

_t_3994 = _mk_tbl_search(0x3994, 0x5CC, 58, 0x7A0)
t(0x3994, 'E2-b55: 0x3994 табличный поиск: 58×8B @RAM+0x5CC (..0x79B), match byte@+4 -> r0=указатель, *u8=1; out ОБЯЗАТЕЛЬНО вне таблицы (strb до скана!)')(_t_3994)
_t_583c = _mk_tbl_search(0x583C, 0x92C, 17, 0xA00)
t(0x583C, 'E2-b55: 0x583c табличный поиск (twin 0x3994): 17×8B @RAM+0x92C')(_t_583c)

def _t_befc(run, rng):
    # 2 записи @RAM+0x7C4: lo=byte@entry+4, hi=lo+byte@[u32@entry+8]; match: lo<=key<hi (эмпирически);
    # r0 = указатель на запись или 0, *u8 = флаг.
    import struct as _st
    from emulator.mcu_emu import RAM as _R
    for _ in range(15):
        e = []
        bounds = []
        for j in range(2):
            lo = rng.randint(0, 0x80)
            ln = rng.randint(1, 0x60)
            p = _R + 0x400 + j * 0x100
            run.ram_write(0x400 + j * 0x100 + 8, bytes([ln]))
            e.append(_st.pack('<IB3x', p, lo))
            bounds.append((lo, lo + ln))
        run.ram_write(0x7C4, b''.join(e))
        key = rng.randint(0, 0x120)
        r0, _ = run.call(0xBEFC, args=(key, _R + 0x600), max_insn=20000)
        exp_i = next((i for i in range(2) if bounds[i][0] <= key < bounds[i][1]), None)
        exp_r0 = (_R + 0x7C4 + exp_i * 8) if exp_i is not None else 0
        assert r0 == exp_r0, f'key={key}: r0={r0:#x} want {exp_r0:#x}'
        assert run.ram_read(0x600, 1)[0] == (1 if exp_i is not None else 0), f'key={key}: *out flag'
t(0xBEFC, 'E2-b55: 0xbefc range-поиск: 2 записи @RAM+0x7C4, [lo, lo+len) через u32-указатель -> r0=указатель')(_t_befc)

def _t_17524(run, rng):
    # boot-wait предикат: byte[RAM+0xFD3]>0x1E -> u32[RAM+8]=0, ret 0;
    # u32[RAM+8] < 0x10E0 -> ret 0; иначе u32[RAM+8]=0x10E0 (clamp), ret 1.
    from emulator.mcu_emu import RAM as _R
    cases = [(0, 0, 0, 0), (0, 4000, 0, 4000), (0, 0x10DF, 0, 0x10DF),
             (0, 0x10E0, 1, 0x10E0), (0, 9999, 1, 0x10E0),
             (0x1E, 5000, 1, 0x10E0), (0x1F, 5000, 0, 0), (0x80, 0x10E0, 0, 0),
             (0xFF, 7, 0, 0)]
    import struct as _st
    for b, v, exp_r0, exp_v in cases:
        run.ram_write(0xFD3, bytes([b]))
        run.ram_write(8, _st.pack('<I', v))
        r0, _ = run.call(0x17524, args=(), max_insn=20000)
        got_v = int.from_bytes(run.ram_read(8, 4), 'little')
        assert r0 == exp_r0, f'({b},{v}): r0={r0} want {exp_r0}'
        assert got_v == exp_v, f'({b},{v}): u32@8={got_v} want {exp_v}'
t(0x17524, 'E2-b55: 0x17524 boot-wait предикат: byte@FD3>0x1e->reset u32@8,ret0; u32@8<0x10e0->ret0; иначе clamp=0x10e0,ret1')(_t_17524)

# --- E2-batch56: чистые предикаты/флаги + stateful-счётчики (pool-литералы эмпирически) ---
def _ref_44c0(gate, u_lo, u_hi, s8a, s8b):
    # 0x44c0: ret1 <=> byte[A73]!=0 && u16[F9B]>0x7D0 && u16[F9D]<0x1194 && s8[FC8]>(-0x28) && s8[FC9]<0x64
    return 1 if (gate != 0 and u_lo > 0x7D0 and u_hi < 0x1194 and s8a > -0x28 and s8b < 0x64) else 0

def _t_44c0(run, rng):
    from emulator.mcu_emu import RAM as _R
    def _s8(b): return b - 0x100 if b >= 0x80 else b
    cases = [(rng.randint(0, 0xFF), rng.randint(0, 0xFFFF), rng.randint(0, 0x2000),
              rng.randint(0, 0xFF), rng.randint(0, 0xFF)) for _ in range(20)]
    cases += [(1, 0x7D1, 0x1193, -39 & 0xFF, 0x63),   # все границы pass
              (0, 0x800, 0, 0, 0),                    # gate=0
              (1, 0x7D0, 0, 0, 0),                    # lo==0x7D0 (не >)
              (1, 0x800, 0x1194, 0, 0),               # hi==0x1194 (не <)
              (1, 0x800, 0, -40 & 0xFF, 0),           # a==-0x28 (не >)
              (1, 0x800, 0, 0, 0x64)]                 # b==0x64 (не <)
    for g, lo, hi, a, b in cases:
        run.ram_write(0xA73, bytes([g]))
        run.ram_write(0xF9B, struct.pack('<H', lo))
        run.ram_write(0xF9D, struct.pack('<H', hi))
        run.ram_write(0xFC8, bytes([a & 0xFF]))
        run.ram_write(0xFC9, bytes([b & 0xFF]))
        r0, _ = run.call(0x44C0, args=(), max_insn=20000)
        exp = _ref_44c0(g, lo, hi, _s8(a), _s8(b))
        assert r0 == exp, f'g={g:#x} lo={lo:#x} hi={hi:#x} a={_s8(a)} b={_s8(b)}: r0={r0} want {exp}'
t(0x44C0, 'E2-b56: 0x44c0 предикат: byte@A73!=0 && u16@F9B>0x7d0 && u16@F9D<0x1194 && s8@FC8>-0x28 && s8@FC9<0x64 -> 1')(_t_44c0)

def _t_c4cc(run, rng):
    # 0xc4cc: REG=u32[PERIPH+0x21000]: сброс бит 0x10000|0x40000; arg==0x10000 -> |=0x10000;
    # arg==0x40000 -> |=0x50000 (оба бита!); иначе только сброс.
    from emulator.mcu_emu import PERIPH
    REG = PERIPH + 0x21000
    for _ in range(10):
        v = rng.randint(0, 0xFFFFFFFF)
        run.periph_write(REG, v)
        arg = rng.choice([0x10000, 0x40000, 0x10000, 0x40000, rng.randint(0, 0xFFFFFF)])
        r0, _ = run.call(0xC4CC, args=(arg,), max_insn=20000)
        e = v & ~0x10000 & ~0x40000
        if arg == 0x10000: e |= 0x10000
        elif arg == 0x40000: e |= 0x50000
        got = run.periph_read(REG)
        assert got == e, f'v={v:#x} arg={arg:#x}: {got:#x} want {e:#x}'
t(0xC4CC, 'E2-b56: 0xc4cc бит-флаги @PERIPH+0x21000: сброс 0x10000|0x40000; arg=0x10000->|=0x10000, arg=0x40000->|=0x50000')(_t_c4cc)

def _t_cc08(run, rng):
    # 0xcc08: u32[PERIPH+0x280C] &= ~0x80 (in-place, оба литерала один адрес)
    from emulator.mcu_emu import PERIPH
    REG = PERIPH + 0x280C
    for v in [0xFF, 0x80, 0x81, 0x7F, 0xFFFFFFFF, 0]:
        run.periph_write(REG, v)
        run.call(0xCC08, args=(), max_insn=20000)
        got = run.periph_read(REG)
        assert got == (v & ~0x80), f'v={v:#x}: {got:#x} want {v & ~0x80:#x}'
t(0xCC08, 'E2-b56: 0xcc08: u32[PERIPH+0x280C] &= ~0x80 (in-place)')(_t_cc08)

def _ref_cc68(arg, v2840, v2808, v280c):
    # 0xcc68: arg∈{0x20000,0x40000,0x80000}: r3 = ((u32[2840]>>16)&0xFF)!=0;
    # иначе r3 = u32[2808]&arg; r2 = u32[280C]&(arg>>4); ret = r3!=0 && (r2&0xFFFF)!=0
    if arg in (0x20000, 0x40000, 0x80000):
        r3 = 1 if ((v2840 >> 16) & 0xFF) else 0
    else:
        r3 = v2808 & arg
    r2 = v280c & (arg >> 4)
    return 1 if (r3 != 0 and (r2 & 0xFFFF) != 0) else 0

def _t_cc68(run, rng):
    from emulator.mcu_emu import PERIPH
    for _ in range(15):
        vA = rng.randint(0, 0xFFFFFFFF)
        vB = rng.randint(0, 0xFFFFFFFF)
        vC = rng.randint(0, 0xFFFFFFFF)
        run.periph_write(PERIPH + 0x2840, vA)
        run.periph_write(PERIPH + 0x2808, vB)
        run.periph_write(PERIPH + 0x280C, vC)
        arg = rng.choice([0x20000, 0x40000, 0x80000, 0x1, 0x3, rng.randint(0, 0xFFFF)])
        r0, _ = run.call(0xCC68, args=(arg,), max_insn=20000)
        exp = _ref_cc68(arg, vA, vB, vC)
        assert r0 == exp, f'arg={arg:#x} A={vA:#x} B={vB:#x} C={vC:#x}: r0={r0} want {exp}'
t(0xCC68, 'E2-b56: 0xcc68 канал-предикат: arg∈{2/4/8}0000 -> (u32@2840>>16)&0xff; иначе u32@2808&arg; && (u32@280C&(arg>>4))&0xffff')(_t_cc68)

def _t_18b0(run, rng):
    # 0x18b0: слияние struct(r0) <- src(r1): u32[s+4]=(old&0xFFF0FEFF)|src[0]<<8;
    # u32[s+8]=(old&0xFFF1F7FD)|(u32[src+4]|u32[src+8]|src[1]<<1); u32[s+0x2C]=(old&~0xF00000)|((src[0xC]-1)&0xFF)<<20
    from emulator.mcu_emu import RAM as _R
    for _ in range(15):
        old4, old8, old2c = (rng.randint(0, 0xFFFFFFFF) for _ in range(3))
        src = bytes(rng.randint(0, 0xFF) for _ in range(14))
        run.ram_write(0x404, struct.pack('<I', old4))
        run.ram_write(0x408, struct.pack('<I', old8))
        run.ram_write(0x42C, struct.pack('<I', old2c))
        run.ram_write(0x500, src)
        run.call(0x18B0, args=(_R + 0x400, _R + 0x500), max_insn=20000)
        e4 = (old4 & 0xFFF0FEFF) | (src[0] << 8)
        e8 = (old8 & 0xFFF1F7FD) | (int.from_bytes(src[4:8], 'little') | int.from_bytes(src[8:12], 'little') | (src[1] << 1))
        e2c = (old2c & ~0xF00000) | (((src[0xC] - 1) & 0xFF) << 20)
        g4 = struct.unpack('<I', run.ram_read(0x404, 4))[0]
        g8 = struct.unpack('<I', run.ram_read(0x408, 4))[0]
        g2c = struct.unpack('<I', run.ram_read(0x42C, 4))[0]
        assert (g4, g8, g2c) == (e4, e8, e2c), f'old=({old4:#x},{old8:#x},{old2c:#x}): got ({g4:#x},{g8:#x},{g2c:#x}) want ({e4:#x},{e8:#x},{e2c:#x})'
t(0x18B0, 'E2-b56: 0x18b0 struct-слияние: маски 0xFFF0FEFF/0xFFF1F7FD; поля +4/+8/+0x2C из src[0],src[1],u32[src+4|8],src[0xC]-1')(_t_18b0)

def _t_2d34(run, rng):
    # 0x2d34: u16[RAM+0xB5C] = max(v-1, 0) — все 4 pool-литерала один и тот же адрес (эмпирически)
    from emulator.mcu_emu import RAM as _R
    for v in [0, 1, 2, 3, 0xFFFF, 0x7FFF] + [rng.randint(0, 0xFFFF) for _ in range(10)]:
        run.ram_write(0xB5C, struct.pack('<H', v))
        run.call(0x2D34, args=(), max_insn=20000)
        got = struct.unpack('<H', run.ram_read(0xB5C, 2))[0]
        exp = max(v - 1, 0)
        assert got == exp, f'v={v:#x}: {got:#x} want {exp:#x}'
t(0x2D34, 'E2-b56: 0x2d34 saturating-decrement u16[RAM+0xB5C] = max(v-1, 0) (все литералы один адрес)')(_t_2d34)

def _ref_f304(pause, gate2, gate3, gate4, cnt):
    # 0xf304: pause=bit3(byte@F72) -> без изменений;
    # если bit0(byte@F71) или byte@80!=1 или u32@FBF<0x3E8 -> u16[A30]=0 (reset);
    # иначе u16+=1; при u16>=0x12C: toggle bit3(byte@F72), u16=0.
    if pause:
        return cnt, False
    if gate2 or gate3 != 1 or gate4 < 0x3E8:
        return 0, False
    c = (cnt + 1) & 0xFFFF
    if c >= 0x12C:
        return 0, True
    return c, False

def _t_f304(run, rng):
    from emulator.mcu_emu import RAM as _R
    for _ in range(15):
        pause = rng.getrandbits(1)
        g2 = rng.getrandbits(1)
        g3 = rng.randint(0, 3)          # byte@80 (==1 — pass)
        g4 = rng.choice([0, 0x3E7, 0x3E8, 0x400, 0xFFFFFFFF])
        cnt = rng.choice([0, 1, 0x12A, 0x12B, 0x12C, rng.randint(0, 0x200)])
        run.ram_write(0xF72, bytes([pause << 3]))
        run.ram_write(0xF71, bytes([g2]))
        run.ram_write(0x80, bytes([g3]))
        run.ram_write(0xFBF, struct.pack('<I', g4))
        run.ram_write(0xA30, struct.pack('<H', cnt))
        run.call(0xF304, args=(), max_insn=20000)
        e_cnt, toggled = _ref_f304(bool(pause), bool(g2), g3, g4, cnt)
        got_cnt = struct.unpack('<H', run.ram_read(0xA30, 2))[0]
        got_pause = (run.ram_read(0xF72, 1)[0] >> 3) & 1
        exp_pause = (pause ^ 1) if toggled else pause
        assert got_cnt == e_cnt, f'cnt={cnt:#x} g=({pause},{g2},{g3},{g4:#x}): {got_cnt:#x} want {e_cnt:#x}'
        assert got_pause == exp_pause, f'cnt={cnt:#x}: pause {got_pause} want {exp_pause}'
t(0xF304, 'E2-b56: 0xf304 gated-счётчик u16@A30: pause=bit3(byte@F72); reset при gate2/3/4 fail; +1; >=0x12c -> toggle bit3(F72)+reset')(_t_f304)

def _t_cbb8(run, rng):
    # 0xcbb8: REG=u32[PERIPH+0x280C]; если REG&0x40 -> ret1 (быстро);
    # иначе REG=0x80, спин до 0x2000 итераций ждёт REG&0x40, ret = (REG&0x40)!=0 (в эмуляторе 0)
    from emulator.mcu_emu import PERIPH
    REG = PERIPH + 0x280C
    for v in [0x40, 0x41, 0x1234, 0x540, 0]:
        run.periph_write(REG, v)
        r0, _ = run.call(0xCBB8, args=(), max_insn=120000)
        exp_r0 = 1 if (v & 0x40) else 0
        exp_reg = v if (v & 0x40) else 0x80
        got_reg = run.periph_read(REG)
        assert r0 == exp_r0, f'v={v:#x}: r0={r0} want {exp_r0}'
        assert got_reg == exp_reg, f'v={v:#x}: REG={got_reg:#x} want {exp_reg:#x}'
t(0xCBB8, 'E2-b56: 0xcbb8: u32@PERIPH+0x280C&0x40 -> ret1; иначе REG=0x80 + спин 0x2000 итераций, ret0')(_t_cbb8)
