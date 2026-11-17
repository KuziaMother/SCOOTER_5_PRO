# -*- coding: utf-8 -*-
# ruff: noqa: F405  (имена из star-import от fv_core)
"""E1: duty/throttle, PB15, batch9, ADC1, §69-73.x модели контура (2326-4331)."""
from fv_core import *  # noqa: F401,F403
from fv_core import _fresh_call, _intercept  # noqa: F401

import re
# ---------------------------------------------------------------------------
# §59: 3-проводная шина (0x23374) + RCC/GPIOC init (0x1E2F8)
# ---------------------------------------------------------------------------

BUS3_STRUCT = 0xAC   # struct @RAM+0xAC (пул 0x2347C = 0x200000AC)


def _bus3(run, a=0, b=0, c=0, sel=0, cur=0, delta=0, lim=0, old_out=0):
    """собрать struct @RAM+0xAC: u16[+8]=a, u16[+A]=b, u16[+C]=c,
    u16[+E]=sel, u32[+0x38]=cur, u32[+0x3C]=delta, u32[+0x40]=lim,
    u16[+0x30]=old_out; вернуть (mid, ...) для ожиданий"""
    buf = bytearray(0x50)
    struct.pack_into('<H', buf, 8, a)
    struct.pack_into('<H', buf, 0xA, b)
    struct.pack_into('<H', buf, 0xC, c)
    struct.pack_into('<H', buf, 0xE, sel)
    struct.pack_into('<I', buf, 0x38, cur)
    struct.pack_into('<I', buf, 0x3C, delta)
    struct.pack_into('<I', buf, 0x40, lim)
    struct.pack_into('<H', buf, 0x30, old_out)
    run.ram_write(BUS3_STRUCT, bytes(buf))
    return (cur + delta) >> 1


@t(0x23374, '§59: 3-проводная шина — полная таблица решений (эмуляторно): C==0 → A=u16[+8] (0/1/2/4), C!=0 → B=u16[+A] (3/5/6/7); mid=(cur+delta)>>1; cur обновляется только на «mid»-ветках; A==0/B==7 → r0 из аргументов; пропущенные ветки → старый out. §59.2: на этом чипе bls/CC = lim≤mid (с равенством!), bhi/HS = lim>mid строго (отклонение от ARM: CC включает Z)')
def _(run, rng):
    # mid=10 везде (cur=10, delta=10); lim: 5(<mid), 10(=mid), 100(>mid)
    cases = [
        # (a, b, c, sel, cur, delta, lim, old_out, arg_r0, exp_out, exp_cur)
        (0, 0, 0, 0, 0, 0, 0, 7, 0x1234, 0x1234, None),   # A==0 → r0 caller'а
        (5, 0, 0, 0, 0, 0, 0, 7, 0x1234, 7, None),        # A∉{0,1,2,4} → старый out
        (3, 0, 0, 4, 0, 0, 0, 9, 0, 9, None),
        # A==1
        (1, 0, 0, 1, 0, 0, 0, 0, 0, 1, None),
        (1, 0, 0, 3, 10, 10, 5, 0, 0, 2, 10),             # lim≤mid → 2
        (1, 0, 0, 3, 10, 10, 10, 0, 0, 2, 10),            # lim==mid → 2 (CC включает =)
        (1, 0, 0, 3, 10, 10, 100, 0, 0, 3, 10),           # lim>mid → 3
        (1, 0, 0, 5, 10, 10, 5, 0, 0, 5, 10),             # lim≤mid → 5
        (1, 0, 0, 5, 10, 10, 10, 0, 0, 5, 10),            # lim==mid → 5
        (1, 0, 0, 5, 10, 10, 100, 0, 0, 4, 10),           # lim>mid → 4
        (1, 0, 0, 7, 1, 1, 1, 0, 0, 6, 1),                # sel 7 → 6, cur не трогает
        (1, 0, 0, 2, 0, 0, 0, 0, 0, 2, None),             # else → out=sel
        # A==2
        (2, 0, 0, 2, 0, 0, 0, 0, 0, 2, None),
        (2, 0, 0, 3, 10, 10, 5, 0, 0, 3, 10),             # lim≤mid → 3
        (2, 0, 0, 3, 10, 10, 10, 0, 0, 3, 10),            # lim==mid → 3
        (2, 0, 0, 3, 10, 10, 100, 0, 0, 1, 10),           # lim>mid → 1
        (2, 0, 0, 6, 10, 10, 100, 0, 0, 6, 10),           # lim>mid строго (bhi) → 6
        (2, 0, 0, 6, 10, 10, 10, 0, 0, 4, 10),            # lim==mid → 4 (bhi нет)
        (2, 0, 0, 6, 10, 10, 5, 0, 0, 4, 10),             # lim<mid → 4
        (2, 0, 0, 7, 0, 0, 0, 0, 0, 5, None),
        # A==4
        (4, 0, 0, 4, 0, 0, 0, 0, 0, 4, None),
        (4, 0, 0, 5, 10, 10, 100, 0, 0, 5, 10),           # lim>mid строго → 5
        (4, 0, 0, 5, 10, 10, 10, 0, 0, 1, 10),            # lim==mid → 1
        (4, 0, 0, 5, 10, 10, 5, 0, 0, 1, 10),
        (4, 0, 0, 6, 10, 10, 5, 0, 0, 6, 10),             # lim≤mid → 6
        (4, 0, 0, 6, 10, 10, 10, 0, 0, 6, 10),            # lim==mid → 6
        (4, 0, 0, 6, 10, 10, 100, 0, 0, 2, 10),           # lim>mid → 2
        (4, 0, 0, 7, 1, 1, 1, 0, 0, 3, 1),                # sel 7 → 3, cur не трогает
        # B==3 (C!=0)
        (0, 3, 1, 0, 0, 0, 0, 0, 0, 4, None),
        (0, 3, 1, 1, 10, 10, 100, 0, 0, 5, 10),           # lim>mid строго → 5
        (0, 3, 1, 1, 10, 10, 10, 0, 0, 1, 10),            # lim==mid → 1
        (0, 3, 1, 1, 10, 10, 5, 0, 0, 1, 10),
        (0, 3, 1, 2, 10, 10, 5, 0, 0, 6, 10),             # lim≤mid → 6
        (0, 3, 1, 2, 10, 10, 10, 0, 0, 6, 10),            # lim==mid → 6
        (0, 3, 1, 2, 10, 10, 100, 0, 0, 2, 10),           # lim>mid → 2
        (0, 3, 1, 3, 0, 0, 0, 0, 0, 3, None),
        (0, 3, 1, 9, 0, 0, 0, 0, 0, 9, None),             # else → out=sel
        # B==5
        (0, 5, 1, 0, 0, 0, 0, 0, 0, 2, None),
        (0, 5, 1, 1, 10, 10, 5, 0, 0, 3, 10),             # lim≤mid → 3
        (0, 5, 1, 1, 10, 10, 10, 0, 0, 3, 10),            # lim==mid → 3
        (0, 5, 1, 1, 10, 10, 100, 0, 0, 1, 10),           # lim>mid → 1
        (0, 5, 1, 4, 10, 10, 100, 0, 0, 6, 10),           # lim>mid строго → 6
        (0, 5, 1, 4, 10, 10, 10, 0, 0, 4, 10),            # lim==mid → 4
        (0, 5, 1, 4, 10, 10, 5, 0, 0, 4, 10),
        (0, 5, 1, 5, 0, 0, 0, 0, 0, 5, None),
        # B==6
        (0, 6, 1, 0, 0, 0, 0, 0, 0, 1, None),
        (0, 6, 1, 2, 10, 10, 5, 0, 0, 2, 10),             # lim≤mid → 2
        (0, 6, 1, 2, 10, 10, 10, 0, 0, 2, 10),            # lim==mid → 2
        (0, 6, 1, 2, 10, 10, 100, 0, 0, 3, 10),           # lim>mid → 3
        (0, 6, 1, 4, 10, 10, 5, 0, 0, 5, 10),             # lim≤mid → 5
        (0, 6, 1, 4, 10, 10, 10, 0, 0, 5, 10),            # lim==mid → 5
        (0, 6, 1, 4, 10, 10, 100, 0, 0, 4, 10),           # lim>mid → 4
        (0, 6, 1, 6, 0, 0, 0, 0, 0, 6, None),
        # B==7 / пропуски
        (0, 7, 1, 0, 0, 0, 0, 7, 0x77, 0x77, None),       # B==7 → r0 caller'а
        (0, 9, 1, 0, 0, 0, 0, 8, 0x55, 8, None),          # B∉{3,5,6,7} → старый out
    ]
    for (a, b, c, sel, cur, delta, lim, old, r0arg, exp_out, exp_cur) in cases:
        _bus3(run, a=a, b=b, c=c, sel=sel, cur=cur, delta=delta,
              lim=lim, old_out=old)
        r0, _ = run.call(0x23374, [r0arg])
        tag = f'A={a} B={b} C={c} sel={sel}'
        assert r0 == exp_out, f'{tag}: out={r0:#x} ≠ {exp_out:#x}'
        if exp_cur is not None:
            got_cur = struct.unpack_from('<I', run.ram_read(BUS3_STRUCT + 0x38, 4), 0)[0]
            assert got_cur == exp_cur, f'{tag}: cur={got_cur:#x} ≠ {exp_cur:#x}'


@t(0x1E2F8, '§59: RCC/GPIOC init: RCC+0x3C |= 0xF0000 (по битам 16-19), +0x40 |= 0xE0000, +0x44 |= 0x4A00, +0x3C |= 0x8001; helper 0x19A9A(sp,0x28): RCC+0x00/04=0, +0x08|=0x900; tail 0x22824 (RCC-делители: +0x08 nibble-логика по MODER=0x44AA200, mid-ветка → 1) → +0x08=0x900; финал RCC+0x00 = 0x100000 (bit20 enable)')
def _(run, rng):
    uc = run.uc
    # RCC-регион обнуляем: OR-записи не идемпотентны (один Run на все тесты)
    uc.mem_write(0x40021000, b'\x00' * 0x100)
    writes = []
    def hw(u_, acc, addr, size, val, usr):
        if 0x40021000 <= addr < 0x40021100:
            writes.append((addr - 0x40021000, val))
    hook = uc.hook_add(UC_HOOK_MEM_WRITE, hw, None, 0x40021000, 0x40021100)
    try:
        r0, _ = run.call(0x1E2F8, [])
    finally:
        uc.hook_del(hook)
    assert r0 == 0x100000, f'r0={r0:#x}'
    seq = [(off, val) for off, val in writes]
    # RCC+0x3C: по битам 16..19 (0x80000→0xC0000→0xE0000→0xF0000)
    c3c = [v for o, v in seq if o == 0x3C]
    assert c3c[:4] == [0x80000, 0xC0000, 0xE0000, 0xF0000], f'+0x3C={ [hex(v) for v in c3c]}'
    # RCC+0x40: 0x80000 → 0xC0000 → 0xE0000
    c40 = [v for o, v in seq if o == 0x40]
    assert c40 == [0x80000, 0xC0000, 0xE0000], f'+0x40={[hex(v) for v in c40]}'
    # RCC+0x44: 0x4000 → 0x4800 → 0x4A00
    c44 = [v for o, v in seq if o == 0x44]
    assert c44 == [0x4000, 0x4800, 0x4A00], f'+0x44={[hex(v) for v in c44]}'
    # RCC+0x3C финал: |= 0x8000 → 0xF8000, |= 1 → 0xF8001
    assert c3c[-2:] == [0xF8000, 0xF8001], f'+0x3C хвост={[hex(v) for v in c3c[-2:]]}'
    # helper 0x19A9A: RCC+0x00=0, +0x04=0 (×2), +0x08=0, +0x08=0x900 (×2)
    c00 = [v for o, v in seq if o == 0x00]
    c04 = [v for o, v in seq if o == 0x04]
    c08 = [v for o, v in seq if o == 0x08]
    assert c00[0] == 0 and c04[:2] == [0, 0], f'+0x00/0x04={c00}/{c04}'
    assert 0 in c08 and 0x900 in c08, f'+0x08={c08}'
    # финал: RCC+0x00 = 0x100000 (bit20)
    assert c00[-1] == 0x100000, f'+0x00 последняя={hex(c00[-1])}'


@t(0x1302C, '§59: RCC-пульсатор USART: base → (рег, бит): 0x40013800(USART1)→+0x0C/0x4000, 0x40004400(USART2)→+0x10/0x20000, 0x40004800(USART3)→+0x10/0x40000, 0x40015000→+0x0C/0x20000, 0x40015400→+0x0C/0x40000; последовательность |=bit затем &=~bit (пульс); неизвестная base → без записей; r0 = бит')
def _(run, rng):
    uc = run.uc
    cases = [
        (0x40013800, 0x0C, 0x4000),
        (0x40004400, 0x10, 0x20000),
        (0x40004800, 0x10, 0x40000),   # USART3
        (0x40015000, 0x0C, 0x20000),
        (0x40015400, 0x0C, 0x40000),
    ]
    for base, reg, bit in cases:
        uc.mem_write(0x40021000, b'\x00' * 0x100)
        writes = []
        def hw(u_, acc, addr, size, val, usr):
            if 0x40021000 <= addr < 0x40021100:
                writes.append((addr - 0x40021000, val))
        hook = uc.hook_add(UC_HOOK_MEM_WRITE, hw, None, 0x40021000, 0x40021100)
        try:
            r0, _ = run.call(0x1302C, [base])
        finally:
            uc.hook_del(hook)
        assert r0 == bit, f'{base:#x}: r0={r0:#x} ≠ {bit:#x}'
        assert writes == [(reg, bit), (reg, 0)], \
            f'{base:#x}: записи={[(hex(o), hex(v)) for o, v in writes]}'
    # неизвестная base → без записей
    uc.mem_write(0x40021000, b'\x00' * 0x100)
    writes = []
    def hw2(u_, acc, addr, size, val, usr):
        if 0x40021000 <= addr < 0x40021100:
            writes.append(1)
    hook = uc.hook_add(UC_HOOK_MEM_WRITE, hw2, None, 0x40021000, 0x40021100)
    try:
        run.call(0x1302C, [0x40010800])
    finally:
        uc.hook_del(hook)
    assert writes == [], f'неизвестная base: записей={len(writes)}'


@t(0x1E298, '§59: DMA+ADC init: bl 0x1A5D4 (ADC1 CR2|=0x20) → validated-write 0x2359C(0x40020000, 0, 0x5D000041) в [0x40020108] c readback-retry → u32[0x40020028]=1 (enable) → ADC1 CR2|=4; возврат pop {r4,pc} (§59.3: на чипе POP всегда восстанавливает pc)')
def _(run, rng):
    uc = run.uc
    # обнуляем ADC1 и блок 0x40020000 (RMW-записи)
    uc.mem_write(0x40012400, b'\x00' * 0x100)
    uc.mem_write(0x40020000, b'\x00' * 0x200)
    writes = []
    def hw(u_, acc, addr, size, val, usr):
        if (0x40012400 <= addr < 0x40012500) or (0x40020000 <= addr < 0x40020200):
            writes.append((addr, val))
    hook = uc.hook_add(UC_HOOK_MEM_WRITE, hw,
                       None, 0x40012400, 0x40012500)
    hook2 = uc.hook_add(UC_HOOK_MEM_WRITE, hw, None, 0x40020000, 0x40020200)
    try:
        r0, _ = run.call(0x1E298, [])
    finally:
        uc.hook_del(hook); uc.hook_del(hook2)
    # §57/§59: возврат через LR-sentinel даёт FETCH_UNMAPPED — это артефакт
    # харнесса (pop {pc} → 0x0BADF001), не fault функции: все записи уже сделаны
    assert r0 == 0x40012400, f'r0={r0:#x}'
    # нормализуем: ADC1-смещения как есть, блок 0x40020000 → +0x10000
    seq = [(a - 0x40012400 if a < 0x40013000 else a - 0x40020000 + 0x10000,
            v) for a, v in writes]
    # порядок: ADC1 CR2|=0x20 → [0x40020108]=0x5D000041 → [0x40020028]=1 → ADC1 CR2|=4
    assert seq[0] == (0x18, 0x20), f'1-я запись={seq[0]}'
    assert (0x10108, 0x5D000041) in seq, f'validated-write нет: {seq}'
    assert (0x10028, 1) in seq, f'enable нет: {seq}'
    assert seq[-1] == (0x18, 0x24), f'последняя={seq[-1]}'
    i_dma = next(i for i, (o, v) in enumerate(seq) if o == 0x10108)
    i_en = next(i for i, (o, v) in enumerate(seq) if o == 0x10028)
    assert seq.index((0x18, 0x20)) < i_dma < i_en < len(seq) - 1, f'порядок: {seq}'


@t(0x1D640, '§59: мотор-TIM init (TIM @0x40012C00 + channel-блоки @0x48000000/0x48000400): детерминированная последовательность 107 записей; финал TIM: +0x3C=0x8CA (prescaler), CCR +0x44/48/4C = 0x45B→0, +0x50=0x8C9, +0x54=0x1D24, +0x30=0x1DDD, +0x28/+0x2C=0x6060, +0x04=0x2A00, +0x0C=0x80; enable +0x00=0x41 — ПОСЛЕДНИЙ; блоки 0x48: A +0x2C=0x666/+0x10=0x2A0000, B +0x2C=0x66660000/+0x10=0xAA000000; r0=0x41')
def _(run, rng):
    import struct as _st
    uc = run.uc
    for base, sz in ((0x40012c00, 0x400), (0x48000000, 0x2000)):
        uc.mem_write(base, b'\x00' * sz)
    writes = []
    def hw(u_, acc, addr, size, val, usr):
        if (0x40012C00 <= addr < 0x40012C60) or (0x48000000 <= addr < 0x48000500):
            writes.append((addr, val))
    h1 = uc.hook_add(UC_HOOK_MEM_WRITE, hw, None, 0x40012C00, 0x40012C60)
    h2 = uc.hook_add(UC_HOOK_MEM_WRITE, hw, None, 0x48000000, 0x48000500)
    try:
        r0, _ = run.call(0x1D640, [], max_insn=300000)
    finally:
        uc.hook_del(h1); uc.hook_del(h2)
    assert r0 == 0x41, f'r0={r0:#x}'
    assert len(writes) == 107, f'записей={len(writes)} (ожидалось 107)'
    # финальные состояния
    def rd(a):
        return _st.unpack_from('<I', bytes(uc.mem_read(a, 4)), 0)[0]
    tim = {off: rd(0x40012C00 + off) for off in range(0, 0x60, 4)}
    assert tim[0x00] == 0x41 and tim[0x04] == 0x2A00 and tim[0x0C] == 0x80
    assert tim[0x24] == 1 and tim[0x28] == 0x6060 and tim[0x2C] == 0x6060
    assert tim[0x30] == 0x1DDD and tim[0x3C] == 0x8CA
    assert tim[0x50] == 0x8C9 and tim[0x54] == 0x1D24
    assert all(tim[o] == 0 for o in (0x44, 0x48, 0x4C)), 'CCR не очищены'
    a = {off: rd(0x48000000 + off) for off in range(0, 0x40, 4)}
    b = {off: rd(0x48000400 + off) for off in range(0, 0x40, 4)}
    assert a[0x2C] == 0x666 and a[0x10] == 0x2A0000
    assert b[0x2C] == 0x66660000 and b[0x10] == 0xAA000000
    assert all(a[o] == 0 for o in (0x14, 0x18, 0x1C, 0x20, 0x24))
    # порядок: CCR-константы 0x45B пишутся ДО их очистки; enable — последняя запись
    i_45b = next(i for i, (ad, v) in enumerate(writes) if ad == 0x40012C44 and v == 0x45B)
    i_clr = next(i for i, (ad, v) in enumerate(writes) if ad == 0x40012C44 and v == 0)
    assert i_45b < i_clr
    assert writes[-1] == (0x40012C00, 0x41), f'последняя запись={writes[-1]}'


@t(0x1BF48, '§59: МОТОР-ИНИТ (221 запись, детерминированно): 1) bl 0x1D640 (мотор-TIM @0x40012C00 + channel-блоки 0x48000000/0x48000400; enable TIM — запись #106); 2) bl 0x1C0B0 (ADC1 sensor-init §58: финал +0x18=1 ADON, +0x54=0x3CA2CC43 SQR ch C/B/A/F); 3) bl 0x1C1AC/0x1BEDC; 4) GPIO-блок @0x48000C00: CRL(+0x04) &= ~2, validated-setter 0x22000(r4, 2, cfg7) → +0x10=4 (bit2), CRL &= ~2, 0x22000(r4, 1, cfg7) → +0x10=5 (bit0+bit2); r0=0x48000C00')
def _(run, rng):
    import struct as _st
    uc = run.uc
    for base, sz in ((0x40012400, 0x1000), (0x40012c00, 0x400), (0x48000000, 0x2000)):
        uc.mem_write(base, b'\x00' * sz)
    writes = []
    def hw(u_, acc, addr, size, val, usr):
        if (0x40012000 <= addr < 0x40013000) or (0x48000000 <= addr < 0x48002000):
            writes.append((addr, val))
    h1 = uc.hook_add(UC_HOOK_MEM_WRITE, hw, None, 0x40012000, 0x40013000)
    h2 = uc.hook_add(UC_HOOK_MEM_WRITE, hw, None, 0x48000000, 0x48002000)
    try:
        r0, _ = run.call(0x1BF48, [], max_insn=500000)
    finally:
        uc.hook_del(h1); uc.hook_del(h2)
    assert r0 == 0x48000C00, f'r0={r0:#x}'
    assert len(writes) == 221, f'записей={len(writes)} (ожидалось 221)'
    # фаза 1 (0x1D640) кончается enable TIM — запись #106
    assert writes[106] == (0x40012C00, 0x41), f'#106={writes[106]}'
    def rd(a):
        return _st.unpack_from('<I', bytes(uc.mem_read(a, 4)), 0)[0]
    # ADC1-финал (§58)
    a1 = {off: rd(0x40012400 + off) for off in range(0, 0x80, 4)}
    assert a1[0x00] == 0x40 and a1[0x18] == 1 and a1[0x1C] == 0x19
    assert a1[0x20] == 0x4040403 and a1[0x24] == a1[0x28] == a1[0x2C] == 0x4040404
    assert a1[0x3C] == 0xFFF0000 and a1[0x40] == 0xE1C6104 and a1[0x44] == 9
    assert a1[0x54] == 0x3CA2CC43, f'SQR={a1[0x54]:#x}'
    # TIM-финал (из 0x1D640)
    tim = {off: rd(0x40012C00 + off) for off in range(0, 0x60, 4)}
    assert tim[0x00] == 0x41 and tim[0x3C] == 0x8CA and tim[0x50] == 0x8C9
    # channel-блоки 0x48
    assert rd(0x4800002C) == 0x666 and rd(0x48000010) == 0x2A0000
    assert rd(0x4800042C) == 0x66660000 and rd(0x48000410) == 0xAA000000
    # GPIO-блок @0x48000C00: только +0x10 = 5, CRL очищен
    c = {off: rd(0x48000C00 + off) for off in range(0, 0x40, 4)}
    assert c[0x10] == 5 and c[0x04] == 0, f'блок C: { {hex(k): hex(v) for k, v in c.items() if v} }'
    # хвост: последовательность CRL/0x22000 на блоке C
    tail = [(a, v) for a, v in writes[107:] if 0x48000C00 <= a < 0x48000C40]
    assert tail[0] == (0x48000C04, 0), f'хвост[0]={tail[0]}'
    i_m2 = next(i for i, (a, v) in enumerate(tail) if a == 0x48000C10 and v == 4)
    i_m1 = next(i for i, (a, v) in enumerate(tail) if a == 0x48000C10 and v == 5)
    assert tail[i_m2 + 1] == (0x48000C04, 0), 'CRL &= ~2 между mode-2 и mode-1'
    assert tail[-1] == (0x48000C10, 5), f'хвост[-1]={tail[-1]}'


@t(0x1C1AC, '§59: ADC-DMA transfer setup (блок @0x40020000): validated-writes [+0x100]=**0x40012450** (src=ADC1 DR), [+0x104]=**0x20001692** (dst=RAM+0x1692), bl 0x2359C → [+0x108]=0x5D000041 (ctrl, тот же что в 0x1E298); enable: +0x28=1, +0x14=1, +0x70=0x19, +0x50|=1; IRQ-хвост: [**0xE000E100**]=0x200 (прямая запись bit9), [NVIC+0x08 (0xE000E408)] &= ~0xFF00 (clear биты 8..15); r0=0')
def _(run, rng):
    uc = run.uc
    uc.mem_write(0x40020000, b'\x00' * 0x200)
    # SYS-регион обнуляем: [0xE000E408] &= ~0xFF00 — значение зависит от предыдущего
    uc.mem_write(0xE000E000, b'\x00' * 0x1000)
    writes = []
    def hw(u_, acc, addr, size, val, usr):
        if addr >= 0x20017F00:   # стек отбрасываем
            writes.append((addr, val))
    h1 = uc.hook_add(UC_HOOK_MEM_WRITE, hw)   # всё пространство
    try:
        r0, _ = run.call(0x1C1AC, [], max_insn=100000)
    finally:
        uc.hook_del(h1)
    assert r0 == 0, f'r0={r0:#x}'
    seq = [(a, v) for a, v in writes if not (0x20017F00 <= a < 0x20018000)]
    assert len(seq) == 11, f'записей={len(seq)}: {seq}'
    # порядок: src → dst → ctrl → enable-группа → ctrl |= 1 → IRQ
    assert seq[0] == (0x40020004, 1)
    assert seq[1] == (0x40020100, 0x40012450), f'src={seq[1]}'
    assert seq[2] == (0x40020104, 0x20001692), f'dst={seq[2]}'
    assert seq[3] == (0x40020108, 0x5D000041)
    assert seq[4] == (0x40020028, 1) and seq[5] == (0x40020014, 1)
    assert seq[6] == (0x40020070, 0x19) and seq[7] == (0x40020050, 1)
    assert seq[8] == (0x40020108, 0x5D000041), 'ctrl |= 1 (bit0 уже стоит — значение не меняется)'
    # IRQ-хвост: ядро + NVIC
    assert seq[9] == (0xE000E100, 0x200), f'IRQ enable={seq[9]}'
    assert seq[10] == (0xE000E408, 0), f'NVIC+0x08={seq[10]}'


# ---------------------------------------------------------------------------
# §59.6: RX-парсер USART3 0x1E9E0 (вызывающий — периодический таск 0x1DFD8)
#
# Контракт (эмпирически):
# - state = byte[RAM+0x172]: 0 → только RAM+0x171=0; 1 → обработать 1 сообщение
# - head = byte[RAM+0x2C0] (кольцо 3 слота × 150 B @RAM+0x881), байт команды = ring[head*150+1]
# - toggle = byte[RAM+0x2C9] (0..7): индекс context-слота @RAM+0x10B5 + i*0x76
# - dispatch по ASCII: '@'→только head++; 'G'/'K'/'c'→frame-start (len 20/27/83);
#   'A'→telemetry-snapshot; 'a' и др. → response-сборщики
# - context: {6,'e',len,'O','K',crc,0x9A} (frame-start) или {'d'-кадры}
# - crc = сумма байтов context[1..] mod 256; checksum = 0xFF - context[1]
# - после обработки: state=0, head++ (wrap при ≥3), toggle++ (wrap при ≥8, frame-start)
#
# Методич. (§59.6.3): на этом чипе Bcond-кодировка D0xx = BEQ c imm8 в [7:0]
# (не стандартный ARM [11:4]); capstone декодирует цели верно, но метки cond — нет.
# ---------------------------------------------------------------------------

def _parser_probe(run, state=1, head=0, toggle=0, byte=0, slot_data=None):
    """засеять состояние парсера и прогнать; вернуть список записей (off, val) в RAM"""
    uc = run.uc
    uc.mem_write(RAM + 0x172, bytes([state]))
    uc.mem_write(RAM + 0x2C0, bytes([head]))
    uc.mem_write(RAM + 0x2C9, bytes([toggle]))
    uc.mem_write(RAM + 0x882 + head * 150, bytes([byte]))
    if slot_data:
        for off, v in slot_data.items():
            uc.mem_write(RAM + 0x881 + head * 150 + off, bytes([v]))
    ev = []
    def hw(u_, acc, addr, size, val, usr):
        if RAM <= addr < RAM + 0x20000 and not (0x20017F00 <= addr < 0x20018000):
            ev.append((addr - RAM, val))
    h = uc.hook_add(UC_HOOK_MEM_WRITE, hw, None, RAM, RAM + 0x20000)
    try:
        run.call(0x1E9E0, [], max_insn=50000)
    finally:
        uc.hook_del(h)
    return ev


def _ctx(run, slot, n=13):
    """context-слот @RAM+0x10B5 + slot*0x96 (n байтов; stride = размер ring-слота)"""
    base = RAM + 0x10B5 + slot * 0x96
    return bytes(run.uc.mem_read(base, n))


@t(0x1E9E0, '§59.6: RX-парсер USART3 — dispatch-каркас: state=0 → только RAM+0x171=0; state=1 + неизвестный байт → RAM+0x171=0, state→0, head 0→1; "G" frame-start (toggle=0): context @0x10B5 = {6,"e",20,"O","K",0x13,0x9A}, CRC-структ {idx=5,crc=0x13,sum=0x9A}, флаг RAM+0x310=0, toggle 0→1, head 0→1; "G" (toggle=7): context @0x14CF, toggle 8→0 (wrap)')
def _(run, rng):
    # state=0: только RAM+0x171=0
    ev = _parser_probe(run, state=0, byte=0x47)
    assert ev == [(0x171, 0)], f'state=0: {ev}'
    # неизвестный байт (0x00): минимальные записи
    ev = _parser_probe(run, state=1, head=0, byte=0x00)
    assert ev == [(0x171, 0), (0x172, 0), (0x2C0, 1)], f'неизв. байт: {ev}'
    # "G" frame-start, toggle=0
    ev = _parser_probe(run, state=1, head=0, toggle=0, byte=0x47)
    got = dict(ev)
    assert got.get(0x310) == 0, f'флаг G: {ev}'
    assert got.get(0x2C9) == 1, f'toggle: {ev}'
    assert got.get(0x2C0) == 1, f'head: {ev}'
    assert got.get(0x172) == 0, f'state: {ev}'
    ctx = _ctx(run, 0)
    assert ctx[:7] == bytes([6, 0x65, 20, 0x4F, 0x4B, 0x13, 0x9A]), f'context G: {ctx.hex(" ")}'
    # CRC-структ @RAM+0x177: idx=5, crc=0x13, sum=0x9A
    assert got.get(0x177) == 5 and got.get(0x178) == 0x13 and got.get(0x179) == 0x9A, f'crc-структ: {ev}'
    # "G" frame-start, toggle=7 → слот 7, wrap toggle 8→0
    ev = _parser_probe(run, state=1, head=0, toggle=7, byte=0x47)
    tw = [v for a, v in ev if a == 0x2C9]
    assert tw == [8, 0], f'toggle wrap: {tw}'
    ctx7 = _ctx(run, 7)
    assert ctx7[:7] == bytes([6, 0x65, 20, 0x4F, 0x4B, 0x13, 0x9A]), f'context G slot7: {ctx7.hex(" ")}'


@t(0x1E9E0, '§59.6: RX-парсер — "A" telemetry-snapshot: ring[3..9] → RAM+0x2E8/9 (rev16(ring4<<8|ring3)), 0x2EA/EB (нибблы ring5), 0x2EC=ring6, ring7 → {bit7→0x2ED, bit6→0x2EE, [5:0]→0x2EF}, 0x2F0=ring8, 0x2F1=ring9; context = {0xC,"d",0x20,7,ring3..9,crc,0x9B}; crc=(0x64+0x20+7+Σring[3..9])&0xFF')
def _(run, rng):
    data = {i: 0x10 + i for i in range(3, 10)}   # ring[3..9] = 0x13..0x19
    ev = _parser_probe(run, state=1, head=0, byte=0x41, slot_data=data)
    uc = run.uc
    def rd(off):
        return uc.mem_read(RAM + off, 1)[0]
    # rev16: u16 LE @0x2E8 = rev16((ring4<<8)|ring3) = rev16(0x1413) = 0x1314
    assert (rd(0x2E8), rd(0x2E9)) == (0x14, 0x13), f'rev16: {rd(0x2E8):#x},{rd(0x2E9):#x}'
    assert rd(0x2EA) == 5 and rd(0x2EB) == 1, f'нибблы ring5: {rd(0x2EA):#x},{rd(0x2EB):#x}'
    assert rd(0x2EC) == 0x16, f'ring6: {rd(0x2EC):#x}'
    # ring7 = 0x17: bit7=0, bit6=0, [5:0]=0x17
    assert rd(0x2ED) == 0 and rd(0x2EE) == 0 and rd(0x2EF) == 0x17, f'ring7-сплит: {rd(0x2ED):#x},{rd(0x2EE):#x},{rd(0x2EF):#x}'
    assert rd(0x2F0) == 0x18 and rd(0x2F1) == 0x19, f'ring8/9: {rd(0x2F0):#x},{rd(0x2F1):#x}'
    # context: {0xC,'d',0x20,7,data[0..6],crc,checksum}
    ctx = _ctx(run, 0)
    assert ctx[0] == 0x0C and ctx[1] == 0x64 and ctx[2] == 0x20 and ctx[3] == 7
    assert ctx[4:11] == bytes([0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19]), f'data: {ctx.hex(" ")}'
    crc = (0x64 + 0x20 + 7 + sum(range(0x13, 0x1A))) & 0xFF   # = 0x25
    assert ctx[11] == crc == 0x25, f'crc: {ctx[11]:#x} (ожидалось {crc:#x})'
    assert ctx[12] == 0x9B, f'checksum: {ctx[12]:#x}'
    # toggle и head
    got = dict(ev)
    assert got.get(0x2C9) == 1 and got.get(0x2C0) == 1 and got.get(0x172) == 0


# ---------------------------------------------------------------------------
# §59.7: «own» round 0x1DD8C (128 B, bl из 0x1a814) — один раунд шифра «own»
#
# Буфер 16 B = 4 группы × 4 байта; каждая группа [A,B,C,D] смешивается
# независимо через CRC-8 (полином 0x1B, MSB-first) как Feistel:
#   X  = A^B^C^D
#   A' = A ^ crc8(A^B) ^ X
#   B' = B ^ crc8(B^C) ^ X
#   C' = C ^ crc8(C^D) ^ X
#   D' = D ^ crc8(D^A) ^ X
# где crc8(x) = ((x<<1) ^ (0x1B & -(x>>7))) & 0xFF (один шаг CRC-8).
# Чистая функция: все обращения к памяти — относительно r0 (буфер),
# без pool/абсолютных RAM-адресов.
# ---------------------------------------------------------------------------

def ref_crc8_step(x):
    return ((x << 1) ^ (0x1B & -(x >> 7))) & 0xFF


def ref_own_round(buf16):
    b = bytearray(buf16)
    for i in range(4):
        g = i * 4
        A, B, C, D = b[g], b[g + 1], b[g + 2], b[g + 3]
        X = A ^ B ^ C ^ D
        b[g + 0] = A ^ ref_crc8_step(A ^ B) ^ X
        b[g + 1] = B ^ ref_crc8_step(B ^ C) ^ X
        b[g + 2] = C ^ ref_crc8_step(C ^ D) ^ X
        b[g + 3] = D ^ ref_crc8_step(D ^ A) ^ X
    return bytes(b)


@t(0x1DD8C, '§59.7: «own» round — 16 B = 4×4 байта; каждая группа [A,B,C,D]: X=A^B^C^D; A''=A^crc8(A^B)^X, B''=B^crc8(B^C)^X, C''=C^crc8(C^D)^X, D''=D^crc8(D^A)^X; crc8(x)=((x<<1)^(0x1B&-(x>>7)))&0xFF (CRC-8 poly 0x1B MSB-first); чистая функция от буфера в r0')
def _(run, rng):
    buf_off = 0x1F000
    for _ in range(32):
        data = bytes(rng.randrange(256) for _ in range(16))
        exp = ref_own_round(data)
        run.ram_write(buf_off, data)
        run.call(0x1DD8C, (RAM + buf_off,), max_insn=20000)
        got = run.ram_read(buf_off, 16)
        assert got == exp, f'own_round:\n in : {data.hex(" ")}\n exp: {exp.hex(" ")}\n got: {got.hex(" ")}'
    # детерминированный якорь: все нули → все нули (X=0, crc8(0)=0)
    run.ram_write(buf_off, b'\x00' * 16)
    run.call(0x1DD8C, (RAM + buf_off,), max_insn=20000)
    assert run.ram_read(buf_off, 16) == b'\x00' * 16, 'нули должны остаться нулями'


# ---------------------------------------------------------------------------
# §59.8: периодический таск USART3 0x1DFD8 (344 B) — inline-логика верифицирована
#
# Тело: u16 tick-счётчик @RAM+0x2BA++ → 3 «утечных интегратора» с обратной
# связью → расчёт % батареи (линейная карта) → вызовы 0x1E9E0/0x1F1CC/
# 0x1F71C/0x211F8 (+ 0x1B67C/0x2186C на старте) → главный u32-счётчик @RAM+0x314++.
#
# Верификация изолирует INLINE-логику: 6 `bl` патчатся в NOP (свежий Run —
# общий не портится). Подфункции верифицируются отдельно (0x1E9E0 — §59.6).
#
# Интегратор (3 шт, пары acc/delta/out):
#   new_acc = (acc + delta - old_out) & 0xFFFFFFFF
#   new_out = asr(new_acc, 5)  (s16)
#   пары: (0x298/0x278/0x27A), (0x288/0x284/0x286), (0x2A0/0x29C/0x29E)
#
# % батареи: level = s16[RAM+0x1794 + 12] (элемент 6 массива @RAM+0x1794):
#   level >= 535 → 100;  level < 415 → 0;  иначе (level-415)*100/120 (signed div)
#   (активный диапазон [415,535] → [0,100]); результат в byte[RAM+0x306].
#   Гейт: вычисляется если flag byte[RAM+0x321]==1 ИЛИ u16[RAM+0x312] >= 30000
#   (тогда flag:=1); иначе — только инкремент u16[RAM+0x312].
# ---------------------------------------------------------------------------

DFD8_BLS = [0x1dfda, 0x1dfe6, 0x1e0ae, 0x1e0b2, 0x1e0cc, 0x1e0d0]
DFD8_NOP4 = b'\x00\xbf\x00\xbf'


def _dfd8_asr(v, n):
    """арифметический сдвиг u32 вправо на n, результат как signed s16"""
    v &= 0xFFFFFFFF
    if v & 0x80000000:
        v -= 0x100000000
    r = (v >> n) & 0xFFFF
    return r - 0x10000 if r >= 0x8000 else r


def ref_dfd8_integ(acc, delta_s16, out_s16):
    na = (acc + delta_s16 - out_s16) & 0xFFFFFFFF
    return na, _dfd8_asr(na, 5)


def ref_dfd8_batpct(level):
    if level >= 535:
        return 100
    if level < 415:
        return 0
    return ((level - 415) * 100) // 120


@t(0x1DFD8, '§59.8: периодический таск USART3 — inline-логика (6 bl патч в NOP, save/restore): u16 tick @0x2BA++; 3 интегратора new_acc=(acc+delta-out)&0xFFFFFFFF, new_out=asr(new_acc,5) s16 (пары 0x298/0x278/0x27A, 0x288/0x284/0x286, 0x2A0/0x29C/0x29E); % батареи из level=s16[0x1794+12]: >=535→100, <415→0, иначе (level-415)*100//120 в byte[0x306]; главный u32 @0x314++')
def _(run, rng):
    uc = run.uc
    S16 = {0x278, 0x284, 0x29C, 0x27A, 0x286, 0x29E}
    INTEG = [(0x298, 0x278, 0x27A), (0x288, 0x284, 0x286), (0x2A0, 0x29C, 0x29E)]
    # сохранить оригинальные байты 6 bl и патчить в NOP (изоляция inline-логики)
    orig = [bytes(uc.mem_read(FLASH0 + b, 4)) for b in DFD8_BLS]
    try:
        for b in DFD8_BLS:
            uc.mem_write(FLASH0 + b, DFD8_NOP4)

        def seed(off, fmt, v):
            uc.mem_write(RAM + off, struct.pack(fmt, v))

        # --- 20 случайных наборов: интеграторы + счётчики ---
        for _ in range(20):
            seeds = {
                0x2BA: rng.randrange(0, 0xFFFF),
                0x314: rng.randrange(0, 0x1D4CA),
                0x312: rng.randrange(0, 30000),
            }
            for acc_o, del_o, out_o in INTEG:
                seeds[acc_o] = rng.getrandbits(32)
                seeds[del_o] = rng.randrange(-32768, 32767)
                seeds[out_o] = rng.randrange(-32768, 32767)
            for off, v in seeds.items():
                if off in S16:
                    seed(off, '<h', v)
                elif off in (0x2BA, 0x312):
                    seed(off, '<H', v)
                else:
                    seed(off, '<I', v)
            uc.mem_write(RAM + 0x321, b'\x00')   # flag=0 → только инкремент u16[0x312]
            run.call(0x1DFD8, [], max_insn=200000)
            got_tick = struct.unpack_from('<H', uc.mem_read(RAM + 0x2BA, 2), 0)[0]
            assert got_tick == (seeds[0x2BA] + 1) & 0xFFFF, f'tick: {got_tick:#x}'
            got_u32 = struct.unpack_from('<I', uc.mem_read(RAM + 0x314, 4), 0)[0]
            assert got_u32 == seeds[0x314] + 1, f'u32: {got_u32:#x}'
            got_bat = struct.unpack_from('<H', uc.mem_read(RAM + 0x312, 2), 0)[0]
            assert got_bat == seeds[0x312] + 1, f'bat-cnt: {got_bat:#x}'
            for acc_o, del_o, out_o in INTEG:
                ea, eo = ref_dfd8_integ(seeds[acc_o], seeds[del_o], seeds[out_o])
                ga = struct.unpack_from('<I', uc.mem_read(RAM + acc_o, 4), 0)[0]
                go = struct.unpack_from('<h', uc.mem_read(RAM + out_o, 2), 0)[0]
                assert (ga, go) == (ea, eo), (
                    f'integ acc@{acc_o:#x}: exp ({ea},{eo}) got ({ga},{go}) '
                    f'from acc={seeds[acc_o]:#x} d={seeds[del_o]} o={seeds[out_o]}')

        # --- % батареи: принудительный compute (flag=1), линейная карта ---
        for level in [0, 300, 414, 415, 416, 417, 435, 500, 511, 534, 535, 700, 1000, -50]:
            uc.mem_write(RAM + 0x312, struct.pack('<H', 100))   # < 30000
            uc.mem_write(RAM + 0x321, b'\x01')                    # flag=1 → compute
            uc.mem_write(RAM + 0x1794 + 12, struct.pack('<h', level))
            run.call(0x1DFD8, [], max_insn=200000)
            got = uc.mem_read(RAM + 0x306, 1)[0]
            exp = ref_dfd8_batpct(level) & 0xFF
            assert got == exp, f'bat% level={level}: exp {exp} got {got}'
    finally:
        for b, o in zip(DFD8_BLS, orig):
            uc.mem_write(FLASH0 + b, o)


# ---------------------------------------------------------------------------
# §60: 0x1be1c — TIM capture → FOC реконструкция фазных токов (подфункция 0x1A938)
#
# Аргумент: r0 = указатель на struct. Гейт: бит15 низких 16 бит u32[0x40012C54]
# (= TIMER_A+0x14): ==0 → режим 1, ==1 → режим 2.
#
# Режим 1 (гейт положит.): OUT @RAM+0x838/0x83C/0x840 = clamp(r0[+0xc/+0x10/+0x14]).
#
# Режим 2 (гейт отрицат.): dispatch по u16[r0+2] (сектор) через computed-goto
# 0x21b52 (byte jump-table, count=7, idx≥7 → table[7]=null):
#   0→null, 1→B, 2/3→C, 4/5→A, 6→B, ≥7→null.
# Хендлеры (T28/T2C/T30 = u32[0x40012440+0x28/0x2c/0x30], C18/C1A/C1C = u16[r0+0x18/0x1a/0x1c]):
#   A: o_c=(T28-C18)<<4, o_10=(T2C-C1A)<<4, o_14=-(o_c+o_10)
#   B: o_10=(T2C-C1A)<<4, o_14=(T30-C1C)<<4, o_c=-(o_10+o_14)
#   C: o_c=(T28-C18)<<4, o_14=(T30-C1C)<<4, o_10=-(o_c+o_14)
# null: r0[+0xc..] не меняются. Затем OUT = clamp(o_c,o_10,o_14) в [-30000,30000].
# ---------------------------------------------------------------------------

TIMER_A_GATE = 0x40012C54      # u32[0x40012C40+0x14] — гейт (бит15 низких 16)
TIMER_B = 0x40012440           # база таблицы capture (+0x28/+0x2c/+0x30)
FOC_OUT = 0x838                # OUT @RAM+0x838/0x83C/0x840


def ref_foc_clamp(v):
    return max(-30000, min(30000, v))


def ref_1be1c(gate_low16, r0vals, sector, T, C):
    """r0vals=(o_c,o_10,o_14) начальные; T=(T28,T2C,T30); C=(C18,C1A,C1C)"""
    if (gate_low16 & 0x8000) == 0:
        return tuple(ref_foc_clamp(v) for v in r0vals)
    i = sector if sector < 7 else 7
    h = [None, 'B', 'C', 'C', 'A', 'A', 'B', None][i]
    oc, o10, o14 = r0vals
    if h == 'A':
        oc = (T[0] - C[0]) << 4; o10 = (T[1] - C[1]) << 4; o14 = -(oc + o10)
    elif h == 'B':
        o10 = (T[1] - C[1]) << 4; o14 = (T[2] - C[2]) << 4; oc = -(o10 + o14)
    elif h == 'C':
        oc = (T[0] - C[0]) << 4; o14 = (T[2] - C[2]) << 4; o10 = -(oc + o14)
    return ref_foc_clamp(oc), ref_foc_clamp(o10), ref_foc_clamp(o14)


@t(0x1BE1C, '§60: TIM capture → FOC реконструкция фазных токов (подфункция 0x1A938): гейт = бит15 низких16 u32[0x40012C54]; режим1(=0) OUT@RAM+0x838=clamp(r0[+0xc/+0x10/+0x14]); режим2(=1) dispatch u16[r0+2] (0→null,1→B,2/3→C,4/5→A,6→B,≥7→null), хендлер A/B/C: две фазы (T-C)<<4 из u32[0x40012440+{28,2c,30}]-u16[r0+{18,1a,1c}], третья=-(сумма), clamp [-30000,30000]')
def _(run, rng):
    uc = run.uc
    S = 0x1F000   # r0-структ в RAM
    # --- режим 1: гейт положит. (бит15=0), clamp+copy ---
    for _ in range(16):
        gate = rng.getrandbits(16) & 0x7FFF   # бит15=0
        vals = tuple(rng.randrange(-40000, 40000) for _ in range(3))
        uc.mem_write(TIMER_A_GATE, struct.pack('<I', gate & 0xFFFFFFFF))
        uc.mem_write(RAM + S + 0x0c, struct.pack('<i', vals[0]))
        uc.mem_write(RAM + S + 0x10, struct.pack('<i', vals[1]))
        uc.mem_write(RAM + S + 0x14, struct.pack('<i', vals[2]))
        run.call(0x1BE1C, (RAM + S,), max_insn=50000)
        got = tuple(struct.unpack_from('<i', uc.mem_read(RAM + FOC_OUT + i * 4, 4), 0)[0] for i in range(3))
        exp = ref_1be1c(gate, vals, 0, (0, 0, 0), (0, 0, 0))
        assert got == exp, f'режим1: gate={gate:#x} vals={vals} got={got} exp={exp}'
    # --- режим 2: гейт отрицат. (бит15=1), dispatch + хендлеры ---
    for _ in range(40):
        gate = 0x8000 | (rng.getrandbits(16) & 0x7FFF)   # бит15=1
        T = tuple(rng.randrange(0, 2000) for _ in range(3))
        C = tuple(rng.randrange(0, 500) for _ in range(3))
        init = tuple(rng.randrange(-40000, 40000) for _ in range(3))   # для null-кейса
        sector = rng.randrange(0, 9)
        uc.mem_write(TIMER_A_GATE, struct.pack('<I', gate & 0xFFFFFFFF))
        uc.mem_write(TIMER_B + 0x28, struct.pack('<I', T[0]))
        uc.mem_write(TIMER_B + 0x2c, struct.pack('<I', T[1]))
        uc.mem_write(TIMER_B + 0x30, struct.pack('<I', T[2]))
        uc.mem_write(RAM + S + 0x18, struct.pack('<H', C[0] & 0xFFFF))
        uc.mem_write(RAM + S + 0x1a, struct.pack('<H', C[1] & 0xFFFF))
        uc.mem_write(RAM + S + 0x1c, struct.pack('<H', C[2] & 0xFFFF))
        uc.mem_write(RAM + S + 0x0c, struct.pack('<i', init[0]))
        uc.mem_write(RAM + S + 0x10, struct.pack('<i', init[1]))
        uc.mem_write(RAM + S + 0x14, struct.pack('<i', init[2]))
        uc.mem_write(RAM + S + 0x02, struct.pack('<H', sector & 0xFFFF))
        run.call(0x1BE1C, (RAM + S,), max_insn=50000)
        got = tuple(struct.unpack_from('<i', uc.mem_read(RAM + FOC_OUT + i * 4, 4), 0)[0] for i in range(3))
        exp = ref_1be1c(gate, init, sector, T, C)
        assert got == exp, f'режим2: sector={sector} T={T} C={C} init={init} got={got} exp={exp}'


# ---------------------------------------------------------------------------
# §60.1: 0x1e410 — табличная декодировка Q15-вектора (подфункция FOC)
# Аргумент r0 = u32 A. Ветвь b=A[15:14]; i1=(A>>6)&0xFF; i2=(0xFF−i1)&0xFF.
# t1=s16[TBL[i1]], t2=s16[TBL[i2]] (TBL = 256×u16 @flash 0xA6C6). По ветви:
#   b0: lo=−t2, hi=−t1   b1: lo=t1, hi=−t2   b2: lo=t2, hi=t1   b3: lo=−t1, hi=t2
# Возврат u32 = (hi<<16)|lo. (4-квадрантная знаковая инверсия одной пары.)
# ---------------------------------------------------------------------------

FOC_TBL_OFF = 0xA6C6   # flash-offset таблицы 256×u16 (FLASH0 base)


def _foc_tbl(uc):
    raw = uc.mem_read(FLASH0 + FOC_TBL_OFF, 512)
    return list(struct.unpack('<256h', raw))


def ref_1e410(A, tbl):
    b = (A >> 14) & 3
    i1 = (A >> 6) & 0xFF
    i2 = (0xFF - i1) & 0xFF
    t1, t2 = tbl[i1], tbl[i2]
    if b == 0: lo, hi = -t2, -t1
    elif b == 1: lo, hi = t1, -t2
    elif b == 2: lo, hi = t2, t1
    else: lo, hi = -t1, t2
    return ((hi & 0xFFFF) << 16) | (lo & 0xFFFF)


def _s16(v):
    v &= 0xFFFF
    return v - 0x10000 if (v & 0x8000) else v


def _asr32(v, n):
    s = v if (v & 0x80000000) == 0 else (v - 0x100000000)
    return s >> n


def _div15(p):
    """значное деление /2^15 с округлением: if p<0 → p+=0x7FFF; asr 15"""
    pu = p & 0xFFFFFFFF
    if p < 0:
        pu = (pu + 0x7FFF) & 0xFFFFFFFF
    return _asr32(pu, 15)


def ref_1d7ac(arg0, arg1, tbl):
    """cross+dot двух Q15-векторов: X=0x1e410(arg1), A=arg0."""
    X = ref_1e410(arg1, tbl)
    X_lo, X_hi = _s16(X), _s16(X >> 16)
    a_lo, a_hi = _s16(arg0), _s16(arg0 >> 16)
    P = _div15(X_hi * a_lo)   # a_lo·X_hi
    Q = _div15(X_lo * a_hi)   # a_hi·X_lo
    R = _div15(X_lo * a_lo)   # a_lo·X_lo
    S = _div15(X_hi * a_hi)   # a_hi·X_hi
    out_lo = (Q - P) & 0xFFFF   # cross: a_hi·X_lo − a_lo·X_hi
    out_hi = (R + S) & 0xFFFF   # dot:   a_lo·X_lo + a_hi·X_hi
    return (out_hi << 16) | out_lo


@t(0x1E410, '§60.1: табличная декодировка Q15-вектора (подфункция FOC): ветвь=A[15:14], i1=(A>>6)&0xFF, i2=~i1&0xFF; t1/t2=s16[TBL@flash0xA6C6[i]]; b0:(−t2,−t1) b1:(t1,−t2) b2:(t2,t1) b3:(−t1,t2) → u32=(hi<<16)|lo')
def _(run, rng):
    tbl = _foc_tbl(run.uc)
    for _ in range(60):
        A = rng.getrandbits(32)
        r0, _ = run.call(0x1E410, (A,), max_insn=50000)
        exp = ref_1e410(A, tbl)
        assert r0 == exp, f'0x1e410: A={A:#010x} got={r0:#010x} exp={exp:#010x}'


@t(0x1D7AC, '§60.1: cross+dot двух Q15-векторов (подфункция FOC): X=0x1e410(arg1), A=arg0; lo=cross(a_hi·X_lo−a_lo·X_hi), hi=dot(a_lo·X_lo+a_hi·X_hi); каждое произведение /2^15 с округлением (p<0→+0x7FFF)')
def _(run, rng):
    tbl = _foc_tbl(run.uc)
    for _ in range(60):
        a0 = rng.getrandbits(32); a1 = rng.getrandbits(32)
        r0, _ = run.call(0x1D7AC, (a0, a1), max_insn=50000)
        exp = ref_1d7ac(a0, a1, tbl)
        assert r0 == exp, f'0x1d7ac: a0={a0:#010x} a1={a1:#010x} got={r0:#010x} exp={exp:#010x}'


# ---------------------------------------------------------------------------
# §60.2: 0x1bd88 — 6-секторный FOC-классификатор (подфункция 0x1A938)
# Аргументы: arg0=r0 = struct вывода (u16[r0+2]=сектор), arg1=r1 = указатель на
# два s16: x0=s16[r1+0], x2=s16[r1+2]. Гейт: бит15 низких16 u32[0x40012C54]
# (TIMER_A+0x14, тот же что в 0x1be1c): ==0 → обход (сектор не пишется).
# A=0x3ce4, B=0x2328 (pool). S=rnd((B·x2+A·x0)/2), D=rnd((B·x2−A·x0)/2),
# rnd(V)=(V−1 if V<0 else V)>>1; r2=B·x2. Сектор по знакам:
#   S<0,D<0→5 ; S<0,D≥0→(3 if r2>0 else 4) ; S≥0,D<0→(1 if r2>0 else 6) ; S≥0,D≥0→2
# ---------------------------------------------------------------------------

BD88_GATE = 0x40012C54   # TIMER_A + 0x14 (гейт, бит15 низких 16)
BD88_A = 0x3CE4
BD88_B = 0x2328


def _rnd2(V):
    if V < 0:
        V -= 1
    return _asr32(V & 0xFFFFFFFF, 1)


def ref_1bd88(gate_low16, x0, x2):
    """вернёт сектор (1..6) или None если гейт положит. (обход)"""
    if (gate_low16 & 0x8000) == 0:
        return None
    S = _rnd2(BD88_B * x2 + BD88_A * x0)
    D = _rnd2(BD88_B * x2 - BD88_A * x0)
    r2 = BD88_B * x2
    if S < 0:
        return 5 if D < 0 else (3 if r2 > 0 else 4)
    else:
        return 1 if (D < 0 and r2 > 0) else (6 if D < 0 else 2)


@t(0x1BD88, '§60.2: 6-секторный FOC-классификатор (подфункция 0x1A938): гейт=бит15 низких16 u32[0x40012C54] (=0→обход); x0=s16[r1+0], x2=s16[r1+2]; S=rnd((B·x2+A·x0)/2), D=rnd((B·x2−A·x0)/2) A=0x3ce4 B=0x2328 rnd(V)=(V−1 if V<0 else V)>>1; u16[r0+2]=сектор: S<0,D<0→5 / S<0,D≥0→(r2>0?3:4) / S≥0,D<0→(r2>0?1:6) / S≥0,D≥0→2, r2=B·x2')
def _(run, rng):
    uc = run.uc
    S_IN = 0x1F000; S_OUT = 0x1F100
    for _ in range(60):
        gate = rng.getrandbits(16)
        x0 = rng.randrange(-400, 400); x2 = rng.randrange(-400, 400)
        uc.mem_write(BD88_GATE, struct.pack('<I', gate))
        uc.mem_write(RAM + S_IN + 0, struct.pack('<h', x0))
        uc.mem_write(RAM + S_IN + 2, struct.pack('<h', x2))
        uc.mem_write(RAM + S_OUT + 2, struct.pack('<H', 0xEEEE))   # sentinel
        run.call(0x1BD88, (RAM + S_OUT, RAM + S_IN), max_insn=50000)
        got = struct.unpack_from('<H', uc.mem_read(RAM + S_OUT + 2, 2), 0)[0]
        exp = ref_1bd88(gate, x0, x2)
        if exp is None:
            assert got == 0xEEEE, f'обход: gate={gate:#06x} x0={x0} x2={x2} got={got:#06x}'
        else:
            assert got == exp, f'сектор: gate={gate:#06x} x0={x0} x2={x2} got={got} exp={exp}'


# ---------------------------------------------------------------------------
# §60.3: 0x1d818 — cross+dot (двойник 0x1d7ac, но X из RAM, не из таблицы)
# Аргумент: arg0=r0 = A=(a_lo,a_hi) Q15. Вектор X = (X_lo,X_hi) из RAM:
#   X_lo=s16[RAM+0x10c], X_hi=s16[RAM+0x10e] (база r6 = pool @flash 0x1d870).
# Вычисление идентично 0x1d7ac: lo=cross(a_hi·X_lo−a_lo·X_hi), hi=dot(a_lo·X_lo
# +a_hi·X_hi); каждое произведение /2^15 с округлением (p<0→+0x7FFF).
# ---------------------------------------------------------------------------

D818_XLO = 0x10C   # RAM-offset X_lo
D818_XHI = 0x10E   # RAM-offset X_hi


def ref_1d818(arg0, X_lo, X_hi):
    a_lo, a_hi = _s16(arg0), _s16(arg0 >> 16)
    P = _div15(X_hi * a_lo); Q = _div15(X_lo * a_hi)
    R = _div15(X_lo * a_lo); S = _div15(X_hi * a_hi)
    return ((R + S) & 0xFFFF) << 16 | ((Q - P) & 0xFFFF)


@t(0x1D818, '§60.3: cross+dot (двойник 0x1d7ac, X из RAM): A=arg0 Q15, X=(s16[RAM+0x10c], s16[RAM+0x10e]); lo=cross(a_hi·X_lo−a_lo·X_hi), hi=dot(a_lo·X_lo+a_hi·X_hi); каждое /2^15 с округлением')
def _(run, rng):
    uc = run.uc
    for _ in range(60):
        arg0 = rng.getrandbits(32)
        X_lo = rng.randrange(-300, 300); X_hi = rng.randrange(-300, 300)
        uc.mem_write(RAM + D818_XLO, struct.pack('<h', X_lo))
        uc.mem_write(RAM + D818_XHI, struct.pack('<h', X_hi))
        r0, _ = run.call(0x1D818, (arg0,), max_insn=50000)
        exp = ref_1d818(arg0, X_lo, X_hi)
        assert r0 == exp, f'0x1d818: arg0={arg0:#010x} X=({X_lo},{X_hi}) got={r0:#010x} exp={exp:#010x}'


# ---------------------------------------------------------------------------
# §60.4: 0x1b3f2..0x1b460 — inline-блок FOC (inlined cross+dot) внутри 0x1A938
# Входы (по трассировке, НЕ capstone pool-offsets): P=u32[RAM+0x388],
# X_lo=s16[RAM+0x108], X_hi=s16[RAM+0x10a], R6=u32[RAM+0x3ac]. r4=RAM+0x040 (struct).
# Вычисления (muls + asrs#15):
#   cross = asr15(R6·X_hi) − asr15(P·X_lo)      → RAM+0x3b8
#   dot   = asr15(R6·X_lo) + asr15(P·X_hi)      → RAM+0x3bc
#   t1 = −(dot<<14)
#   r4+0x1c = asr15(t1 + 0x6ed9·cross)
#   r4+0x20 = asr15(t1 − 0x6ed9·cross)
#   r4+0x28 = dot>>1
#   r4+0x24 = asr15(0x376d·cross + (dot<<13))
# (тот же комплексный произведение, что 0x1d7ac/0x1d818, но inline)
# Верификация: mid-function jump в 0x1b3f2 с r4=RAM+0x040, stop в 0x1b48a.
# ---------------------------------------------------------------------------


def _asr15(v):
    s = v if (v & 0x80000000) == 0 else (v - 0x100000000)
    return s >> 15


def ref_1b3f2(P, X_lo, X_hi, R6):
    cross = _asr15((R6 * X_hi) & 0xFFFFFFFF) - _asr15((P * X_lo) & 0xFFFFFFFF)
    dot = _asr15((R6 * X_lo) & 0xFFFFFFFF) + _asr15((P * X_hi) & 0xFFFFFFFF)
    t1 = -(dot << 14)
    out = [cross, dot,
           _asr15((t1 + 0x6ED9 * cross) & 0xFFFFFFFF),
           _asr15((t1 - 0x6ED9 * cross) & 0xFFFFFFFF),
           dot >> 1,
           _asr15((0x376D * cross + (dot << 13)) & 0xFFFFFFFF)]
    return out


@t(0x1B3F2, '§60.4: inline-блок FOC в 0x1A938 (inlined cross+dot): P=u32[RAM+0x388], X_lo=s16[RAM+0x108], X_hi=s16[RAM+0x10a], R6=u32[RAM+0x3ac]; cross=asr15(R6·Xhi)−asr15(P·Xlo)→RAM+0x3b8, dot=asr15(R6·Xlo)+asr15(P·Xhi)→RAM+0x3bc; r4+0x1c/0x20=asr15(∓t1±0x6ed9·cross), r4+0x28=dot>>1, r4+0x24=asr15(0x376d·cross+dot<<13); верификация mid-function jump (r4=RAM+0x040, stop 0x1b48a)')
def _(run, rng):
    uc = run.uc
    for _ in range(40):
        P = rng.getrandbits(32) & 0x7FFFFFFF
        X_lo = rng.randrange(-500, 500); X_hi = rng.randrange(-500, 500)
        R6 = rng.getrandbits(20)
        uc.mem_write(RAM, bytes(0x20000))
        uc.mem_write(RAM + 0x388, struct.pack('<I', P))
        uc.mem_write(RAM + 0x108, struct.pack('<h', X_lo))
        uc.mem_write(RAM + 0x10a, struct.pack('<h', X_hi))
        uc.mem_write(RAM + 0x3ac, struct.pack('<i', R6))
        uc.reg_write(UC_ARM_REG_SP, STACK_TOP)
        uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        uc.reg_write(UC_ARM_REG_R4, RAM + 0x040)
        run.emu.insn = 0
        try:
            uc.emu_start(0x1B3F2 | 1, 0x1B48A | 1, count=200)
        except UcError:
            pass
        got = [struct.unpack_from('<i', uc.mem_read(RAM + o, 4), 0)[0]
               for o in (0x3b8, 0x3bc, 0x5c, 0x60, 0x68, 0x64)]
        exp = ref_1b3f2(P, X_lo, X_hi, R6)
        assert got == exp, f'0x1b3f2: P={P} Xlo={X_lo} Xhi={X_hi} R6={R6} got={got} exp={exp}'


# ---------------------------------------------------------------------------
# §60.5: 0x1aa08..0x1aae6 — inline-блок FOC в 0x1A938: обработка/кламп моторных
# параметров + leaky-интегратор. Зависит от live-in регистров (r4=RAM+0x040 base,
# r5=RAM+0x108, r6=0x2033) и stack-frame ([sp+0x18]=base). Изоляция: mid-function
# jump в 0x1aa08 с этими регистрами + [sp+0x18]=RAM+0x040, stop в 0x1abd4.
# Верифицированные операции (ключевые из ~13 выходов):
#   (1) u16[RAM+0x044] = lo16(r0)          — store результата cross+dot (из bl 0x1d7ac)
#   (2) u16[RAM+0x38c] = clamp(−s16[RAM+0x0a6], ±s16[RAM+0x390])  — симм. кламп
#   (3) leaky-интегратор: acc=u32[RAM+0x094] (new=acc+delta−old_out),
#       u16[RAM+0x046] = asr(acc_new, 5)   — тот же паттерн, что 0x1DFD8 (§59.8)
# ---------------------------------------------------------------------------


def _asr5(v):
    s = v if (v & 0x80000000) == 0 else (v - 0x100000000)
    return s >> 5


@t(0x1AA08, '§60.5: inline-блок FOC в 0x1A938 — обработка/кламп параметров + leaky-интегратор. (1) u16[RAM+0x044]=lo16(r0=cross+dot); (2) u16[RAM+0x38c]=clamp(−s16[RAM+0x0a6],±s16[RAM+0x390]); (3) интегратор acc=u32[RAM+0x094]: u16[RAM+0x046]=asr(acc_new,5) (паттерн 0x1DFD8). Изоляция mid-function jump (r4=RAM+0x040, r5=RAM+0x108, r6=0x2033, [sp+0x18]=RAM+0x040, stop 0x1abd4)')
def _(run, rng):
    uc = run.uc
    for _ in range(60):
        r0val = rng.getrandbits(32)
        a0a6 = rng.randrange(-1000, 1000); limit = rng.randrange(1, 800); acc0 = rng.getrandbits(24)
        uc.mem_write(RAM, bytes(0x20000))
        uc.mem_write(RAM + 0x0a6, struct.pack('<h', a0a6))
        uc.mem_write(RAM + 0x390, struct.pack('<h', limit))
        uc.mem_write(RAM + 0x094, struct.pack('<i', acc0))
        SP = 0x20017F00
        uc.mem_write(SP + 0x18, struct.pack('<I', RAM + 0x040))
        uc.reg_write(UC_ARM_REG_SP, SP)
        uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        uc.reg_write(UC_ARM_REG_R0, r0val)
        uc.reg_write(UC_ARM_REG_R4, RAM + 0x040)
        uc.reg_write(UC_ARM_REG_R5, RAM + 0x108)
        uc.reg_write(UC_ARM_REG_R6, 0x2033)
        run.emu.insn = 0
        try:
            uc.emu_start(0x1AA08 | 1, 0x1ABD4 | 1, count=200)
        except UcError:
            pass
        o44 = struct.unpack_from('<H', uc.mem_read(RAM + 0x044, 2), 0)[0]
        o38c = struct.unpack_from('<H', uc.mem_read(RAM + 0x38c, 2), 0)[0]
        o94 = struct.unpack_from('<i', uc.mem_read(RAM + 0x094, 4), 0)[0]
        o46 = struct.unpack_from('<H', uc.mem_read(RAM + 0x046, 2), 0)[0]
        assert o44 == (r0val & 0xFFFF), f'0x1aa08(1): r0={r0val:#x} got={o44} exp={r0val&0xFFFF}'
        cv = max(-limit, min(limit, -a0a6))
        assert o38c == (cv & 0xFFFF), f'0x1aa08(2): a0a6={a0a6} limit={limit} got={o38c} exp={cv&0xFFFF}'
        assert o46 == (_asr5(o94) & 0xFFFF), f'0x1aa08(3): acc={o94} got_out={o46} exp={_asr5(o94)&0xFFFF}'


# ---------------------------------------------------------------------------
# §60.6: 0x1b48a..0x1b5f4 — inline-блок FOC в 0x1A938: коммутация/классификатор
# секторов. Входы: v2c=u32[r4+0x2c], v30=u32[r4+0x30], v34=u32[r4+0x34] (значения из
# блока 0x1b3f2). Порог = 16383 (0x3fff): если все ≤ порога — pass-through
# (r4+0x38=v2c, r4+0x3c=v30, r4+0x40=v34); иначе секторная логика: определяется
# максимум из (v2c,v30,v34) = сектор, считается switching-функция.
# Верифицировано: default pass-through + v2c-max сектор:
#   r4+0x38 = 16383, r4+0x3c = min(v30 − asr(v2c,1) + 8192, 16383), r4+0x40 = r1
# Изоляция: mid-function jump (r4=RAM+0x040, r7=RAM+0x3b8, [sp+0x18]=base, stop 0x1b584).
# ---------------------------------------------------------------------------


@t(0x1B48A, '§60.6: inline-блок FOC в 0x1A938 — коммутация/классификатор секторов. Входы v2c/v30/v34=u32[r4+0x2c/0x30/0x34]; порог 16383. Default (все≤порога): pass-through r4+0x38=v2c,0x3c=v30,0x40=v34. v2c-max сектор: r4+0x38=16383, r4+0x3c=min(v30−asr(v2c,1)+8192,16383), r4+0x40=r1. Изоляция mid-function jump (stop 0x1b584)')
def _(run, rng):
    uc = run.uc
    def run_sector(v2c, v30, v34, r1):
        uc.mem_write(RAM, bytes(0x20000))
        r4 = RAM + 0x040
        for o, v in ((0x2c, v2c), (0x30, v30), (0x34, v34)):
            uc.mem_write(r4 + o, struct.pack('<i', v))
        SP = 0x20017F00
        uc.mem_write(SP + 0x18, struct.pack('<I', r4))
        uc.reg_write(UC_ARM_REG_SP, SP)
        uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        uc.reg_write(UC_ARM_REG_R4, r4)
        uc.reg_write(UC_ARM_REG_R1, r1)
        run.emu.insn = 0
        try:
            uc.emu_start(0x1B48A | 1, 0x1B584 | 1, count=200)
        except UcError:
            pass
        return (struct.unpack_from('<i', uc.mem_read(r4 + 0x38, 4), 0)[0],
                struct.unpack_from('<i', uc.mem_read(r4 + 0x3c, 4), 0)[0],
                struct.unpack_from('<i', uc.mem_read(r4 + 0x40, 4), 0)[0])
    for _ in range(40):
        # default path: все значения ≤ порога
        v2c = rng.randrange(-16000, 16000); v30 = rng.randrange(-16000, 16000)
        v34 = rng.randrange(-16000, 16000)
        a, b, c = run_sector(v2c, v30, v34, 0)
        assert (a, b, c) == (v2c, v30, v34), f'0x1b48a default: ({v2c},{v30},{v34})->({a},{b},{c})'
    for _ in range(40):
        # v2c-max сектор: v2c > порога и v2c>=v30>=v34
        v2c = rng.randrange(17000, 30000); v30 = v2c - rng.randrange(0, 4000)
        v34 = v30 - rng.randrange(0, 4000); r1 = rng.getrandbits(16)
        a, b, c = run_sector(v2c, v30, v34, r1)
        e38 = 16383; e3c = min(v30 - (v2c >> 1) + 8192, 16383); e40 = r1
        assert (a, b, c) == (e38, e3c, e40), f'0x1b48a v2cmax: ({v2c},{v30},{v34},r1={r1})->({a},{b},{c}) exp=({e38},{e3c},{e40})'


# ---------------------------------------------------------------------------
# §60.7: мелкие inline-фрагменты 0x1A938 (между крупными блоками)
# (a) 0x1b470..0x1b488 — вычисление v2c/v30/v34 (входы блока 3) из r0/r1/r2:
#       if r0<=r2: (v2c,v30,v34)=(r1, r2−r0, −r0)  else: (r0−r2, r1, −r2)
#     (связка блок 1 cross+dot → блок 3 коммутация)
# (b) 0x1b584..0x1b5e2 — хвост: масштабирование выходов блока 3 + offset + фазы:
#       svX=asr15(4500·vX) → r4+0x44/0x48/0x4c (V38/V3C/V40); pool-константа 4500
#       offset=r4+0x50=asr1(2250−max(sv)); фазы u16[RAM+0x382/0x384/0x386]=2250−(svX+offset)
# ---------------------------------------------------------------------------


def _s32(v):
    v &= 0xFFFFFFFF
    return v - 0x100000000 if (v & 0x80000000) else v


def _asr(v, n):
    return _s32(v) >> n


@t(0x1B470, '§60.7a: inline-фрагмент 0x1A938 — вычисление v2c/v30/v34 (входы блока 3) из r0/r1/r2: if r0<=r2: (v2c,v30,v34)=(r1,r2−r0,−r0) else: (r0−r2,r1,−r2). Изоляция mid-function jump (r4=RAM+0x040, stop 0x1b492)')
def _(run, rng):
    uc = run.uc
    for _ in range(80):
        r0 = rng.randrange(-50000, 50000); r1 = rng.randrange(-50000, 50000)
        r2 = rng.randrange(-50000, 50000)
        uc.mem_write(RAM, bytes(0x20000))
        r4 = RAM + 0x040
        SP = 0x20017F00
        uc.mem_write(SP + 0x18, struct.pack('<I', r4))
        from unicorn import UC_HOOK_CODE as _H
        def _st(uc_, addr, size, u):
            a = addr & ~1
            if a >= 0x1B492 or not (FLASH0 <= a < FLASH0 + FW_LEN or 0x08000000 <= a < 0x08000000 + FW_LEN):
                uc_.emu_stop()
        sh = uc.hook_add(_H, _st)
        uc.reg_write(UC_ARM_REG_SP, SP); uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        uc.reg_write(UC_ARM_REG_R4, r4)
        uc.reg_write(UC_ARM_REG_R0, r0 & 0xFFFFFFFF); uc.reg_write(UC_ARM_REG_R1, r1 & 0xFFFFFFFF)
        uc.reg_write(UC_ARM_REG_R2, r2 & 0xFFFFFFFF)
        run.emu.insn = 0
        try:
            uc.emu_start(0x1B470 | 1, 0, count=15)
        except UcError:
            pass
        uc.hook_del(sh)
        got = (struct.unpack_from('<i', uc.mem_read(r4 + 0x2c, 4), 0)[0],
               struct.unpack_from('<i', uc.mem_read(r4 + 0x30, 4), 0)[0],
               struct.unpack_from('<i', uc.mem_read(r4 + 0x34, 4), 0)[0])
        exp = (r1, r2 - r0, -r0) if _s32(r0) <= _s32(r2) else (r0 - r2, r1, -r2)
        assert got == exp, f'0x1b470: r0={r0} r1={r1} r2={r2} got={got} exp={exp}'


@t(0x1B584, '§60.7b: inline-фрагмент 0x1A938 — хвост: svX=asr15(4500·vX)→r4+0x44/0x48/0x4c; offset=r4+0x50=asr1(2250−max(sv)); фазы u16[RAM+0x382/0x384/0x386]=2250−(svX+offset). Изоляция mid-function jump (r4=RAM+0x040, stop 0x1b5e4)')
def _(run, rng):
    uc = run.uc
    for _ in range(80):
        v38 = rng.randrange(-20000, 20000); v3c = rng.randrange(-20000, 20000)
        v40 = rng.randrange(-20000, 20000)
        uc.mem_write(RAM, bytes(0x20000))
        r4 = RAM + 0x040
        for o, v in ((0x38, v38), (0x3c, v3c), (0x40, v40)):
            uc.mem_write(r4 + o, struct.pack('<i', v))
        SP = 0x20017F00
        uc.mem_write(SP + 0x18, struct.pack('<I', r4))
        from unicorn import UC_HOOK_CODE as _H
        def _st(uc_, addr, size, u):
            a = addr & ~1
            if a >= 0x1B5E4 or not (FLASH0 <= a < FLASH0 + FW_LEN or 0x08000000 <= a < 0x08000000 + FW_LEN):
                uc_.emu_stop()
        sh = uc.hook_add(_H, _st)
        uc.reg_write(UC_ARM_REG_SP, SP); uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        uc.reg_write(UC_ARM_REG_R4, r4)
        run.emu.insn = 0
        try:
            uc.emu_start(0x1B584 | 1, 0, count=60)
        except UcError:
            pass
        uc.hook_del(sh)
        o44 = struct.unpack_from('<i', uc.mem_read(r4 + 0x44, 4), 0)[0]
        o48 = struct.unpack_from('<i', uc.mem_read(r4 + 0x48, 4), 0)[0]
        o4c = struct.unpack_from('<i', uc.mem_read(r4 + 0x4c, 4), 0)[0]
        o50 = struct.unpack_from('<i', uc.mem_read(r4 + 0x50, 4), 0)[0]
        qa = struct.unpack_from('<H', uc.mem_read(RAM + 0x382, 2), 0)[0]
        qb = struct.unpack_from('<H', uc.mem_read(RAM + 0x384, 2), 0)[0]
        qc = struct.unpack_from('<H', uc.mem_read(RAM + 0x386, 2), 0)[0]
        sv38 = _asr(4500 * v38, 15); sv3c = _asr(4500 * v3c, 15); sv40 = _asr(4500 * v40, 15)
        e50 = _asr(2250 - max(sv38, sv3c, sv40), 1)
        assert (o44, o48, o4c, o50) == (sv38, sv3c, sv40, e50), \
            f'0x1b584 scale: v=({v38},{v3c},{v40}) got=({o44},{o48},{o4c},{o50}) exp=({sv38},{sv3c},{sv40},{e50})'
        exp_q = ((2250 - (sv38 + e50)) & 0xFFFF, (2250 - (sv3c + e50)) & 0xFFFF, (2250 - (sv40 + e50)) & 0xFFFF)
        assert (qa, qb, qc) == exp_q, \
            f'0x1b584 phase: v=({v38},{v3c},{v40}) got=({qa},{qb},{qc}) exp={exp_q}'


@t(0x1A9F2, '§60.7c: inline-фрагмент 0x1A938 — pre-block-2 frame setup: base=pool(RAM+0x40), [sp+0x18]=base+0x60=RAM+0xa0, [sp+4]=u16[RAM+0xa0], [sp+6]=u16[RAM+0xa2] (затем bl 0x1d7ac). Изоляция mid-function jump (stop 0x1aa04)')
def _(run, rng):
    uc = run.uc
    for _ in range(50):
        a = rng.getrandbits(16); b = rng.getrandbits(16)
        uc.mem_write(RAM, bytes(0x20000))
        uc.mem_write(RAM + 0xa0, struct.pack('<H', a)); uc.mem_write(RAM + 0xa2, struct.pack('<H', b))
        SP = 0x20017F00
        from unicorn import UC_HOOK_CODE as _H
        def _st(uc_, addr, size, u):
            aa = addr & ~1
            if aa >= 0x1AA04 or not (FLASH0 <= aa < FLASH0 + FW_LEN or 0x08000000 <= aa < 0x08000000 + FW_LEN):
                uc_.emu_stop()
        sh = uc.hook_add(_H, _st)
        uc.reg_write(UC_ARM_REG_SP, SP); uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        run.emu.insn = 0
        try:
            uc.emu_start(0x1A9F2 | 1, 0, count=12)
        except UcError:
            pass
        uc.hook_del(sh)
        s18 = struct.unpack_from('<I', uc.mem_read(SP + 0x18, 4), 0)[0]
        s4 = struct.unpack_from('<H', uc.mem_read(SP + 4, 2), 0)[0]
        s6 = struct.unpack_from('<H', uc.mem_read(SP + 6, 2), 0)[0]
        assert (s18, s4, s6) == (RAM + 0xa0, a, b), \
            f'0x1a9f2: a={a} b={b} got=({s18:#x},{s4},{s6}) exp={(RAM+0xa0,a,b)}'


# ---------------------------------------------------------------------------
# §60.8: 0x1A938 entry (0x1a938..0x1a9d0) — prologue + setup + табличная выборка.
# (a) Табличная выборка (главный расчёт), вход s16[r4+2]=value, таблица E в flash
#     @0x9E38 (2048 u16). Треугольный mapping:
#       idx = value>>4  (value<16384)  |  1023−(value−16384)>>4  (value>=16384)
#       u16[r4+4]=idx;  u16[RAM+0x108]=tableE[idx];
#       r0 = tableE[1024−idx] (value<16384)  |  −tableE[1024−idx] (value>=16384)
#     (branch C неактивен — branch B покрывает весь верхний диапазон [16384,32767])
# (b) scaled-delta: u16[r4+0x60]=u16[poolC=RAM+0x838],
#     u16[r4+0x62]=asr16(0x93cc·(u32[poolC+4]−u32[poolC+8]))
# (bl 0x1be1c — уже верифицированная подфункция)
# ---------------------------------------------------------------------------

_ENTRY_TBL_BASE = 0x9E38   # flash-таблица E
_ENTRY_TBL = None          # кэш: список 2048 u16


def _entry_table():
    global _ENTRY_TBL
    if _ENTRY_TBL is None:
        with open(r'D:/SCOOTER_5_PRO/research/images/mcu_0007.bin', 'rb') as f:
            img = bytearray(f.read())
        _ENTRY_TBL = [struct.unpack_from('<H', img, _ENTRY_TBL_BASE + i * 2)[0]
                      for i in range(2048)]
    return _ENTRY_TBL


@t(0x1A938, '§60.8: entry 0x1A938 — табличная выборка (треугольный mapping по flash-таблице @0x9E38): idx=value>>4 | 1023−(value−16384)>>4; u16[r4+4]=idx, u16[RAM+0x108]=tableE[idx], r0=±tableE[1024−idx]; + scaled-delta u16[r4+0x62]=asr16(0x93cc·delta). Изоляция mid-function jump (r4=RAM+0x040)')
def _(run, rng):
    uc = run.uc
    tbl = _entry_table()
    # (a) табличная выборка — полный диапазон value [0, 32767]
    for _ in range(150):
        val = rng.randrange(0, 32768)
        uc.mem_write(RAM, bytes(0x20000))
        r4 = RAM + 0x040
        uc.mem_write(r4 + 2, struct.pack('<h', val))
        from unicorn import UC_HOOK_CODE as _H
        def _st(uc_, addr, size, u):
            aa = addr & ~1
            if aa >= 0x1A9D0 or not (FLASH0 <= aa < FLASH0 + FW_LEN or 0x08000000 <= aa < 0x08000000 + FW_LEN):
                uc_.emu_stop()
        sh = uc.hook_add(_H, _st)
        uc.reg_write(UC_ARM_REG_SP, 0x20017F00); uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        uc.reg_write(UC_ARM_REG_R4, r4)
        run.emu.insn = 0
        try:
            uc.emu_start(0x1A966 | 1, 0, count=30)
        except UcError:
            pass
        uc.hook_del(sh)
        idx_got = struct.unpack_from('<H', uc.mem_read(r4 + 4, 2), 0)[0]
        b_got = struct.unpack_from('<H', uc.mem_read(RAM + 0x108, 2), 0)[0]
        r0_got = uc.reg_read(UC_ARM_REG_R0) & 0xFFFF
        if val < 16384:
            idx = val >> 4; neg = False
        else:
            idx = 1023 - ((val - 16384) >> 4); neg = True
        e_b = tbl[idx]
        e_r0 = (-tbl[1024 - idx]) & 0xFFFF if neg else tbl[1024 - idx]
        assert (idx_got, b_got, r0_got) == (idx, e_b, e_r0), \
            f'0x1a938 table: val={val} got=({idx_got},{b_got},{r0_got}) exp=({idx},{e_b},{e_r0})'
    # (b) scaled-delta
    POOLC = RAM + 0x838; POOLD = 0x93CC
    for _ in range(50):
        c0 = rng.getrandbits(16); c4 = rng.getrandbits(32); c8 = rng.getrandbits(32)
        uc.mem_write(RAM, bytes(0x20000))
        uc.mem_write(POOLC + 0, struct.pack('<H', c0))
        uc.mem_write(POOLC + 4, struct.pack('<I', c4)); uc.mem_write(POOLC + 8, struct.pack('<I', c8))
        r4 = RAM + 0x040
        def _st2(uc_, addr, size, u):
            aa = addr & ~1
            if aa >= 0x1A966 or not (FLASH0 <= aa < FLASH0 + FW_LEN or 0x08000000 <= aa < 0x08000000 + FW_LEN):
                uc_.emu_stop()
        sh2 = uc.hook_add(_H, _st2)
        uc.reg_write(UC_ARM_REG_SP, 0x20017F00); uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        uc.reg_write(UC_ARM_REG_R4, r4)
        run.emu.insn = 0
        try:
            uc.emu_start(0x1A94E | 1, 0, count=12)
        except UcError:
            pass
        uc.hook_del(sh2)
        o60 = struct.unpack_from('<H', uc.mem_read(r4 + 0x60, 2), 0)[0]
        o62 = struct.unpack_from('<H', uc.mem_read(r4 + 0x62, 2), 0)[0]
        delta = (c4 - c8) & 0xFFFFFFFF
        e62 = (_s32(POOLD * delta) >> 16) & 0xFFFF
        assert (o60, o62) == (c0, e62), \
            f'0x1a938 delta: c0={c0} c4={c4:#x} c8={c8:#x} got=({o60},{o62}) exp=({c0},{e62})'


# ---------------------------------------------------------------------------
# §61: оставшиеся некаталогизированные функции (досмотр карты)
# 0x11bac — форматтер даты/времени: total-seconds → байты через цепочку остатков.
# Аргументы: arg0=r0=out-буфер, arg1=r1=total seconds. Дивизоры [31104000,2592000,
# 86400,3600,60] (≈360d-год, 30d-месяц, день, час, минута):
#   out[0]=v//31104000; out[i]=(v%D[i-1])//D[i]; out[5]=v%60
# ---------------------------------------------------------------------------

_FMT_D = [31104000, 2592000, 86400, 3600, 60]


def ref_11bac(v):
    out = [(v // _FMT_D[0]) & 0xFF]
    for i in range(1, len(_FMT_D)):
        out.append(((v % _FMT_D[i - 1]) // _FMT_D[i]) & 0xFF)
    out.append((v % _FMT_D[-1]) & 0xFF)
    return out


@t(0x11BAC, '§61: форматтер даты/времени — total-seconds → байты (цепочка остатков, дивизоры [31104000,2592000,86400,3600,60] ≈ 360d-год/30d-месяц/день/час/мин/сек): out[0]=v//D0, out[i]=(v%D[i-1])//D[i], out[5]=v%60')
def _(run, rng):
    uc = run.uc
    OUT = RAM + 0x300
    for _ in range(100):
        v = rng.getrandbits(26)
        uc.mem_write(RAM, bytes(0x20000))
        from unicorn import UC_HOOK_CODE as _H
        def _st(uc_, addr, size, u):
            a = addr & ~1
            if a >= 0x11C2E or not (FLASH0 <= a < FLASH0 + FW_LEN or 0x08000000 <= a < 0x08000000 + FW_LEN):
                uc_.emu_stop()
        sh = uc.hook_add(_H, _st)
        uc.reg_write(UC_ARM_REG_SP, 0x20017F00); uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        uc.reg_write(UC_ARM_REG_R0, OUT); uc.reg_write(UC_ARM_REG_R1, v)
        run.emu.insn = 0
        try:
            uc.emu_start(0x11BAC | 1, 0, count=80)
        except UcError:
            pass
        uc.hook_del(sh)
        got = list(bytes(uc.mem_read(OUT, 6)))
        exp = ref_11bac(v)
        assert got == exp, f'0x11bac: v={v} got={got} exp={exp}'


# --- 0x1d078 timer capture/period + speed-limit ramp (§69, corrected by random-sweep) ---
def _sdiv(a, b):
    if b == 0:
        return 0
    q = abs(a) // abs(b)
    return q if (a < 0) == (b < 0) else -q
def _s16(x):
    x &= 0xFFFF
    return x - 0x10000 if x >= 0x8000 else x

@t(0x1D078, '§69: val=s16(sdiv(48000,V)) if F=byte[RAM+0x100]!=0 else 0; struct r4=RAM+0x1768: [+0]=u16(val), 2 leaky-интегратора (asr5 / asr3 clamp≥0) → out1=s16[+0x10], out2=s16[+8]; pct=u16[RAM+0x236]=sdiv(100*out2,208); mode-target: flag=byte[RAM+0x339]==1→522 / mode@0x229 0xb→125/2→u16@0x324/3→u16@0x326/else→208; struct[+0x14]=target if s16(target)<=u16[RAM+0x326] else u16[RAM+0x326] (signed clamp); structB@0x3c8[+0x2a]=target = setpoint замкнутого контура скорости (out2=сглаж. оценка ∝ 48000/V; вывод r4[+0x18]=structB[+0x64]=throttle/duty, НЕ скорость). Вериф. 200/200 random-sweep + setpoint 300/300')
def _(run, rng):
    V = rng.randint(50, 60000)
    F = rng.getrandbits(1)
    acc1 = rng.getrandbits(32); out1 = rng.randint(-32768, 32767)
    acc2 = rng.getrandbits(32); out2 = rng.randint(-32768, 32767)
    mode = rng.choice([2, 3, 0xb, 5, 7])
    f339 = rng.getrandbits(16)   # flag = low byte @0x339
    c326 = rng.getrandbits(16)   # u16[RAM+0x326] (clamp-значение)
    m2t  = rng.getrandbits(16)   # u16[RAM+0x324] (target при mode==2)
    run.ram_write(0x158, struct.pack('<I', V))
    run.ram_write(0x100, bytes([F]))
    run.ram_write(0x1768, struct.pack('<H', 0))
    run.ram_write(0x176c, struct.pack('<I', acc2))
    run.ram_write(0x1770, struct.pack('<h', out2))
    run.ram_write(0x1774, struct.pack('<I', acc1))
    run.ram_write(0x1778, struct.pack('<h', out1))
    run.ram_write(0x229, bytes([mode]))
    run.ram_write(0x339, struct.pack('<H', f339))
    run.ram_write(0x324, struct.pack('<H', m2t))
    run.ram_write(0x326, struct.pack('<H', c326))
    run.call(0x1D078, (), max_insn=400000)
    val = 0 if F == 0 else _s16(_sdiv(48000, V))
    na1 = (acc1 + val - out1) & 0xFFFFFFFF; e_o1 = _s16(na1 >> 5)
    na2 = (acc2 + val - out2) & 0xFFFFFFFF; e_o2 = max(0, _s16(na2 >> 3))
    e_pct = _sdiv(100 * e_o2, 208) & 0xFFFF
    flag = f339 & 0xFF
    if flag == 1: tgt = 522
    elif mode == 0xb: tgt = 125
    elif mode == 2: tgt = m2t
    elif mode == 3: tgt = c326
    else: tgt = 208
    e_tgt = (tgt if _s16(tgt) <= c326 else c326) & 0xFFFF
    g_sp0 = struct.unpack('<H', run.ram_read(0x1768, 2))[0]
    g_o1  = struct.unpack('<H', run.ram_read(0x1778, 2))[0]
    g_o2  = struct.unpack('<H', run.ram_read(0x1770, 2))[0]
    g_pct = struct.unpack('<H', run.ram_read(0x236, 2))[0]
    g_tgt = struct.unpack('<H', run.ram_read(0x177c, 2))[0]
    g_set = struct.unpack('<H', run.ram_read(0x3F2, 2))[0]   # structB@0x3c8[+0x2a] setpoint
    assert g_sp0 == val & 0xFFFF, f'sp0 {g_sp0} != {val & 0xffff} (V={V},F={F})'
    assert g_o1 == e_o1 & 0xFFFF, f'out1 {g_o1} != {e_o1}'
    assert g_o2 == e_o2 & 0xFFFF, f'out2 {g_o2} != {e_o2}'
    assert g_pct == e_pct, f'pct {g_pct} != {e_pct}'
    assert g_tgt == e_tgt, f'tgt {g_tgt} != {e_tgt} (mode={mode},flag={flag})'
    assert g_set == e_tgt, f'setpoint +0x2a {g_set} != {e_tgt} (mode={mode},flag={flag})'


# --- 0x1d078 ramp-core PI-регулятор: P-term + 2-фазный toggle (§72) ---
@t(0x1D078, '§72: ramp-core (Phase B, counter S+0x28=1) = PI-регулятор. P-term: S+0x2c=min(err,300), err=(target−out2_new) if out1_new<target else (out2_new−target); S+0x5c=s16(S+0x2c)<<7. Toggle: counter 1→2→reset 0. positive-target домен; вериф. 400/400')
def _(run, rng):
    V = rng.randint(10, 60000)
    F = rng.getrandbits(1)
    mode = rng.choice([2, 3, 0xb, 5, 7])
    f339 = rng.getrandbits(16)
    c326 = rng.randint(1, 0x7fff)   # positive s16 (реалистичный speed-setpoint)
    m2t = rng.randint(1, 0x7fff)
    acc1 = rng.getrandbits(32); out1 = rng.randint(-32768, 32767)
    acc2 = rng.getrandbits(32); out2 = rng.randint(-32768, 32767)
    run.ram_write(0x158, struct.pack('<I', V))
    run.ram_write(0x100, bytes([F]))
    run.ram_write(0x229, bytes([mode]))
    run.ram_write(0x339, struct.pack('<H', f339))
    run.ram_write(0x324, struct.pack('<H', m2t))
    run.ram_write(0x326, struct.pack('<H', c326))
    run.ram_write(0x1768, struct.pack('<H', 0))
    run.ram_write(0x176C, struct.pack('<I', acc2))
    run.ram_write(0x1770, struct.pack('<H', out2 & 0xFFFF))
    run.ram_write(0x1774, struct.pack('<I', acc1))
    run.ram_write(0x1778, struct.pack('<H', out1 & 0xFFFF))
    for off in (0x1760, 0x1764, 0x388, 0x224):   # anti-windup inходы = 0
        run.ram_write(off, struct.pack('<I', 0))
    run.ram_write(0x3C8, b'\x00' * 0x70)          # Phase B: counter S+0x28=1
    run.ram_write(0x3C8 + 0x28, struct.pack('<H', 1))
    run.call(0x1D078, (), max_insn=400000)
    val = 0 if F == 0 else _s16(_sdiv(48000, V))
    o1n = _s16(((acc1 + val - out1) & 0xFFFFFFFF) >> 5)
    o2n = max(0, _s16(((acc2 + val - out2) & 0xFFFFFFFF) >> 3))
    flag = f339 & 0xFF
    tgt = 522 if flag == 1 else (125 if mode == 0xb else
                                 (m2t if mode == 2 else (c326 if mode == 3 else 208)))
    tgt = (tgt if _s16(tgt) <= c326 else c326) & 0xFFFF
    tsgn = _s16(tgt)
    err = (tsgn - o2n) if o1n < tsgn else (o2n - tsgn)
    e_2c = min(err, 300)
    e_5c = (_s16(e_2c & 0xFFFF) << 7) & 0xFFFFFFFF
    g_2c = struct.unpack('<H', run.ram_read(0x3C8 + 0x2C, 2))[0]
    g_5c = struct.unpack('<I', run.ram_read(0x3C8 + 0x5C, 4))[0]
    g_28 = struct.unpack('<H', run.ram_read(0x3C8 + 0x28, 2))[0]
    assert g_2c == (e_2c & 0xFFFF), f'S+0x2c {g_2c} != {e_2c & 0xffff} (tgt={tsgn},o1n={o1n},o2n={o2n})'
    assert g_5c == e_5c, f'S+0x5c {g_5c:#x} != {e_5c:#x}'
    assert g_28 == 0, f'toggle counter {g_28} != 0 (Phase B)'


# --- 0x1d078 Phase B полная модель: I-term + anti-windup (§72.4) ---
@t(0x1D078, '§72: Phase B полная модель — I-term clamp[8000,131040] + anti-windup tail (reset u1760==0 / slew) + sxth out1/out2. S58/S60/S64/S2e; вериф. 2000/2000')
def _(run, rng):
    V = rng.randint(10, 60000)
    F = rng.getrandbits(1)
    mode = rng.choice([2, 3, 0xb, 5, 7])
    f339 = rng.getrandbits(16)
    c326 = rng.randint(1, 0x7fff)
    m2t = rng.randint(1, 0x7fff)
    acc1 = rng.getrandbits(32); out1 = rng.randint(-32768, 32767)
    acc2 = rng.getrandbits(32); out2 = rng.randint(-32768, 32767)
    old_int = rng.getrandbits(32)
    s2e_old = rng.randint(0, 5)
    u1760 = rng.choice([0, 0, rng.getrandbits(16), rng.getrandbits(20)])
    u1764 = rng.getrandbits(24); u388 = rng.getrandbits(24); u224 = rng.getrandbits(20)
    run.ram_write(0x158, struct.pack('<I', V))
    run.ram_write(0x100, bytes([F]))
    run.ram_write(0x229, bytes([mode]))
    run.ram_write(0x339, struct.pack('<H', f339))
    run.ram_write(0x333, b'\x00')          # skip mode-change block
    run.ram_write(0x263, b'\x00')          # gate → ramp-core
    run.ram_write(0x324, struct.pack('<H', m2t))
    run.ram_write(0x326, struct.pack('<H', c326))
    run.ram_write(0x1768, struct.pack('<H', 0))
    run.ram_write(0x176C, struct.pack('<I', acc2))
    run.ram_write(0x1770, struct.pack('<H', out2 & 0xFFFF))
    run.ram_write(0x1774, struct.pack('<I', acc1))
    run.ram_write(0x1778, struct.pack('<H', out1 & 0xFFFF))
    run.ram_write(0x1760, struct.pack('<I', u1760))
    run.ram_write(0x1764, struct.pack('<I', u1764))
    run.ram_write(0x388, struct.pack('<I', u388))
    run.ram_write(0x224, struct.pack('<I', u224))
    run.ram_write(0x3C8, b'\x00' * 0x70)   # Phase B: counter S+0x28=1
    run.ram_write(0x3C8 + 0x28, struct.pack('<H', 1))
    run.ram_write(0x3C8 + 0x58, struct.pack('<I', old_int))
    run.ram_write(0x3C8 + 0x2E, struct.pack('<H', s2e_old))
    run.call(0x1D078, (), max_insn=400000)
    # --- модель (совпадает с _d078_fullB.model_phaseB) ---
    val = 0 if F == 0 else _s16(_sdiv(48000, V))
    o1n = _s16(_s32(acc1 + val - out1) >> 5)          # asr5 + sxth
    o2n = max(0, _s16(_s32(acc2 + val - out2) >> 3))   # asr3 + sxth + clamp>=0
    flag = f339 & 0xFF
    tgt = 522 if flag == 1 else (125 if mode == 0xb else
                                 (m2t if mode == 2 else (c326 if mode == 3 else 208)))
    tgt = (tgt if _s16(tgt) <= c326 else c326) & 0xFFFF
    tsgn = _s16(tgt)
    if o1n < tsgn:   # INCREASE
        err = _s16(tsgn - o2n); interim = (5 * err + old_int) & 0xFFFFFFFF
    else:            # DECREASE
        err = _s16(o2n - tsgn); interim = (old_int - 5 * err) & 0xFFFFFFFF
    adj = _s32(u1764 - u388) >> 3
    integral = _s32(interim - adj)
    S58 = max(8000, min(integral, 131040))            # clamp (верх → 131040!)
    S60 = _s32(S58 & 0xFFFFFFFF) >> 2
    if o1n < tsgn:   # INCREASE
        e2 = _s16(tsgn - o2n); S2c = e2 if e2 <= 300 else 300
        P = _s16(S2c & 0xFFFF) << 7; output = P + S60
    else:            # DECREASE
        e2 = _s16(o2n - tsgn); S2c = e2 if e2 <= 300 else 300
        P = _s16(S2c & 0xFFFF) << 7; output = S60 - P
    S64 = max(1000, min(32760, output))
    if u1760 == 0:   # RESET path
        S58 = (u224 * 4) & 0xFFFFFFFF; S64 = 0; S2e = 0
    else:            # SLEW path
        new2e = _s16(_s16(s2e_old) + 1)
        if new2e > 2:
            S2e = 2
            if u1760 < S60:
                S58 = (u1760 * 4) & 0xFFFFFFFF
            up = _s32(u224 * 7) >> 1
            if up > _s32(S58):
                S58 = up & 0xFFFFFFFF
        else:
            S2e = new2e
        if u1760 < S64:
            S64 = u1760
    g58 = struct.unpack('<I', run.ram_read(0x3C8 + 0x58, 4))[0]
    g60 = struct.unpack('<I', run.ram_read(0x3C8 + 0x60, 4))[0]
    g64 = struct.unpack('<I', run.ram_read(0x3C8 + 0x64, 4))[0]
    g2e = struct.unpack('<H', run.ram_read(0x3C8 + 0x2E, 2))[0]
    assert g58 == (S58 & 0xFFFFFFFF), f'S+0x58 {g58} != {S58 & 0xffffffff}'
    assert g60 == (S60 & 0xFFFFFFFF), f'S+0x60 {g60} != {S60 & 0xffffffff}'
    assert g64 == (S64 & 0xFFFFFFFF), f'S+0x64 {g64} != {S64 & 0xffffffff}'
    assert g2e == S2e, f'S+0x2e {g2e} != {S2e}'


# --- 0x1a938 FOC: конфигурация моторного таймера (§73) ---
@t(0x1A938, '§73: FOC entry конфигурирует моторный таймер @0x40012c00 — CTRL(+0x30) RMW &= 0xDFFF (clear бит 13); DATA0/1/2 (+0x44/48/4c) = u16[RAM+0x386/384/382]. Эмулятор: TimModel + periph-capture. Детерминизм: 4 записи для любого value.')
def _(run, rng):
    from emulator.mcu_emu import TimModel, MOTOR_TIM_BASE
    uc = run.uc
    uc.mem_write(RAM, bytes(0x20000))          # чистая RAM → детерминизм
    r4 = RAM + 0x040
    uc.mem_write(r4, bytes(0x80))
    val = rng.randrange(0, 32768)              # вход FOC: s16[r4+2]
    uc.mem_write(r4 + 2, struct.pack('<h', val))
    tim = TimModel(run.emu, MOTOR_TIM_BASE)
    tim.set(0x54, 0x8000)                      # STAT бит15=1 → гейт FOC открыт (иначе обход)
    tim.set(0x30, 0xFFFF)                      # known pre-value для проверки RMW
    def _st(uc_, addr, size, u):
        aa = addr & ~1
        if not (FLASH0 <= aa < FLASH0 + FW_LEN or
                FLASH1 <= aa < FLASH1 + FW_LEN):
            uc_.emu_stop()                      # чистый возврат (bx lr → 0x0BADF001)
    sh = uc.hook_add(UC_HOOK_CODE, _st)
    try:
        uc.reg_write(UC_ARM_REG_SP, STACK_TOP - 0x80)
        uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        uc.reg_write(UC_ARM_REG_R4, r4)
        uc.reg_write(UC_ARM_REG_R0, 0)
        run.emu.insn = 0
        try:
            uc.emu_start(0x1A938 | 1, 0, count=200000)
        except UcError:
            pass
    finally:
        uc.hook_del(sh)
        uc.hook_del(tim._hook)
    # --- проверка конфигурации таймера ---
    d0 = struct.unpack('<H', run.ram_read(0x386, 2))[0]
    d1 = struct.unpack('<H', run.ram_read(0x384, 2))[0]
    d2 = struct.unpack('<H', run.ram_read(0x382, 2))[0]
    t0 = tim.read(0x44) & 0xFFFF
    t1 = tim.read(0x48) & 0xFFFF
    t2 = tim.read(0x4c) & 0xFFFF
    ctrl = tim.read(0x30)
    assert (t0, t1, t2) == (d0, d1, d2), \
        f'FOC timer DATA {t0,t1,t2} != u16[RAM+0x386/384/382] {d0,d1,d2}'
    assert ctrl == 0xDFFF, \
        f'FOC timer CTRL 0x{ctrl:x} != 0xDFFF (RMW 0xFFFF & 0xDFFF, clear бит 13)'
    offs = sorted(set(o for _, o, _, _ in tim.writes))
    assert {0x30, 0x44, 0x48, 0x4c} <= set(offs), \
        f'FOC timer не записал все регистры: offs={offs}'


# --- 0x1a938 FOC + TIM clock model (§73.x) ---
@t(0x1A938, '§73.x: TIM clock model — такт контура (tick→update по period) управляет режимом FOC через STAT бит15: =0 → обход (0 записей таймера), event → set bit15 → config (4 записи). Свободно-ходный счётчик wrap; модель параметризована (period/step).')
def _(run, rng):
    from emulator.mcu_emu import TimModel, MOTOR_TIM_BASE
    uc = run.uc
    TIM_OFFS = (MOTOR_TIM_BASE + 0x30, MOTOR_TIM_BASE + 0x44,
                MOTOR_TIM_BASE + 0x48, MOTOR_TIM_BASE + 0x4c)

    def run_foc(stat_bit15):
        uc.mem_write(RAM, bytes(0x20000))
        uc.mem_write(MOTOR_TIM_BASE, bytes(0x100))      # чистый моторный блок
        r4 = RAM + 0x040
        uc.mem_write(r4, bytes(0x80))
        uc.mem_write(r4 + 2, struct.pack('<h', rng.randrange(0, 32768)))
        uc.mem_write(MOTOR_TIM_BASE + 0x54,
                     struct.pack('<I', 0x8000 if stat_bit15 else 0x0000))
        before = len(run.emu.periph_writes)

        def _st(uc_, addr, size, u):
            aa = addr & ~1
            if not (FLASH0 <= aa < FLASH0 + FW_LEN or
                    FLASH1 <= aa < FLASH1 + FW_LEN):
                uc_.emu_stop()
        sh = uc.hook_add(UC_HOOK_CODE, _st)
        try:
            uc.reg_write(UC_ARM_REG_SP, STACK_TOP - 0x80)
            uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
            uc.reg_write(UC_ARM_REG_R4, r4)
            uc.reg_write(UC_ARM_REG_R0, 0)
            run.emu.insn = 0
            try:
                uc.emu_start(0x1A938 | 1, 0, count=200000)
            except UcError:
                pass
        finally:
            uc.hook_del(sh)
        return sum(1 for _, a, s, v in run.emu.periph_writes[before:]
                   if a in TIM_OFFS)

    period = rng.randrange(2, 16)                        # период контура (тактов)
    tim = TimModel(run.emu, MOTOR_TIM_BASE, period=period, step=1)
    try:
        # фаза 1: STAT бит15=0 → обход (0 записей таймера)
        n_off = run_foc(stat_bit15=False)
        assert n_off == 0, f'FOC bit15=0: записей {n_off} != 0 (ожид. обход)'
        # такты до первого update-события (wrap счётчика)
        t0 = tim.ticks
        while not tim.update:
            tim.tick()
            assert (tim.ticks - t0) <= period + 2, 'clock не завернул за period'
        assert tim.cnt == 0 and tim.update, \
            f'clock: cnt={tim.cnt} update={tim.update} (ожид. wrap→0/True)'
        # фаза 2: event → модель задает STAT бит15 → config (4 записи)
        tim.set_status_bits(MOTOR_TIM_BASE + 0x54, 0x8000)
        n_on = run_foc(stat_bit15=True)
        assert n_on == 4, f'FOC bit15=1: записей {n_on} != 4 (ожид. config)'
    finally:
        uc.hook_del(tim._hook)


# --- 0x1be1c ADC/capture model (§73.x) ---
@t(0x1BE1C, '§73.x: ADC/capture model — 0x1be1c реконструирует фазные токи из T28/T2C/T30 (periph @0x40012468/6c/70): фаза=(T−C)<<4, 3-я=−сумма (Кирхгоф). sector→handler: 0→null,1→B,2/3→A,4/5→C,6→B. AdcModel.set_captures/set_currents.')
def _(run, rng):
    from emulator.mcu_emu import (AdcModel, ADC_SECTOR_HANDLER,
                                  ADC_HANDLER_MEASURED)
    uc = run.uc
    r0 = RAM + 0x100

    def setup(sector, c18, c1a, c1c):
        uc.mem_write(RAM, bytes(0x20000))
        uc.mem_write(r0, bytes(0x40))
        uc.mem_write(r0 + 2, struct.pack('<H', sector))
        uc.mem_write(r0 + 0x18, struct.pack('<h', c18))
        uc.mem_write(r0 + 0x1a, struct.pack('<h', c1a))
        uc.mem_write(r0 + 0x1c, struct.pack('<h', c1c))
        uc.mem_write(0x40012c54, struct.pack('<I', 0x8000))   # mode-2 гейт

    def run_be1c():
        def _st(uc_, addr, size, u):
            aa = addr & ~1
            if not (FLASH0 <= aa < FLASH0 + FW_LEN or
                    FLASH1 <= aa < FLASH1 + FW_LEN):
                uc_.emu_stop()
        sh = uc.hook_add(UC_HOOK_CODE, _st)
        try:
            uc.reg_write(UC_ARM_REG_SP, STACK_TOP - 0x80)
            uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
            uc.reg_write(UC_ARM_REG_R0, r0)
            run.emu.insn = 0
            try:
                uc.emu_start(0x1BE1C | 1, 0, count=200000)
            except UcError:
                pass
        finally:
            uc.hook_del(sh)
        return (struct.unpack('<i', uc.mem_read(r0 + 0xc, 4))[0],
                struct.unpack('<i', uc.mem_read(r0 + 0x10, 4))[0],
                struct.unpack('<i', uc.mem_read(r0 + 0x14, 4))[0])

    adc = AdcModel(run.emu)
    c18 = rng.randrange(500, 2000)
    c1a = rng.randrange(500, 2000)
    c1c = rng.randrange(500, 2000)
    # --- (1) set_captures: raw T → pre-clamp (T−C)<<4 + −sum по handler ---
    for sector in range(7):
        setup(sector, c18, c1a, c1c)
        t28 = rng.randrange(0, 4000)
        t2c = rng.randrange(0, 4000)
        t30 = rng.randrange(0, 4000)
        adc.set_captures(t28, t2c, t30)
        oc, o10, o14 = run_be1c()
        h = ADC_SECTOR_HANDLER[sector]
        if h is None:
            assert (oc, o10, o14) == (0, 0, 0), \
                f'sector={sector} null: got {(oc, o10, o14)} != (0,0,0)'
            continue
        d28 = (t28 - c18) << 4
        d2c = (t2c - c1a) << 4
        d30 = (t30 - c1c) << 4
        if h == 'A':
            e = (d28, d2c, -(d28 + d2c))       # A: o_c=T28, o_10=T2C, o_14=−sum
        elif h == 'B':
            e = (-(d2c + d30), d2c, d30)       # B: o_c=−sum, o_10=T2C, o_14=T30
        else:  # C
            e = (d28, -(d28 + d30), d30)       # C: o_c=T28, o_10=−sum, o_14=T30
        assert (oc, o10, o14) == e, \
            f'sector={sector} h={h}: got {(oc, o10, o14)} != exp {e}'
    # --- (2) set_currents: инжект токов → измеренные фазы совпадают (×16 квант) ---
    for sector in (1, 2, 4, 6):
        setup(sector, c18, c1a, c1c)
        h = ADC_SECTOR_HANDLER[sector]
        meas_out = [m[2] for m in ADC_HANDLER_MEASURED[h]]
        targets = {0xc: rng.randrange(-500, 500) * 16,
                   0x10: rng.randrange(-500, 500) * 16,
                   0x14: rng.randrange(-500, 500) * 16}
        adc.set_currents(r0, targets, sector)
        oc, o10, o14 = run_be1c()
        got = {0xc: oc, 0x10: o10, 0x14: o14}
        for off in meas_out:
            assert got[off] == targets[off], \
                f'set_currents sector={sector} h={h}: out{off:#x} {got[off]} != {targets[off]}'


# --- 0x1d078 closed loop: SpeedModel (замер скорости) (§73.x) ---
@t(0x1D078, '§73.x closed loop: SpeedModel — замер скорости замыкает контур. set_period(V)→PID вычисляет val=s16(48000/V); set_speed(val) (V=48000//val) → PID даёт ровно val (для делителей 48000); stop() (F=0) → val=0. V=u32[RAM+0x158], F=byte[RAM+0x100].')
def _(run, rng):
    from emulator.mcu_emu import SpeedModel
    sm = SpeedModel(run.emu)

    def run_pid():
        # минимальное безопасное состояние 0x1d078 (как §69)
        run.ram_write(0x229, bytes([3]))                 # mode=3 → target=u16[RAM+0x326]
        run.ram_write(0x326, struct.pack('<H', 200))
        run.ram_write(0x339, b'\x00')                    # flag=0
        run.ram_write(0x1768, struct.pack('<H', 0))      # чистый val
        run.ram_write(0x176c, struct.pack('<I', 0))      # acc2
        run.ram_write(0x1770, struct.pack('<h', 0))      # out2
        run.ram_write(0x1774, struct.pack('<I', 0))      # acc1
        run.ram_write(0x1778, struct.pack('<h', 0))      # out1
        run.call(0x1D078, (), max_insn=400000)

    # --- (1) set_period: V → PID val=s16(48000/V) ---
    for _ in range(6):
        V = rng.randint(1, 48000)
        sm.set_period(V)
        run_pid()
        got = sm.get_val()
        exp = _s16(_sdiv(48000, V))
        assert got == exp, f'set_period V={V}: PID val {got} != s16(48000/V)={exp}'
    # --- (2) set_speed: делители 48000 → PID даёт ровно val ---
    for val in (100, 200, 480, 1200, 4800, 12000):
        sm.set_speed(val)
        run_pid()
        got = sm.get_val()
        assert got == val, f'set_speed val={val}: PID {got} != {val}'
    # --- (3) stop: F=0 → val=0 ---
    sm.set_period(1000)
    sm.stop()
    run_pid()
    assert sm.get_val() == 0, f'stop(): val {sm.get_val()} != 0'


# --- 0x1d078 motor dynamics: АВТОНОМНЫЙ симул замкнутого контура (§73.x) ---
@t(0x1D078, '§73.x motor dynamics: MotorModel (plant) замыкает АВТОНОМНЫЙ симул. target=208 → PID 0x1d078 → throttle(u16[RAM+0x42c]) → plant(speed) → SpeedModel(V) → PID ... Скорость сходится к target: 0→overshoot~338→settle~207; throttle спадает. Детерминированно (fixed params).')
def _(run, rng):
    from emulator.mcu_emu import MotorModel, SpeedModel
    uc = run.uc
    target = 208
    # начальное состояние PID: ramp-core + гейты + мощность разрешена (u1760≠0)
    uc.mem_write(RAM, bytes(0x20000))
    uc.mem_write(RAM + 0x229, bytes([3]))                 # mode=3 → target=u16[RAM+0x326]
    uc.mem_write(RAM + 0x326, struct.pack('<H', target))
    uc.mem_write(RAM + 0x339, b'\x00')
    uc.mem_write(RAM + 0x333, b'\x00')                    # skip mode-change
    uc.mem_write(RAM + 0x263, b'\x00')                    # gate → ramp-core
    uc.mem_write(RAM + 0x1760, struct.pack('<I', 32760))  # мощность разрешена (не reset)
    uc.mem_write(RAM + 0x1764, struct.pack('<I', 0))
    uc.mem_write(RAM + 0x388, struct.pack('<I', 0))
    uc.mem_write(RAM + 0x224, struct.pack('<I', 0))
    uc.mem_write(RAM + 0x3C8 + 0x28, struct.pack('<H', 1))  # counter → ramp-core
    sm = SpeedModel(run.emu)
    mm = MotorModel(run.emu, v_max=520.0, tau=15.0, throttle_ref=4000.0)
    speeds, thrs = [], []
    for _ in range(40):
        sm.set_speed(int(mm.speed))
        run.call(0x1D078, (), max_insn=400000)
        thr = struct.unpack('<h', uc.mem_read(RAM + 0x42c, 2))[0]
        thrs.append(thr)
        mm.step(thr)
        speeds.append(mm.speed)
    # --- замкнутый контур сходится к target ---
    assert speeds[0] > 0, f'ускорение не началось: speed[0]={speeds[0]}'
    assert max(speeds) > target, \
        f'скорость не достигла target: max={max(speeds):.1f} < {target}'
    assert abs(speeds[-1] - target) < 0.5 * target, \
        f'схождение: speed_end={speeds[-1]:.1f} вне полосы ±50% от target={target}'
    assert thrs[0] > thrs[-1], \
        f'throttle не спадает при подходе к target: {thrs[0]} -> {thrs[-1]}'


# --- батарея: BatteryModel (SoC + разряд) (§73.x) ---
@t(0x1DFD8, '§73.x battery: BatteryModel — SoC%→u16[RAM+0x306] (+сырое i16@0x17a0 [415..535]). set_soc round-trip; mapping 0%→415/100%→535; разряд монотонно падает с нагрузкой, bounded [0,100], без нагрузки не меняется. Пороги FOC 90/10 гейтятся (byte@0x22e).')
def _(run, rng):
    from emulator.mcu_emu import BatteryModel, BATT_RAW_MIN, BATT_RAW_MAX
    uc = run.uc
    bm = BatteryModel(run.emu)
    # --- (1) set_soc round-trip + raw mapping [415..535] ---
    for pct in (0, 25, 50, 75, 100):
        bm.set_soc(pct)
        assert bm.get_soc() == pct, f'set_soc({pct}): get={bm.get_soc()}'
        raw = struct.unpack('<h', uc.mem_read(RAM + 0x17A0, 2))[0]
        exp_raw = BATT_RAW_MIN + round(pct * (BATT_RAW_MAX - BATT_RAW_MIN) / 100.0)
        assert raw == exp_raw, f'set_soc({pct}): raw {raw} != {exp_raw}'
    bm.set_soc(0)
    assert struct.unpack('<h', uc.mem_read(RAM + 0x17A0, 2))[0] == 415
    bm.set_soc(100)
    assert struct.unpack('<h', uc.mem_read(RAM + 0x17A0, 2))[0] == 535
    # --- (2) разряд: монотонно падает с нагрузкой, bounded [0,100] ---
    bm.set_soc(80)
    prev = 80.0
    for _ in range(20):
        thr = rng.randint(5000, 32760)          # нагрузка (прокси тока)
        s = bm.discharge(thr, dt=1.0)
        assert 0 <= s <= 100, f'разряд вне [0,100]: {s}'
        assert s <= prev, f'разряд не монотонен: {prev} -> {s}'
        prev = s
    # без нагрузки SoC не меняется
    bm.set_soc(50)
    assert bm.discharge(0, dt=1.0) == 50, 'разряд без нагрузки изменил SoC'


# --- запас хода: RangeModel (0x1d898) (§73.x) ---
@t(0x1D898, '§73.x range: RangeModel — v=i16[RAM+0x27A]→X=(8000·v)>>16, R=10000·X/(500−X) (делитель 0x19994; div-by-zero→-1, отриц. знаменатель→отриц.). Closed-form вериф. random-sweep (v≥0) против firmware 0x1d898 + edge-cases (v=0/415/535/4096).')
def _(run, rng):
    from emulator.mcu_emu import RangeModel
    rm = RangeModel(run.emu)
    def fw(v):
        rm.set_value(v)
        run.call(0x1D898, (0, 0, 0, 0), max_insn=300000)
        X = struct.unpack('<H', run.uc.mem_read(RAM + 0x3E8, 2))[0]
        R = struct.unpack('<i', run.uc.mem_read(RAM + 0x408, 4))[0]
        return X, R
    # --- random-sweep: closed-form vs firmware (v≥0) ---
    for _ in range(150):
        v = rng.randint(0, 12000)
        mx, mr = rm.estimate(v)
        fx, fr = fw(v)
        assert (fx, fr) == (mx, mr), f'v={v}: fw=({fx},{fr}) model=({mx},{mr})'
    # --- edge-cases ---
    assert rm.estimate(0) == (0, 0) and fw(0) == (0, 0)
    assert rm.estimate(415) == (50, 1111) and fw(415) == (50, 1111)
    assert rm.estimate(535) == (65, 1494) and fw(535) == (65, 1494)
    # div-by-zero: X=500 при v=4096 → R=-1
    assert rm.estimate(4096) == (500, -1) and fw(4096) == (500, -1)


# --- 0x1d898 аккумулятор (leaky integrator) (§73.x) ---
@t(0x1D898, '§73.x range-acc: аккумулятор 0x1d898 (leaky integrator) — new_0x3c=(old_0x3c+delta−prev_0x14)&0xFFFFFFFF, new_0x14=asr(new_0x3c,10)[i16]; delta=i16[RAM+0x26E]. Stateful-sweep против firmware + edge-cases.')
def _(run, rng):
    from emulator.mcu_emu import RangeModel, McuEmu
    from unicorn import UC_HOOK_CODE, UcError
    from unicorn.arm_const import UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3
    rm = RangeModel(run.emu)
    # 0x1d898 state-зависим (поздние под-вызовы, data-driven jump) → self-contained:
    # fresh McuEmu на каждый вызов (чистый путь, как в probe 250/250). Reuse emu +
    # re-zero RAM ломает large-A итерации (нере-zeroed periph → early unmapped fetch).
    def fw_acc(A, B, D):
        femu = McuEmu(max_insn=300000)
        femu.uc.mem_write(RAM, bytes(0x20000))
        femu.uc.mem_write(RAM + 0x404, struct.pack('<I', A & 0xFFFFFFFF))  # old_0x3c
        femu.uc.mem_write(RAM + 0x3DC, struct.pack('<h', B))               # prev_0x14
        femu.uc.mem_write(RAM + 0x26E, struct.pack('<h', D))               # delta
        femu.uc.mem_write(RAM + 0x27A, struct.pack('<h', 500))             # v (не влияет на acc)
        def stop(uc_, a, s, u):
            aa = a & ~1
            if not (0 <= aa < 0x25000 or 0x08000000 <= aa < 0x08000000 + 0x25000):
                uc_.emu_stop()
        sh = femu.uc.hook_add(UC_HOOK_CODE, stop)
        femu.uc.reg_write(UC_ARM_REG_SP, STACK_TOP - 0x80)
        femu.uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        for r in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3):
            femu.uc.reg_write(r, 0)
        try:
            femu.uc.emu_start(0x1D898 | 1, 0, count=300000)
        except UcError:
            pass
        femu.uc.hook_del(sh)
        n3c = struct.unpack('<I', femu.uc.mem_read(RAM + 0x404, 4))[0]
        n14 = struct.unpack('<h', femu.uc.mem_read(RAM + 0x3DC, 2))[0]
        return n3c, n14
    # --- stateful-sweep: closed-form vs firmware (fresh emu per call) ---
    for _ in range(80):
        A = rng.randint(0, 0xFFFFFFFF)
        B = rng.randint(-3000, 3000)
        D = rng.randint(-5000, 5000)
        mx, ms = rm.acc_step(A, B, D)
        fx, fs = fw_acc(A, B, D)
        assert (fx, fs) == (mx, ms), f'A={A:#x} B={B} D={D}: fw=({fx},{fs}) model=({mx},{ms})'
    # --- edge-cases ---
    assert fw_acc(0, 0, 0) == rm.acc_step(0, 0, 0) == (0, 0)
    assert fw_acc(0, 0, 1024) == rm.acc_step(0, 0, 1024) == (1024, 1)


# --- 0x1d898 state-machine: гейты статус-флагов (§73.x) ---
@t(0x1D898, '§73.x range-sm: state-machine 0x1d898 — дефолт (zeroed): (0x290,0x292,0x2a8,0x2aa)=(2,140,1,78); гейт +0x286≠0 → (0x290,0x292)=(0,0); гейт +0x29e≠0 → (0x2a8,0x2aa)=(0,0). Флаги mode/LUT-driven (LUT 0x614-0x6c4/0x738-0x808), v/SoC не влияют. Fresh emu/call.')
def _(run, rng):
    from unicorn import UC_HOOK_CODE, UcError
    from unicorn.arm_const import UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3
    def status(extra):
        femu = McuEmu(max_insn=300000)
        femu.uc.mem_write(RAM, bytes(0x20000))
        femu.uc.mem_write(RAM + 0x27A, struct.pack('<h', 500))
        for off, val in extra.items():
            femu.uc.mem_write(RAM + off, struct.pack('<B', val))
        def stop(uc_, a, s, u):
            aa = a & ~1
            if not (0 <= aa < 0x25000 or 0x08000000 <= aa < 0x08000000 + 0x25000):
                uc_.emu_stop()
        sh = femu.uc.hook_add(UC_HOOK_CODE, stop)
        femu.uc.reg_write(UC_ARM_REG_SP, STACK_TOP - 0x80)
        femu.uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        for r in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3):
            femu.uc.reg_write(r, 0)
        try:
            femu.uc.emu_start(0x1D898 | 1, 0, count=300000)
        except UcError:
            pass
        femu.uc.hook_del(sh)
        def h(o):
            return struct.unpack('<h', femu.uc.mem_read(RAM + o, 2))[0]
        return (h(0x290), h(0x292), h(0x2a8), h(0x2aa))
    # --- дефолт (zeroed state) ---
    assert status({}) == (2, 140, 1, 78)
    # --- гейт +0x286: (0x290,0x292)→(0,0), (0x2a8,0x2aa) не меняется ---
    assert status({0x286: 1}) == (0, 0, 1, 78)
    # --- гейт +0x29e: (0x2a8,0x2aa)→(0,0), (0x290,0x292) не меняется ---
    assert status({0x29E: 1}) == (2, 140, 0, 0)
    # --- оба гейта ---
    assert status({0x286: 1, 0x29E: 1}) == (0, 0, 0, 0)


# --- FOC-интеграция в автономный контур (§73.x) ---
FW_LEN = 0x25000

def _foc_amp(ccr):
    center = sum(ccr) / 3.0
    return max(abs(c - center) for c in ccr), center


def _foc_run(uc, current_ref):
    """Полный FOC 0x1a938 на данном uc (общий RAM): current-ref u16[RAM+0x224] → CCR (RAM+0x382/384/386)."""
    from unicorn import UC_HOOK_CODE
    from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R4, UC_ARM_REG_SP, UC_ARM_REG_LR
    r4 = RAM + 0x040
    uc.mem_write(r4, bytes(0x80))
    uc.mem_write(r4 + 2, struct.pack('<h', 16384))          # value (mid) — не управляет PWM
    uc.mem_write(RAM + 0x224, struct.pack('<H', current_ref & 0xFFFF))
    def stop(uc_, a, s, u):
        aa = a & ~1
        if not (FLASH0 <= aa < FLASH0 + FW_LEN or FLASH1 <= aa < FLASH1 + FW_LEN):
            uc_.emu_stop()
    sh = uc.hook_add(UC_HOOK_CODE, stop)
    uc.reg_write(UC_ARM_REG_SP, STACK_TOP - 0x80)
    uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
    uc.reg_write(UC_ARM_REG_R4, r4)
    uc.reg_write(UC_ARM_REG_R0, 0)
    try:
        uc.emu_start(0x1A938 | 1, 0, count=200000)
    except Exception:
        pass
    uc.hook_del(sh)
    return tuple(struct.unpack('<H', uc.mem_read(RAM + o, 2))[0] for o in (0x382, 0x384, 0x386))


@t(0x1A938, '§73.x FOC-интеграция: transfer-функция current-ref u16[RAM+0x224]→PWM CCR (RAM+0x382/384/386): amp монотонно растёт с ref (0→~0, 4000→~41, 8000→~83, 16384→~169, 28624→~296), center≈1125..1131; CCR_A↑/CCR_B↓ (2-фазная FOC-модуляция). Интегрир. контур: PID(0x1d078)→throttle 0x42c→0x224→FOC→PWM, скорость растёт от 0.')
def _(run, rng):
    # --- transfer-функция FOC: amp монотонна в current-ref (fresh emu/call для чистоты) ---
    refs = (0, 4000, 8000, 16384, 28624)
    amps = []; centers = []
    for ref in refs:
        femu = McuEmu(trace=False, max_insn=200000)
        femu.uc.mem_write(RAM, bytes(0x20000))
        femu.hook_periph_ready()
        ccr = _foc_run(femu.uc, ref)
        amp, center = _foc_amp(ccr)
        amps.append(amp); centers.append(center)
    assert amps[0] < 1.0, f'ref=0 → amp должен ≈0, got {amps[0]}'
    for i in range(1, len(refs)):
        assert amps[i] > amps[i - 1], f'amp не монотонен: {amps}'
    for c in centers:
        assert 1120.0 <= c <= 1135.0, f'center вне [1120,1135]: {centers}'
    # CCR_A растёт, CCR_B падает с ref (2-фазная модуляция)
    femu = McuEmu(trace=False, max_insn=200000); femu.uc.mem_write(RAM, bytes(0x20000)); femu.hook_periph_ready()
    ccr_lo = _foc_run(femu.uc, 4000)
    femu = McuEmu(trace=False, max_insn=200000); femu.uc.mem_write(RAM, bytes(0x20000)); femu.hook_periph_ready()
    ccr_hi = _foc_run(femu.uc, 28624)
    assert ccr_hi[0] > ccr_lo[0], f'CCR_A не растёт: {ccr_lo} -> {ccr_hi}'
    assert ccr_hi[1] < ccr_lo[1], f'CCR_B не падает: {ccr_lo} -> {ccr_hi}'


# --- интегрированный контур: PID → throttle → FOC → PWM → plant (ОДИН emu, общий RAM) ---
@t(0x1D078, '§73.x FOC-контур (интегрир.): ОДИН McuEmu, общий RAM. Шаги: SpeedModel(speed→V)→PID 0x1d078→throttle s16[RAM+0x42c]→u16[RAM+0x224]=throttle→FOC 0x1a938 (тот же emu)→PWM CCR→plant(throttle→speed). За 6 шагов скорость монотонно растёт от 0, throttle>0, FOC-amp>0 (полная цепочка прошивки — PID+FOC — исполняется каждый шаг на общем RAM).')
def _(run, rng):
    from unicorn import UC_HOOK_CODE
    from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R4, UC_ARM_REG_SP, UC_ARM_REG_LR
    emu = McuEmu(max_insn=400000)
    uc = emu.uc
    sm = SpeedModel(emu)
    uc.mem_write(RAM, bytes(0x20000))
    uc.mem_write(RAM + 0x229, bytes([3]))
    uc.mem_write(RAM + 0x326, struct.pack('<H', 208))   # target
    uc.mem_write(RAM + 0x339, b'\x00'); uc.mem_write(RAM + 0x333, b'\x00'); uc.mem_write(RAM + 0x263, b'\x00')
    uc.mem_write(RAM + 0x1760, struct.pack('<I', 32760))
    uc.mem_write(RAM + 0x1764, struct.pack('<I', 0))
    uc.mem_write(RAM + 0x388, struct.pack('<I', 0))
    uc.mem_write(RAM + 0x3C8 + 0x28, struct.pack('<H', 1))
    def stop(uc_, a, s, u):
        aa = a & ~1
        if not (0 <= aa < FW_LEN or FLASH0 <= aa < FLASH0 + FW_LEN or FLASH1 <= aa < FLASH1 + FW_LEN):
            uc_.emu_stop()
    speed = 0.0; v_max = 522.0; tau = 15.0; tref = 28624.0
    speeds = []
    for it in range(6):
        sm.set_speed(int(speed))
        sh = uc.hook_add(UC_HOOK_CODE, stop)
        uc.reg_write(UC_ARM_REG_SP, STACK_TOP - 0x80); uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        for r in (UC_ARM_REG_R0, UC_ARM_REG_R4): uc.reg_write(r, 0)
        try: uc.emu_start(0x1D078 | 1, 0, count=400000)
        except Exception: pass
        uc.hook_del(sh)
        thr = struct.unpack('<h', uc.mem_read(RAM + 0x42c, 2))[0]
        ccr = _foc_run(uc, thr & 0xFFFF)   # FOC на ТОМ ЖЕ emu (общий RAM)
        amp, center = _foc_amp(ccr)
        if it == 0:
            assert thr > 0, f'PID не дал throttle: {thr}'
            assert amp > 10.0, f'FOC не дал PWM из throttle: amp={amp}'
        tnorm = max(0.0, min(1.0, thr / tref)) if tref else 0.0
        speed += (1.0 / tau) * (v_max * tnorm - speed)
        speeds.append(speed)
    assert speeds[-1] > speeds[0], f'скорость не растёт: {speeds}'
    assert all(speeds[i + 1] >= speeds[i] for i in range(len(speeds) - 1)), f'скорость не монотонна в рост: {speeds}'


# --- FOC current-ref→P copy + электро-контур (§73.x) ---
def _foc_run_pp(uc, current_ref, xlo=0, xhi=0, gate=False):
    """FOC 0x1a938: возвращает (ccr_a,ccr_b,ccr_c, P). current-ref u16[RAM+0x224], вектор 0x108/0x10a."""
    from unicorn import UC_HOOK_CODE
    from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R4, UC_ARM_REG_SP, UC_ARM_REG_LR
    r4 = RAM + 0x040
    uc.mem_write(r4, bytes(0x80))
    uc.mem_write(r4 + 2, struct.pack('<h', 16384))
    uc.mem_write(RAM + 0x224, struct.pack('<H', current_ref & 0xFFFF))
    uc.mem_write(RAM + 0x108, struct.pack('<h', xlo))
    uc.mem_write(RAM + 0x10a, struct.pack('<h', xhi))
    if gate:
        uc.mem_write(0x40012C54, struct.pack('<I', 0x8000))   # STAT bit15=1
    def stop(uc_, a, s, u):
        aa = a & ~1
        if not (FLASH0 <= aa < FLASH0 + FW_LEN or FLASH1 <= aa < FLASH1 + FW_LEN):
            uc_.emu_stop()
    sh = uc.hook_add(UC_HOOK_CODE, stop)
    uc.reg_write(UC_ARM_REG_SP, STACK_TOP - 0x80)
    uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
    uc.reg_write(UC_ARM_REG_R4, r4)
    uc.reg_write(UC_ARM_REG_R0, 0)
    try:
        uc.emu_start(0x1A938 | 1, 0, count=200000)
    except Exception:
        pass
    uc.hook_del(sh)
    ccr = tuple(struct.unpack('<H', uc.mem_read(RAM + o, 2))[0] for o in (0x382, 0x384, 0x386))
    P = struct.unpack('<I', uc.mem_read(RAM + 0x388, 4))[0]
    return ccr, P


@t(0x1A938, '§73.x FOC current-ref→P: P=u32[RAM+0x388]=[u16 RAM+0x224] (1:1, PC 0x1aae4) — current-ref идёт в cross+dot (§60.4) как P. Электро-контур НЕАКТИВЕН в изолированном FOC: measured vector s16[RAM+0x108/0x10a] не меняет PWM CCR (ни с gate=0, ни с STAT bit15=1) — feedback требует полного state-machine (сектор+реконструкция из ADC+PI) и live-gains мотора.')
def _(run, rng):
    # --- P = [0x224] (1:1 copy), для нескольких ref ---
    for ref in (4000, 8000, 16384):
        femu = McuEmu(trace=False, max_insn=200000)
        femu.uc.mem_write(RAM, bytes(0x20000))
        femu.hook_periph_ready()
        ccr, P = _foc_run_pp(femu.uc, ref)
        assert P == (ref & 0xFFFF), f'P({P:#x}) != [0x224]({ref:#x})'
    # --- электро-контур неактивен: вектор 0x108/0x10a не меняет CCR ---
    femu = McuEmu(trace=False, max_insn=200000); femu.uc.mem_write(RAM, bytes(0x20000)); femu.hook_periph_ready()
    ccr_base, _ = _foc_run_pp(femu.uc, 8000, 0, 0)
    for (xlo, xhi) in ((1000, 0), (0, 2000), (3000, -3000)):
        femu = McuEmu(trace=False, max_insn=200000); femu.uc.mem_write(RAM, bytes(0x20000)); femu.hook_periph_ready()
        ccr, _ = _foc_run_pp(femu.uc, 8000, xlo, xhi)
        assert ccr == ccr_base, f'veктор ({xlo},{xhi}) изменил CCR: {ccr} != {ccr_base}'
    # --- даже с активным гейтом (STAT bit15=1) feedback не включается в изоляции ---
    femu = McuEmu(trace=False, max_insn=200000); femu.uc.mem_write(RAM, bytes(0x20000)); femu.hook_periph_ready()
    ccr_g, _ = _foc_run_pp(femu.uc, 8000, 3000, -3000, gate=True)
    assert ccr_g == ccr_base, f'гейт включил feedback: {ccr_g} != {ccr_base}'
