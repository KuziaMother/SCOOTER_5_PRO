# -*- coding: utf-8 -*-
# ruff: noqa: F405  (имена из star-import от fv_core)
"""E2-batch49..53 (6222-6565)."""
from fv_core import *  # noqa: F401,F403
from fv_core import _fresh_call, _intercept  # noqa: F401
# --- E2-batch50: single-bl reachable delegates (34) ---
def _t_01218(run, rng):
    cap, _ = _intercept(0x01218, 0x1232, max_insn=50000)
    assert cap
t(0x01218, 'E2-b50: delegate -> bl 0x1232')(_t_01218)
def _t_01ac8(run, rng):
    cap, _ = _intercept(0x01AC8, 0x1AE2, max_insn=50000)
    assert cap
t(0x01AC8, 'E2-b50: delegate -> bl 0x1ae2')(_t_01ac8)
def _t_03700(run, rng):
    cap, _ = _intercept(0x03700, 0x370A, max_insn=50000)
    assert cap and cap.get('r0') == 0x40
t(0x03700, 'E2-b50: delegate -> bl 0x370a (r0==0x40)')(_t_03700)
def _t_04994(run, rng):
    cap, _ = _intercept(0x04994, 0x4996, max_insn=50000)
    assert cap
t(0x04994, 'E2-b50: delegate -> bl 0x4996')(_t_04994)
def _t_04b20(run, rng):
    cap, _ = _intercept(0x04B20, 0x4B44, max_insn=50000)
    assert cap
t(0x04B20, 'E2-b50: delegate -> bl 0x4b44')(_t_04b20)
def _t_053fc(run, rng):
    cap, _ = _intercept(0x053FC, 0x540A, max_insn=50000)
    assert cap and cap.get('r0') == 0x40
t(0x053FC, 'E2-b50: delegate -> bl 0x540a (r0==0x40)')(_t_053fc)
def _t_08bec(run, rng):
    cap, _ = _intercept(0x08BEC, 0x8C1E, max_insn=50000)
    assert cap
t(0x08BEC, 'E2-b50: delegate -> bl 0x8c1e')(_t_08bec)
def _t_098c8(run, rng):
    cap, _ = _intercept(0x098C8, 0x98E6, max_insn=50000)
    assert cap
t(0x098C8, 'E2-b50: delegate -> bl 0x98e6')(_t_098c8)
def _t_0a8c4(run, rng):
    cap, _ = _intercept(0x0A8C4, 0xA8E8, max_insn=50000)
    assert cap
t(0x0A8C4, 'E2-b50: delegate -> bl 0xa8e8')(_t_0a8c4)
def _t_0a910(run, rng):
    cap, _ = _intercept(0x0A910, 0xA938, max_insn=50000)
    assert cap
t(0x0A910, 'E2-b50: delegate -> bl 0xa938')(_t_0a910)
def _t_0bc5c(run, rng):
    cap, _ = _intercept(0x0BC5C, 0xBC7E, max_insn=50000)
    assert cap
t(0x0BC5C, 'E2-b50: delegate -> bl 0xbc7e')(_t_0bc5c)
def _t_0c138(run, rng):
    cap, _ = _intercept(0x0C138, 0xC13A, max_insn=50000)
    assert cap
t(0x0C138, 'E2-b50: delegate -> bl 0xc13a')(_t_0c138)
def _t_0c984(run, rng):
    cap, _ = _intercept(0x0C984, 0xC98A, max_insn=50000)
    assert cap
t(0x0C984, 'E2-b50: delegate -> bl 0xc98a')(_t_0c984)
def _t_0e160(run, rng):
    cap, _ = _intercept(0x0E160, 0xE170, max_insn=50000)
    assert cap
t(0x0E160, 'E2-b50: delegate -> bl 0xe170')(_t_0e160)
def _t_0e2cc(run, rng):
    cap, _ = _intercept(0x0E2CC, 0xE2F0, max_insn=50000)
    assert cap
t(0x0E2CC, 'E2-b50: delegate -> bl 0xe2f0')(_t_0e2cc)
def _t_0e3ec(run, rng):
    cap, _ = _intercept(0x0E3EC, 0xE3FC, max_insn=50000)
    assert cap
t(0x0E3EC, 'E2-b50: delegate -> bl 0xe3fc')(_t_0e3ec)
def _t_10a5c(run, rng):
    cap, _ = _intercept(0x10A5C, 0x10A84, max_insn=50000)
    assert cap
t(0x10A5C, 'E2-b50: delegate -> bl 0x10a84')(_t_10a5c)
def _t_11c3c(run, rng):
    cap, _ = _intercept(0x11C3C, 0x11C42, max_insn=50000)
    assert cap and cap.get('r0') == 0x29bc
t(0x11C3C, 'E2-b50: delegate -> bl 0x11c42 (r0==0x29bc)')(_t_11c3c)
def _t_11d98(run, rng):
    cap, _ = _intercept(0x11D98, 0x11DB6, max_insn=50000)
    assert cap
t(0x11D98, 'E2-b50: delegate -> bl 0x11db6')(_t_11d98)
# (Остальные b50-записи из 5c27a3b — 0x13cc8/0x145e8/0x14a50/0x16b70/0x17198/0x172d8/
# 0x17c6c/0x17d38/0x17df4/0x18420/0x18a48/0x19cd0/0x1a300/0x1a928 — удалены: это были
# не входы функций (mid-code), а «цели» — fallthrough-адреса, не bl; тесты тривиально
# проходили и ничего не верифицировали.)
def _t_158f8(run, rng):
    import struct as _st
    from emulator.mcu_emu import RAM as _R
    # I2C-старт: byte@RAM+0xB8C=1 (гейт 0x15ffc) -> bl 0x15ffc(r0=0xA) -> byte@RAM+0x1FAF=1
    cap, _ = _intercept(0x158F8, 0x15FFC, max_insn=50000)
    assert cap and cap.get('r0') == 0xA, f'r0={cap.get("r0"):#x} want 0xa'
    # полный прогон (target = pop после финального strb): верифицируем побочные эффекты
    cap, emu = _intercept(0x158F8, 0x1590C, max_insn=50000)
    assert cap, 'не дошёл до pop'
    b8c = emu.uc.mem_read(_R + 0xB8C, 1)[0]
    c80 = _st.unpack_from('<I', bytes(emu.uc.mem_read(_R + 0xC80, 4)), 0)[0]
    faf = emu.uc.mem_read(_R + 0x1FAF, 1)[0]
    assert b8c == 1, f'byte@RAM+0xb8c={b8c:#x} want 0x1'
    assert c80 == 9, f'u32@RAM+0xc80={c80:#x} want 0x9 (0xa-1, decrement-path 0x15ffc)'
    assert faf == 1, f'byte@RAM+0x1faf={faf:#x} want 0x1'
t(0x158F8, 'E2-b50: 0x158f8 I2C-старт: byte@RAM+0xb8c=1 -> bl 0x15ffc(r0=0xa) -> byte@RAM+0x1faf=1')(_t_158f8)

# --- E2-batch51: новые reachable single-bl (13) ---
def _t_14924(run, rng):
    cap, _ = _intercept(0x14924, 0x14938, max_insn=50000)
    assert cap
t(0x14924, 'E2-b51: delegate -> bl 0x14938')(_t_14924)
def _t_155ac(run, rng):
    cap, _ = _intercept(0x155AC, 0x155E2, max_insn=50000)
    assert cap
t(0x155AC, 'E2-b51: delegate -> bl 0x155e2')(_t_155ac)
def _t_15918(run, rng):
    cap, _ = _intercept(0x15918, 0x15934, max_insn=50000)
    assert cap
t(0x15918, 'E2-b51: delegate -> bl 0x15934')(_t_15918)
def _t_15a1c(run, rng):
    cap, _ = _intercept(0x15A1C, 0x15A50, max_insn=50000)
    assert cap
t(0x15A1C, 'E2-b51: delegate -> bl 0x15a50')(_t_15a1c)
def _t_15c94(run, rng):
    cap, _ = _intercept(0x15C94, 0x15CCA, max_insn=50000)
    assert cap
t(0x15C94, 'E2-b51: delegate -> bl 0x15cca')(_t_15c94)
def _t_17094(run, rng):
    cap, _ = _intercept(0x17094, 0x170A2, max_insn=50000)
    assert cap
t(0x17094, 'E2-b51: delegate -> bl 0x170a2')(_t_17094)
def _t_170e0(run, rng):
    cap, _ = _intercept(0x170E0, 0x170EE, max_insn=50000)
    assert cap
t(0x170E0, 'E2-b51: delegate -> bl 0x170ee')(_t_170e0)
def _t_19ff4(run, rng):
    cap, _ = _intercept(0x19FF4, 0x1A004, max_insn=50000)
    assert cap
t(0x19FF4, 'E2-b51: delegate -> bl 0x1a004')(_t_19ff4)
def _t_1a894(run, rng):
    cap, _ = _intercept(0x1A894, 0x1A896, max_insn=50000)
    assert cap
t(0x1A894, 'E2-b51: delegate -> bl 0x1a896')(_t_1a894)
def _t_1c234(run, rng):
    cap, _ = _intercept(0x1C234, 0x1C24E, max_insn=50000)
    assert cap
t(0x1C234, 'E2-b51: delegate -> bl 0x1c24e')(_t_1c234)
def _t_1dea4(run, rng):
    cap, _ = _intercept(0x1DEA4, 0x1DEAE, max_insn=50000)
    assert cap
t(0x1DEA4, 'E2-b51: delegate -> bl 0x1deae')(_t_1dea4)
def _t_1e1a0(run, rng):
    cap, _ = _intercept(0x1E1A0, 0x1E1D0, max_insn=50000)
    assert cap
t(0x1E1A0, 'E2-b51: delegate -> bl 0x1e1d0')(_t_1e1a0)
def _t_2360c(run, rng):
    cap, _ = _intercept(0x2360C, 0x23620, max_insn=50000)
    assert cap
t(0x2360C, 'E2-b51: delegate -> bl 0x23620')(_t_2360c)

# --- E2-batch52: multi-2-bl init-groups (21) ---
def _t_01858(run, rng):
    cap, _ = _intercept(0x01858, 0x187A, max_insn=50000)
    assert cap
t(0x01858, 'E2-b52: init-group -> bl 0x185e + bl 0x187a')(_t_01858)

def _t_018fc(run, rng):
    cap, _ = _intercept(0x018FC, 0x1932, max_insn=50000)
    assert cap
t(0x018FC, 'E2-b52: init-group -> bl 0x191e + bl 0x1932')(_t_018fc)

def _t_029e8(run, rng):
    cap, _ = _intercept(0x029E8, 0x2A00, max_insn=50000)
    assert cap
t(0x029E8, 'E2-b52: init-group -> bl 0x29fc + bl 0x2a00')(_t_029e8)

def _t_03600(run, rng):
    cap, _ = _intercept(0x03600, 0x360C, max_insn=50000)
    assert cap
t(0x03600, 'E2-b52: init-group -> bl 0x3606 + bl 0x360c')(_t_03600)

def _t_04c84(run, rng):
    cap, _ = _intercept(0x04C84, 0x4CAE, max_insn=50000)
    assert cap
t(0x04C84, 'E2-b52: init-group -> bl 0x4c94 + bl 0x4cae')(_t_04c84)

def _t_04fc0(run, rng):
    cap, _ = _intercept(0x04FC0, 0x4FD0, max_insn=50000)
    assert cap
t(0x04FC0, 'E2-b52: init-group -> bl 0x4fc6 + bl 0x4fd0')(_t_04fc0)

def _t_05000(run, rng):
    cap, _ = _intercept(0x05000, 0x5014, max_insn=50000)
    assert cap
t(0x05000, 'E2-b52: init-group -> bl 0x5008 + bl 0x5014')(_t_05000)

def _t_05888(run, rng):
    cap, _ = _intercept(0x05888, 0x58A4, max_insn=50000)
    assert cap
t(0x05888, 'E2-b52: init-group -> bl 0x588e + bl 0x58a4')(_t_05888)

def _t_081b4(run, rng):
    cap, _ = _intercept(0x081B4, 0x826A, max_insn=50000)
    assert cap
t(0x081B4, 'E2-b52: init-group -> bl 0x81bc + bl 0x826a')(_t_081b4)

def _t_082b8(run, rng):
    cap, _ = _intercept(0x082B8, 0x82C4, max_insn=50000)
    assert cap
t(0x082B8, 'E2-b52: init-group -> bl 0x82c0 + bl 0x82c4')(_t_082b8)

def _t_08a90(run, rng):
    cap, _ = _intercept(0x08A90, 0x8AA0, max_insn=50000)
    assert cap
t(0x08A90, 'E2-b52: init-group -> bl 0x8a98 + bl 0x8aa0')(_t_08a90)

def _t_08b10(run, rng):
    cap, _ = _intercept(0x08B10, 0x8B30, max_insn=50000)
    assert cap
t(0x08B10, 'E2-b52: init-group -> bl 0x8b14 + bl 0x8b30')(_t_08b10)

def _t_08b58(run, rng):
    cap, _ = _intercept(0x08B58, 0x8B78, max_insn=50000)
    assert cap
t(0x08B58, 'E2-b52: init-group -> bl 0x8b5c + bl 0x8b78')(_t_08b58)

def _t_096dc(run, rng):
    cap, _ = _intercept(0x096DC, 0x9708, max_insn=50000)
    assert cap
t(0x096DC, 'E2-b52: init-group -> bl 0x96fa + bl 0x9708')(_t_096dc)

def _t_09714(run, rng):
    cap, _ = _intercept(0x09714, 0x9740, max_insn=50000)
    assert cap
t(0x09714, 'E2-b52: init-group -> bl 0x9732 + bl 0x9740')(_t_09714)

def _t_0a7ec(run, rng):
    cap, _ = _intercept(0x0A7EC, 0xA88E, max_insn=50000)
    assert cap
t(0x0A7EC, 'E2-b52: init-group -> bl 0xa80a + bl 0xa88e')(_t_0a7ec)

def _t_0cd0c(run, rng):
    cap, _ = _intercept(0x0CD0C, 0xCD5C, max_insn=50000)
    assert cap
t(0x0CD0C, 'E2-b52: init-group -> bl 0xcd1e + bl 0xcd5c')(_t_0cd0c)

def _t_0d298(run, rng):
    cap, _ = _intercept(0x0D298, 0xD2B8, max_insn=50000)
    assert cap
t(0x0D298, 'E2-b52: init-group -> bl 0xd2a0 + bl 0xd2b8')(_t_0d298)

def _t_0de0a(run, rng):
    cap, _ = _intercept(0x0DE0A, 0xDE52, max_insn=50000)
    assert cap
t(0x0DE0A, 'E2-b52: init-group -> bl 0xde24 + bl 0xde52')(_t_0de0a)

def _t_139fc(run, rng):
    cap, _ = _intercept(0x139FC, 0x13ABC, max_insn=50000)
    assert cap
t(0x139FC, 'E2-b52: init-group -> bl 0x13a0a + bl 0x13abc')(_t_139fc)

def _t_13bb8(run, rng):
    cap, _ = _intercept(0x13BB8, 0x13BDC, max_insn=50000)
    assert cap
t(0x13BB8, 'E2-b52: init-group -> bl 0x13bc4 + bl 0x13bdc')(_t_13bb8)

# --- E2-batch53: stateful single-bl делегаторы с RAM-гейтами (extra_ram; открытая+закрытая ветка) ---
def _t_8834(run, rng):
    from emulator.mcu_emu import RAM as _R
    # гейт: byte@RAM+0x107==1 && byte@RAM+0x35==1 -> bl 0xa6a4
    cap, _ = _intercept(0x8834, 0xA6A4, max_insn=30000,
                        extra_ram=[(_R + 0x107, b'\x01'), (_R + 0x35, b'\x01')])
    assert cap, 'bl 0xa6a4 not reached (gate open)'
    cap, _ = _intercept(0x8834, 0xA6A4, max_insn=30000)
    assert not cap, 'bl 0xa6a4 reached with gate closed'
t(0x8834, 'E2-b53: 0x8834 gated delegate -> bl 0xa6a4 (RAM+0x107==1 && RAM+0x35==1)')(_t_8834)

def _t_1238c(run, rng):
    from emulator.mcu_emu import RAM as _R
    # b=byte@RAM+0x35: b==0/1 -> bl 0xa7ec (+ bl 0xc098 после возврата); b==2 -> только 0xa7ec; b>=3 -> нет.
    # bl 0xc098 верифицируем только в отрицательной ветке: возврат из 0xa7ec на нулевом RAM
    # невозможен (внутренний blx [RAM-func-ptr] = runtime-потолок §74.1).
    cap, _ = _intercept(0x1238C, 0xA7EC, max_insn=30000)
    assert cap, 'bl 0xa7ec not reached (b=0)'
    cap, _ = _intercept(0x1238C, 0xA7EC, max_insn=30000, extra_ram=[(_R + 0x35, b'\x02')])
    assert cap, 'bl 0xa7ec not reached (b=2)'
    cap, _ = _intercept(0x1238C, 0xA7EC, max_insn=30000, extra_ram=[(_R + 0x35, b'\x03')])
    assert not cap, 'bl 0xa7ec reached with b=3'
    cap, _ = _intercept(0x1238C, 0xC098, max_insn=30000, extra_ram=[(_R + 0x35, b'\x03')])
    assert not cap, 'bl 0xc098 reached with b=3'
t(0x1238C, 'E2-b53: 0x1238c mode-gate (byte@RAM+0x35<3) -> bl 0xa7ec; b>=3 -> нет bl')(_t_1238c)

def _t_14ed0(run, rng):
    from emulator.mcu_emu import RAM as _R
    # гейт: byte@RAM+0x31==1 -> bl 0x8e14
    cap, _ = _intercept(0x14ED0, 0x8E14, max_insn=30000, extra_ram=[(_R + 0x31, b'\x01')])
    assert cap, 'bl 0x8e14 not reached (gate open)'
    cap, _ = _intercept(0x14ED0, 0x8E14, max_insn=30000)
    assert not cap, 'bl 0x8e14 reached with gate closed'
t(0x14ED0, 'E2-b53: 0x14ed0 gated delegate -> bl 0x8e14 (RAM+0x31==1)')(_t_14ed0)

def _t_15f00(run, rng):
    from emulator.mcu_emu import RAM as _R
    # гейт: byte@RAM+0x1F11==1 && u16@RAM+0x1FB8==0 -> bl 0x15a1c
    cap, _ = _intercept(0x15F00, 0x15A1C, max_insn=30000, extra_ram=[(_R + 0x1F11, b'\x01')])
    assert cap, 'bl 0x15a1c not reached (gate open)'
    cap, _ = _intercept(0x15F00, 0x15A1C, max_insn=30000)
    assert not cap, 'bl 0x15a1c reached with gate closed'
t(0x15F00, 'E2-b53: 0x15f00 gated delegate -> bl 0x15a1c (RAM+0x1F11==1 && u16@RAM+0x1FB8==0)')(_t_15f00)

def _t_15ffc(run, rng):
    from emulator.mcu_emu import RAM as _R
    # r0->u32@RAM+0xC80; гейт: byte@RAM+0xB8C==1 && u32@RAM+0xC80==0 -> bl 0x15a1c
    cap, _ = _intercept(0x15FFC, 0x15A1C, max_insn=30000, arg=0,
                        extra_ram=[(_R + 0xB8C, b'\x01')])
    assert cap, 'bl 0x15a1c not reached (gate open)'
    cap, _ = _intercept(0x15FFC, 0x15A1C, max_insn=30000, arg=0)
    assert not cap, 'bl 0x15a1c reached with gate closed'
t(0x15FFC, 'E2-b53: 0x15ffc gated delegate -> bl 0x15a1c (RAM+0xB8C==1 && u32@RAM+0xC80==0)')(_t_15ffc)

def _t_d33c(run, rng):
    from emulator.mcu_emu import RAM as _R
    # counter byte@RAM+0xA67: ++, >5 -> bl 0x1c60(r0=8, r1=0x7f, r2=&RAM+0x164B, r3=1)
    cap, _ = _intercept(0xD33C, 0x1C60, max_insn=30000, extra_ram=[(_R + 0xA67, b'\x05')])
    assert cap, 'bl 0x1c60 not reached (counter=5 -> 6>5)'
    assert cap.get('r0') == 8, f'r0={cap.get("r0"):#x} want 0x8'
    assert cap.get('r1') == 0x7F, f'r1={cap.get("r1"):#x} want 0x7f'
    assert cap.get('r2') == _R + 0x164B, f'r2={cap.get("r2"):#x}'
    assert cap.get('r3') == 1, f'r3={cap.get("r3")} want 1'
    cap, _ = _intercept(0xD33C, 0x1C60, max_insn=30000)
    assert not cap, 'bl 0x1c60 reached with counter=0 (1<=5)'
t(0xD33C, 'E2-b53: 0xd33c counter-gate -> bl 0x1c60(op=8, reg=0x7f, buf=&RAM+0x164b, len=1) при counter>5')(_t_d33c)

def _t_f1ec(run, rng):
    from emulator.mcu_emu import RAM as _R
    import struct as _st
    # bit1(RAM+0xF72)==0 && u16(RAM+0xF9B)<=u16(flash 0x19d98)=6084 && counter u16@RAM+0xA22 >= порог u16(flash 0x19d9c)=16801 -> bl 0x156ac
    # (сравнение `cmp r0,r1; bgt` инвертировано: bl когда порог <= счётчик)
    cap, _ = _intercept(0xF1EC, 0x156AC, max_insn=30000,
                        extra_ram=[(_R + 0xA22, _st.pack('<H', 16801))])
    assert cap, 'bl 0x156ac not reached (counter at threshold)'
    cap, _ = _intercept(0xF1EC, 0x156AC, max_insn=30000)
    assert not cap, 'bl 0x156ac reached with counter=0'
t(0xF1EC, 'E2-b53: 0xf1ec dual-counter throttle -> bl 0x156ac (когда counter>=порога flash 0x19d9c)')(_t_f1ec)

def _t_5b5a(run, rng):
    # delay-loop делегатор: 2 цикла countdown 0x2710 -> bl 0x1c1c(r0=0x90)
    cap, _ = _intercept(0x5B5A, 0x1C1C, max_insn=300000)
    assert cap, 'bl 0x1c1c not reached after delay loops'
    assert cap.get('r0') == 0x90, f'r0={cap.get("r0"):#x} want 0x90'
t(0x5B5A, 'E2-b53: 0x5b5a delay-loop delegate (2x0x2710) -> bl 0x1c1c(r0=0x90)')(_t_5b5a)
