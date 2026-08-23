#!/usr/bin/env python3
"""Эмуляция round-robin-диспетчера 0x0E658 (моторная цепочка, §39.5b) с seed «живого» стейта.

Слоты TBB: 0=0x6E50, 1=0x63B8, 2=0x799C (управление), 3=0x7A30, 4=0x69E4, 5=0x6838.
Гейты: byte@RAM[0xA49]=1, byte@RAM[0x35]=0. Stub `bx lr` в хвосте образа (0x08024D00).

Запуск: python mcu_dispatch_emu.py [sensor] [mode] [state]
"""
import os
import struct as st
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HERE))), "emulator"))
from mcu_emu import McuEmu, STACK_TOP  # noqa: E402
from unicorn import UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE  # noqa: E402
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR  # noqa: E402

STUB = 0x08024D00          # bx lr в хвосте образа


def main():
    sensor = int(sys.argv[1], 0) if len(sys.argv) > 1 else 5000
    mode = int(sys.argv[2], 0) if len(sys.argv) > 2 else 1
    state = int(sys.argv[3], 0) if len(sys.argv) > 3 else 100

    emu = McuEmu(max_insn=20_000_000)
    uc = emu.uc
    uc.mem_write(0x40000000, bytes(0x100000))     # периферия = 0
    try:
        uc.mem_map(0x48000000, 0x1000)            # порт-блок
    except Exception:
        pass
    uc.mem_write(STUB, b"\x70\x47")               # bx lr

    # seed «живого» стейта
    uc.mem_write(0x20000A49, b"\x01")             # гейт диспетчера
    uc.mem_write(0x20000035, b"\x00")             # RAM[0x35] = 0 (разрешено)
    uc.mem_write(0x20001384 + 0x20, st.pack("<h", sensor))   # сенсор i16
    uc.mem_write(0x20001384 + 0x06, st.pack("<I", state))    # state u32
    uc.mem_write(0x20001359 + 1, bytes([mode]))             # mode-byte

    events = []

    def h_tim1(uc, access, address, size, value, user):
        events.append((uc.reg_read(UC_ARM_REG_PC), "R" if access == 1 else "W",
                       address - 0x40012C00, value))

    def h_tbl(uc, access, address, size, value, user):
        events.append((uc.reg_read(UC_ARM_REG_PC), "TBL", address - 0x08000000, 0))

    def h_portw(uc, access, address, size, value, user):
        events.append((uc.reg_read(UC_ARM_REG_PC), "PW", address - 0x48000000, value))

    uc.hook_add(UC_HOOK_MEM_READ, h_tim1, None, 0x40012C30, 0x40012C50)
    uc.hook_add(UC_HOOK_MEM_WRITE, h_tim1, None, 0x40012C30, 0x40012C50)
    uc.hook_add(UC_HOOK_MEM_READ, h_tbl, None, 0x08017D36, 0x08017D7A)
    uc.hook_add(UC_HOOK_MEM_WRITE, h_portw, None, 0x48000000, 0x48000E00)

    emu.broad = True
    emu.spin_limit = 5000
    emu.pc_hits = {}
    emu.spins = 0
    emu.mapped_pages = 0

    for i in range(12):                            # полный цикл round-robin + запас
        uc.reg_write(UC_ARM_REG_SP, STACK_TOP)
        uc.reg_write(UC_ARM_REG_LR, STUB | 1)
        try:
            uc.emu_start(0xE658 | 1, STUB | 1, timeout=0, count=3_000_000)
        except Exception:
            pass                                   # срыв в stub-возврате — норма
        counter = bytes(uc.mem_read(0x20000A62, 1))[0]
        out = st.unpack_from("<H", bytes(uc.mem_read(0x20001357, 2)), 0)[0]
        ctl = st.unpack_from("<h", bytes(uc.mem_read(0x200013A4, 2)), 0)[0]
        print(f"итер {i:2d}: counter={counter} out@1357={out} ctl@st+24={ctl}")

    print(f"insn всего: {emu.insn}; события TIM1/TBL/PORT: {len(events)}")
    for ev in events[:30]:
        print("  ", ev)


if __name__ == "__main__":
    main()
