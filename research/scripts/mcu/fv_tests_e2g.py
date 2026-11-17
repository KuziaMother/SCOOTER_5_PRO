# -*- coding: utf-8 -*-
# ruff: noqa: F405  (имена из star-import от fv_core)
"""E2-batch57 + пороговые счётчики (7177-8203)."""
from fv_core import *  # noqa: F401,F403
from fv_core import _fresh_call, _intercept  # noqa: F401
# --- E2-batch57: предикаты/валидаторы/NVIC-сеты/пороговые счётчики (pool-литералы эмпирически) ---
def _t_12804(run, rng):
    # 0x12804: ret = (arg <= u16[FLASH+0x19B3C]) ? 0x65 : -31.
    # Блок бинарного поиска (0x1282c..) — мёртвый код для этой таблицы (first<last).
    from emulator.mcu_emu import FLASH0
    img = open('D:/SCOOTER_5_PRO/research/images/mcu_0007.bin', 'rb').read()
    first = struct.unpack_from('<H', img, 0x19B3C)[0]
    for arg in (0, first - 1, first, first + 1, 0xFFFF):
        r0, _ = run.call(0x12804, args=(arg,), max_insn=20000)
        exp = 0x65 if arg <= first else (-31 & 0xFFFFFFFF)
        assert r0 == exp, f'arg={arg:#x}: r0={r0:#x} want {exp:#x}'
t(0x12804, 'E2-b57: 0x12804 порог: arg<=u16[FLASH+0x19B3C](=0x1980) -> 0x65; иначе -31 (блок поиска мёртв)')(_t_12804)

def _t_b978(run, rng):
    # 0xb978: q = u32[orig_sp+4] (stack-arg!); u32[q]==0 -> ret1; byte[q+0x13]!=0 -> ret0;
    # иначе init-путь: u16[q+0x36]=0 + запись флагов, ret3. Запускаем на отдельном McuEmu
    # (Run.call ставит SP=STACK_TOP, и [SP+4] уже вне RAM).
    from unicorn import UC_HOOK_CODE
    from unicorn.arm_const import UC_ARM_REG_SP as _SP, UC_ARM_REG_LR as _LR
    Q = 0x400
    sp0 = STACK_TOP - 0x80
    for _ in range(12):
        q0 = rng.choice([0, 1, rng.randint(1, 0xFFFF)])
        b13 = rng.choice([0, 0, 2, 3, 0xFF])   # b13==1 — handler-путь (blx в ноль), не проверяем
        emu = McuEmu(max_insn=50000)
        uc = emu.uc
        uc.mem_write(RAM, bytes(0x20000))
        qb = bytearray(0x60)
        struct.pack_into('<I', qb, 0, q0); qb[0x13] = b13
        uc.mem_write(RAM + Q, bytes(qb))
        uc.mem_write(sp0 + 4, struct.pack('<I', RAM + Q))
        def _code(uc_, a, s, ud):
            aa = a & ~1
            if not (FLASH0<=aa<FLASH0+0x23680 or FLASH1<=aa<FLASH1+0x23680):
                uc_.emu_stop()
        sh = uc.hook_add(UC_HOOK_CODE, _code)
        uc.reg_write(_SP, sp0)
        uc.reg_write(_LR, 0x0BADF001)
        emu.insn = 0
        try: uc.emu_start(0xB978 | 1, 0, count=50000)
        except UcError as e: pass
        r0 = uc.reg_read(UC_ARM_REG_R0)
        if q0 == 0:
            exp = 1
        elif b13 == 0:
            exp = 3
            u36 = struct.unpack('<H', bytes(uc.mem_read(RAM + Q + 0x36, 2)))[0]
            assert u36 == 0, f'q0={q0:#x}: u16[q+0x36]={u36:#x} want 0'
        else:   # b13 >= 2 — активное состояние
            exp = 0
        assert r0 == exp, f'q0={q0:#x} b13={b13}: r0={r0} want {exp}'
t(0xB978, 'E2-b57: 0xb978 очередь (stack-arg q=[sp+4]): u32[q]==0->1; byte[q+0x13]>=2->0; ==0 -> init u16[q+0x36]=0->3')(_t_b978)

def _ref_bcc0(type_, val, b1, e0_lo, p0a, p0h, e1_lo, p1a, p1h):
    # 0xbcc0: type/val = u16_be[f+2]/[f+4]; local=(val<<1)&0xFFFF; если b1==6: local=2;
    # range-поиск 0xbeec по таблице @RAM+0x7C4 (out/gate=@RAM+0x7D4);
    # при match: (byte[ptr+8]*byte[ptr+1]) >= local && lo+H >= val+type -> success.
    local = (val << 1) & 0xFFFF
    if b1 == 6:
        local = 2
    entry = None
    for lo, A, H in ((e0_lo, p0a, p0h), (e1_lo, p1a, p1h)):
        if lo <= type_ < lo + H:
            entry = (lo, A, H); break
    if entry is None:
        return 0, 0
    lo, A, H = entry
    if (H * A) < local:
        return 0, 0
    if lo + H < val + type_:
        return 0, 0
    return 1, local & 0xFF

def _t_bcc0(run, rng):
    from emulator.mcu_emu import RAM as _R
    for _ in range(15):
        e0_lo = rng.randint(0, 0x40); p0a = rng.randint(0, 0x20); p0h = rng.randint(1, 0x40)
        e1_lo = rng.randint(0x40, 0x80); p1a = rng.randint(0, 0x20); p1h = rng.randint(1, 0x40)
        type_ = rng.randint(0, 0xC0); val = rng.randint(0, 0x60); b1 = rng.choice([0, 0, 6])
        run.ram_write(0x7C4, struct.pack('<IB3x', _R + 0x500, e0_lo) + struct.pack('<IB3x', _R + 0x600, e1_lo))
        pl0 = bytearray(16); pl0[1] = p0a; pl0[8] = p0h
        pl1 = bytearray(16); pl1[1] = p1a; pl1[8] = p1h
        run.ram_write(0x500, bytes(pl0)); run.ram_write(0x600, bytes(pl1))
        fr = bytearray(0x20)
        fr[1] = b1; fr[2], fr[3] = type_ >> 8, type_ & 0xFF   # u16 BE
        fr[4], fr[5] = val >> 8, val & 0xFF
        run.ram_write(0x400, bytes(fr))
        r0, _ = run.call(0xBCC0, args=(_R + 0x400,), max_insn=20000)
        exp_r0, exp_f6 = _ref_bcc0(type_, val, b1, e0_lo, p0a, p0h, e1_lo, p1a, p1h)
        got_f6 = run.ram_read(0x406, 1)[0]
        assert r0 == exp_r0, f'type={type_} val={val} b1={b1}: r0={r0} want {exp_r0}'
        assert got_f6 == exp_f6, f'type={type_} val={val}: f[6]={got_f6:#x} want {exp_f6:#x}'
t(0xBCC0, 'E2-b57: 0xbcc0 frame-валидатор: u16_BE type/val; range-поиск 0xbeec (gate@RAM+0x7D4); H*A>=local && lo+H>=val+type -> f[6]=local,f[7]=0,ret1')(_t_bcc0)

def _t_22b7c(run, rng):
    # 0x22b7c: k=byte[r1+4]∈{0..4}, j=byte[r1+0xC]∈{0..2} (иначе спин);
    # k>=2: u32[base]=(old&~0x60)|((k-2)<<6); иначе u32[base]&=~0x70;
    # base∈{0x40000000,TIM4..}: u32[base]=(old&~0x300)|(j<<8);
    # u32[base+0x3C]=u32[r1+8]; u32[base+0x38]=u32[r1+0];
    # base∈{TIM4..,TIM2}: u32[base+0x40]=(old&0xFF00FF)|(u32[r1+0x10]&0xFF); u32[base+0x24]|=1
    # base — абсолютные адреса регистров TIM (PERIPH-диапазон); эмпирика:
    VJ = {0x40000000, 0x40000400, 0x40012C00, 0x40014000, 0x40014400, 0x40014800, 0x40014C00}
    V40 = {0x40012C00, 0x40014000, 0x40014400, 0x40014800, 0x40014C00}
    for _ in range(15):
        k = rng.randint(0, 4); j = rng.randint(0, 2)
        base = rng.choice(sorted(VJ) + [0x40001000])
        f0 = rng.randint(0, 0xFFFFFFFF); f8 = rng.randint(0, 0xFFFFFFFF)
        f10 = rng.randint(0, 0xFF); old = rng.randint(0, 0xFFFFFFFF)
        st = bytearray(0x20); st[4] = k; st[0xC] = j
        struct.pack_into('<I', st, 0, f0); struct.pack_into('<I', st, 8, f8)
        struct.pack_into('<I', st, 0x10, f10)
        run.ram_write(0x400, bytes(st))
        run.periph_write(base, old)
        run.call(0x22B7C, args=(base, RAM + 0x400), max_insn=20000)
        e = old
        if k >= 2: e = (e & ~0x60) | ((k << 5) - 0x20)   # биты[7:6] = k-1
        else: e = (e & ~0x70) | (k << 4)                 # k=0/1: свой путь (0x22c3a), j-блок всё же применяется
        if base in VJ: e = (e & ~0x300) | (j << 8)
        g = run.periph_read(base)
        assert g == e, f'k={k} j={j} base={base:#x} old={old:#x}: {g:#x} want {e:#x}'
        assert run.periph_read(base + 0x3C) == f8, 'field+0x3c'
        assert run.periph_read(base + 0x38) == f0, 'field+0x38'
        if base in V40:
            assert (run.periph_read(base + 0x40) & 0xFF) == f10, 'field+0x40'
        assert run.periph_read(base + 0x24) & 1, 'bit0 @+0x24'
    # спин при k>4 / j>2: на отдельном McuEmu — дошёл до лимита инструкций
    from unicorn import UC_HOOK_CODE
    from unicorn.arm_const import UC_ARM_REG_SP as _SP, UC_ARM_REG_LR as _LR
    for bad in ((5, 0), (0, 3)):
        emu = McuEmu(max_insn=2000)
        uc = emu.uc
        uc.mem_write(RAM, bytes(0x20000))
        st = bytearray(16); st[4] = bad[0]; st[0xC] = bad[1]
        uc.mem_write(RAM + 0x400, bytes(st))
        def _code(uc_, a, s, ud):
            aa = a & ~1
            if not (FLASH0<=aa<FLASH0+0x23680 or FLASH1<=aa<FLASH1+0x23680):
                uc_.emu_stop()
        sh = uc.hook_add(UC_HOOK_CODE, _code)
        uc.reg_write(UC_ARM_REG_R0, 0x40012C00); uc.reg_write(UC_ARM_REG_R1, RAM + 0x400)
        uc.reg_write(_SP, STACK_TOP - 0x40); uc.reg_write(_LR, 0x0BADF001)
        emu.insn = 0
        try: uc.emu_start(0x22B7C | 1, 0, count=2000)
        except UcError as e: pass
        assert emu.insn >= 1990, f'k={bad[0]} j={bad[1]}: insn={emu.insn} (ожидался спин)'
t(0x22B7C, 'E2-b57: 0x22b7c TIM-CR1 сеттер: k=byte[r1+4]∈0..4,j=byte[r1+0xC]∈0..2 (иначе спин); k≥2: биты[7:6]=k-1; k∈{0,1}: чистит[7:5], k=1 ставит бит5; j-блок (7 баз): биты[9:8]=j; поля +0x3C/+0x38/+0x40')(_t_22b7c)

# --- пороговые счётчики #5/#2/#6 (общий паттерн: фаза A считает, latch-бит, фаза B) ---
def _s8(b): return b - 0x100 if b >= 0x80 else b

def _ref_10468(mode, b5, v, c1, c2):
    # 0x10468: b5=bit5(byte@FCD); V=s8[FC8];
    # фаза A (gate byte@80∈{1,2} и b5==0): s8[F+0x19E3A]=10, cap u16[F+0x19E3B]=0xAAE:
    #   v>10 -> c1=0; иначе c1+=1; c1>=cap -> b5=1, c1=0.
    # фаза B (b5==1) — ВСЕГДА (gate не влияет): s8[F+0x19E3D]=-32, cap u16[F+0x19E3F]=0x5F:
    #   v<-32 -> c2=0; иначе c2+=1; c2>=cap -> b5=0, c2=0.
    if mode in (1, 2) and b5 == 0:
        if v > 10: c1 = 0
        else:
            c1 += 1
            if c1 >= 0xAAE: b5 = 1; c1 = 0
    if b5 == 1:
        if v < -32: c2 = 0
        else:
            c2 += 1
            if c2 >= 0x5F: b5 = 0; c2 = 0
    return c1, c2, b5

def _t_10468(run, rng):
    from emulator.mcu_emu import RAM as _R
    for _ in range(15):
        mode = rng.randint(0, 3)
        b5 = rng.getrandbits(1)
        v = rng.choice([0, 10, 11, -32, -33, rng.randint(-0x80, 0x7F)])
        c1 = rng.choice([0, 1, 0xAAD, 0xAAE, 0xAAF])
        c2 = rng.choice([0, 1, 0x5E, 0x5F, 0x60])
        run.ram_write(0x80, bytes([mode]))
        run.ram_write(0xFCD, bytes([b5 << 5]))
        run.ram_write(0xFC8, bytes([v & 0xFF]))
        run.ram_write(0x9EE, struct.pack('<H', c1))
        run.ram_write(0x9EC, struct.pack('<H', c2))
        run.call(0x10468, args=(), max_insn=20000)
        e1, e2, eb5 = _ref_10468(mode, b5, v, c1, c2)
        g1 = struct.unpack('<H', run.ram_read(0x9EE, 2))[0]
        g2 = struct.unpack('<H', run.ram_read(0x9EC, 2))[0]
        gb5 = (run.ram_read(0xFCD, 1)[0] >> 5) & 1
        assert (g1, g2, gb5) == (e1, e2, eb5), f'mode={mode} b5={b5} v={v}: got ({g1},{g2},{gb5}) want ({e1},{e2},{eb5})'
t(0x10468, 'E2-b57: 0x10468 порог #5: gate byte@80∈{1,2}; bit5(byte@FCD); s8[FC8] vs flash 10/-32; счётчики @9EE/@9EC, latch-бит5')(_t_10468)

def _ref_10524(b1, v, c1, c2):
    # 0x10524: b1=bit1(byte@FD0); V=s8[FCF]; фаза A (b1==0): s8[F+0x19E4C]=-86, cap u16[F+0x19E4D]=0x7C18:
    #   v<-86 -> c1=0; иначе c1+=1; c1>=cap -> b1=1, c1=0. Фаза B (b1==1): s8[F+0x19E4F]=65, cap u16[F+0x19E50]=0x1C49:
    #   v>65 -> c2=0; иначе c2+=1; c2>=cap -> b1=0, c2=0.
    if b1 == 0:
        if v < -86: c1 = 0
        else:
            c1 += 1
            if c1 >= 0x7C18: b1 = 1; c1 = 0
    else:
        if v > 65: c2 = 0
        else:
            c2 += 1
            if c2 >= 0x1C49: b1 = 0; c2 = 0
    return c1, c2, b1

def _t_10524(run, rng):
    for _ in range(15):
        b1 = rng.getrandbits(1)
        v = rng.choice([0, -86, -87, 65, 66, rng.randint(-0x80, 0x7F)])
        c1 = rng.choice([0, 1, 0x7C18, 0x7C19])
        c2 = rng.choice([0, 1, 0x1C49, 0x1C4A])
        run.ram_write(0xFD0, bytes([b1 << 1]))
        run.ram_write(0xFCF, bytes([v & 0xFF]))
        run.ram_write(0x9E4, struct.pack('<H', c1))
        run.ram_write(0x9E6, struct.pack('<H', c2))
        run.call(0x10524, args=(), max_insn=20000)
        e1, e2, eb1 = _ref_10524(b1, v, c1, c2)
        g1 = struct.unpack('<H', run.ram_read(0x9E4, 2))[0]
        g2 = struct.unpack('<H', run.ram_read(0x9E6, 2))[0]
        gb1 = (run.ram_read(0xFD0, 1)[0] >> 1) & 1
        assert (g1, g2, gb1) == (e1, e2, eb1), f'b1={b1} v={v}: got ({g1},{g2},{gb1}) want ({e1},{e2},{eb1})'
t(0x10524, 'E2-b57: 0x10524 порог #2: bit1(byte@FD0); s8[FCF] vs flash -86/65; счётчики @9E4/@9E6, latch-бит1')(_t_10524)

def _ref_105c4(mode, b6, v, cA, cB, fb):
    # 0x105c4: b6=bit6(byte@FA1); V=u16[F99] (беззнак);
    # фаза A (gate byte@80∈{1,2} и b6==0): v>u16[F+0x19DDC](=0x849) -> cA=0; иначе cA+=1;
    #   cA>u16[F+0x19DE0](=0x9909) -> b6=1, cA=0.
    # фаза B (b6==1) — ВСЕГДА (gate не влияет):
    #   доп. сброс: byte@80==0 и u32[RAM+0xFBF]>=0x64 -> b6=0, cB=0;
    #   иначе v<u16[F+0x19DDE](=0x910B) -> cB=0; иначе cB+=1; cB>u16[F+0x19DE2](=0x9808) -> b6=0, cB=0.
    if mode in (1, 2) and b6 == 0:
        if v > 0x849: cA = 0
        else:
            cA += 1
            if cA >= 0x9909: b6 = 1; cA = 0
    if b6 == 1:
        if mode == 0 and fb >= 0x64:
            b6 = 0; cB = 0
        elif v < 0x910B: cB = 0
        else:
            cB += 1
            if cB >= 0x9808: b6 = 0; cB = 0
    return cA, cB, b6

def _t_105c4(run, rng):
    for _ in range(15):
        mode = rng.randint(0, 3)
        b6 = rng.getrandbits(1)
        v = rng.choice([0, 0x849, 0x84A, 0x910A, 0x910B, rng.randint(0, 0xFFFF)])
        cA = rng.choice([0, 1, 0x9908, 0x9909, 0x990A])
        cB = rng.choice([0, 1, 0x9807, 0x9808, 0x9809])
        fb = rng.choice([0, 0x63, 0x64, rng.randint(0, 0xFFFFFFFF)])   # u32[RAM+0xFBF] (лит. @FBB + 4)
        run.ram_write(0x80, bytes([mode]))
        run.ram_write(0xFA1, bytes([b6 << 6]))
        run.ram_write(0xF99, struct.pack('<H', v))
        run.ram_write(0x9F8, struct.pack('<H', cA))
        run.ram_write(0x9FA, struct.pack('<H', cB))
        run.ram_write(0xFBF, struct.pack('<I', fb))
        run.call(0x105C4, args=(), max_insn=20000)
        eA, eB, eb6 = _ref_105c4(mode, b6, v, cA, cB, fb)
        gA = struct.unpack('<H', run.ram_read(0x9F8, 2))[0]
        gB = struct.unpack('<H', run.ram_read(0x9FA, 2))[0]
        gb6 = (run.ram_read(0xFA1, 1)[0] >> 6) & 1
        assert (gA, gB, gb6) == (eA, eB, eb6), f'mode={mode} b6={b6} v={v:#x}: got ({gA},{gB},{gb6}) want ({eA},{eB},{eb6})'
t(0x105C4, 'E2-b57: 0x105c4 порог #6: gate byte@80∈{1,2}; bit6(byte@FA1); u16[F99] vs flash 0x849/0x910B; счётчики @9F8/@9FA; доп. сброс b6 при mode==0 и u32[FBB]>=0x64')(_t_105c4)

def _t_23544(run, rng):
    # 0x23544: r2∈{0,1}, r1<4 (иначе спин). mode0: r0>=0 -> u32[SYS+0xE180]=1<<(r0&31) (ICER0).
    # mode1: r0>=0: u32[SYS+0xE100]=u32[SYS+0xE280]=1<<(r0&31); u32[SYS+0xE400+(r0>>2)*4] |= (r1&3)<<((r0&3)*8+6);
    # r0<0: u32[SYS+0xED24+(r0>>2)*4] = (r1&3)<<((r0&3)*8+6).
    from emulator.mcu_emu import SYS as _S
    for _ in range(15):
        mode = rng.getrandbits(1)
        idx = rng.choice([rng.randint(0, 31), rng.randint(-8, -1)])
        r1 = rng.randint(0, 3)
        run.call(0x23544, args=(idx & 0xFFFFFFFF, r1, mode), max_insn=20000)
        if mode == 0:
            if idx >= 0:
                assert run.periph_read(_S + 0xE180) == (1 << (idx & 31)), f'ICER idx={idx}'
        else:
            if idx >= 0:
                m = 1 << (idx & 31)
                # ISER0/E280 — assignment (эмпирика); ITNS/SHPR — OR
                assert run.periph_read(_S + 0xE100) == m, f'ISER idx={idx}: {run.periph_read(_S+0xE100):#x}'
                assert run.periph_read(_S + 0xE280) == m, f'E280 idx={idx}'
                w = _S + 0xE400 + (idx >> 2) * 4
                if r1 & 3:
                    assert run.periph_read(w) & ((r1 & 3) << ((idx & 3) * 8 + 6)), f'ITNS idx={idx} r1={r1}'
            else:
                w = _S + 0xED24 + (idx >> 2) * 4
                if r1 & 3:
                    assert run.periph_read(w) & ((r1 & 3) << ((idx & 3) * 8 + 6)), f'SHPR idx={idx} r1={r1}'
    # спин: r2=5 / r1=4 — на отдельном McuEmu дошёл до лимита
    from unicorn import UC_HOOK_CODE
    from unicorn.arm_const import UC_ARM_REG_SP as _SP, UC_ARM_REG_LR as _LR
    for bad in ((0, 0, 5), (0, 4, 1)):
        emu = McuEmu(max_insn=2000)
        uc = emu.uc
        uc.mem_write(RAM, bytes(0x20000))
        def _code(uc_, a, s, ud):
            aa = a & ~1
            if not (FLASH0<=aa<FLASH0+0x23680 or FLASH1<=aa<FLASH1+0x23680):
                uc_.emu_stop()
        sh = uc.hook_add(UC_HOOK_CODE, _code)
        uc.reg_write(UC_ARM_REG_R0, bad[0]); uc.reg_write(UC_ARM_REG_R1, bad[1]); uc.reg_write(UC_ARM_REG_R2, bad[2])
        uc.reg_write(_SP, STACK_TOP - 0x40); uc.reg_write(_LR, 0x0BADF001)
        emu.insn = 0
        try: uc.emu_start(0x23544 | 1, 0, count=2000)
        except UcError as e: pass
        assert emu.insn >= 1990, f'args={bad}: insn={emu.insn} (ожидался спин)'
t(0x23544, 'E2-b57: 0x23544 NVIC-сеттер: mode0 r0>=0 -> ICER0=1<<(r0&31); mode1 r0>=0 -> ISER0+E280=маска, ITNS|=(r1&3)<<((r0&3)*8+6); r0<0 -> SHPR; r2∉{0,1}/r1>=4 -> спин')(_t_23544)


# ===========================================================================
# E2-b58: 8 leaf-функций (bl==0) — packer/getter/flag-setter/spin/countdown
# ===========================================================================

def _t_ded4(run, rng):
    # 0xded4: push{r0..r3}; если byte1(r0)==3:
    #   u32[RAM+0xFE9] = (r0>>24)<<24 | (byte0(r1)<<16) | (byte1(r1)<<8) | byte2(r1)  (байты r1 в перевёрнутом порядке!)
    #   ret 1; иначе ret 0.
    for _ in range(12):
        hit = rng.getrandbits(1)
        b1 = 3 if hit else rng.choice([0, 1, 2, 4, 0xFF])
        r0a = (rng.getrandbits(8)) | (b1 << 8) | (rng.getrandbits(16) << 16)
        r1a = rng.randint(0, 0xFFFFFFFF)
        r0v, _ = run.call(0xDed4, args=(r0a, r1a), max_insn=5000)
        if hit:
            want = ((r0a >> 24) << 24) | ((r1a & 0xFF) << 16) | (((r1a >> 8) & 0xFF) << 8) | ((r1a >> 16) & 0xFF)
            got = struct.unpack('<I', run.ram_read(0xFE9, 4))[0]
            assert r0v == 1 and got == want, f'r0={r0a:#x} r1={r1a:#x}: ret={r0v} u32@FE9={got:#x} want {want:#x}'
        else:
            assert r0v == 0, f'r0={r0a:#x} (byte1={b1}): ret={r0v} want 0'
t(0xDed4, 'E2-b58: 0xded4 stack-packer: byte1(r0)==3 -> u32[RAM+0xFE9]=(r0>>24)<<24|(b0<<16|b1<<8|b2) r1 (байты r1 перевёрнуты), ret1; иначе ret0')(_t_ded4)

def _t_164f8(run, rng):
    # 0x164f8: ret = s16[RAM+0x13A4] (sign-extend)
    for _ in range(10):
        v = rng.choice([0, 1, -1, 0x7FFF, -0x8000, rng.randint(-0x8000, 0x7FFF)])
        run.ram_write(0x13A4, struct.pack('<h', v))
        r0v, _ = run.call(0x164F8, max_insn=2000)
        assert r0v == (v & M32), f'v={v}: ret={r0v:#x} want {v & M32:#x}'
t(0x164F8, 'E2-b58: 0x164f8 getter: ret = s16[RAM+0x13A4] (sign-extend)')(_t_164f8)

def _t_174fc(run, rng):
    # 0x174fc: u32[RAM+8]=0; u32[RAM+0x10]=u32[RAM+0xF95]; u32[RAM+0xC]=0
    for _ in range(10):
        f95 = rng.randint(0, 0xFFFFFFFF)
        run.ram_write(0xF95, struct.pack('<I', f95))
        run.call(0x174FC, max_insn=2000)
        assert struct.unpack('<I', run.ram_read(8, 4))[0] == 0, 'u32@8'
        assert struct.unpack('<I', run.ram_read(0xC, 4))[0] == 0, 'u32@C'
        assert struct.unpack('<I', run.ram_read(0x10, 4))[0] == f95, 'u32@10'
t(0x174FC, 'E2-b58: 0x174fc helper: u32[RAM+8]=0, u32[RAM+0x10]=u32[RAM+0xF95], u32[RAM+0xC]=0')(_t_174fc)

def _t_12fe0(run, rng):
    # 0x12fe0: type=(r1>>5)&7 -> off = {1:+0xC, 2:+0x10, else:+0x14}; mask=1<<(r1&0x1F);
    # r2 ? u32[ptr+off]|=mask : &=~mask; ret = ptr+off
    B = 0x600
    for _ in range(15):
        typ = rng.randint(0, 7)
        bit = rng.randint(0, 31)
        setc = rng.getrandbits(1)
        old = rng.randint(0, 0xFFFFFFFF)
        off = {1: 0xC, 2: 0x10}.get(typ, 0x14)
        run.ram_write(B + off, struct.pack('<I', old))
        r0v, _ = run.call(0x12FE0, args=(RAM + B, (typ << 5) | bit, setc), max_insn=5000)
        got = struct.unpack('<I', run.ram_read(B + off, 4))[0]
        want = (old | (1 << bit)) if setc else (old & ~(1 << bit))
        assert r0v == (RAM + B + off) & M32, f'typ={typ}: ret={r0v:#x}'
        assert got == want, f'typ={typ} bit={bit} set={setc} old={old:#x}: {got:#x} want {want:#x}'
t(0x12FE0, 'E2-b58: 0x12fe0 flag-setter: type=(r1>>5)&7 -> off +0xC/+0x10/+0x14; mask=1<<(r1&0x1F); r2 ? |= : &=~; ret=ptr+off')(_t_12fe0)

def _t_c2a8(run, rng):
    # 0xc2a8: спин до u32[PERIPH+0x7010]&2==2 (seed в тесте); затем:
    #   u32[P+0x7008] = (old & ~0x3000) | r1; u32[P+0x7000] = (old & ~7)|2 -> ret;
    #   u32[SYS+0xED10] |= 4; arg==1: WFI, иначе SEV+WFE — эмулятор останавливается на WFI/WFE,
    #   финальный ED10 &= ~4 НЕ выполняется.
    from emulator.mcu_emu import PERIPH as _P, SYS as _S
    for _ in range(10):
        arg = rng.choice([0, 1, 5])
        r1 = rng.randint(0, 0xFFFF)
        old7008 = rng.randint(0, 0xFFFFFFFF)
        old7000 = rng.randint(0, 0xFFFFFFFF)
        run.periph_write(_P + 0x7010, 2)
        run.periph_write(_P + 0x7008, old7008)
        run.periph_write(_P + 0x7000, old7000)
        r0v, _ = run.call(0xC2A8, args=(arg, r1), max_insn=5000)
        assert run.periph_read(_P + 0x7008) == (old7008 & ~0x3000) | r1, f'P+7008: {run.periph_read(_P+0x7008):#x}'
        w = (old7000 & ~7) | 2
        assert run.periph_read(_P + 0x7000) == w, 'P+7000'
        assert r0v == w, f'ret={r0v:#x} want {w:#x}'
        assert run.periph_read(_S + 0xED10) & 4, 'ED10 bit2'
t(0xC2A8, 'E2-b58: 0xc2a8: спин u32[P+7010]&2; P+7008=(old&~0x3000)|r1; P+7000=(old&~7)|2->ret; ED10|=4; стоп на WFI/WFE (clear не достигается)')(_t_c2a8)

def _t_b860(run, rng):
    # 0xb860: u32[RAM+0xEFC]=0x10000; byte=byte[arg+0x10C];
    #   byte==3: wait-цикл (bl 0x9874 -> в эмуляторе сразу 0) -> ret0, u32[EFC]=0x10000;
    #   иначе: цикл old=u32[EFC]; u32[EFC]=old-1; old==0 -> ret3; byte!=0 -> повтор.
    #   byte=0: 1 итерация (0x10000->0xFFFF), ret3; byte∈{1,2}: полный отсчёт ~721K инстр. -> wrap 0xFFFFFFFF, ret3.
    for _ in range(6):
        run.ram_write(0x50C, b'\x00')
        r0v, _ = run.call(0xB860, args=(RAM + 0x400,), max_insn=5000)
        efc = struct.unpack('<I', run.ram_read(0xEFC, 4))[0]
        assert r0v == 3 and efc == 0xFFFF, f'ret={r0v} u32@EFC={efc:#x}'
    # byte=3: wait-путь; опрашивает (u32[PERIPH+0x5818] & 2) — константа за цикл!
    #   bit==0 -> сразу ret0, u32[EFC]=0x10000; bit==1 -> спин до wrap счётчика.
    from emulator.mcu_emu import PERIPH as _P
    run.ram_write(0x50C, b'\x03')
    run.periph_write(_P + 0x5818, 0)
    r0v, _ = run.call(0xB860, args=(RAM + 0x400,), max_insn=5000)
    efc = struct.unpack('<I', run.ram_read(0xEFC, 4))[0]
    assert r0v == 0 and efc == 0x10000, f'byte=3: ret={r0v} u32@EFC={efc:#x}'
    # bit==1: спин — счётчик падает, возврат не достигается за лимит
    run.ram_write(0x50C, b'\x03')
    run.periph_write(_P + 0x5818, 2)
    r0v, _ = run.call(0xB860, args=(RAM + 0x400,), max_insn=3000)
    efc = struct.unpack('<I', run.ram_read(0xEFC, 4))[0]
    assert efc < 0x10000, f'byte=3 спин: u32@EFC={efc:#x} (ожид. декремент)'
    # медленный путь — отдельный эмулятор с большим лимитом
    emu = McuEmu(max_insn=800000)
    uc = emu.uc
    uc.mem_write(RAM, bytes(0x20000))
    uc.mem_write(RAM + 0x50C, b'\x01')
    def _code(uc_, a, s, ud):
        aa = a & ~1
        if not (FLASH0 <= aa < FLASH0 + FW_LEN or FLASH1 <= aa < FLASH1 + FW_LEN):
            uc_.emu_stop()
    sh = uc.hook_add(UC_HOOK_CODE, _code)
    uc.reg_write(UC_ARM_REG_R0, RAM + 0x400)
    uc.reg_write(UC_ARM_REG_SP, STACK_TOP - 0x40)
    uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
    emu.insn = 0
    try: uc.emu_start(0xB860 | 1, 0, count=800000)
    except UcError as e: pass
    r0v = uc.reg_read(UC_ARM_REG_R0)
    efc = struct.unpack('<I', bytes(uc.mem_read(RAM + 0xEFC, 4)))[0]
    assert r0v == 3 and efc == 0xFFFFFFFF, f'ret={r0v} u32@EFC={efc:#x} (полный отсчёт)'
t(0xB860, 'E2-b58: 0xb860 countdown/wait: u32[RAM+0xEFC]=0x10000; byte==3 -> wait-цикл ret0; иначе декр. пока byte[arg+0x10C]!=0 и old!=0; ret3')(_t_b860)

def _t_7e98(run, rng):
    # 0x7e98(arg): (arg&0x7FF)!=0 -> 0; arg>=0x0801FFFF -> 0; arg<0x08003000 -> 0;
    # в диапазоне: bl 0x6378 (u32[PERIPH+0x22004] <- константы, fingerprint 0xCDEF89AB после полного пути)
    # + 0x6230(arg) — flash-зависимый код; эмпирика на mcu_0007: всегда !=6 -> ret 0.
    from emulator.mcu_emu import PERIPH as _P
    CANARY = 0x5A5A5A5A
    for _ in range(12):
        kind = rng.choice(['mis', 'lo', 'hi', 'in'])
        if kind == 'mis':
            arg = rng.choice([0x08003000, 0x08010000]) + rng.randint(1, 0x7FF)
        elif kind == 'lo':
            arg = rng.randint(0, 0x08002FFF)
        elif kind == 'hi':
            arg = rng.choice([0x0801FFFF, 0x08020000, 0x09000000])
        else:
            arg = rng.choice([0x08003000, 0x08003800, 0x08010000, 0x0801F800])
        run.periph_write(_P + 0x22004, CANARY)
        if kind == 'in':
            # статусное слово P+0x2200C: 0x61d4 ставит 0x7C, затем 0x6284 читает его -> детерм. ret3!=6
            run.periph_write(_P + 0x2200C, 0)
        r0v, _ = run.call(0x7E98, args=(arg,), max_insn=50000)
        fp = run.periph_read(_P + 0x22004)
        if kind == 'in':
            assert r0v == 0 and fp == 0xCDEF89AB, f'arg={arg:#x}: ret={r0v} fp={fp:#x}'
        else:
            assert r0v == 0 and fp == CANARY, f'arg={arg:#x} ({kind}): ret={r0v} fp={fp:#x} (ожид. gate-reject)'
t(0x7E98, 'E2-b58: 0x7e98 flash-range предикат: arg∈[0x08003000,0x0801FFFF), align 0x800 -> bl-путь (fp P+22004=0xCDEF89AB), ret эмпирически 0; иначе gate->0')(_t_7e98)

def _t_2359c(run, rng):
    # 0x2359c(base, idx, val): r0 = base + (idx<<4) + 0x100; цикл записи u32[r0+8]=val с read-back до совпадения
    B = 0x600
    for _ in range(12):
        idx = rng.randint(0, 15)
        val = rng.randint(0, 0xFFFFFFFF)
        run.call(0x2359C, args=(RAM + B, idx, val), max_insn=5000)
        off = B + (idx << 4) + 0x108
        got = struct.unpack('<I', run.ram_read(off, 4))[0]
        assert got == val, f'idx={idx} val={val:#x}: u32[{off:#x}]={got:#x}'
t(0x2359C, 'E2-b58: 0x2359c store-with-readback: u32[base+(idx<<4)+0x108]=val (цикл до совпадения)')(_t_2359c)


# E2-b59: 8 state/compute-функций (bl==0) — пороговые счётчики, спин-вейт, чистые вычисления
def _t_19f4(run, rng):
    # 0x19f4: A=RAM+0xF95 (gate byte[A+0xC]=byte[0xFA1] bit1, блок2 byte[A+0x17]=byte[0xFAC] bit0),
    #   B=RAM+0x15F7 (byte[B+0x11]=byte[0x1608] bit2, byte[B+3]=byte[0x15FA] bit3), C=RAM+0xA41 счётчик
    #   CAP=byte[flash+0x19E6B]=219
    #   if byte[A+0xC]&2:
    #     if byte[B+0x11]&4: C=0
    #     else: C+=1; if C>=CAP: byte[A+0xC]&=~2; C=0
    #   блок 2 (всегда): if byte[A+0x17]&1 and not byte[B+3]&8: byte[A+0x17]&=~1
    CAP = 219
    cases = [rng.randint(0, 255) for _ in range(10)] + [CAP - 2, CAP - 1, CAP, CAP + 1, 255]
    for c in cases:
        b11 = rng.randint(0, 255); b3 = rng.randint(0, 255)
        a17 = rng.randint(0, 255); ac = rng.choice([0, 2, 3, 4, 6, 7])
        run.ram_write(0xF95, bytes([rng.randint(0, 255)]))
        run.ram_write(0xFA1, struct.pack('<B', ac))
        run.ram_write(0xFAC, struct.pack('<B', a17))
        run.ram_write(0x15FA, struct.pack('<B', b3))
        run.ram_write(0x1608, struct.pack('<B', b11))
        run.ram_write(0xA41, struct.pack('<B', c))
        run.call(0x19F4, max_insn=2000)
        exp_c, exp_ac, exp_a17 = c, ac, a17
        if ac & 2:
            if b11 & 4:
                exp_c = 0
            else:
                exp_c = (c + 1) & 0xFF
                if not (CAP > exp_c):
                    exp_ac &= ~2
                    exp_c = 0
        if exp_a17 & 1 and not (b3 & 8):
            exp_a17 &= ~1
        got = (run.ram_read(0xFA1, 1)[0], run.ram_read(0xA41, 1)[0], run.ram_read(0xFAC, 1)[0])
        assert got[0] == exp_ac and got[1] == exp_c and got[2] == exp_a17, \
            f'c={c} ac={ac} b11={b11} b3={b3}: got={got} want ac={exp_ac} c={exp_c} a17={exp_a17}'
t(0x19F4, 'E2-b59: 0x19f4 state-машина: gate byte[0xFA1]&2; бит2 byte[0x1608] -> C(0xA41)=0; иначе C+=1, C>=CAP=219(flash) -> сброс gate+C; блок2: бит0 0xFAC (если не бит3 0x15FA)')(_t_19f4)

def _t_1a68(run, rng):
    # 0x1a68: A=RAM+0xF95 (gate bit4 byte[A+0xC]), C=RAM+0xA40; TH=u16[flash+0x19E76]=0x9000, CAP=byte[flash+0x19E79]=155
    #   if byte[A+0xC]&0x10:
    #     if u16[A+6] < TH: C=0
    #     else: C+=1; if C>=CAP: byte[A+0xC]&=~0x10; C=0
    TH, CAP = 0x9000, 155
    for _ in range(12):
        gate = rng.choice([0, 0x10, 0x1F])
        v = rng.choice([0, 1, TH - 1, TH, TH + 1, 0xFFFF, rng.randint(0, 0xFFFF)])
        c = rng.choice([0, CAP - 2, CAP - 1, CAP, CAP + 1, 255, rng.randint(0, 255)])
        run.ram_write(0xFA1, struct.pack('<B', gate))
        run.ram_write(0xF9B, struct.pack('<H', v))
        run.ram_write(0xA40, struct.pack('<B', c))
        run.call(0x1A68, max_insn=2000)
        exp_c, exp_gate = c, gate
        if gate & 0x10:
            if v < TH:
                exp_c = 0
            else:
                exp_c = (c + 1) & 0xFF
                if not (CAP > exp_c):
                    exp_gate &= ~0x10
                    exp_c = 0
        got_c = run.ram_read(0xA40, 1)[0]
        got_gate = run.ram_read(0xFA1, 1)[0]
        assert got_c == exp_c and got_gate == exp_gate, \
            f'gate={gate:#x} v={v:#x} c={c}: C={got_c} want {exp_c}, gate={got_gate:#x} want {exp_gate:#x}'
t(0x1A68, 'E2-b59: 0x1a68 state-машина: gate bit4 byte[0xFA1]; u16[0xF9B]>=TH=0x9000(flash) -> счётчик 0xA40 vs CAP=155; сброс gate+счётчика')(_t_1a68)

def _t_ce70(run, rng):
    # 0xce70: u32[P+0x2824]=0xCA; =0x53; u32[P+0x280C]&=~0x20 (сначала clear!);
    #   спин до bit5(P+0x280C) или 0x8000 итераций; ret = bit5?1:0; u32[P+0x2824]=0xFF.
    #   В эмуляторе bit5 никто не ставит -> полный спин ~98K инстр, всегда ret 0.
    from emulator.mcu_emu import PERIPH as _P
    for seed in [0, 0x20, 0x7F, 0xFF, rng.randint(0, 0xFFFFFFFF), rng.randint(0, 0xFFFFFFFF)]:
        run.periph_write(_P + 0x280C, seed)
        r0v, _ = run.call(0xCE70, max_insn=400000)
        assert r0v == 0, f'seed={seed:#x}: ret={r0v} want 0 (bit5 сначала чистится)'
        assert run.periph_read(_P + 0x2824) == 0xFF, 'u32[P+0x2824] != 0xFF'
        assert run.emu.insn > 90000, f'seed={seed:#x}: insn={run.emu.insn} (ожид. полный спин ~98K)'
t(0xCE70, 'E2-b59: 0xce70 spin-wait: P+0x2824=0xCA/0x53; clear bit5 P+0x280C; полный спин 0x8000 (~98K инстр) -> ret0; P+0x2824=0xFF')(_t_ce70)

def _t_f290(run, rng):
    # 0xf290: гейты: byte[0xF72]&4 (выход БЕЗ сброса) / byte[0xF71]&2 / byte[0x80]!=0 /
    #   u32[0xFBF]<0x3E8 / byte[0x107]!=1 -> C(0xA2E)=0
    #   иначе C+=1; if C>=0x12C: byte[0xF72]^=4 (toggle); C=0
    for _ in range(15):
        f72 = rng.choice([0, 4, 5, rng.randint(0, 255)])
        b81 = rng.choice([0, 2, 3, rng.randint(0, 255)])
        b80 = rng.choice([0, 1, rng.randint(0, 255)])
        fbb = rng.choice([0, 0x3E7, 0x3E8, 0x3E9, rng.randint(0, 0xFFFFFFFF)])
        b107 = rng.choice([0, 1, 2, rng.randint(0, 255)])
        c = rng.choice([0, 0x12B, 0x12C, 0x12D, 0xFFFF, rng.randint(0, 0xFFFF)])
        run.ram_write(0xF72, struct.pack('<B', f72))
        run.ram_write(0xF71, struct.pack('<B', b81))
        run.ram_write(0x80, struct.pack('<B', b80))
        run.ram_write(0xFBF, struct.pack('<I', fbb))
        run.ram_write(0x107, struct.pack('<B', b107))
        run.ram_write(0xA2E, struct.pack('<H', c))
        run.call(0xF290, max_insn=2000)
        # гейт1 (f72&4) выходит БЕЗ сброса; остальные гейты -> C=0
        exp_c, exp_f72 = c, f72
        if f72 & 4:
            pass
        elif (b81 & 2) or b80 != 0 or fbb < 0x3E8 or b107 != 1:
            exp_c = 0
        else:
            exp_c = (c + 1) & 0xFFFF
            if exp_c >= 0x12C:
                exp_f72 ^= 4
                exp_c = 0
        got_c = struct.unpack('<H', run.ram_read(0xA2E, 2))[0]
        got_f72 = run.ram_read(0xF72, 1)[0]
        assert got_c == exp_c and got_f72 == exp_f72, \
            f'f72={f72} b81={b81} b80={b80} fbb={fbb:#x} b107={b107} c={c:#x}: C={got_c:#x} want {exp_c:#x}, f72={got_f72} want {exp_f72}'
t(0xF290, 'E2-b59: 0xf290 threshold-counter: гейт1 0xF72&4 (без сброса), гейты 0xF71&2/0x80!=0/u32[0xFBF]<0x3E8/0x107!=1 -> C=0; иначе C+=1, C>=0x12C -> toggle bit2 0xF72, C=0')(_t_f290)

def _t_f36c(run, rng):
    # 0xf36c: mode = bit3 byte[RAM+0xFD0]; x = s8[RAM+0xFCF]
    #   A (bit3=0): x<-30 or x>100 -> C(0xA36)+=1; C>=0x32 -> toggle bit3, C=0; иначе C=0
    #   B (bit3=1): -30<=x<=100 -> C(0xA38)+=1; C>=0x32 -> clear bit3, C=0; иначе C=0
    for _ in range(15):
        m = rng.choice([0, 8, 9, rng.randint(0, 255)])
        x = rng.choice([-128, -31, -30, -29, 0, 99, 100, 101, 127, rng.randint(-128, 127)])
        ca = rng.choice([0, 0x31, 0x32, 0x33, 0xFFFF, rng.randint(0, 0xFFFF)])
        cb = rng.choice([0, 0x31, 0x32, 0x33, 0xFFFF, rng.randint(0, 0xFFFF)])
        run.ram_write(0xFD0, struct.pack('<B', m))
        run.ram_write(0xFCF, struct.pack('<b', x))
        run.ram_write(0xA36, struct.pack('<H', ca))
        run.ram_write(0xA38, struct.pack('<H', cb))
        run.call(0xF36C, max_insn=2000)
        exp_ca, exp_cb, exp_m = ca, cb, m
        if not (m & 8):
            if x < -30 or x > 100:
                exp_ca = (ca + 1) & 0xFFFF
                if exp_ca >= 0x32:
                    exp_m ^= 8
                    exp_ca = 0
            else:
                exp_ca = 0
        else:
            if -30 <= x <= 100:
                exp_cb = (cb + 1) & 0xFFFF
                if exp_cb >= 0x32:
                    exp_m &= ~8
                    exp_cb = 0
            else:
                exp_cb = 0
        got_ca = struct.unpack('<H', run.ram_read(0xA36, 2))[0]
        got_cb = struct.unpack('<H', run.ram_read(0xA38, 2))[0]
        got_m = run.ram_read(0xFD0, 1)[0]
        assert got_ca == exp_ca and got_cb == exp_cb and got_m == exp_m, \
            f'm={m:#x} x={x} ca={ca:#x} cb={cb:#x}: CA={got_ca:#x}/{exp_ca:#x} CB={got_cb:#x}/{exp_cb:#x} m={got_m:#x}/{exp_m:#x}'
t(0xF36C, 'E2-b59: 0xf36c dual-threshold: bit3 0xFD0 выбирает блок; x=s8[0xFCF]; A: вне[-30,100] -> C(0xA36), latch 0x32 toggle; B: внутри -> C(0xA38), latch clear')(_t_f36c)

def _t_1093c(run, rng):
    # 0x1093c: src=RAM+0x4A, dst=RAM+0xFC7 (dst[6]=0xFCD гейт, dst[5]=0xFCC ввод b),
    #   cnt=byte[RAM+0x60], U=u32[RAM+0x8C]
    #   dst[0..4]=src[0..4]; if bit6(dst[6]): cnt=0
    #   elif s8(dst[2])<=s8(dst[5]): cnt=0
    #   else: cnt+=1; if cnt>10: dst[5]=dst[2]; U|=0x1000; cnt=0
    for _ in range(15):
        src = bytes(rng.randint(0, 255) for _ in range(6))
        d6 = rng.choice([0, 0x40, 0x7F, rng.randint(0, 255)])
        b5 = rng.randint(0, 255)
        cnt = rng.choice([0, 10, 11, 255, rng.randint(0, 255)])
        u8c = rng.randint(0, 0xFFFFFFFF)
        run.ram_write(0x4A, src)
        run.ram_write(0xFCC, struct.pack('<B', b5))   # dst[5]
        run.ram_write(0xFCD, struct.pack('<B', d6))   # dst[6]
        run.ram_write(0x60, struct.pack('<B', cnt))
        run.ram_write(0x8C, struct.pack('<I', u8c))
        run.call(0x1093C, max_insn=2000)
        exp_dst = bytearray(src[:5]) + bytes([b5, d6])
        exp_cnt, exp_u8c = cnt, u8c
        if d6 & 0x40:
            exp_cnt = 0
        else:
            a = src[2] - 256 if src[2] >= 128 else src[2]
            b = b5 - 256 if b5 >= 128 else b5
            if a <= b:
                exp_cnt = 0
            else:
                exp_cnt = (cnt + 1) & 0xFF
                if exp_cnt > 10:
                    exp_dst[5] = exp_dst[2]
                    exp_u8c |= 0x1000
                    exp_cnt = 0
        got_dst = run.ram_read(0xFC7, 7)
        got_cnt = run.ram_read(0x60, 1)[0]
        got_u8c = struct.unpack('<I', run.ram_read(0x8C, 4))[0]
        assert got_dst == bytes(exp_dst), f'src={src.hex()} d6={d6:#x}: dst={got_dst.hex()} want {bytes(exp_dst).hex()}'
        assert got_cnt == exp_cnt, f'cnt: got={got_cnt} want {exp_cnt} (src={src.hex()} d6={d6:#x})'
        assert got_u8c == exp_u8c, f'u32[0x8C]: got={got_u8c:#x} want {exp_u8c:#x}'
t(0x1093C, 'E2-b59: 0x1093c copy+counter: dst[0..4]=src[0..4] (0xFC7<-0x4A); гейты bit6(dst[6])/s8(dst[2])<=s8(dst[5]); счётчик 0x60, latch>10 -> dst[5]=dst[2], u32[0x8C]|=0x1000')(_t_1093c)

def _t_11350(run, rng):
    # 0x11350: if bit7(byte[RAM+0xFA1]): byte[0xA55]=0; u16[0xA56]=0; byte[0xA59]=0; byte[0xA5A]=0 (чистый возврат);
    #   else: fall-through в соседнюю state-машину @0x1136e (insn > 20, память не проверяем)
    for _ in range(12):
        gate = rng.choice([0, 0x80, 0xFF, rng.randint(0, 255)])
        seed = bytes([rng.randint(1, 255) for _ in range(6)])
        run.ram_write(0xFA1, struct.pack('<B', gate))
        run.ram_write(0xA55, seed)
        r0v, _ = run.call(0x11350, max_insn=2000)
        if gate & 0x80:
            got = bytearray(run.ram_read(0xA55, 6))
            # чистятся 0xA55, 0xA56-0xA57 (u16), 0xA59, 0xA5A; 0xA58 нетронут
            want = bytearray([0, 0, 0, seed[3], 0, 0])
            assert bytes(got) == bytes(want), f'gate={gate:#x} seed={seed.hex()}: got={bytes(got).hex()} want={bytes(want).hex()}'
        else:
            assert run.emu.insn > 20, f'gate={gate:#x}: insn={run.emu.insn} (ожид. fall-through в 0x1136e)'
t(0x11350, 'E2-b59: 0x11350 gated-clear: bit7(byte[RAM+0xFA1]) -> byte[0xA55]=u16[0xA56]=byte[0xA59]=byte[0xA5A]=0; иначе fall-through в state-машину @0x1136e')(_t_11350)

def _t_22a48(run, rng):
    # 0x22a48(r0) — валидатор-трамплин: arg==0 -> ret1; v=u32[arg];
    #   v НЕ в множестве 10 TIM-баз -> бесконечный спин (cpsid i; b .);
    #   v в множестве -> переход в тело @0x22a96 (r4=arg): проверки byte[arg+8]∈{0..4},
    #   byte[arg+0x10]∈{0..2} (иначе спин), byte[arg+0x1A]=0 -> strb 0 [arg+0x19];
    #   byte[arg+0x1A]=2; bl 0x22b7c(arg+4, 2); byte[arg+0x1A]=1; ret 0.
    TIMS = {0x40012C00, 0x40001000, 0x40014000, 0x40014400, 0x40014800, 0x40014C00,
            0x40000400, 0x40000800, 0x40000C00, 0x40000000}
    r0v, _ = run.call(0x22A48, args=(0,), max_insn=2000)
    assert r0v == 1 and run.emu.insn < 50, f'arg=0: ret={r0v} insn={run.emu.insn}'
    # невалидные значения -> спин
    bad = rng.getrandbits(32)
    while bad in TIMS:
        bad = rng.getrandbits(32)
    for v in [0x12345678, 0xDEADBEEF, 1, 0x40015000, bad]:
        run.ram_write(0x300, struct.pack('<I', v))
        r0v, _ = run.call(0x22A48, args=(RAM + 0x300,), max_insn=3000)
        assert run.emu.insn >= 2900, f'v={v:#x}: не спин (insn={run.emu.insn})'
    # валидные базы: чистый путь (ret0) и спин-путь (byte[arg+8]>4)
    for v in sorted(TIMS):
        run.ram_write(0x300, struct.pack('<I', v))
        run.ram_write(0x308, b'\x00')
        run.ram_write(0x310, b'\x00')
        run.ram_write(0x31A, b'\x00')
        # bl 0x22b7c(r1=2) читает k=byte[RAM+6], j=byte[RAM+0xE] — сидим валидные
        run.ram_write(0x6, b'\x00')
        run.ram_write(0xE, b'\x00')
        r0v, _ = run.call(0x22A48, args=(RAM + 0x300,), max_insn=5000)
        got_1a = run.ram_read(0x31A, 1)[0]
        assert r0v == 0 and got_1a == 1 and run.emu.insn < 500, \
            f'v={v:#x}: ret={r0v} insn={run.emu.insn} byte[+0x1A]={got_1a}'
    run.ram_write(0x300, struct.pack('<I', 0x40012C00))
    run.ram_write(0x308, b'\x05')
    r0v, _ = run.call(0x22A48, args=(RAM + 0x300,), max_insn=3000)
    assert run.emu.insn >= 2900, f'byte[arg+8]=5: не спин (insn={run.emu.insn})'
t(0x22A48, 'E2-b59: 0x22a48(r0) валидатор-трамплин: arg==0 -> ret1; u32[arg] вне 10 TIM-баз -> спин; валидная база + нулевые байты -> тело @0x22a96 (bl 0x22b7c), byte[+0x1A]=1, ret0; byte[+8]>4 -> спин')(_t_22a48)

# ================= E2-b60: 8 state/compute-функций (bl==0) =================

def _ref_1bfa0(src0):
    # 0x1bfa0(dst, src): dst[0..15]=src[0..15]; 40 раундов (i=4..43):
    #   w = dst[(i-1)*4..+3]; if i%4==0: t1=T[w1]; w1=T[w2]; w2=T[w3]; w3=T[w0]; w0=t1^T2[i>>2]
    #   dst[i*4..+3] = dst[(i-4)*4..+3] ^ w   (T=flash+0xA907, T2=flash+0xAB07, по 256 B)
    T = FW[0xA907:0xA907 + 256]
    T2 = FW[0xAB07:0xAB07 + 256]
    dst = bytearray(200)
    dst[:16] = src0[:16]
    for i in range(4, 44):
        w = list(dst[(i-1)*4:(i-1)*4+4])
        if i % 4 == 0:
            t1 = T[w[1]]
            w[1], w[2], w[3] = T[w[2]], T[w[3]], T[w[0]]
            w[0] = t1 ^ T2[i >> 2]
        for j in range(4):
            dst[i*4+j] = dst[(i-4)*4+j] ^ w[j]
    return bytes(dst)

def _t_1bfa0(run, rng):
    # 0x1bfa0(dst, src) — табличный блочный шифр 128->176 байт (2 S-таблицы в flash)
    for trial in range(4):
        src = bytes(rng.getrandbits(8) for _ in range(16))
        run.ram_write(0x200, bytes(200))
        run.ram_write(0x480, src)
        run.call(0x1BFA0, args=(RAM + 0x200, RAM + 0x480), max_insn=50000)
        got = run.ram_read(0x200, 176)
        exp = _ref_1bfa0(src)[:176]
        assert bytes(got) == exp, f'trial{trial}: got[:24]={bytes(got[:24]).hex()} exp[:24]={exp[:24].hex()}'
        assert 1800 < run.emu.insn < 2000, f'trial{trial}: insn={run.emu.insn}'
t(0x1BFA0, 'E2-b60: 0x1bfa0(dst,src) табличный шифр: dst[0..15]=src; 40 раундов XOR-цепочка + S-таблицы flash 0xA907/0xAB07 (каждые 4 раунда)')(_t_1bfa0)

def _sdiv(a, b):
    q = abs(a) // abs(b)
    return q if (a >= 0) == (b > 0) else -q

def _ref_4d48(cnt, idx, ring, v):
    # 0x4d48(r0): ring u32[0xF3C..+10*4]; cnt=byte[0x7A], idx=byte[0x7B]
    ring = list(ring)
    if cnt < 10:
        ring[cnt] = v & 0xFFFFFFFF
        cnt = (cnt + 1) & 0xFF
    else:
        ring[idx] = v & 0xFFFFFFFF
        idx = (idx + 1) & 0xFF
        if idx == cnt:
            idx = 0
    s = sum(ring[:cnt]) & 0xFFFFFFFF
    if s >= 0x80000000:
        s -= 0x100000000
    avg = _sdiv(s, cnt)
    return cnt, idx, ring, avg

def _t_4d48(run, rng):
    # 0x4d48(r0) — скользящее signed-среднее: ring 10×u32 @0xF3C, счётчик byte[0x7A], idx byte[0x7B]
    run.ram_write(0x7A, b'\x00')
    run.ram_write(0x7B, b'\x00')
    run.ram_write(0xF3C, bytes(40))
    for _ in range(25):  # 10 до заполнения + 15 по кольцу (включая wrap idx 9->10->0)
        v = rng.choice([rng.getrandbits(32), rng.randint(-1000, 1000),
                        0xFFFFFFFF, 0x80000000, 0x7FFFFFFF]) & 0xFFFFFFFF
        pre_cnt = run.ram_read(0x7A, 1)[0]
        pre_idx = run.ram_read(0x7B, 1)[0]
        pre_ring = struct.unpack('<10I', run.ram_read(0xF3C, 40))
        r0v, _ = run.call(0x4D48, args=(v,), max_insn=5000)
        cnt, idx, ring, avg = _ref_4d48(pre_cnt, pre_idx, pre_ring, v)
        got_cnt = run.ram_read(0x7A, 1)[0]
        got_idx = run.ram_read(0x7B, 1)[0]
        got_ring = list(struct.unpack('<10I', run.ram_read(0xF3C, 40)))
        assert r0v == (avg & 0xFFFFFFFF), f'v={v:#x}: ret={r0v:#x} want {avg & 0xFFFFFFFF:#x} (avg={avg})'
        assert got_cnt == cnt and got_idx == idx, f'v={v:#x}: cnt={got_cnt}/{got_idx} want {cnt}/{idx}'
        assert got_ring == ring, f'v={v:#x}: ring diverged'
t(0x4D48, 'E2-b60: 0x4d48(r0) скользящее signed-среднее: ring 10×u32 @0xF3C; cnt<10 -> ring[cnt]=v, cnt++; иначе ring[idx]=v, idx++ (==cnt -> 0); ret sdiv(sum, cnt)')(_t_4d48)

EVQ_TH = 0xFFC91170  # flash-литерал пула 0x4c14

def _ref_4c14(cnt, slots, b0_vals):
    # 0x4c14(): cnt=u32[0xB4C]; ring 6×0x10 @0x164C (поле +4 = слот)
    cnt = (cnt + 1) & 0xFFFFFFFF
    slots = list(slots)
    if cnt >= EVQ_TH:
        for i in range(6):
            # slot+1==0 (slot==0xFFFFFFFF) -> без изменений; иначе slot -= TH (mod 2^32)
            if slots[i] != 0xFFFFFFFF:
                slots[i] = (slots[i] - EVQ_TH) & 0xFFFFFFFF
        cnt = (cnt - EVQ_TH) & 0xFFFFFFFF
    flags = []
    for i in range(6):
        # сравнение с НОВЫМ счётчиком u32[0xB4C] (не с TH!): pool 0x4c5e -> 0x20000B4C
        flags.append(1 if (b0_vals[i] == 1 and slots[i] <= cnt) else 0)
    return cnt, slots, flags

def _t_4c14(run, rng):
    # 0x4c14() — event-очередь wrap: u32[0xB4C]++; если >= 0xFFC91170: +1 к слотам ring (wrap -TH), cnt-=TH;
    #   затем промаркировать: slot0==1 и slot<=TH -> byte[+1]=1; ret 0x200016AC
    for _ in range(8):
        cnt = rng.choice([0, 1, EVQ_TH - 2, EVQ_TH - 1, EVQ_TH, EVQ_TH + 5, rng.getrandbits(32)])
        run.ram_write(0xB4C, struct.pack('<I', cnt))
        slot_vals = [rng.choice([0, EVQ_TH - 1, EVQ_TH, EVQ_TH + 3, 0xFFFFFFFF, rng.getrandbits(32)]) for _ in range(6)]
        b0_vals = [rng.choice([0, 1, 2, 255]) for _ in range(6)]
        for i in range(6):
            run.ram_write(0x164C + i*0x10, bytes([b0_vals[i]]) + bytes(3) + struct.pack('<I', slot_vals[i]))
        r0v, _ = run.call(0x4C14, max_insn=3000)
        exp_cnt, exp_slots, exp_flags = _ref_4c14(cnt, slot_vals, b0_vals)
        got_cnt = struct.unpack('<I', run.ram_read(0xB4C, 4))[0]
        got_slots = [struct.unpack('<I', run.ram_read(0x164C + i*0x10 + 4, 4))[0] for i in range(6)]
        got_flags = [run.ram_read(0x164C + i*0x10 + 1, 1)[0] for i in range(6)]
        assert r0v == 0x200016AC, f'cnt={cnt:#x}: ret={r0v:#x}'
        assert got_cnt == exp_cnt, f'cnt={cnt:#x}: got={got_cnt:#x} want {exp_cnt:#x}'
        assert got_slots == exp_slots, f'cnt={cnt:#x}: slots {got_slots} want {exp_slots}'
        assert got_flags == exp_flags, f'cnt={cnt:#x}: flags {got_flags} want {exp_flags}'
t(0x4C14, 'E2-b60: 0x4c14() event-очередь wrap: u32[0xB4C]++; >= 0xFFC91170 -> slot-=TH mod 2^32 (0xFFFFFFFF без изменений), cnt-=TH; маркировка byte[+1]=1 (byte[+0]==1 и slot<=cnt); ret ring+0x60')(_t_4c14)

def _ref_f5c4(bit6, v1, v2, cA, cB):
    # 0xf5c4: бит6(byte[0xFCD]); A (бит6=0): счёт cA при ОБЕХАХ вне [-0x1E,0x64], latch 0x32 -> set бит6;
    #   B (бит6=1): счёт cB при ОБЕХАХ в [-0x1E,0x64], latch 0x32 -> clear бит6
    def s8(x):
        return x - 256 if x >= 128 else x
    a, b = s8(v1), s8(v2)
    in_a = (-0x1E <= a <= 0x64)
    in_b = (-0x1E <= b <= 0x64)
    out_bit6 = bit6
    if bit6 == 0:
        # A: счёт при ЛЮБОМ выходе за диапазон (OR); сброс только когда оба внутри
        if (not in_a) or (not in_b):
            cA = (cA + 1) & 0xFFFF
            if cA >= 0x32:
                out_bit6 = 1
                cA = 0
        else:
            cA = 0
    else:
        if in_a and in_b:
            cB = (cB + 1) & 0xFFFF
            if cB >= 0x32:
                out_bit6 = 0
                cB = 0
        else:
            cB = 0
    return out_bit6, cA, cB

def _t_f5c4(run, rng):
    # 0xf5c4() — dual-range state-machine: бит6(byte[0xFCD]); i8[0x44]/i8[0x45]
    vals = [0, 0x1E, 0x1F, 0x20, 0x64, 0x65, 0x66, 0x1E | 0x80, 0x65 | 0x80, rng.randint(0, 255)]
    for _ in range(14):
        bit6 = rng.choice([0, 0x40])
        v1 = rng.choice(vals)
        v2 = rng.choice(vals)
        cA = rng.choice([0, 0x31, 0x32, 0xFFFF, rng.randint(0, 0xFFFF)])
        cB = rng.choice([0, 0x31, 0x32, 0xFFFF, rng.randint(0, 0xFFFF)])
        run.ram_write(0xFCD, bytes([bit6]))
        run.ram_write(0x44, bytes([v1, v2]))
        run.ram_write(0xA3A, struct.pack('<H', cA))
        run.ram_write(0xA3C, struct.pack('<H', cB))
        run.call(0xF5C4, max_insn=2000)
        exp_bit6, exp_cA, exp_cB = _ref_f5c4(1 if bit6 else 0, v1, v2, cA, cB)
        got_bit6 = run.ram_read(0xFCD, 1)[0] & 0x40
        got_cA = struct.unpack('<H', run.ram_read(0xA3A, 2))[0]
        got_cB = struct.unpack('<H', run.ram_read(0xA3C, 2))[0]
        assert got_bit6 == (exp_bit6 << 6), \
            f'bit6={bit6:#x} v1={v1} v2={v2} cA={cA:#x} cB={cB:#x}: бит6={got_bit6:#x} want {exp_bit6 << 6:#x}'
        assert got_cA == exp_cA and got_cB == exp_cB, \
            f'v1={v1} v2={v2}: cA={got_cA:#x}/{got_cB:#x} want {exp_cA:#x}/{exp_cB:#x}'
t(0xF5C4, 'E2-b60: 0xf5c4() dual-range: бит6 0xFCD; A(0): cA(0xA3A)++ когда i8[0x44]/i8[0x45] ЛЮБОЙ вне [-0x1E,0x64], latch 0x32 -> set бит6; B(1): cB(0xA3C)++ когда ОБА в диапазоне, latch -> clear')(_t_f5c4)

def _ref_1e94(b9, bb, bfe):
    # 0x1e94(): bit-pack из byte[0x15F9]/[0x15FB]/[0x15FE] -> out0@0xAD4, out1@0xAD5
    out0 = 0
    out1 = 0
    if b9 & 0x80: out0 |= 0x01
    if b9 & 0x20: out0 |= 0x02
    if b9 & 0x40: out0 |= 0x04
    if b9 & 0x10: out0 |= 0x08
    if b9 & 0x08: out0 |= 0x10
    if b9 & 0x04: out0 |= 0x20
    if bb & 0x80: out0 |= 0x40
    if bb & 0x20: out1 |= 0x01
    if bb & 0x10: out1 |= 0x02
    if bb & 0x02: out1 |= 0x08
    if bb & 0x01: out1 |= 0x10
    if bfe & 0x80: out1 |= 0x20
    return out0, out1

def _t_1e94(run, rng):
    # 0x1e94() — flag bit-pack: 3 входных байта -> 2 упакованных (stm {r1,r2} в RAM+0xAD4)
    for _ in range(6):
        b9, bb, bfe = rng.randint(0, 255), rng.randint(0, 255), rng.randint(0, 255)
        run.ram_write(0x15F9, bytes([b9]))
        run.ram_write(0x15FB, bytes([bb]))
        run.ram_write(0x15FE, bytes([bfe]))
        run.ram_write(0xAD4, bytes(8))
        r0v, _ = run.call(0x1E94, max_insn=2000)
        out = run.ram_read(0xAD4, 8)
        exp0, exp1 = _ref_1e94(b9, bb, bfe)
        assert out[0] == exp0 and out[1] == exp1 and bytes(out[2:]) == b'\x00' * 6, \
            f'b9={b9:#x} bb={bb:#x} bfe={bfe:#x}: out0={out[0]:#x} out1={out[1]:#x} want {exp0:#x}/{exp1:#x}'
        assert r0v == 0x20000ADC, f'ret={r0v:#x} (stm r0! -> +8)'
t(0x1E94, 'E2-b60: 0x1e94() flag bit-pack: биты 0x15F9[7,5,6,4,3,2]->out0[0..5], 0x15FB[7]->out0[6]; 0x15FB[5,4,1,0]->out1[0,1,3,4], 0x15FE[7]->out1[5]; stm в RAM+0xAD4, ret 0xADC')(_t_1e94)

def _t_1e2ca(run, rng):
    # 0x1e2ca(r0, r1): если u32(r0-1) > u32(r1) -> ret1; иначе SysTick init:
    #   RVR(0xE000E014)=r0-1; CVR(0xE000E018)=0; bl 0x21b84(-1,3): u32[0xE000ED20]=(old&~0xFF000000)|0xC0;
    #   CTRL(0xE000E010)=7; ret0
    for a, b in [(0x100, 0x100), (0x100, 0x1FF), (0x100, 0x1FE), (0x100, 0x200),
                 (5, 4), (5, 5), (1, 0), (0, 0), (0, 1), (0xFFFFFFFF, 0), (0xFFFFFFFF, 0xFFFFFFFE),
                 (rng.getrandbits(32), rng.getrandbits(32))]:
        old_ed20 = rng.getrandbits(32)
        run.periph_write(0xE000ED20, old_ed20)
        r0v, _ = run.call(0x1E2CA, args=(a, b), max_insn=5000)
        if (a - 1) & 0xFFFFFFFF > b:
            assert r0v == 1, f'a={a:#x} b={b:#x}: ret={r0v}'
        else:
            rv = run.periph_read(0xE000E014)
            cv = run.periph_read(0xE000E018)
            ct = run.periph_read(0xE000E010)
            ed20 = run.periph_read(0xE000ED20)
            exp_ed20 = (old_ed20 & 0x00FFFFFF) | 0xC0000000
            assert r0v == 0 and rv == (a - 1) & 0xFFFFFFFF and cv == 0 and ct == 7, \
                f'a={a:#x} b={b:#x}: ret={r0v} RVR={rv:#x} CVR={cv:#x} CTRL={ct:#x}'
            assert ed20 == exp_ed20, f'a={a:#x} b={b:#x}: ED20={ed20:#x} want {exp_ed20:#x}'
t(0x1E2CA, 'E2-b60: 0x1e2ca(r0,r1) SysTick init: u32(r0-1)>r1 -> ret1; иначе RVR=r0-1, CVR=0, u32[0xE000ED20]=(old&~0xFF000000)|0xC0000000 (bl 0x21b84), CTRL=7, ret0')(_t_1e2ca)

def _t_61e4(run, rng):
    # 0x61e4() — HSI-старт: u32[P+0x21000]&2 -> ret0 (нетронут); иначе |=1 (HSION),
    #   спин до bit1 (HSIRDY) до 1280 итераций; ret = bit1?0:1 (в эмуляторе bit1 статичен -> 1)
    for seed in [0, 0x20, 0x7F, 0xFF, rng.randint(0, 0xFFFFFFFF), rng.randint(0, 0xFFFFFFFF)]:
        run.periph_write(0x40021000, seed)
        r0v, _ = run.call(0x61E4, max_insn=200000)
        if seed & 2:
            assert r0v == 0 and run.emu.insn < 50, f'seed={seed:#x}: ret={r0v} insn={run.emu.insn}'
            assert run.periph_read(0x40021000) == seed, 'word изменён без необходимости'
        else:
            assert r0v == 1, f'seed={seed:#x}: ret={r0v} (ожид. 1 после полного спина)'
            assert run.emu.insn > 12000, f'seed={seed:#x}: insn={run.emu.insn} (ожид. полный спин ~12.8K)'
            assert run.periph_read(0x40021000) == (seed | 1), 'HSION (bit0) не выставлен'
t(0x61E4, 'E2-b60: 0x61e4() HSI-старт: bit1(P+0x21000) -> ret0; иначе bit0|=1 (HSION), спин до bit1 (1280 итер., ~12.8K инстр) -> ret1 в эмуляторе')(_t_61e4)

FBC = {  # flash-константы 0xfbf8 (u16 в mcu_0007.bin)
    'TH_A': struct.unpack('<H', FW[0x19DAA:0x19DAC])[0],    # порог пути A (u16[0xF9D]) = 0xE755
    'CAP_A': struct.unpack('<H', FW[0x19DAE:0x19DB0])[0],   # latch счётчика A = 0x2401
    'GATE_C': struct.unpack('<H', FW[0x19DAC:0x19DAE])[0],  # гейт пути C: f9d > 0xB430 -> e92=0
    'LATCH_C': struct.unpack('<H', FW[0x19DB0:0x19DB2])[0], # latch счётчика C: e92 >= 0x7E4
}

def _ref_fbf8(mode, fa1, f9d, e90, e92, fbf):
    # 0xfbf8: A/B (mode∈{0,2}, бит0(0xFA1)==0): f9d<TH_A -> e90=0; иначе e90++, >=CAP_A -> set бит0, e90=0
    #   C (всегда): бит0(0xFA1): mode==1 и u32[0xFBF]>=0x64 -> clear бит0, e92=0;
    #   иначе f9d>GATE_C -> e92=0; иначе e92++, >=LATCH_C -> clear бит0, e92=0
    if mode in (0, 2) and not (fa1 & 1):
        if f9d < FBC['TH_A']:
            e90 = 0
        else:
            e90 = (e90 + 1) & 0xFFFF
            if e90 >= FBC['CAP_A']:
                fa1 |= 1
                e90 = 0
    if fa1 & 1:
        if mode == 1 and fbf >= 0x64:
            fa1 &= ~1
            e92 = 0
        else:
            if f9d > FBC['GATE_C']:
                e92 = 0
            else:
                e92 = (e92 + 1) & 0xFFFF
                if e92 >= FBC['LATCH_C']:
                    fa1 &= ~1
                    e92 = 0
    return fa1, e90, e92

def _t_fbf8(run, rng):
    # 0xfbf8() — threshold counter #1: три пути (A: счёт до 0x2401 при 0xF9D>=0xE755; C: счёт 0x9E2 до 0x7E4)
    th_a, cap_a = FBC['TH_A'], FBC['CAP_A']
    gate_c, latch_c = FBC['GATE_C'], FBC['LATCH_C']
    f9d_vals = [th_a - 1, th_a, th_a + 100, gate_c - 1, gate_c, gate_c + 1, 0, 0xFFFF, rng.randint(0, 0xFFFF)]
    for _ in range(14):
        mode = rng.choice([0, 1, 2, 3, 255])
        fa1 = rng.choice([0, 1, 0x41, rng.randint(0, 255)])
        f9d = rng.choice(f9d_vals)
        e90 = rng.choice([0, cap_a - 1, cap_a, 0xFFFF, rng.randint(0, 0xFFFF)])
        e92 = rng.choice([0, latch_c - 1, latch_c, 0xFFFF, rng.randint(0, 0xFFFF)])
        fbf = rng.choice([0, 0x63, 0x64, 0x65, rng.randint(0, 0xFFFFFFFF)])
        run.ram_write(0x80, bytes([mode]))
        run.ram_write(0xFA1, bytes([fa1]))
        run.ram_write(0xF9D, struct.pack('<H', f9d))
        run.ram_write(0x9E0, struct.pack('<H', e90))
        run.ram_write(0x9E2, struct.pack('<H', e92))
        run.ram_write(0xFBF, struct.pack('<I', fbf))
        run.call(0xFBF8, max_insn=3000)
        exp_fa1, exp_e90, exp_e92 = _ref_fbf8(mode, fa1, f9d, e90, e92, fbf)
        got_fa1 = run.ram_read(0xFA1, 1)[0]
        got_e90 = struct.unpack('<H', run.ram_read(0x9E0, 2))[0]
        got_e92 = struct.unpack('<H', run.ram_read(0x9E2, 2))[0]
        assert got_fa1 == exp_fa1 and got_e90 == exp_e90 and got_e92 == exp_e92, \
            f'mode={mode} fa1={fa1:#x} f9d={f9d:#x} e90={e90:#x} e92={e92:#x} fbf={fbf:#x}: fa1={got_fa1:#x} e90={got_e90:#x} e92={got_e92:#x} want {exp_fa1:#x}/{exp_e90:#x}/{exp_e92:#x}'
t(0xFBF8, 'E2-b60: 0xfbf8() threshold #1: A/B(mode 0/2, !бит0 0xFA1): 0xF9D>=0xE755 -> 0x9E0++, >=0x2401 -> set бит0; C: бит0(0xFA1): mode1&0xFBF>=0x64 -> clear+0x9E2=0, иначе 0xF9D>0xB430 -> 0x9E2=0, иначе 0x9E2++, >=0x7E4 -> clear+0x9E2=0')(_t_fbf8)
