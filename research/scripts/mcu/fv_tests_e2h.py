# -*- coding: utf-8 -*-
"""E2-b61..63 (8204-9459)."""
from fv_core import *  # noqa: F401,F403
from fv_core import _fresh_call, _intercept  # noqa: F401
# --- E2-b61: 8 функций (NVIC setter, retry-счётчик, bulk erase, TIM-init, clamp, TIM-reg update, mode setter, counter-каскад) ---

def _t_21b6c(run, rng):
    # 0x21b6c(r0): s32(r0) >= 0 → u32[0xE000E100] = 1 << (r0 & 31), ret = 1<<(r0&31)
    #              s32(r0) <  0 → запись нет, ret = r0
    for _ in range(12):
        if rng.getrandbits(1):
            r0 = rng.choice([0, 1, 5, 16, 31, 32, 33, 40, 0x1F, 0x7FFFFFFF,
                             rng.getrandbits(31)])
        else:
            r0 = rng.choice([0x80000000, 0x80000001, 0xFFFFFFFE, 0xFFFFFFFF,
                             (0x80000000 | rng.getrandbits(31))])
        init = rng.getrandbits(32)
        run.periph_write(0xE000E100, init)
        ret = run.call(0x21B6C, (r0,), max_insn=1000)
        got = run.periph_read(0xE000E100)
        if r0 < 0x80000000:
            exp = 1 << (r0 & 31)
            assert got == exp, f'r0={r0:#x}: E100={got:#x}, ждали {exp:#x}'
            assert ret[0] == exp, f'r0={r0:#x}: ret={ret[0]:#x} ≠ {exp:#x}'
        else:
            assert got == init, f'r0={r0:#x}: E100={got:#x} изменился (дали {init:#x})'
            assert ret[0] == r0, f'r0={r0:#x}: ret={ret[0]:#x} ≠ r0'

t(0x21B6C, 'E2-b61: 0x21b6c(r0) NVIC ISER0 setter: s32(r0)>=0 → u32[0xE000E100]=1<<(r0&31) (ret=значение), иначе skip+ret=r0')(_t_21b6c)


def _t_15ce0(run, rng):
    # 0x15ce0(): gate = byte[0xC7F]; counter = byte[0xC84]
    #   gate==0 → counter=0, быстрый возврат
    #   gate!=0 → counter++; counter<=2 → быстрый возврат
    #              counter==3 → bl 0xd878 + 0xdd80 (I2C-цепочка — спин в эмуляторе)
    for _ in range(10):
        gate = rng.choice([0, 0, 1, 2, rng.getrandbits(8)])
        if gate == 0:
            cnt = rng.getrandbits(8)
        else:
            cnt = rng.choice([0, 1, 2, rng.getrandbits(8)])
        run.ram_write(0xC7F, bytes([gate]))
        run.ram_write(0xC84, bytes([cnt]))
        run.call(0x15CE0, max_insn=5000)
        got = run.ram_read(0xC84, 1)[0]
        if gate == 0:
            assert got == 0, f'gate=0 cnt={cnt}: counter={got:#x} ≠ 0'
        elif cnt + 1 <= 2:
            assert got == cnt + 1, f'gate={gate} cnt={cnt}: counter={got:#x} ≠ {cnt+1}'
        else:
            assert got == (cnt + 1) & 0xFF, f'gate={gate} cnt={cnt}: counter={got:#x} ≠ {(cnt+1)&0xFF}'

t(0x15CE0, 'E2-b61: 0x15ce0() retry-счётчик: gate byte[0xC7F]==0 → 0xC84=0; иначе 0xC84++ (wrap), ≤2 → return, ==3 → bl 0xd878+0xdd80 (спин в эмуляторе)')(_t_15ce0)


def _t_7e70(run, rng):
    # 0x7e70(base, n): цикл i=0..n-1: ret = 0x7e98(base + i*0x800)
    #   0x7e98 в эмуляторе всегда возвращает 0 → при n>0 первый сектор → ret 0
    #   n==0 → цикл не выполняется → ret 1
    for _ in range(10):
        n = rng.choice([0, 0, 1, 2, 3, 5])
        if rng.getrandbits(1):
            base = 0x08003000 + rng.choice(range(0, 0x10000, 0x800))
        else:
            base = rng.getrandbits(32) & ~0x7FF
        ret = run.call(0x7E70, (base, n), max_insn=200000)
        if n == 0:
            assert ret[0] == 1, f'n=0: ret={ret[0]:#x} ≠ 1'
        else:
            assert ret[0] == 0, f'base={base:#x} n={n}: ret={ret[0]:#x} ≠ 0'

t(0x7E70, 'E2-b61: 0x7e70(base,n) bulk erase: n==0 → ret1; иначе 0x7e98(base+i*0x800) — в эмуляторе всегда 0 → ret0 после первого сектора')(_t_7e70)


def _t_22234(run, rng):
    # 0x22234(): bl 0x22994 (TIM2/clock init: u32[RAM+0x10]=0xFA0, +0x14=0x190, +0x18=0x28,
    #   SysTick RVR=0xFFFFFF/CVR/CTRL=5) → затем toggle-цикл P+0x21000 bit0x10 с
    #   задержками 0x22a0c — в эмуляторе 0x22994 зависает в задержке (CVR-poll),
    #   toggle-цикл не достигается; наблюдаемо = сайд-эффекты 0x22994 + спин.
    for _ in range(3):
        run.periph_write(0x40021000, rng.getrandbits(32))
        run.periph_write(0xE000E014, 0)
        run.periph_write(0xE000E018, 0)
        run.periph_write(0xE000E010, 0)
        run.call(0x22234, max_insn=30000)
        r10 = struct.unpack('<I', run.ram_read(0x10, 4))[0]
        r14 = struct.unpack('<I', run.ram_read(0x14, 4))[0]
        r18 = struct.unpack('<I', run.ram_read(0x18, 4))[0]
        assert r10 == 0xFA0, f'u32[0x10]={r10:#x} ≠ 0xfa0'
        assert r14 == 0x190, f'u32[0x14]={r14:#x} ≠ 0x190'
        assert r18 == 0x28, f'u32[0x18]={r18:#x} ≠ 0x28'
        assert run.periph_read(0xE000E014) == 0xFFFFFF, 'SysTick RVR ≠ 0xffffff'
        assert run.periph_read(0xE000E018) == 0xFFFFFF, 'SysTick CVR ≠ 0xffffff'
        assert run.periph_read(0xE000E010) == 0x5, f'SysTick CTRL={run.periph_read(0xE000E010):#x} ≠ 0x5'
        assert run.emu.insn == 30000, f'insn={run.emu.insn}: ожидался спин в задержке'

t(0x22234, 'E2-b61: 0x22234() TIM-init: bl 0x22994 (u32[0x10]=0xFA0/+0x14=0x190/+0x18=0x28, SysTick RVR/CVR=0xFFFFFF CTRL=5) → toggle-цикл P+0x21000 недостижим (спин в задержке 0x22994)')(_t_22234)


def _t_e704(run, rng):
    # 0xe704(): v = s32 u32[RAM+0x138A] (getter 0x1654c);
    #   v>=0 → |v| = v; v<0 → |v| = -v (v==-2^31 → 0x7FFFFFFF)
    #   |v| > 0xC8 → byte[RAM+0x1310] = 0, ret 0
    #   иначе ret = raw u32[0x138A]
    def ref(v):
        sv = v - 0x100000000 if v >= 0x80000000 else v
        if sv >= 0:
            av = sv
        elif sv == -0x80000000:
            av = 0x7FFFFFFF
        else:
            av = -sv
        clear = av > 0xC8
        return (0 if clear else v), clear
    for _ in range(12):
        if rng.getrandbits(1):
            v = rng.choice([0, 100, 200, 201, 0xFFFFFF9C, 0xFFFFFF38, 0xFFFFFF37,
                            0xFFFFFF36, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFF, 0x1F4])
        else:
            v = rng.getrandbits(32)
        init = rng.getrandbits(8)
        run.ram_write(0x1310, bytes([init]))
        run.ram_write(0x138A, struct.pack('<I', v))
        ret = run.call(0xE704, max_insn=50000)
        got = run.ram_read(0x1310, 1)[0]
        exp_ret, clear = ref(v)
        exp_byte = 0 if clear else init
        assert ret[0] == exp_ret, f'v={v:#x}: ret={ret[0]:#x} ≠ {exp_ret:#x}'
        assert got == exp_byte, f'v={v:#x}: byte[0x1310]={got:#x} ≠ {exp_byte:#x}'

t(0xE704, 'E2-b61: 0xe704() clamp: v=s32 u32[0x138A] (0x1654c); |v|>0xC8 → byte[0x1310]=0+ret0; иначе ret=raw (v==-2^31 → |v|=0x7FFFFFFF)')(_t_e704)


def _t_22e0c(run, rng):
    # 0x22e0c(base, args): CCMR1 [base+0x28] = (old & ~0x7300) | (k<<12)
    #   DIER [base+0x30]: &=~0x10; &=~0x20 | (j<<5)  (j = byte[args+8])
    #   base == 0x40012C00: ex=byte[args+9] ∈ {0,1} иначе cpsid+спин; &=~0x80|(ex<<7); &=~0x40
    #   base ∈ {0x40014000, 0x40014400, 0x40014800, 0x40014C00}: без ex-гейта (bits[7:5]=j)
    #   иначе: [base+0x48] = u32[args+4], return
    #   xc=byte[args+0xC] ∈ {0,1} иначе спин; xb=byte[args+0xB] ∈ {0,1} иначе спин
    #   [base+0x04] = (old & ~0xC00) | (xb<<10) | (xc<<11); [base+0x48] = u32[args+4]; ret = base
    VALID = (0x40014000, 0x40014400, 0x40014800, 0x40014C00)
    for _ in range(10):
        base = rng.choice([0x40012C00] + list(VALID) +
                          [0x40010000 + rng.choice(range(0, 0x2C00, 0x400))])
        k = rng.getrandbits(2)
        j = rng.getrandbits(3)
        ex = rng.choice([0, 1, 2, 3, 7])
        xb = rng.choice([0, 1, 2])
        xc = rng.choice([0, 1, 2])
        u32v = rng.getrandbits(16)
        old28 = rng.getrandbits(16)
        old30 = rng.getrandbits(8)
        old4 = rng.getrandbits(16)
        old48 = rng.getrandbits(32)
        run.periph_write(base + 0x28, old28)
        run.periph_write(base + 0x30, old30)
        run.periph_write(base + 0x04, old4)
        run.periph_write(base + 0x48, old48)
        s = bytearray(0x20)
        s[0] = k; s[4] = u32v & 0xFF; s[5] = (u32v >> 8) & 0xFF
        s[8] = j; s[9] = ex; s[0xB] = xb; s[0xC] = xc
        run.ram_write(0x1000, bytes(s))
        # модель
        ccmr1 = (old28 & ~0x7300) | ((k & 3) << 12)
        dier = (old30 & ~0x10) & ~0x20 | ((j & 7) << 5)
        spin = None
        if base == 0x40012C00:
            if ex not in (0, 1):
                spin = 'ex'
            else:
                dier = (dier & ~0x80) | ((ex & 1) << 7)
                dier &= ~0x40
        elif base not in VALID:
            run.call(0x22E0C, (base, 0x20001000), max_insn=2000)
            assert run.periph_read(base + 0x28) == ccmr1, f'invalid {base:#x}: CCMR1={run.periph_read(base + 0x28):#x} ≠ {ccmr1:#x}'
            assert run.periph_read(base + 0x30) == dier, f'invalid {base:#x}: DIER={run.periph_read(base + 0x30):#x} ≠ {dier:#x}'
            assert run.periph_read(base + 0x48) == u32v, f'invalid {base:#x}: +0x48={run.periph_read(base + 0x48):#x} ≠ {u32v:#x}'
            assert run.emu.insn < 2000, f'invalid {base:#x}: insn={run.emu.insn}'
            continue
        if spin is None and xc not in (0, 1):
            spin = 'xc'
        if spin is None and xb not in (0, 1):
            spin = 'xb'
        run.call(0x22E0C, (base, 0x20001000), max_insn=2000)
        assert run.periph_read(base + 0x28) == ccmr1, f'k={k} {base:#x}: CCMR1={run.periph_read(base + 0x28):#x} ≠ {ccmr1:#x}'
        assert run.periph_read(base + 0x30) == dier, f'j={j} ex={ex} {base:#x}: DIER={run.periph_read(base + 0x30):#x} ≠ {dier:#x}'
        if spin:
            assert run.emu.insn == 2000, f'spin={spin}: insn={run.emu.insn}'
        else:
            exp4 = (old4 & ~0xC00) | ((xb & 1) << 10) | ((xc & 1) << 11)
            assert run.periph_read(base + 0x04) == exp4, \
                f'xb={xb} xc={xc}: +0x4={run.periph_read(base + 0x04):#x} ≠ {exp4:#x}'
            assert run.periph_read(base + 0x48) == u32v, f'+0x48={run.periph_read(base + 0x48):#x} ≠ {u32v:#x}'
            assert run.emu.insn < 2000, f'не спин, а insn={run.emu.insn}'

t(0x22E0C, 'E2-b61: 0x22e0c(base,args) TIM-reg update: CCMR1=(old&~0x7300)|(k<<12); DIER: &=~0x10, &=~0x20|(j<<5); 0x40012C00: ex∈{0,1}+&=~0x80|(ex<<7)+&=~0x40; TIM5/6/7/8: без ex; иначе +0x48=u32[args+4]; xc/xb∈{0,1} (иначе спин); +0x4=(old&~0xC00)|(xb<<10)|(xc<<11)')(_t_22e0c)


def _t_17554(run, rng):
    # 0x17554(r0): r0 ∈ {0,1} → byte[RAM+0x11C] = r0; ret = r0
    for _ in range(10):
        if rng.getrandbits(1):
            a = rng.choice([0, 1])
        else:
            a = rng.choice([2, 3, 5, 0xFF, 0x100, 0x80000000, rng.getrandbits(32)])
        init = rng.getrandbits(8)
        run.ram_write(0x11C, bytes([init]))
        ret = run.call(0x17554, (a,), max_insn=1000)
        got = run.ram_read(0x11C, 1)[0]
        exp = a if a in (0, 1) else init
        assert got == exp, f'arg={a:#x}: byte[0x11C]={got:#x} ≠ {exp:#x}'
        assert ret[0] == (a & M32), f'arg={a:#x}: ret={ret[0]:#x} ≠ {a:#x}'

t(0x17554, 'E2-b61: 0x17554(r0) mode setter: r0 ∈ {0,1} → byte[0x11C]=r0; иначе нет записи; ret=r0')(_t_17554)


def _t_2186c(run, rng):
    # 0x2186c(): каскад счётчиков @RAM+0x2B0..0x2BA (u16b0=0 в тесте — 0x19968(0,·)=0)
    #   cnt=u16[0x2BA] < 1000 → ничего
    #   иначе cnt=0; c2=(b9+1)&FF; c2<0x3C → стоп
    #   b9=0; c3=(b8+1)&FF; c3<0x3C → стоп
    #   b8=0; c4=(b7+1)&FF; cap = 0x18 если b5==1 else 0x0C; c4<cap → стоп
    #   b7=0; дальше по b5/b6/b2 (см. модель)
    def ref(cnt, b9, b8, b7, b6, b5, b4, b3, b2):
        st = {'b9': b9, 'b8': b8, 'b7': b7, 'b6': b6, 'b4': b4, 'b3': b3, 'b2': b2}
        if cnt < 1000:
            return None
        st['b9'] = (b9 + 1) & 0xFF
        if st['b9'] < 0x3C:
            return st
        st['b9'] = 0
        st['b8'] = (b8 + 1) & 0xFF
        if st['b8'] < 0x3C:
            return st
        st['b8'] = 0
        st['b7'] = (b7 + 1) & 0xFF
        cap = 0x18 if b5 == 1 else 0x0C
        if st['b7'] < cap:
            return st
        st['b7'] = 0
        ip = (b4 + 1) & 0xFF
        r1b3 = (b3 + 1) & 0xFF
        r2b2 = (b2 + 1) & 0xFF
        if b5 == 1:
            st['b4'] = ip
            st['b3'] = r1b3 if r1b3 <= 7 else 1
            if b2 == 2:
                if ip > 0x1D:
                    st['b4'] = 1
                    st['b2'] = 3
                return st
            if b2 in (4, 6, 9, 0xB):
                if ip > 0x1E:
                    st['b4'] = 1
                    st['b2'] = r2b2
                if st['b2'] > 0xC:
                    st['b2'] = 1
                return st
            if ip > 0x1F:
                st['b4'] = 1
                st['b2'] = r2b2
            if st['b2'] > 0xC:
                st['b2'] = 1
            return st
        # b5 == 0
        st['b6'] = (b6 + 1) & 1
        if st['b6'] == 0:
            st['b4'] = ip
            st['b3'] = r1b3 if r1b3 <= 7 else 1
        if b2 == 2:
            if st['b4'] > 0x1D:
                st['b4'] = 1
                st['b2'] = 3
            return st
        if b2 in (4, 6, 9, 0xB):
            if st['b4'] > 0x1E:
                st['b4'] = 1
                st['b2'] = r2b2
            if st['b2'] > 0xC:
                st['b2'] = 1
            return st
        if st['b4'] > 0x1F:
            st['b4'] = 1
            st['b2'] = r2b2
        if st['b2'] > 0xC:
            st['b2'] = 1
        return st

    OFFS = {'b9': 0x2B9, 'b8': 0x2B8, 'b7': 0x2B7, 'b6': 0x2B6,
            'b5': 0x2B5, 'b4': 0x2B4, 'b3': 0x2B3, 'b2': 0x2B2}
    for _ in range(14):
        fam = rng.getrandbits(4)
        cnt = rng.choice([0, 500, 999, 1000, 63488, 0xFFFF]) if fam >= 2 else rng.choice([0, 999])
        b9 = rng.choice([0, 0x3B, 0x3C, 0xFF]) if fam >= 4 else rng.choice([0, 1])
        b8 = rng.choice([0, 0x3B, 0x3C]) if fam >= 6 else rng.choice([0, 1])
        b7 = rng.choice([0, 0xB, 0xC, 0x16, 0x17, 0x18]) if fam >= 8 else rng.choice([0, 0xB])
        b6 = rng.getrandbits(1)
        b5 = rng.getrandbits(1) if fam >= 10 else 0
        b4 = rng.choice([0, 1, 0x1C, 0x20]) if fam >= 12 else 0
        b3 = rng.choice([0, 6, 7, 8]) if fam >= 13 else 0
        b2 = rng.choice([0, 2, 4]) if fam >= 13 else 0
        seed = dict(b9=b9, b8=b8, b7=b7, b6=b6, b5=b5, b4=b4, b3=b3, b2=b2)
        run.ram_write(0x2BA, struct.pack('<H', cnt))
        for name, off in OFFS.items():
            run.ram_write(off, bytes([seed[name]]))
        run.ram_write(0x2B0, struct.pack('<H', 0))
        run.call(0x2186C, max_insn=50000)
        exp = ref(cnt, b9, b8, b7, b6, b5, b4, b3, b2)
        got_cnt = struct.unpack('<H', run.ram_read(0x2BA, 2))[0]
        if exp is None:
            assert got_cnt == cnt, f'cnt={cnt}: u16[0x2BA]={got_cnt:#x} изменился'
        else:
            assert got_cnt == 0, f'cnt={cnt}: u16[0x2BA]={got_cnt:#x} ≠ 0'
        for name, off in OFFS.items():
            g = run.ram_read(off, 1)[0]
            e = exp[name] if exp and name in exp else seed[name]
            assert g == e, f'{name}@0x{off:x}: {g:#x} ≠ {e:#x} (fam={fam} cnt={cnt} b9={b9:#x} b8={b8:#x} b7={b7:#x} b5={b5} b6={b6} b4={b4:#x} b3={b3:#x} b2={b2:#x})'
        assert run.emu.insn < 50000, f'insn={run.emu.insn}: спин?'

t(0x2186C, 'E2-b61: 0x2186c() counter-каскад: u16[0x2BA]≥1000 → =0, b9++(cap 0x3C), b8++(cap 0x3C), b7++(cap 0xC/0x18 по b5), далее b6-toggle/b4/b3-цепочка и b2-dispatch {2,4,6,9,0xB}')(_t_2186c)



# --- E2-b62: 8 функций (endianness, u16-getter, TIM-reg update #2, DIER-сеттер, timer dispatcher, TLV-парсер, флаг-хендлер, slew-лимитер) ---

def _t_5a68(run, rng):
    # 0x5a68(dst, src, width, size):
    #   sdiv(size, width); mls → остаток; остаток != 0 → ret 0 (без записей)
    #   width==1: bl 0x11a4(dst, src, size) — memcpy; ret 1
    #   width==2/4/8: разворот байтов в группах (BE-swap); ret 1
    #   иначе: ret 0
    def ref(src, width, size):
        if width != 0 and size % width != 0:
            return 0, None
        if width == 0:
            return 0, None
        if width == 1:
            return 1, bytes(src[:size])
        if width in (2, 4, 8):
            out = bytearray(size)
            for i in range(0, size, width):
                for j in range(width):
                    out[i + j] = src[i + width - 1 - j]
            return 1, bytes(out)
        return 0, None

    for _ in range(20):
        width = rng.choice([1, 1, 2, 2, 4, 4, 8, 3, 5, 0])
        if width in (1, 2, 4, 8) and rng.getrandbits(1) == 0:
            size = width * rng.randint(1, 16)
        else:
            size = rng.randint(0, 127)  # ≤128 (размер буферов)
        src = bytes(rng.getrandbits(8) for _ in range(128))
        run.ram_write(0x500, src)
        run.ram_write(0x600, b'\x55' * 128)
        ret = run.call(0x5A68, (0x20000600, 0x20000500, width, size), max_insn=20000)
        exp, expdata = ref(src, width, size)
        assert ret[0] == exp, f'width={width} size={size}: ret={ret[0]} ≠ {exp}'
        got = run.ram_read(0x600, 128)
        if exp == 1:
            assert got[:size] == expdata, f'width={width} size={size}: dst mismatch'
        else:
            assert got == b'\x55' * 128, f'width={width} size={size}: dst изменился'

t(0x5A68, 'E2-b62: 0x5a68(dst,src,width,size) endianness: size%width!=0 → ret0; width1 → memcpy (0x11a4); width2/4/8 → разворот групп; иначе ret0')(_t_5a68)


def _t_16504(run, rng):
    # 0x16504(): ret = u16[RAM+0x13AB] (pool 0x20001384 + 0x27)
    for _ in range(10):
        v = rng.getrandbits(16)
        run.ram_write(0x13AB, struct.pack('<H', v))
        ret = run.call(0x16504, max_insn=100)
        assert ret[0] == v, f'u16[0x13AB]={v:#x}: ret={ret[0]:#x}'

t(0x16504, 'E2-b61→b62: 0x16504() getter u16[RAM+0x13AB]')(_t_16504)


def _t_22edc(run, rng):
    # 0x22edc(base, args) — TIM-reg update (4 TIM-базы; остальные — общий хвост):
    #   общий (все базы): 0x2C = (v2c & ~0x73) | (byte[args] << 4)
    #     (bics 0x70; (>>2)<<2; bics 0x70; ldrb r3,[r1]; lsl 4; orr)
    #     0x30 = (v30 & ~0x100 & ~0x200) | ((byte[args+8] & 1) << 9)
    #   base == 0x40012C00: byte[args+9] ∉ {0,1} → спин (cpsid i); иначе
    #     0x30 = (… & ~0x800 | ((byte[args+9] & 1) << 11)) & ~0x400
    #   base ∈ {0x40012C00, 0x40014000, 0x40014400, 0x40014800}:
    #     byte[args+12] ∉ {0,1} → спин; byte[args+11] ∉ {0,1} → спин; иначе
    #     0x04 = (v4 & ~0x1000 | ((byte[args+11] & 1) << 12))
    #             & ~0x2000 | ((byte[args+12] & 1) << 13)
    #   хвост (все базы): [base+0x4C] = u32[args+4]; ret = base
    TIM = (0x40012C00, 0x40014000, 0x40014400, 0x40014800)
    for _ in range(10):
        spin = rng.getrandbits(1) == 0
        if spin:
            base = rng.choice(TIM)
            a8 = 0
            if base == 0x40012C00:
                a9 = 2 + rng.getrandbits(3)
                a11 = a12 = 0
            elif rng.getrandbits(1):
                a9 = 0
                a11 = 2 + rng.getrandbits(3)
                a12 = rng.choice([0, 1])
            else:
                a9 = 0
                a11 = rng.choice([0, 1])
                a12 = 2 + rng.getrandbits(3)
        else:
            base = rng.choice(TIM + (0x40000400, 0x40000800, 0x40000C00, 0x40013000,
                                     0x40013C00, 0x40000000, 0x40002800))
            a8 = a9 = 0
            a11 = a12 = rng.choice([0, 1])
        v30 = rng.getrandbits(32)
        v2c = rng.getrandbits(32)
        v4 = rng.getrandbits(32)
        a0 = rng.getrandbits(8)
        val = rng.getrandbits(32)
        run.periph_write(base + 0x30, v30)
        run.periph_write(base + 0x2C, v2c)
        run.periph_write(base + 4, v4)
        args = struct.pack('<4B', a0, 0, 0, 0) + struct.pack('<I', val)             + bytes([a8, a9]) + bytes([0, a11, a12])
        run.ram_write(0x400, args)
        ret = run.call(0x22EDC, (base, 0x20000400), max_insn=600)
        w30 = run.periph_read(base + 0x30)
        w2c = run.periph_read(base + 0x2C)
        exp2c = (v2c & ~0x73) | (a0 << 4)
        assert w2c == exp2c, f'base={base:#x}: 0x2C={w2c:#x} ≠ {exp2c:#x} (v2c={v2c:#x}, a0={a0})'
        if spin:
            assert run.emu.insn == 600, f'base={base:#x}: insn={run.emu.insn} (ожидали спин)'
            # до спина выполнены только общий блок 0x2C/0x30 (без 0x800/0x400)
            exp30 = (v30 & ~0x300) | ((a8 & 1) << 9)
            assert w30 == exp30, f'base={base:#x}: 0x30={w30:#x} ≠ {exp30:#x} (v30={v30:#x})'
        else:
            assert run.emu.insn < 600, f'base={base:#x}: insn={run.emu.insn} (ожидали возврат)'
            if base == 0x40012C00:
                exp30 = (v30 & ~0xF00) | ((a9 & 1) << 11)
            else:
                exp30 = (v30 & ~0x300)
            assert w30 == exp30, f'base={base:#x}: 0x30={w30:#x} ≠ {exp30:#x} (v30={v30:#x})'
            if base in TIM:
                exp4 = (((v4 & ~0x1000) | ((a11 & 1) << 12)) & ~0x2000) | ((a12 & 1) << 13)
                w4 = run.periph_read(base + 4)
                assert w4 == exp4, f'base={base:#x}: 0x04={w4:#x} ≠ {exp4:#x} (v4={v4:#x})'
            got = run.periph_read(base + 0x4C)
            assert got == val, f'base={base:#x}: 0x4C={got:#x} ≠ {val:#x}'
            assert ret[0] == base, f'base={base:#x}: ret={ret[0]:#x}'

t(0x22EDC, 'E2-b62: 0x22edc(base,args) TIM-reg: 0x2C=(v2c&~0x73)|(byte[args]<<4); 0x30=(v30&~0x300)|((a[8]&1)<<9); base 0x40012C00: a[9]∉{0,1}→спин, иначе 0x30=(..&~0xF00)|(a[9]&1)<<11; base∈{..C00,14000,14400,14800}: a[12]/a[11]∉{0,1}→спин, иначе 0x04=(v4&~0x1000|(a[11]<<12))&~0x2000|(a[12]<<13); все: +0x4C=u32[args+4], ret=base')(_t_22edc)


def _t_22c70(run, rng):
    # 0x22c70(struct_ptr, args): base = u32[struct]
    #   base ∉ {0x40012C00, 0x40014000..0x40014C00} → спин
    #   k=byte[args+2] ∉ {0..3} → спин; u32[args+4] > 0xFF → спин; byte[args+9] ∉ {0,1} → спин
    #   [base+0x54] = enc; byte[struct+0x1A] = 1; ret = struct_ptr
    #   enc: v = (v0 & 0xFFFF8000) | a0<<11 | a1<<10 | k<<8 | r6;
    #        v = (v&0xEFFF)|a8<<12; (v&0xDFFF)|ex<<13; (v&0xBFFF)|a10<<14
    def enc(v0, a0, a1, k, r6, a8, ex, a10):
        v = (v0 & 0xFFFF8000) | (a0 << 11) | (a1 << 10) | (k << 8) | (r6 & 0xFF)
        v = (v & 0xFFFFEFFF) | (a8 << 12)
        v = (v & 0xFFFFDFFF) | (ex << 13)
        v = (v & 0xFFFFBFFF) | (a10 << 14)
        return v & M32

    TIM5 = (0x40012C00, 0x40014000, 0x40014400, 0x40014800, 0x40014C00)
    for _ in range(12):
        base = rng.choice(TIM5 + (0x40013000,))
        a0, a1, a8, a10 = (rng.getrandbits(4) for _ in range(4))
        k = rng.choice([0, 1, 2, 3, 4, 5])
        r6 = rng.choice([0, 0xFF, rng.getrandbits(8), 0x100, 0x3FF])
        ex = rng.choice([0, 1, 2])
        v0 = rng.getrandbits(32)
        run.ram_write(0x300, struct.pack('<I', base))
        run.periph_write(base + 0x54, v0)
        run.ram_write(0x31A, bytes([0]))
        run.ram_write(0x400, struct.pack('<12B', a0, a1, k, 9, r6 & 0xFF, r6 >> 8,
                                         0, 0, a8, ex, a10, 0))
        ret = run.call(0x22C70, (0x20000300, 0x20000400), max_insn=400)
        if base not in TIM5 or k > 3 or r6 > 0xFF or ex > 1:
            assert run.emu.insn == 400, (f'base={base:#x} k={k} r6={r6:#x} ex={ex}: '
                                         f'insn={run.emu.insn} (ожидали спин)')
            continue
        got = run.periph_read(base + 0x54)
        exp = enc(v0, a0, a1, k, r6, a8, ex, a10)
        assert got == exp, (f'base={base:#x} a0={a0} a1={a1} k={k} r6={r6:#x} '
                            f'a8={a8} ex={ex} a10={a10:#x} v0={v0:#x}: 0x54={got:#x} ≠ {exp:#x}')
        assert run.ram_read(0x31A, 1)[0] == 1, f'byte[struct+0x1A] ≠ 1'
        assert ret[0] == 0x20000300, f'ret={ret[0]:#x}'

t(0x22C70, 'E2-b62: 0x22c70(ptr,args) DIER-сеттер: base∈{TIM4/5-8}, k∈{0..3}, r6≤0xFF, ex∈{0,1} (иначе спин); [base+0x54]=(v0&0xFFFF8000)|a0<<11|a1<<10|k<<8|r6, &0xEFFF|a8<<12, &0xDFFF|ex<<13, &0xBFFF|a10<<14; byte[struct+0x1A]=1')(_t_22c70)


def _t_23040(run, rng):
    # 0x23040(struct_ptr, args, mode): base = u32[struct]
    #   mode-наборы: 0x40012C00/0x40000400/0x40000800/0x40000C00/0x40000000: {0,1,2,4}
    #                0x40014000/0x40014400/0x40014800/0x40014C00: {0,1}
    #                иначе спин
    #   byte[args] ∈ {0..7}, byte[args+8] ∈ {0,1} (иначе спин)
    #   byte[struct+0x19] == 1 → ret 2 (без записей)
    #   иначе: +0x19=1, +0x1A=2; dispatch: 0→0x22d2c (+0x44), 1→0x22e0c (+0x48),
    #                2→0x22edc (+0x4C), 4→0x22fac (+0x50) — все копируют u32[args+4]
    #   финал: +0x1A=1, +0x19=0, ret 0
    FULL = (0x40012C00, 0x40000400, 0x40000800, 0x40000C00, 0x40000000)
    HALF = (0x40014000, 0x40014400, 0x40014800, 0x40014C00)
    TAIL = {0: 0x44, 1: 0x48, 2: 0x4C, 4: 0x50}

    def ok_mode(base, mode):
        if base in FULL:
            return mode in (0, 1, 2, 4)
        if base in HALF:
            return mode in (0, 1)
        return False

    for _ in range(14):
        base = rng.choice(FULL + HALF + (0x40013000,))
        if ok_mode(base, rng.getrandbits(2) * 2):
            mode = rng.choice([m for m in (0, 1, 2, 4) if ok_mode(base, m)] or [3])
        else:
            mode = rng.choice([0, 1, 2, 3, 4])
        a0 = rng.choice([0, 1, 7, 8, rng.getrandbits(8)])
        a8 = rng.choice([0, 1, 2])
        a19 = rng.choice([0, 1])
        val = rng.getrandbits(32)
        run.ram_write(0x300, struct.pack('<I', base))
        run.ram_write(0x319, bytes([a19]))
        # args: 16B, явные нули на [9]/[11]/[12] (калли 0x22d2c/0x22e0c/0x22edc
        # читают их и спят при ∉{0,1}; в shared-Run там мусор от других тестов)
        abuf = bytearray(16)
        abuf[0] = a0
        struct.pack_into('<I', abuf, 4, val)
        abuf[8] = a8
        run.ram_write(0x400, bytes(abuf))
        for o in range(0, 0x60, 4):
            run.periph_write(base + o, rng.getrandbits(32))
        ret = run.call(0x23040, (0x20000300, 0x20000400, mode), max_insn=2000)
        if not ok_mode(base, mode) or a0 > 7 or a8 > 1:
            assert run.emu.insn == 2000, (f'base={base:#x} mode={mode} a0={a0} a8={a8}: '
                                          f'insn={run.emu.insn} (ожидали спин)')
            continue
        if a19 == 1:
            assert ret[0] == 2, f'a19=1: ret={ret[0]} ≠ 2'
            assert run.emu.insn < 2000
            continue
        assert ret[0] == 0, f'base={base:#x} mode={mode}: ret={ret[0]} ≠ 0'
        assert run.ram_read(0x319, 1)[0] == 0, f'+0x19={run.ram_read(0x319,1)[0]} ≠ 0'
        assert run.ram_read(0x31A, 1)[0] == 1, f'+0x1A={run.ram_read(0x31A,1)[0]} ≠ 1'
        got = run.periph_read(base + TAIL[mode])
        assert got == val, (f'base={base:#x} mode={mode}: +{TAIL[mode]:#x}={got:#x} '
                            f'≠ {val:#x} (u32[args+4])')
        assert run.emu.insn < 2000

t(0x23040, 'E2-b62: 0x23040(ptr,args,mode) timer-dispatcher: base/mode-наборы {0,1,2,4}/{0,1}, byte[args]∈{0..7}, byte[args+8]∈{0,1} (иначе спин); +0x19==1 → ret2; иначе dispatch 0x22d2c/0x22e0c/0x22edc/0x22fac (копирование u32[args+4] в +0x44/48/4C/50), +0x19=0, +0x1A=1, ret0')(_t_23040)


def _t_15d14(run, rng):
    # 0x15d14(): A = RAM+0x1F10, B = RAM+0x1FAC
    #   byte[A+1] != 1 → byte[B+3] = 2; ret (0xC, 0); ничего другого
    #   byte[A+1] == 1 → (b10..b13 = A[0x10..0x13]):
    #     byte[B+3] = 2
    #     u16[B+0x0A] = (b10 << 5) | ((b11 >> 3) & 0x1F)   (13+5 бит)
    #     u16[B+0x10] = (b11 << 8) | b12
    #     byte[B+0x12] = b10
    #     byte[B+0x15] = b13
    #     ret (0x1C, 0xA); A не меняется
    A, B = 0x1F10, 0x1FAC
    for _ in range(15):
        status = rng.choice([0, 1, 1, 2, rng.getrandbits(8)])
        b13, b12, b11, b10 = (rng.getrandbits(8) for _ in range(4))
        buf = bytearray(0x40)
        buf[1] = status
        buf[0x13], buf[0x12], buf[0x11], buf[0x10] = b13, b12, b11, b10
        run.ram_write(A, bytes(buf))
        run.ram_write(0x1F98, bytes(0x60))
        ret = run.call(0x15D14, max_insn=20000)
        gb = run.ram_read(0x1F98, 0x60)
        gotA = run.ram_read(A, 0x40)
        assert gotA == bytes(buf), f'status={status}: A изменился'
        if status != 1:
            diffs = [(i, v) for i, v in enumerate(gb) if v]
            assert diffs == [(B + 3 - 0x1F98, 2)], f'status={status}: записи в B: {diffs}'
            assert ret[0] == 0xC and ret[1] == 0, f'status={status}: ret={ret[0]:#x},{ret[1]:#x}'
            continue
        assert ret[0] == 0x1C and ret[1] == 0xA, f'ret={ret[0]:#x},{ret[1]:#x} (ожид. 0x1C,0xA)'
        diffs = sorted((i, v) for i, v in enumerate(gb) if v)
        exp = [(B + 3 - 0x1F98, 2),
               (B + 0x0A - 0x1F98, (b10 << 5 | ((b11 >> 3) & 0x1F)) & 0xFF),
               (B + 0x0B - 0x1F98, (b10 << 5 | ((b11 >> 3) & 0x1F)) >> 8),
               (B + 0x10 - 0x1F98, b12),
               (B + 0x11 - 0x1F98, b11),
               (B + 0x12 - 0x1F98, b10),
               (B + 0x15 - 0x1F98, b13)]
        exp = [(i, v) for i, v in exp if v]
        assert diffs == exp, (f'b10={b10:#x} b11={b11:#x} b12={b12:#x} b13={b13:#x}: '
                              f'B: {diffs} ≠ {exp}')

t(0x15D14, 'E2-b62: 0x15d14() parser: A=RAM+0x1F10, B=RAM+0x1FAC; byte[A+1]!=1 → byte[B+3]=2+ret(0xC,0); иначе (b10..b13=A[0x10..0x13]): byte[B+3]=2, u16[B+0x0A]=(b10<<5)|((b11>>3)&0x1F), u16[B+0x10]=(b11<<8)|b12, B+0x12=b10, B+0x15=b13, ret(0x1C,0xA); A не трогается')(_t_15d14)


def _t_1395c(run, rng):
    # 0x1395c(): P1 = RAM+0xCAC (флаг), P2 = RAM+0xCB2 (счётчик), SRC = RAM+0xA73
    #   byte[P1] == 0 → возврат (без записей)
    #   byte[SRC] != 0 (bl 0x8af0) → P2=0, P1=0, bl 0x13c78(sp) — I2C-пакет (0x13ca0)
    #   byte[SRC] == 0 → P2++; P2 ≤ 5 → чистый возврат; P2 > 5 → P2=0, P1=0 + bl 0x13c78
    #   Детерминизм: ACK-эмуляция на 0x844E (r0=0); длина спина I2C зависит от
    #   накопленного состояния → проверяем визит 0x13ca0 (I2C-отправка), а не insn
    P1, P2, SRC = 0xCAC, 0xCB2, 0xA73
    for _ in range(8):
        p1 = rng.choice([0, 0, 1, rng.getrandbits(8)])
        src = rng.choice([0, 0, 1, rng.getrandbits(8)])
        p2 = rng.choice([0, 1, 3, 5, 6, rng.getrandbits(8)])
        run.periph_write(0x40013008, 3)
        state = {'i2c': False}
        def _ack(uc_, a, s, ud):
            aa = a & ~1
            if aa == 0x844E:
                uc_.reg_write(UC_ARM_REG_R0, 0)
            elif aa == 0x13CA0:
                state['i2c'] = True
        sh = run.uc.hook_add(UC_HOOK_CODE, _ack)
        run.ram_write(0x98, bytes(4))
        run.ram_write(P1, bytes([p1]))
        run.ram_write(P2, bytes([p2]))
        run.ram_write(SRC, bytes([src]))
        run.call(0x1395C, max_insn=50000)
        run.uc.hook_del(sh)
        gp1 = run.ram_read(P1, 1)[0]
        gp2 = run.ram_read(P2, 1)[0]
        if p1 == 0:
            assert gp1 == 0 and gp2 == p2, f'P1=0: P1={gp1} P2={gp2}'
            assert not state['i2c'], f'P1=0: I2C выполнен'
            continue
        if src != 0:
            assert gp1 == 0 and gp2 == 0, f'SRC={src}: P1={gp1} P2={gp2}'
            assert state['i2c'], f'SRC={src}: 0x13c78 не выполнен (insn={run.emu.insn})'
            continue
        if p2 + 1 <= 5:
            assert gp1 == p1 and gp2 == p2 + 1, f'P2={p2}: P1={gp1} P2={gp2}'
            assert not state['i2c'], f'P2={p2}: I2C выполнен'
        else:
            assert gp1 == 0 and gp2 == 0, f'P2={p2}: P1={gp1} P2={gp2}'
            assert state['i2c'], f'P2={p2}: 0x13c78 не выполнен (insn={run.emu.insn})'

t(0x1395C, 'E2-b62: 0x1395c() флаг-хендлер: byte[0xCAC]==0 → ret; byte[0xA73]!=0 → 0xCB2=0,0xCAC=0 + 0x13c78 (I2C-пакет); иначе 0xCB2++ (≤5 чистый возврат, >5 → сброс + 0x13c78); ACK-эмуляция на 0x844E')(_t_1395c)


def _t_e408(run, rng):
    # 0xe408(a0..a3 + стек a4, a5): slew-лимитер (ramp-контроллер)
    #   t=s16(a0), mn=s16(a1), rate=s16(a2), sb=s16(a3); push 48B (12 рег.)
    #   u32[SP0+0]=below (источник fp), u32[SP0+4]=a4 (sl, ptr выходного u16),
    #   u32[SP0+8]=a5 (ptr байта)
    #   sb>0 и t<mn: direction-флаг buf8=1 (fp не применяется, *a5 не трогается)
    #   sb≤0 и t>mn: ветка B: d=t-mn; sb>-0x14 → buf8=1; иначе d<0→7, d<9→1, d<0xC8→2,
    #     d<0x190→3, else 7; fp=s16(u32[below]//10); buf8=max(buf8,fp)
    #   иначе (sb≤0&t≤mn или sb>0&t≥mn): ветка C: cnt_new=(byte[*a5]+(rate≠0))&0xFF;
    #     f=(cnt_new%3==0); *a5=cnt_new; buf8=f
    #   хвост: out=s16(rate*buf8+t); t≥0x64 → out=max(out,0x64) (signed);
    #     res=clamp(out,[0,0x2710]); *a4=res (u16); ret=res
    def s16(v):
        v &= 0xFFFF
        return v - 0x10000 if v >= 0x8000 else v

    def sat_s16(x):
        if x > 0x7FFF:
            return 0x7FFF
        if x < -0x8000:
            return -1
        return x

    def ref(t, mn, rate, sb, below, cnt0):
        if sb > 0 and t < mn:
            # флаг-ветка: buf8 по sb и r4=s16(mn-t): sb<0x14→1; 0x14≤sb: r4<9→1,
            # r4<0x32→2, else 5; out=sat(sat(rate*buf8)+t); out=max(out,mn);
            # t>9940→out=t; elif out>9940→9940
            r4 = s16(mn - t)
            if sb < 0x14:
                buf8 = 1
            elif r4 < 9:
                buf8 = 1
            elif r4 < 0x32:
                buf8 = 2
            else:
                buf8 = 5
            cnt = cnt0
            out = sat_s16(sat_s16(rate * buf8) + t)
            if out >= mn:
                out = mn
            if t > 9940:
                out = t
            elif out > 9940:
                out = 9940
        elif sb < 0 and t > mn:
            # ветка B: d=s16(t-mn); d<0→|d| (clamp 0x7FFF); sb>-0x14→1;
            # |d|<9→1, <0xC8→2, <0x190→3, else 7; fp=s16(u32[b]//10); buf8=max
            # out=s16(rate*buf8+t); out=max(out,mn); u16; t≥0x64→u16=max(u16,0x64)
            d = s16(t - mn)
            if d < 0:
                d = 0x7FFF if -d >= 0x8000 else -d
            if sb > -0x14:
                buf8 = 1
            elif d < 9:
                buf8 = 1
            elif d < 0xC8:
                buf8 = 2
            elif d < 0x190:
                buf8 = 3
            else:
                buf8 = 7
            fp = s16((below // 10) & 0xFFFF)
            if buf8 < fp:
                buf8 = fp
            cnt = cnt0
            out = s16((rate * buf8 + t) & 0xFFFFFFFF)
            if out <= mn:
                out = mn
            u = out & 0xFFFF
            if t >= 0x64 and u < 0x64:
                u = 0x64
            out = s16(u)
        else:
            # ветка C: cnt_new=byte[*a5]+(rate≠0); f=cnt_new%3==0; *a5=cnt_new
            # out=sat_s16(f*rate+t); t≥0x64 и out<0x64 → 0x64 (bypass 9940);
            # иначе блок 9940: t>9940→t; out>9940→9940; out≤0→0
            inc = 1 if rate != 0 else 0
            cnt = (cnt0 + inc) & 0xFF
            f = 1 if cnt % 3 == 0 else 0
            out = sat_s16(f * rate + t)
            if t >= 0x64 and out < 0x64:
                out = 0x64
            else:
                if t > 9940:
                    out = t
                elif out > 9940:
                    out = 9940
                elif out <= 0:
                    out = 0
        res = 0x2710 if out > 0x2710 else (0 if out < 0 else out)
        return res, cnt


    OUT, CNT = 0x1357, 0xFD3
    S0 = STACK_TOP - RAM
    for _ in range(24):
        a0 = rng.getrandbits(16)
        a1 = rng.getrandbits(16)
        sb = rng.choice([1, 2, 0x10, 0, -1, -0x13, -0x14, -0x15,
                         -rng.getrandbits(8), rng.getrandbits(8),
                         rng.getrandbits(16)])
        a2 = rng.choice([0, 1, 3, 10, rng.getrandbits(8),
                         -rng.getrandbits(8), rng.getrandbits(16)])
        below = rng.getrandbits(32)
        cnt0 = rng.getrandbits(8)
        run.ram_write(S0, struct.pack('<I', below))
        run.ram_write(S0 + 4, struct.pack('<I', RAM + OUT))
        run.ram_write(S0 + 8, struct.pack('<I', RAM + CNT))
        run.ram_write(OUT, bytes(2))
        run.ram_write(CNT, bytes([cnt0]))
        # аргументы — sign-extended s16 (реальная конвенция вызова: ldrsh/movs
        # из 16-битных полей); raw-u16 меняет поведение 32-битных cmp до sxth
        t, mn, rate, sb16 = s16(a0), s16(a1), s16(a2), s16(sb)
        ret = run.call(0xE408, (t, mn, rate, sb16), max_insn=5000)
        exp, expc = ref(t, mn, rate, sb16, below, cnt0)
        got = struct.unpack('<H', run.ram_read(OUT, 2))[0]
        gotc = run.ram_read(CNT, 1)[0]
        assert ret[0] == exp, (f'a0={t} a1={mn} a2={rate} sb={sb16} below={below:#x} c={cnt0}: '
                               f'ret={ret[0]:#x} ≠ {exp:#x}')
        assert got == exp, (f'a0={t} a1={mn} a2={rate} sb={sb16} below={below:#x}: '
                            f'u16[out]={got:#x} ≠ {exp:#x}')
        assert gotc == expc, (f'a0={t} a1={mn} a2={rate} sb={sb16} below={below:#x} c={cnt0}: '
                              f'byte[cnt]={gotc} ≠ {expc}')

t(0xE408, 'E2-b62: 0xe408(t,mn,rate,sb + стек [SP0+0]=below fp-src, [SP0+4]=a4 out-u16 ptr, [SP0+8]=a5 byte ptr): sb>0&t<mn → флаг: buf8(sb<0x14→1; r4=s16(mn-t): <9→1, <0x32→2, else 5), out=sat(sat(rate*buf8)+t), out=max(out,mn), t>9940→t/else cap 9940; sb<0&t>mn → B: d=|s16(t-mn)|, sb>-0x14→1/д<9→1/д<0xC8→2/д<0x190→3/else 7, fp=s16(u32[b]//10), out=s16(rate*buf8+t), out=max(out,mn), u16, t≥0x64→max(u16,0x64); else → C: cnt_new=byte[*a5]+(rate≠0), f=cnt%3==0, *a5=cnt_new, out=sat(f*rate+t); t≥0x64: out<0x64→0x64; t<0x64: out>9940→9940/≤0→0; res=clamp[0,0x2710], *a4=res, ret=res')(_t_e408)



def _cleanc(run):
    """чистый возврат: LR-sentinel даёт FETCH_UNMAPPED — это норма для run.call()"""
    le = run.last_error
    assert le in (None, 'Invalid memory fetch (UC_ERR_FETCH_UNMAPPED)'), le

# --- E2-b63: 8 функций (WWDG CFR/CR-декодеры, threshold #5, threshold-счётчик #2, signed fixed-point, double bsearch u32/u16, u16-бит setter) ---

def _t_cc1c(run, rng):
    """0xcc1c(mode, out*): v=u32[0x40002804]&0x00FFFF3F (WWDG CFR).
    out[3]=(v>>16)&0xFF, out[1]=(v>>8)&0x1F, out[2]=v&0x3F, out[0]=(v>>13)&0x7.
    mode==0 → out[1..3] = BCD→десятичный (0xc9a8: hi*10+lo); out[0] не кодируется."""
    OUT = 0x500
    for _ in range(12):
        mode = rng.choice([0, 1])
        v = rng.getrandbits(32)
        run.periph_write(0x40002804, v)
        run.ram_write(OUT, bytes(4))
        ret = run.call(0xCC1C, (mode, RAM + OUT), max_insn=2000)
        _cleanc(run)
        m = v & 0x00FFFF3F
        o3 = (m >> 16) & 0xFF
        o1 = (m >> 8) & 0x1F
        o2 = m & 0x3F
        o0 = (m >> 0xD) & 0x7
        if mode == 0:
            o3 = (o3 >> 4) * 10 + (o3 & 0xF)
            o1 = (o1 >> 4) * 10 + (o1 & 0xF)
            o2 = (o2 >> 4) * 10 + (o2 & 0xF)
        got = run.ram_read(OUT, 4)
        assert got[0] == o0, f'v={v:#x} mode={mode}: out[0]={got[0]} ≠ {o0}'
        assert got[1] == o1, f'v={v:#x} mode={mode}: out[1]={got[1]} ≠ {o1}'
        assert got[2] == o2, f'v={v:#x} mode={mode}: out[2]={got[2]} ≠ {o2}'
        assert got[3] == o3, f'v={v:#x} mode={mode}: out[3]={got[3]} ≠ {o3}'

def _t_ccbc(run, rng):
    """0xccbc(mode, out*): v=u32[0x40002800]&0x007F7F7F (WWDG CR).
    out[0]=(v>>16)&0x3F, out[1]=(v>>8)&0x7F, out[2]=v&0x7F, out[3]=(v>>16)&1.
    mode==0 → out[0..2] = BCD→десятичный (0xc9a8); out[3] не кодируется."""
    OUT = 0x500
    for _ in range(12):
        mode = rng.choice([0, 1])
        v = rng.getrandbits(32)
        run.periph_write(0x40002800, v)
        run.ram_write(OUT, bytes(4))
        ret = run.call(0xCCBC, (mode, RAM + OUT), max_insn=2000)
        _cleanc(run)
        m = v & 0x007F7F7F
        o0 = (m >> 16) & 0x3F
        o1 = (m >> 8) & 0x7F
        o2 = m & 0x7F
        o3 = 0x40 if (m & 0x400000) else 0   # (v&0x400000)>>0x10
        if mode == 0:
            o0 = (o0 >> 4) * 10 + (o0 & 0xF)
            o1 = (o1 >> 4) * 10 + (o1 & 0xF)
            o2 = (o2 >> 4) * 10 + (o2 & 0xF)
        got = run.ram_read(OUT, 4)
        assert got[0] == o0, f'v={v:#x} mode={mode}: out[0]={got[0]} ≠ {o0}'
        assert got[1] == o1, f'v={v:#x} mode={mode}: out[1]={got[1]} ≠ {o1}'
        assert got[2] == o2, f'v={v:#x} mode={mode}: out[2]={got[2]} ≠ {o2}'
        assert got[3] == o3, f'v={v:#x} mode={mode}: out[3]={got[3]} ≠ {o3}'

def _t_f40c(run, rng):
    """0xf40c(): threshold #5 (без push) + tail-блок 0xf4d8 (threshold #4) —
    функция падает в него перед bx lr (0xf5a4). gate = bit4 byte[0xF72]
    (toggle-флаг; тот же байт, что и gate4=bit0):
    v1=u16[0xF9D], v2=u16[0xF9B] (RAM), d=|v1-v2|:
    gate=0: d < u16[0x19D8E+0x12] (flash) → u16[0xA2A]=0;
      u16[0xF9B] ≤ 0xC1C → u16[0xA2A]=0; иначе u16[0xA2A]+=1;
      cap u16[0x19D8E+0x16] ≤ new → byte[0xF72]|=0x10, u16[0xA2A]=0
    gate=1: d > u16[0x19D8E+0x14] → u16[0xA2C]=0; иначе u16[0xA2C]+=1;
      cap u16[0x19D8E+0x18] ≤ new → byte[0xF72]&=~0x10, u16[0xA2C]=0
    tail (gate4=bit0 byte[0xF72]):
    gate4=0: d < u16[0x19D8E+2] или u16[0xF9B] ≤ 0xC1C → u16[0xA26]=0, ret=0;
      иначе u16[0xA26]+=1; cap u16[0x19D8E+6] ≤ new → byte[0xF72]|=1, 0xA26=0, ret=0;
      else ret=u16[0x19D8E+6]
    gate4=1: d > u16[0x19D8E+4] → u16[0xA28]=0, ret=0; иначе u16[0xA28]+=1;
      cap u16[0x19D8E+8] ≤ new → byte[0xF72]&=~1, 0xA28=0, ret=0; else ret=u16[0x19D8E+8]"""
    FL = 0x08019D8E
    for _ in range(16):
        gb = rng.getrandbits(8)
        v1 = rng.getrandbits(16)
        v2 = rng.getrandbits(16)
        w = {off: rng.getrandbits(16) for off in (2, 4, 6, 8, 0x12, 0x14, 0x16, 0x18)}
        cnt_a = rng.getrandbits(16)
        cnt_b = rng.getrandbits(16)
        cnt_26 = rng.getrandbits(16)
        cnt_28 = rng.getrandbits(16)
        run.ram_write(0xF72, bytes([gb]))
        run.ram_write(0xF95 + 6, struct.pack('<H', v2))
        run.ram_write(0xF95 + 8, struct.pack('<H', v1))
        run.ram_write(0xA2A, struct.pack('<H', cnt_a))
        run.ram_write(0xA2C, struct.pack('<H', cnt_b))
        run.ram_write(0xA26, struct.pack('<H', cnt_26))
        run.ram_write(0xA28, struct.pack('<H', cnt_28))
        for off, val in w.items():
            run.uc.mem_write(FL + off, struct.pack('<H', val))
        d = abs(v1 - v2)
        ret = run.call(0xF40C, (), max_insn=2000)
        _cleanc(run)
        # --- модель ---
        e_a, e_b, e_26, e_28, e_gb, e_ret = cnt_a, cnt_b, cnt_26, cnt_28, gb, 0
        gate = (gb >> 4) & 1
        if gate == 0:
            if d < w[0x12] or v2 <= 0xC1C:
                e_a = 0
            else:
                new = (cnt_a + 1) & 0xFFFF
                e_a = new
                if w[0x16] <= new:
                    e_gb = (gb & ~0x10) | 0x10
                    e_a = 0
        else:
            if d > w[0x14]:
                e_b = 0
            else:
                new = (cnt_b + 1) & 0xFFFF
                e_b = new
                if w[0x18] <= new:
                    e_gb = gb & ~0x10
                    e_b = 0
        gate4 = e_gb & 1
        if gate4 == 0:
            if d < w[2] or v2 <= 0xC1C:
                e_26 = 0
                e_ret = 0
            else:
                new = (cnt_26 + 1) & 0xFFFF
                e_26 = new
                if w[6] <= new:
                    e_gb = (e_gb & ~1) | 1
                    e_26 = 0
                    e_ret = 0
                else:
                    e_ret = w[6]
        else:
            if d > w[4]:
                e_28 = 0
                e_ret = 0
            else:
                new = (cnt_28 + 1) & 0xFFFF
                e_28 = new
                if w[8] <= new:
                    e_gb = e_gb & ~1
                    e_28 = 0
                    e_ret = 0
                else:
                    e_ret = w[8]
        # --- проверка ---
        f72 = run.ram_read(0xF72, 1)[0]
        got_a = struct.unpack('<H', run.ram_read(0xA2A, 2))[0]
        got_b = struct.unpack('<H', run.ram_read(0xA2C, 2))[0]
        got_26 = struct.unpack('<H', run.ram_read(0xA26, 2))[0]
        got_28 = struct.unpack('<H', run.ram_read(0xA28, 2))[0]
        assert ret[0] == e_ret,             f'gb={gb:#x} d={d}: ret={ret[0]:#x} ≠ {e_ret:#x}'
        assert f72 == e_gb, f'gb={gb:#x}: F72={f72:#x} ≠ {e_gb:#x}'
        assert got_a == e_a, f'A2A={got_a:#x} ≠ {e_a:#x}'
        assert got_b == e_b, f'A2C={got_b:#x} ≠ {e_b:#x}'
        assert got_26 == e_26, f'A26={got_26:#x} ≠ {e_26:#x}'
        assert got_28 == e_28, f'A28={got_28:#x} ≠ {e_28:#x}'

def _t_fcd0(run, rng):
    """0xfcd0(): threshold-счётчик #2, ДВЕ фазы (ret ≠ 0 на нек-рых путях).
    Фаза 1: gate = byte[0x80] ∈ {1,2} И bit3 byte[0xFA1]==0:
      v=u16[0xF9B] > ref=u16[0x19DAA+0xE] → u16[0x9FC]=0;
      иначе u16[0x9FC]+=1; cap=u16[0x19DAA+0x12] ≤ new → FA1|=8, 9FC=0, 9FE=0,
      ret=0; else ret=cap (р0 несёт cap дальше)
    Фаза 2 (всегда, если bit3 FA1):
      byte[0x80]==0 И u32[0xFBB+4] ≥ 0x64 → FA1&=~8, 9FE=0, ret=0;
      иначе (byte[0x80]≠0 или u32[0xFBB+4]<0x64):
        v < u16[0x19DAA+0x10] → 9FE=0, ret=0;
        иначе 9FE+=1; cap2=u16[0x19DAA+0x14] ≤ new2 → FA1&=~8, 9FE=0, ret=0;
        else ret=cap2"""
    FL = 0x08019DAA
    for _ in range(14):
        b80 = rng.choice([0, 0, 1, 2, 3])
        fa1 = (rng.getrandbits(8) & ~8) | (rng.choice([0, 0, 1]) << 3)
        v = rng.getrandbits(16)
        ref_e = rng.choice([v, v - 1 if v else 0, v + 1, rng.getrandbits(16)])
        ref_10 = rng.choice([v, v - 1 if v else 0, v + 1, rng.getrandbits(16)])
        cnt_fc = rng.getrandbits(16)
        cnt_fe = rng.getrandbits(16)
        fbf = rng.getrandbits(32)
        cap_12 = rng.getrandbits(16)
        cap_14 = rng.getrandbits(16)
        run.ram_write(0x80, bytes([b80]))
        run.ram_write(0xFA1, bytes([fa1]))
        run.ram_write(0xF95 + 6, struct.pack('<H', v))
        run.ram_write(0x9FC, struct.pack('<H', cnt_fc))
        run.ram_write(0x9FE, struct.pack('<H', cnt_fe))
        run.ram_write(0xFBB + 4, struct.pack('<I', fbf))
        run.uc.mem_write(FL + 0xE, struct.pack('<H', ref_e))
        run.uc.mem_write(FL + 0x10, struct.pack('<H', ref_10))
        run.uc.mem_write(FL + 0x12, struct.pack('<H', cap_12))
        run.uc.mem_write(FL + 0x14, struct.pack('<H', cap_14))
        ret = run.call(0xFCD0, (), max_insn=2000)
        _cleanc(run)
        # --- модель ---
        e_fa1, e_fc, e_fe, e_ret = fa1, cnt_fc, cnt_fe, 0
        if b80 in (1, 2) and not (e_fa1 & 8):
            if v > ref_e:   # ldrh → zero-extend → сравнение unsigned
                e_fc = 0
            else:
                new = (cnt_fc + 1) & 0xFFFF
                e_fc = new
                if cap_12 <= new:
                    e_fa1 |= 8
                    e_fc = 0
                    e_fe = 0
                    e_ret = 0
                else:
                    e_ret = cap_12
        if e_fa1 & 8:
            if b80 == 0 and fbf >= 0x64:
                e_fa1 &= ~8
                e_fe = 0
                e_ret = 0
            else:
                if v < ref_10:   # unsigned
                    e_fe = 0
                    e_ret = 0
                else:
                    new2 = (e_fe + 1) & 0xFFFF
                    e_fe = new2
                    if cap_14 <= new2:
                        e_fa1 &= ~8
                        e_fe = 0
                        e_ret = 0
                    else:
                        e_ret = cap_14
        else:
            e_ret = 0     # фаза 2 с бит3=0 затирает r0 (ubfx) → ret=0
        # --- проверка ---
        g_fa1 = run.ram_read(0xFA1, 1)[0]
        g_fc = struct.unpack('<H', run.ram_read(0x9FC, 2))[0]
        g_fe = struct.unpack('<H', run.ram_read(0x9FE, 2))[0]
        assert ret[0] == (e_ret & M32),             f'b80={b80} fa1={fa1:#x} v={v} fbf={fbf:#x}: ret={ret[0]:#x} ≠ {e_ret:#x}'
        assert g_fa1 == e_fa1, f'FA1={g_fa1:#x} ≠ {e_fa1:#x}'
        assert g_fc == e_fc, f'9FC={g_fc:#x} ≠ {e_fc:#x}'
        assert g_fe == e_fe, f'9FE={g_fe:#x} ≠ {e_fe:#x}'

def ref_19b64(a, b, a2=0):
    """0x19b64(a,b) — signed fixed-point умножение/нормализация (bit-точная модель).
    r2 = u32[0x19C68] = 0x0059460E (константа; r3 = её sign-bit = 0)."""
    a &= M32
    b &= M32
    r0s = (a << 1) & M32
    if r0s == 0:
        return 0
    r2s = (b << 1) & M32
    if r2s == 0:
        return 0
    r1 = (r0s >> 24) + (r2s >> 24)    # полный u32 (без & 0xFF)
    r0 = ((a << 9) & M32) >> 9     # a & 0x7FFFFF
    r2 = ((b << 9) & M32) >> 9     # b & 0x7FFFFF
    r4 = (r0 + r2) & M32
    r5 = (r4 << 7) & M32
    prod = (r2 * r0) & M32
    r6 = (r4 << 0x17) & M32
    prod_hi = ((r2 >> 8) * (r0 >> 8)) & M32
    r4a = (prod + r6) & M32
    r2a = (prod_hi + r5) & M32
    r2a = ((M32 - (r4a >> 16)) + r2a) & M32
    r2b = (r2a >> 16)
    r2b = (r2b + 1 + 0x4000) & M32
    r2b = (r2b << 16) & M32
    r1s = (r1 - 0x7F) & M32
    r4a_sh = (r4a << 16) & M32
    if r4a_sh != 0:                # beq после lsls r4: инкремент при r4a_sh != 0
        r2b = (r2b + 1) & M32
    # orrs r0, r2: r0 = (r4a >> 16) (от lsrs 0x19b96) | r2b
    r0 = (r2b | ((r4a >> 16) & 0xFFFF)) & M32
    if (r0 >> 31) == 0:
        r0 = (r0 << 1) & M32
        r1s = (r1s - 1) & M32
    lo = r0 & 0xFF            # uxtb ПОСЛЕ нормализации <<1
    r0 = ((((r1s << 24) & M32) + (r0 >> 7) + 1) & M32) >> 1   # adds mod 2^32
    if lo == 0x80:
        r0 = ((r0 >> 1) << 1) & M32
    if (r1s & 0x80000000):
        r0 = 0
    r3 = ((a2 ^ b) & M32) & 0x80000000   # eor r2,a2 → sign-bit; а2 обычно 0
    return (r0 | r3) & M32               # orrs r0, r3 (даже при r1s<0)

def _t_19b64(run, rng):
    """0x19b64(a,b): signed fixed-point умножение/нормализация (см. ref_19b64)."""
    for _ in range(30):
        a = rng.choice([0, 1, -1, 0x40000000, -0x40000000,
                        rng.getrandbits(16), -rng.getrandbits(16),
                        rng.getrandbits(32), -rng.getrandbits(32)])
        b = rng.choice([0, 1, -1, 0x40000000, -0x40000000,
                        rng.getrandbits(16), -rng.getrandbits(16),
                        rng.getrandbits(32), -rng.getrandbits(32)])
        ret = run.call(0x19B64, (a & M32, b & M32, 0), max_insn=2000)  # a2=0: r3=sign(b)
        _cleanc(run)
        exp = ref_19b64(a, b)
        assert ret[0] == exp, f'a={a} b={b}: ret={ret[0]:#x} ≠ {exp:#x}'

def _lb_idx(vals, k):
    """lower_bound: первый i с vals[i] > k (0..n); fast-path x[last]<=k → n"""
    lo, hi = 0, len(vals)
    while lo < hi:
        mid = (lo + hi) // 2
        if vals[mid] <= k:
            lo = mid + 1
        else:
            hi = mid
    return lo

def _t_16f42(run, rng):
    """0x16f42(kx, ky, struct*, y*): double binary search (u32-x-таблица).
    struct = u32[nx, ny, x2.., X] (x[0]=nx, x[1]=ny, x[nx]=sentinel);
    y = i16[y0.., Y] (y[ny]=sentinel). Стек: [SP0+0]=byte-таблица,
    [SP0+4]=size-поинтер (== struct), [SP0+8]=sb (шаг).
    idx1: nx ≥ kx → 0; x[nx] ≤ kx → nx; else last i<nx: x[i] ≤ kx.
    idx2: ky ≤ y[0] → 0; y[ny] ≤ ky → ny; else last i<ny: y[i] ≤ ky.
    ret = byte[r8 + idx1 + sb*idx2]."""
    ST, YS, BT = 0x600, 0x680, 0x700
    for _ in range(10):
        nx = rng.randint(1, 8)
        ny = rng.randint(max(nx, 1), max(nx, 1) + 8)
        rest = sorted(rng.sample(range(ny, 4000), max(nx - 2, 0)))
        xs = [nx, ny] + rest                  # x[0]=nx, x[1]=ny
        if nx >= 2:
            xs = xs + [50000]   # x[nx] sentinel (nx=1: x[1]=ny)
        ys = sorted(rng.sample(range(-2000, 2000), ny))
        ys = ys + [32767]                     # y[ny] sentinel
        bt_len = (nx + 1) * (ny + 1) + 64
        bt = [rng.getrandbits(8) for _ in range(bt_len)]
        sb = nx
        run.ram_write(ST, struct.pack(f'<{nx + 1}I', *xs))
        run.ram_write(YS, struct.pack(f'<{ny + 1}h', *ys))
        run.ram_write(BT, struct.pack(f'<{bt_len}B', *bt))
        run.ram_write(0x18000, struct.pack('<I', RAM + BT))
        run.ram_write(0x18004, struct.pack('<I', RAM + ST))
        run.ram_write(0x18008, struct.pack('<I', sb))
        kx = rng.choice([xs[0] - 1, xs[0], rng.choice(xs[:nx]),
                         (xs[0] + xs[nx - 1]) // 2, xs[nx - 1], xs[nx - 1] + 7])
        ky = rng.choice([ys[0] - 1, ys[0], rng.choice(ys[:ny]),
                         ys[ny - 1], ys[ny - 1] + 1, -3000, 3000])
        ret = run.call(0x16F42, (kx, ky, RAM + ST, RAM + YS), max_insn=5000)
        _cleanc(run)
        if nx >= kx:
            i1 = 0
        elif xs[nx] <= kx:
            i1 = nx
        else:
            i1 = max(i for i in range(nx) if xs[i] <= kx)
        if ky <= ys[0]:
            i2 = 0
        elif ys[ny] <= ky:
            i2 = ny
        else:
            i2 = max(i for i in range(ny) if ys[i] <= ky)
        exp = bt[i1 + sb * i2]
        assert ret[0] == (exp & M32),             f'kx={kx} ky={ky} i=({i1},{i2}): ret={ret[0]:#x} ≠ {exp:#x}'

def _t_16fde(run, rng):
    """0x16fde(kx, ky, u16x*, y*): twin 0x16f42 с u16-x-таблицей.
    u16x = u16[nx, ny, x2.., X] (x[nx]=sentinel); size-блок u32[nx, ny]
    по [SP0+4] (отдельный); [SP0+0]=i16-таблица; [SP0+8]=sb.
    ret = i16[r8 + 2*(idx1 + sb*idx2)] (sign-extended)."""
    SU, X16, YS, BT = 0x580, 0x600, 0x680, 0x700
    for _ in range(10):
        nx = rng.randint(1, 8)
        ny = rng.randint(max(nx, 1), max(nx, 1) + 8)
        rest = sorted(rng.sample(range(ny, 4000), max(nx - 2, 0)))
        xs = [nx, ny] + rest                  # x[0]=nx, x[1]=ny
        if nx >= 2:
            xs = xs + [50000]   # x[nx] sentinel (nx=1: x[1]=ny)
        ys = sorted(rng.sample(range(-2000, 2000), ny))
        ys = ys + [32767]                     # y[ny] sentinel
        bt_len = (nx + 1) * (ny + 1) + 64
        bt = [rng.getrandbits(16) for _ in range(bt_len)]
        sb = nx
        run.ram_write(SU, struct.pack('<2I', nx, ny))
        run.ram_write(X16, struct.pack(f'<{nx + 1}H', *xs))
        run.ram_write(YS, struct.pack(f'<{ny + 1}h', *ys))
        run.ram_write(BT, struct.pack(f'<{bt_len}H', *bt))
        run.ram_write(0x18000, struct.pack('<I', RAM + BT))
        run.ram_write(0x18004, struct.pack('<I', RAM + SU))
        run.ram_write(0x18008, struct.pack('<I', sb))
        kx = rng.choice([xs[0] - 1, xs[0], rng.choice(xs[:nx]),
                         (xs[0] + xs[nx - 1]) // 2, xs[nx - 1], xs[nx - 1] + 7])
        ky = rng.choice([ys[0] - 1, ys[0], rng.choice(ys[:ny]),
                         ys[ny - 1], ys[ny - 1] + 1, -3000, 3000])
        ret = run.call(0x16FDE, (kx, ky, RAM + X16, RAM + YS), max_insn=5000)
        _cleanc(run)
        if nx >= kx:
            i1 = 0
        elif xs[nx] <= kx:
            i1 = nx
        else:
            i1 = max(i for i in range(nx) if xs[i] <= kx)
        if ky <= ys[0]:
            i2 = 0
        elif ys[ny] <= ky:
            i2 = ny
        else:
            i2 = max(i for i in range(ny) if ys[i] <= ky)
        v = bt[i1 + sb * i2]
        exp = v - 0x10000 if v >= 0x8000 else v
        assert ret[0] == (exp & M32),             f'kx={kx} ky={ky} i=({i1},{i2}): ret={ret[0]:#x} ≠ {exp & M32:#x}'

t(0x16F42, 'E2-b63: 0x16f42(kx,ky,struct*,y*+стек r8/sb/struct) double bsearch: idx1=floor-idx u32-x-таблицы, idx2=floor-idx i16-y-таблицы (clamped 0..size), ret=byte[r8+idx1+sb*idx2]')(_t_16f42)
t(0x16FDE, 'E2-b63: 0x16fde(kx,ky,u16x*,y*) twin 0x16f42 с u16-x-таблицей: ret=i16[r8+2*(idx1+sb*idx2)] (sign-extended)')(_t_16fde)
t(0xCC1C, 'E2-b63: 0xcc1c(mode,out*) WWDG CFR(+4) декодер: v=u32[0x40002804]&0x00FFFF3F; out[3]=(v>>16)&FF, out[1]=(v>>8)&0x1F, out[2]=v&0x3F, out[0]=(v>>13)&7; mode=0 → out[1..3]=BCD→decimal (0xc9a8)')(_t_cc1c)
t(0xCCBC, 'E2-b63: 0xccbc(mode,out*) WWDG CR(+0) декодер: v=u32[0x40002800]&0x007F7F7F; out[0]=(v>>16)&0x3F, out[1]=(v>>8)&0x7F, out[2]=v&0x7F, out[3]=(v>>16)&1; mode=0 → out[0..2]=BCD→decimal')(_t_ccbc)
t(0xF40C, 'E2-b63: 0xf40c() threshold #5 (gate bit4[0xF72]): gate0: d=|u16[0x19D8E+8]-u16[0x19D8E+6]|, d<u16[0x19D8E+0x12]→A2C=0; u16[0xF9B]≤0xC1C→A2C=0; иначе new=u16[0xA2A]+1→A2C, cap A3A≤new → F97=(F72&~0x10)|0x10, A2A=0; gate1: d=|u16[0xF9D]-u16[0xF9B]|, d>A3E→A2C=0; иначе new=u16[0xA26]+1→A2C, cap u16[0x19D8E+0x18]≤new → F97&=~0x10, A2C=0; ret=0')(_t_f40c)
t(0xFCD0, 'E2-b63: 0xfcd0() threshold-счётчик #2: гейт byte[0x80]∈{1,2} и bit3[0xFA1]=0; u16[0x19DAA+6]>u16[0xA0A]→9FE=0; иначе new=u16[0x9FE]+1→9FC; cap u16[0x19DAA+0x12]≤new → FA1=(byte[0x19DAA+0xC]&~8)|8, 9FE=0, FBB=0; ret=0')(_t_fcd0)
t(0x19B64, 'E2-b63: 0x19b64(a,b) signed fixed-point умножение/нормализация: (a<<1|b<<1)==0→0; prod=(a*b)+(a+b)<<7-компоновка Q-формат, +0x4000 rounding, нормализация (r0≥0 → <<1), sign-bit если знаки различны (bit-точная модель ref_19b64)')(_t_19b64)
def _t_c708(run, rng):
    """0xc708(out*): расчёт частоты тактирования (RCC-реестры → struct из 6 u32).
    CFGR0=u32[RCC+4], CFGR2=u32[RCC+0x24], CFGR3=u32[RCC+0x2C], X=u32[RCC+0x40];
    m=CFGR0&0x083C0000; r3 = 0x1F0-(m>>18)+1 если m&0x8000000, иначе 2+(m>>18);
    r2 = r3 * (0x7A1200 если (CFGR0&0x10000 ? (CFGR0&0x20000) : X&1) else 0xF42400);
    X&2 → r2>>=1; s=CFGR0&0xC:
      s==0/other → T2[(CFGR2>>4)&7], s==4/8 → 0xF42400, s==0xC → r2 (T2=u32[0x0801A920..]);
    *out=f; +4=f>>T0[(CFGR0&0xF0)>>4]; +8=(+4)>>T0[(CFGR0&0x700)>>8];
    +0xC=(+4)>>T0[(CFGR0&0x3800)>>0xB]; +0x14=(+4)/T1[CFGR3&0xF] (udiv);
    +0x10=r2/T3[((CFGR3&0x1F0)>>4)&0xF] (udiv). ret=ptr."""
    T0 = bytes([0xC5, 0x60, 0x02, 0x25, 0x0D, 0x70, 0x03, 0x25,
                0x4D, 0x70, 0x45, 0x69, 0x1D, 0x43, 0x45, 0x61])
    T1 = bytes([0x01, 0x25, 0x25, 0x70, 0x8D, 0x88, 0x6D, 0x1E,
                0x8D, 0x80, 0xFB, 0xD2, 0xFF, 0x25, 0xF5, 0x35])
    T2 = [0x40012C40, 0x20000102, 0x20000218, 0x1388,
          0x8CA, 0x20000246, 0x4CFEB5F0, 0xB08748FC]
    T3 = [0x808D, 0x6945, 0x439D, 0x6145, 0x7022, 0x8888, 0x1E43, 0x808B,
          0xD2FB, 0x808F, 0x2004, 0x7008, 0x7048, 0x4806, 0x7002, 0xBDF0]
    RCC = 0x40021000
    OUT = 0x500

    def sh32(v, n):
        n &= 0xFF
        if n == 0:
            return v
        if n >= 32:
            return 0
        return v >> n

    for _ in range(10):
        cfgr0 = rng.getrandbits(32)
        cfgr2 = rng.getrandbits(32)
        cfgr3 = rng.getrandbits(32)
        x40 = rng.getrandbits(32)
        run.periph_write(RCC + 4, cfgr0)
        run.periph_write(RCC + 0x24, cfgr2)
        run.periph_write(RCC + 0x2C, cfgr3)
        run.periph_write(RCC + 0x40, x40)
        run.ram_write(OUT, bytes(24))
        ret = run.call(0xC708, (RAM + OUT,), max_insn=2000)
        _cleanc(run)
        m = cfgr0 & 0x083C0000
        r3 = ((m >> 18) - 0x1F0 + 1) & M32 if (m & 0x8000000) else (2 + (m >> 18)) & M32
        src_sel = ((cfgr0 & 0x20000) != 0) if (cfgr0 & 0x10000) else ((x40 & 1) != 0)
        r2 = (r3 * (0x7A1200 if src_sel else 0xF42400)) & M32
        if x40 & 2:
            r2 >>= 1
        r5 = (cfgr2 >> 4) & 7
        s = cfgr0 & 0xC
        if s in (4, 8):
            f = 0xF42400
        elif s == 0xC:
            f = r2
        else:
            f = T2[r5]
        f &= M32
        d0 = sh32(f, T0[(cfgr0 & 0xF0) >> 4])
        d1 = sh32(d0, T0[(cfgr0 & 0x700) >> 8])
        d2 = sh32(d0, T0[(cfgr0 & 0x3800) >> 0xB])
        div14 = T1[cfgr3 & 0xF]
        d14 = (d0 // div14) if div14 else 0
        idx = ((cfgr3 & 0x1F0) >> 4) & 0xF
        d10 = (r2 // T3[idx]) if T3[idx] else 0
        got = struct.unpack('<6I', run.ram_read(OUT, 24))
        assert ret[0] == RAM + OUT, f'ret={ret[0]:#x}'
        assert got[0] == f, f'cfgr0={cfgr0:#x}: out[0]={got[0]:#x} ≠ {f:#x}'
        assert got[1] == d0, f'cfgr0={cfgr0:#x}: out[1]={got[1]:#x} ≠ {d0:#x}'
        assert got[2] == d1, f'cfgr0={cfgr0:#x}: out[2]={got[2]:#x} ≠ {d1:#x}'
        assert got[3] == d2, f'cfgr0={cfgr0:#x}: out[3]={got[3]:#x} ≠ {d2:#x}'
        assert got[4] == d10, f'cfgr3={cfgr3:#x}: out[4]={got[4]:#x} ≠ {d10:#x}'
        assert got[5] == d14, f'cfgr3={cfgr3:#x}: out[5]={got[5]:#x} ≠ {d14:#x}'

t(0xC708, 'E2-b63: 0xc708(out*) расчёт частоты тактирования: m=CFGR0&0x083C0000; r3=2+(m>>18) / 0x1F1-(m>>18) (m&0x8000000); r2=r3*(8МГц/15,9МГц) (CFGR0 b16?b17:RCC+0x40 b0), RCC+0x40 b1 → r2>>=1; *out: CFGR0&0xC: 4/8→0xF42400, 0xC→r2, else→u32[0x1A920+4*((CFGR2>>4)&7)]; +4/+8/+0C=f>>T0[индексы CFGR0]; +0x14=(+4)/T1[CFGR3&0xF]; +0x10=r2/T3[((CFGR3&0x1F0)>>4)&0xF] (udiv); ret=ptr')(_t_c708)
