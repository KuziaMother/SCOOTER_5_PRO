# -*- coding: utf-8 -*-
"""E2-b65: OTA-команды (0xE0/0xE2), stack-структура init, event-queue push,
duty-регулятор, TX-дескриптор (USART3/USART4), local-table через 0x12f44,
"queue-empty" предикат, one-shot flag u32@0x8C, GPIO-дескриптор {ptr,0,0}."""
# ruff: noqa: F405  (имена из star-import от fv_core)
from fv_core import *  # noqa: F401,F403
from fv_core import _fresh_call, _intercept  # noqa: F401

from emulator.mcu_emu import PERIPH, PERIPH2

STA_PTR = STACK_TOP + 4  # 0x0bb14: ldrd sb,r4,[sp+0x58] → r4 = u32[STACK_TOP+4]


def _call_regs(off, regvals, seeds=(), max_insn=50000):
    """Свежий McuEmu (zero-RAM + periph-ready), заданные регистры, LR=0x0BADF001,
    стоп при выходе из flash. Возвращает emu."""
    emu = McuEmu(max_insn=max_insn)
    uc = emu.uc
    uc.mem_write(RAM, bytes(0x20000))
    emu.hook_periph_ready()
    for a, d in seeds:
        uc.mem_write(a, d)
    for reg, v in regvals.items():
        uc.reg_write(reg, v)
    uc.reg_write(UC_ARM_REG_SP, STACK_TOP)
    uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)

    def _stop(uc_, addr, size, user):
        if not (FLASH0 <= addr < FLASH0 + 0x23680 or FLASH1 <= addr < FLASH1 + 0x23680):
            uc_.emu_stop()
    h = uc.hook_add(UC_HOOK_CODE, _stop)
    try:
        uc.emu_start(off | 1, 0, count=max_insn)
    except UcError:
        pass
    uc.hook_del(h)
    return emu


@t(0x0DDC4, 'E2-b65: 0x0ddc4() — OTA-команды из u16[0x1260/0x1262] (база 0x124E+0x12/0x14): '
            '0xE0+0x5AA5 → 0x7e98(erase-адрес из пула, ∈[0x08003000,0x0801FFFF) → fp P+0x22004='
            '0xCDEF89AB) + 0xdd80; 0xE2+0x5AA5 → 0xdd80 (u32[0xE000ED0C] SysTick CTRL '
            '= 0x05FA0004, спин); magic-mismatch → ret = последний ldrh (0xE2-ветка: u16[0x1262], '
            'иначе u16[0x1260]); нет действия.')
def _(run, rng):
    from emulator.mcu_emu import PERIPH as _P
    SYST = 0xE000ED0C  # SysTick CTRL (литерал L3 в 0xdd80)
    CANARY = 0x5A5A5A5A
    for _ in range(6):
        kind = rng.choice(['none', 'e0', 'e0bad', 'e2', 'e2bad'])
        if kind == 'none':
            m0 = rng.choice([0x1234, 0xE1, 0xE3, 0x0000])
            m1 = rng.getrandbits(16)
        elif kind == 'e0':
            m0, m1 = 0xE0, 0x5AA5
        elif kind == 'e0bad':
            m0, m1 = 0xE0, rng.choice([0x5AA4, 0x5AA6, 0x0000])
        elif kind == 'e2':
            m0, m1 = 0xE2, 0x5AA5
        else:
            m0, m1 = 0xE2, rng.choice([0x5AA4, 0x5AA6, 0x0000])
        run.ram_write(0x1260, struct.pack('<HH', m0, m1))
        run.periph_write(_P + 0x22004, CANARY)
        run.periph_write(_P + 0x2200C, 0)  # детерм. путь 0x7e98 (как в его тесте b58)
        run.periph_write(SYST, 0)
        max_i = 100000 if kind == 'e0' else 30000
        ret, _ = run.call(0x0DDC4, (), max_insn=max_i)
        fp = run.periph_read(_P + 0x22004)
        syst = run.periph_read(SYST)
        if kind == 'none':
            assert ret == m0 and fp == CANARY and syst == 0, (
                f'magic нет: ret={ret:#x} fp={fp:#x} syst={syst:#x} ждём ret=m0={m0:#x} (ldrh [L+0x12])')
        elif kind == 'e0':
            assert fp == 0xCDEF89AB, f'0xE0+magic: fp={fp:#x} ждём erase-путь (0x7e98)'
        elif kind == 'e2':
            assert syst == 0x05FA0004, f'0xE2+magic: SysTick={syst:#x} ждём 0x05fa0004 (0xdd80)'
            assert fp == CANARY, f'0xE2+magic: fp={fp:#x} — erase не вызывается'
        else:
            exp_ret = m1 if m0 == 0xE2 else m0  # r0 = последний ldrh (0xE2-ветка догружает m1)
            assert ret == exp_ret and fp == CANARY and syst == 0, (
                f'{kind}: ret={ret:#x} fp={fp:#x} syst={syst:#x} ждём ret={exp_ret:#x}')


@t(0x02D70, 'E2-b65: 0x02d70() — stack-структура init (fresh-emu, SP=STACK_TOP−0x40): [sp+4]='
            '0x000186A0 (литерал), [sp+8]=0, [sp+0xA]=0xBFFF, [sp+0xC]=0x30, [sp+0xE]=0x400, '
            '[sp+0x10]=0x4000; 0x332c×2, wait-цикл 0x3E8, 0x2e0c(sp+4), 0x9874(0x20000)→0 → '
            'без инкремента; ret 0.')
def _(run, rng):
    for _ in range(3):
        ret, emu = _fresh_call(0x02D70, (), max_insn=20000)
        sp_final = (STACK_TOP - 0x40 - 4 - 0x14) & M32
        blob = bytes(emu.uc.mem_read(sp_final + 4, 0x10))
        exp = struct.pack('<IHHHHI', 0x000186A0, 0x0000, 0xBFFF, 0x0030, 0x0400, 0x4000)
        assert blob == exp, (
            f'struct {blob.hex()} ≠ {exp.hex()}: '
            f'[+4]={struct.unpack_from("<I", blob, 0)[0]:#x} [+8]={blob[4:6].hex()} '
            f'[+A]={blob[6:8].hex()} [+C]={blob[8:10].hex()} [+E]={blob[10:12].hex()} '
            f'[+10]={blob[12:14].hex()}')
        assert ret == 0, f'ret={ret:#x}'


@t(0x04C98, 'E2-b65: 0x04c98(r4=slot, r6=delta) — event-queue @0x164C: u32[slot+4]=u32[0xB4C]+r6, '
            'byte[slot]=1, byte[slot+1]=(r6==0), bl 0x2d34 (снять критсек).')
def _(run, rng):
    for _ in range(10):
        delta = rng.choice([0, 1, 5, 100, 0x7FFF])
        b4c = rng.getrandbits(32)
        emu = _call_regs(0x04C98, {UC_ARM_REG_R4: RAM + 0x164C, UC_ARM_REG_R6: delta},
                         seeds=[(RAM + 0xB4C, struct.pack('<I', b4c))], max_insn=5000)
        uc = emu.uc
        slot = bytes(uc.mem_read(RAM + 0x164C, 8))
        exp_val = (b4c + delta) & M32
        assert slot[0] == 1, f'r6={delta}: byte[slot]={slot[0]} ждём 1'
        assert slot[1] == (1 if delta == 0 else 0), (
            f'r6={delta}: byte[slot+1]={slot[1]} ждём {1 if delta == 0 else 0}')
        got = struct.unpack_from('<I', slot, 4)[0]
        assert got == exp_val, f'r6={delta} b4c={b4c:#x}: u32[slot+4]={got:#x} ждём {exp_val:#x}'


@t(0x0799C, 'E2-b65: 0x0799c() — duty-регулятор (fresh-emu): 0x8f58() пишет u16[0x135E]=s8(FC8); '
            'цепь 0x11010/0xe160/0x16222/0x164f8/0x162ce деградирует на свежих входах: u16[0x1346] '
            'не меняется (любой FC8/0x138C), u16[0x1390]:=0, byte[0x138F]:=0.')
def _(run, rng):
    for _ in range(12):
        fc8 = rng.choice([0, 1, 2, 3, 0x7F])
        v = rng.getrandbits(16)
        seeds = [(RAM + 0xFC8, bytes([fc8])),
                 (RAM + 0x1346, struct.pack('<H', v)),
                 (RAM + 0x138C, struct.pack('<H', rng.getrandbits(16)))]
        ret, emu = _fresh_call(0x0799C, (), extra_ram=seeds, max_insn=50000)
        uc = emu.uc
        got = struct.unpack_from('<H', bytes(uc.mem_read(RAM + 0x1346, 2)))[0]
        assert got == v, f'FC8={fc8} in={v:#x}: u16[0x1346]={got:#x} ждём {v:#x} (pass-through)'
        assert struct.unpack_from('<H', bytes(uc.mem_read(RAM + 0x1390, 2)))[0] == 0, 'u16[0x1390] ≠ 0'
        assert bytes(uc.mem_read(RAM + 0x138F, 1))[0] == 0, 'byte[0x138F] ≠ 0'
        got135e = struct.unpack_from('<H', bytes(uc.mem_read(RAM + 0x135E, 2)))[0]
        exp135e = (fc8 - 0x100 if fc8 >= 0x80 else fc8) & 0xFFFF  # s8 → i16 → u16
        assert got135e == exp135e, f'u16[0x135E]={got135e:#x} ждём {exp135e:#x} (0x8f58)'


@t(0x1F6B4, 'E2-b65: 0x1f6b4() — TX-дескриптор (fresh-emu, L=0x48000800 из пула): [sp]='
            '{02 00 00 00 00 00 02 00}, [sp+8]=0x40004800, [sp+0xC]=0x4B00, [sp+0x10]=0, [sp+0x14]=0; '
            '0x22000(L,sp,0x40/0x80) → [L+0x10]=0xA000, [L+0x14..0x24]=0, [L+0x28]=0x22000000; '
            '0x23188(sp+8), 0x21bc8(0x1D,5), 0x21b6c(0x1D) → ret 0xFFFFFFFF (tail-блок 0x1f6b4 обходится).')
def _(run, rng):
    for _ in range(3):
        ret, emu = _fresh_call(0x1F6B4, (), max_insn=100000)
        uc = emu.uc
        B = PERIPH2 + 0x800
        sp_rel = (STACK_TOP - 0x40 - RAM - 0xC - 0x8C) & M32
        blob = bytes(uc.mem_read(RAM + sp_rel, 0x18))
        exp = bytes([2, 0, 0, 0, 0, 0, 2, 0]) + struct.pack('<IIII', 0x40004800, 0x4B00, 0, 0)
        assert blob == exp, f'desc {blob.hex()} ≠ {exp.hex()}'
        assert struct.unpack_from('<I', bytes(uc.mem_read(B + 0x10, 4)))[0] == 0xA000, (
            f"[L+0x10]={struct.unpack_from('<I', bytes(uc.mem_read(B + 0x10, 4)))[0]:#x}")
        for off in (0x14, 0x18, 0x1C, 0x20, 0x24):
            assert struct.unpack_from('<I', bytes(uc.mem_read(B + off, 4)))[0] == 0, f'[L+{off:#x}]≠0'
        assert struct.unpack_from('<I', bytes(uc.mem_read(B + 0x28, 4)))[0] == 0x22000000, (
            f"[L+0x28]={struct.unpack_from('<I', bytes(uc.mem_read(B + 0x28, 4)))[0]:#x}")
        assert ret == 0xFFFFFFFF, f'ret={ret:#x} ждём 0xffffffff (0x21b6c)'


@t(0x04A30, 'E2-b65: 0x04a30() — local-table lookup: bl 0x4a04 (заполнение таблицы 0x12C..), '
            'r0=sp+4; bl 0x12f44 (free #2, база 0x1D38): state&7==0 → ret 0; иначе free '
            '(сценарий _free3_ref: скан (cnt0+1)%3.. до заданного бита), u16[dst]=len, '
            'data→dst+2; bl 0xdf10(dst): magic-gate byte[dst+2]≠0xAA → ret=byte[dst+2] '
            '(первый байт освобождённых данных).')
def _(run, rng):
    S = 0x1D38
    for _ in range(8):
        empty = rng.random() < 0.3
        if empty:
            state, cnt0 = 0, rng.randint(0, 2)
        else:
            state = rng.choice([0b001, 0b010, 0b100, 0b110, 0b101, 0b111])
            cnt0 = rng.randint(0, 2)
        data0 = rng.choice([0x55, 0x77, 0x01, 0x3C, 0xFF])  # ≠ 0xAA — magic-mismatch путь
        slots = []
        for i in range(3):
            ln = rng.randint(1, 8)
            data = bytes(rng.getrandbits(8) for _ in range(8))
            if i == 0:
                data = bytes([data0]) + data[1:]
            slots.append((ln, data))
        for i in range(3):
            ln, data = slots[i]
            run.ram_write(S + 2 + 152 * i, struct.pack('<H', ln) + data)
        run.ram_write(S, bytes([state, cnt0]))
        ret, _ = run.call(0x04A30, (), max_insn=20000)
        if empty:
            assert ret == 0, f'пусто: ret={ret:#x}'
            continue
        cnt = cnt0
        while True:
            cnt = (cnt + 1) % 3
            if state & (1 << cnt):
                break
        got_state = run.ram_read(S, 1)[0]
        got_cnt = run.ram_read(S + 1, 1)[0]
        assert got_state == (state & ~(1 << cnt)) & 0xFF, (
            f'byte[S]={got_state:#x} ждём {(state & ~(1 << cnt)):#x}')
        assert got_cnt == cnt, f'byte[S+1]={got_cnt} ждём {cnt}'
        exp = slots[cnt][1][0]
        assert ret == exp, f'ret={ret:#x} ждём {exp:#x} (0xdf10 magic-mismatch)'


@t(0x0BB14, 'E2-b65: 0x0bb14() — "queue-empty" (указатель struct из u32[STACK_TOP−0x3C] через ldrd, '
            'fresh-emu): u32[st]==0 → ret 1 (пусто); u32[st]!=0 && byte[st+0x13]==0 → полный путь '
            '(0x11a4×2, 0xb8dc(st)) → ret 3, byte[0xF0B]:=0, u16[st+0x9E]=0, u16[st+0xA0]=0; '
            'byte[st+0x13]==1 → путь 0x2d1c → ret 0 (fresh-emu).')
def _(run, rng):
    ST = 0x1400
    # _fresh_call: SP = STACK_TOP−0x40, push 11 + sub 0x2C → sp_f = STACK_TOP−0x98;
    # ldrd sb,r4,[sp+0x58]: r4 = u32[sp_f+0x5C] = u32[STACK_TOP−0x3C]
    PTR_SLOT = (STACK_TOP - 0x3C) & M32
    for _ in range(6):
        empty = rng.random() < 0.4
        st_val = 0 if empty else rng.randint(1, 0xFFFFFFFF)
        b13 = 0 if not empty else rng.getrandbits(8)
        seeds = [(PTR_SLOT, struct.pack('<I', RAM + ST)),
                 (RAM + ST, struct.pack('<I', st_val)),
                 (RAM + ST + 0x13, bytes([b13])),
                 (RAM + 0xF0B, bytes([rng.getrandbits(8)]))]
        ret, emu = _fresh_call(0x0BB14, (), extra_ram=seeds, max_insn=200000)
        uc = emu.uc
        if empty:
            assert ret == 1, f'пусто: ret={ret:#x} ждём 1'
            continue
        if b13 == 0:
            assert ret == 3, f'непусто st+0x13=0: ret={ret:#x} ждём 3 (0xb8dc fresh-emu)'
            assert bytes(uc.mem_read(RAM + 0xF0B, 1))[0] == 0, 'byte[0xF0B] ≠ 0 (запись 0 в bb38)'
            assert struct.unpack_from('<H', bytes(uc.mem_read(RAM + ST + 0x9E, 2)))[0] == 0, 'u16[st+0x9E] ≠ 0'
            assert struct.unpack_from('<H', bytes(uc.mem_read(RAM + ST + 0xA0, 2)))[0] == 0, 'u16[st+0xA0] ≠ 0'
        else:
            assert ret == 0, f'b13={b13}: ret={ret:#x} ждём 0 (путь 0x2d1c, fresh-emu)'
            assert bytes(uc.mem_read(RAM + 0xF0B, 1))[0] == seeds[3][1][0], 'b13≠0: byte[0xF0B] должен не меняться'


@t(0x0D700, 'E2-b65: 0x0d700(r0) — one-shot flag u32@0x8C: "lsls r0,r0" → u32[0x8C] = r0 << '
            '(r0&0x3F) mod 2^32 (для r0 с нулевыми низкими 6 битами — тождественно).')
def _(run, rng):
    for _ in range(10):
        r0 = rng.choice([0x200, 0x1000, 0x2000, 0x8000, 0, 0x7000, 0x05FA0000])
        seed = rng.getrandbits(32)
        emu = _call_regs(0x0D700, {UC_ARM_REG_R0: r0},
                         seeds=[(RAM + 0x8C, struct.pack('<I', seed))], max_insn=1000)
        got = struct.unpack_from('<I', bytes(emu.uc.mem_read(RAM + 0x8C, 4)))[0]
        exp = (r0 << (r0 & 0x3F)) & M32
        assert got == exp, f'r0={r0:#x}: u32[0x8C]={got:#x} ждём {exp:#x}'


@t(0x0BC86, 'E2-b65: 0x0bc86() — GPIO-дескриптор (fresh-emu): 0x87b0(sp), local: u16[sp]=0 '
            '(после 0x85c8), byte[sp+3]=1, byte[sp+4]=0, u32[sp+8]=3; r0=[caller SP+8], '
            'bl 0x85c8(r0, sp) → ret 0x1000000 (оба варианта base: 0 и GPIO).')
def _(run, rng):
    for _ in range(4):
        base = rng.choice([0, PERIPH2 + 0x800])
        a, b = rng.getrandbits(16), rng.getrandbits(16)
        seeds = [(STACK_TOP + 0, struct.pack('<H', a)),
                 (STACK_TOP + 4, struct.pack('<H', b)),
                 (STACK_TOP + 8, struct.pack('<I', base))]
        emu = _call_regs(0x0BC86, {}, seeds=seeds, max_insn=50000)
        uc = emu.uc
        sp_final = (STACK_TOP - 24) & M32
        blob = bytes(uc.mem_read(sp_final, 0xC))
        assert blob[0] == 0 and blob[1] == 0, f'u16[sp]={blob[0:2].hex()} ждём 0000'
        assert blob[3] == 1, f'byte[sp+3]={blob[3]} ждём 1'
        assert blob[4] == 0, f'byte[sp+4]={blob[4]} ждём 0'
        assert struct.unpack_from('<I', blob, 8)[0] == 3, (
            f'u32[sp+8]={struct.unpack_from("<I", blob, 8)[0]} ждём 3')
        assert uc.reg_read(UC_ARM_REG_R0) == 0x1000000, (
            f'r0={uc.reg_read(UC_ARM_REG_R0):#x} ждём 0x1000000')
