#!/usr/bin/env python3
"""
Динамический разбор агрегатора 0x1f71c (mcu_0007.bin).

Агрегатор — 24-состоянная машина (jump-table по CTX[0x10]), обрабатывает
сырые кадры из RX-кольца @0x20000c05 (3 слота × 150Б) и лог-кольца
@0x200010b5. Семантика состояний:

  CTX = 0x20000170: state=@0x180, byte_off=@0x182
  slotA = byte@0x2c8 → descA = 0x20000c05 + idx*0x96   (RX-кольцо)
  slotB = byte@0x2c9 → descB = 0x200010b5 + idx*0x96   (лог-кольцо)
  гейт: byte@0x2c8 != byte@0x2c7 (иначе tail-call 0x2000c)

Запуск:  python research_bin/mcu_agg.py [--frame 51525354] [--state N]
"""
import argparse
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "emulator"))
from mcu_emu import McuEmu, STACK_TOP, PERIPH, PERIPH_SIZE, SYS, SYS_SIZE  # noqa: E402
from unicorn import UC_HOOK_MEM_WRITE  # noqa: E402
from unicorn.arm_const import UC_ARM_REG_PC  # noqa: E402

CTX = 0x20000170
STATE_OFF = 0x180
OFF_OFF = 0x182
RX_RING = 0x20000c05
LOG_RING = 0x200010b5
SLOT = 0x96


def run(frame_hex, state=0, off=0, slot_a=0, slot_b=0, max_insn=300000):
    emu = McuEmu(trace=False, max_insn=max_insn)
    uc = emu.uc
    # периферия: status-биты готовы
    uc.mem_write(PERIPH, b"\xff" * PERIPH_SIZE)
    uc.mem_write(SYS, bytes(SYS_SIZE))

    # гейт: 0x2c8 != 0x2c7
    uc.mem_write(0x200002c8, struct.pack("<B", slot_a))
    uc.mem_write(0x200002c7, b"\x01")
    uc.mem_write(0x200002c9, struct.pack("<B", slot_b))

    # CTX: state, byte_off
    uc.mem_write(CTX + (STATE_OFF - 0x170), struct.pack("<B", state))
    uc.mem_write(CTX + (OFF_OFF - 0x170), struct.pack("<B", off))

    # системный тик
    uc.mem_write(0x200001e0, struct.pack("<Q", 0x00100000))

    # RX-кольцо: засеваем кадр в слот slot_a
    frame = bytes.fromhex(frame_hex) if frame_hex else b""
    uc.mem_write(RX_RING + slot_a * SLOT, frame.ljust(SLOT, b"\x00"))
    # лог-кольцо пусто

    # перехват ВСЕХ записей в RAM (кроме стека)
    writes = []

    def on_w(uc_, access, address, size, value, user):
        if 0x20000000 <= address < 0x20018000:
            pc = uc_.reg_read(UC_ARM_REG_PC)
            writes.append((pc, address - 0x20000000, size, value))

    uc.hook_add(UC_HOOK_MEM_WRITE, on_w)

    from unicorn.arm_const import UC_ARM_REG_SP, UC_ARM_REG_LR
    uc.reg_write(UC_ARM_REG_SP, STACK_TOP)
    uc.reg_write(UC_ARM_REG_LR, 1)
    try:
        uc.emu_start(0x1f71c | 1, 0, count=max_insn + 5)
    except Exception as e:
        pc = uc.reg_read(UC_ARM_REG_PC)
        print(f"[agg] UcError {e} @pc=0x{pc:05x}")

    # итог
    st = struct.unpack("<B", uc.mem_read(CTX + (STATE_OFF - 0x170), 1))[0]
    of = struct.unpack("<B", uc.mem_read(CTX + (OFF_OFF - 0x170), 1))[0]
    print(f"[agg] frame={frame.hex(' ') if frame else '(пусто)'} state_in={state} off_in={off}")
    print(f"[agg] инструкций: {emu.insn}, останов: {emu.stopped or 'нормально'}")
    print(f"[agg] state_out={st} off_out={of}")
    # записи, сгруппированные по адресу (только RAM-поля, не стек)
    ram_w = [w for w in writes if not (0x7000 <= w[1] < 0x8000)]
    # стек = 0x2001xxxx → смещение 0x1xxxx..0x17fff; отфильтруем
    ram_w = [w for w in writes if w[1] < 0x10000]
    print(f"[agg] записей в RAM: {len(ram_w)}")
    # показываем уникальные адреса с последним значением
    byaddr = {}
    for pc, a, sz, v in ram_w:
        byaddr.setdefault(a, []).append((pc, sz, v))
    for a in sorted(byaddr):
        recs = byaddr[a]
        vals = " ".join(f"0x{v:0{sz*2}x}" for _, sz, v in recs[:6])
        print(f"      [0x{a:05x}] {len(recs)} запис.: {vals}")
    if emu.usart_out:
        print(f"[agg] USART3: {bytes(emu.usart_out).hex(' ')}")
    return emu, byaddr


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--frame", default="51525354")
    ap.add_argument("--state", type=int, default=0)
    ap.add_argument("--off", type=int, default=0)
    ap.add_argument("--slot-a", type=int, default=0)
    a = ap.parse_args()
    run(a.frame, a.state, a.off, a.slot_a)
