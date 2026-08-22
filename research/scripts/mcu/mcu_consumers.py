#!/usr/bin/env python3
"""
Потребители (readers) RAM-адресов RX-телеметрии — кто читает поля ответов BLE→MCU.

Цель: физическая семантика полей из карты §16.4.4 («поле кадра -> адрес RAM»).
Для каждого целевого диапазона в RAM находим функции, которые его ЧИТАЮТ:

  1) СТАТИКА: литеральные пулы — все `ldr rX,[pc,#imm]` (16- и 32-битные), чьё
     слово пула попадает в целевой диапазон. Даёт кандидата + PC загрузки.
  2) ДИНАМИКА (read-taint): прогон всех функций под Unicorn с READ-хуком на
     диапазонах; фиксируем реально исполняемые чтения (pc, addr, size).
     Ловит и вычисляемые доступы (база+смещение), если они исполняются при RAM=0.

Результат: для каждого поля — список потребительских функций + окно дизассемблера
вокруг точки чтения (что делается со значением: cmp/mul/shift/clamp).

Запуск:  python research/mcu_consumers.py [--dynamic] [--win 24]
"""
import argparse
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.dirname(os.path.dirname(HERE))   # research/
sys.path.insert(0, os.path.join(os.path.dirname(RES), "emulator"))

from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB

FW = os.path.join(RES, "images", "mcu_0007.bin")
RAM = 0x20000000

# Кодовые секции (из functions_mcu/README.md)
CODE = [(0x01200, 0x02400), (0x02600, 0x10200), (0x10400, 0x10e00),
        (0x11000, 0x12400), (0x12800, 0x13e00), (0x14200, 0x14400),
        (0x14600, 0x17a00), (0x18e00, 0x19200), (0x19a00, 0x24200),
        (0x24400, 0x24600)]

# Целевые диапазоны: RAM-офсеты полей из §16.4.4 (карта «поле -> RAM»)
TARGETS = [
    # (имя, lo_o, hi_o) — офсеты ОТ 0x20000000, диапазон включительно..исключительно
    ("C41",   0x2b0, 0x2ba),   # CMD 0x41: u16 BE + байты
    ("C41M",  0x2e8, 0x2f2),   # CMD 0x41 зеркало
    ("C42",   0x2cb, 0x2d2),   # CMD 0x42: 7 байт
    ("C43",   0x2d2, 0x2d9),   # CMD 0x43: 7 байт
    ("C45",   0x2da, 0x2e6),   # CMD 0x45: 6x u16 LE
    ("C44a",  0x2e6, 0x2e8),   # CMD 0x44: byte @0x2e6
    ("C46",   0x2f2, 0x306),   # CMD 0x46: буфер (len cap 0x14)
    ("C44b",  0x306, 0x310),   # CMD 0x44: 0x306..0x30f
    ("C48",   0x354, 0x358),   # CMD 0x48: 4 байта
    ("C49",   0x36a, 0x36c),   # CMD 0x49: u16 LE
    ("C4A",   0x36c, 0x36e),   # CMD 0x4A: u16 LE
    ("B49",   0x1585, 0x1607), # CMD 0x49: буфер данных
    ("B4A",   0x1607, 0x1690), # CMD 0x4A: буфер данных
]


def target_of(off):
    for name, lo, hi in TARGETS:
        if lo <= off < hi:
            return name
    return None


def load_funcs():
    """Список подтверждённых функций из справочника (имена файлов)."""
    d = os.path.join(RES, "functions_mcu")
    out = []
    for fn in sorted(os.listdir(d)):
        if fn.startswith("func_0x") and fn.endswith(".md"):
            out.append(int(fn[7:-3], 16))
    return sorted(out)


def func_of(pc, funcs):
    """Функция, содержащая pc (по началу; границы из справочника не нужны —
    для атрибуции достаточно ближайшего старта <= pc)."""
    best = None
    for f in funcs:
        if f <= pc:
            best = f
        else:
            break
    return best


def static_scan(d, funcs):
    """Все ldr rX,[pc,#imm] со словом пула в целевых диапазонах.

    ВАЖНО: sequential-декод целых регионов десинхронизируется на встроенных
    данных (см. README functions_mcu), поэтому деассемблируем ОКНА каждой
    функции (skipdata=True) — так же, как gen_functions_mcu.py."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "gen_fm", os.path.join(os.path.dirname(HERE), "gen_functions_mcu.py"))
    gen = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gen)
    md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    md.skipdata = True
    flist, _fakes, _thunks = gen.detect_functions(d, md)
    hits = []   # (pc, func, reg, addr, tname)
    for fa, fb, _r in flist:
        for ins in md.disasm(d[fa:fb], fa):
            ops = ins.op_str.replace(" ", "")
            if not (ins.mnemonic == "ldr" and "[pc,#" in ops):
                continue
            imm_s = ops.split("[pc,#")[1][:-1]
            imm = int(imm_s, 16) if imm_s.startswith("0x") else int(imm_s)
            # 16-битная форма: (addr+4)&~3 ; 32-битная: (addr+8)&~3
            base = (ins.address + (4 if len(ins.bytes) == 2 else 8)) & ~3
            pool = base + imm
            if not (0 <= pool < len(d) - 3):
                continue
            v = struct.unpack_from("<I", d, pool)[0]
            off = v - RAM
            tname = target_of(off)
            if tname is None:
                continue
            reg = ins.op_str.split(",")[0].replace(" ", "").split("[pc")[0]
            hits.append((ins.address, fa, reg, v, tname))
    return hits


def dynamic_scan(funcs, cap=20000):
    """Read-taint: прогнать все функции, хук чтения на целевых диапазонах."""
    from mcu_emu import (McuEmu, PERIPH, SYS, PERIPH_SIZE, SYS_SIZE, STACK_TOP)
    from unicorn import UC_HOOK_MEM_READ
    from unicorn.arm_const import UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC
    from unicorn import UcError

    lo_all = min(t[1] for t in TARGETS) + RAM
    hi_all = max(t[2] for t in TARGETS) + RAM
    results = {}   # func -> [(pc, addr, size)]
    for i, f in enumerate(funcs):
        emu = McuEmu(trace=False, max_insn=cap)
        e = emu.uc
        e.mem_write(PERIPH, bytes(PERIPH_SIZE))
        e.mem_write(SYS, bytes(SYS_SIZE))
        rec = []

        def on_r(uc, access, address, size, value, user, _rec=rec):
            tname = target_of(address - RAM)
            if tname is not None:
                pc = uc.reg_read(UC_ARM_REG_PC)
                _rec.append((pc, address, size))

        h = e.hook_add(UC_HOOK_MEM_READ, on_r, begin=lo_all, end=hi_all)
        e.reg_write(UC_ARM_REG_SP, STACK_TOP)
        e.reg_write(UC_ARM_REG_LR, 1)
        try:
            e.emu_start(f | 1, 0, count=cap + 5)
        except UcError:
            pass
        e.hook_del(h)
        if rec:
            results[f] = rec
        del emu
        if (i + 1) % 100 == 0:
            print(f"  ...{i+1}/{len(funcs)} функций", flush=True)
    return results


def disasm_window(d, pc, win=24):
    """Окно дизассемблера вокруг pc (по 2 инструкции назад, win вперёд)."""
    md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    start = max(a for a, _ in CODE if a <= pc)
    end = min(b for _, b in CODE if b > pc)
    chunk = d[start:end]
    lines = []
    hit = False
    for ins in md.disasm(chunk, start):
        if ins.address == pc:
            hit = True
        if hit:
            lines.append(f"  {ins.address:06x}: {ins.mnemonic} {ins.op_str}")
            if len(lines) > win:
                break
    return lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dynamic", action="store_true", help="read-taint по всем функциям")
    ap.add_argument("--win", type=int, default=24, help="размер окна дизассемблера")
    ap.add_argument("--only", default="", help="только эти имена целей: C42,C43,...")
    a = ap.parse_args()

    d = open(FW, "rb").read()
    funcs = load_funcs()
    print(f"функций в справочнике: {len(funcs)}")

    only = set(a.only.split(",")) if a.only else None

    # ---- статика ----
    hits = static_scan(d, funcs)
    if only:
        hits = [h for h in hits if h[4] in only]
    by_t = {}
    for pc, f, reg, v, tname in hits:
        by_t.setdefault(tname, []).append((pc, f, reg, v))

    print(f"\n=== СТАТИКА: ldr-ссылок на целевые диапазоны: {len(hits)} ===")
    for tname, lo, hi in TARGETS:
        if only and tname not in only:
            continue
        hs = by_t.get(tname, [])
        fs = sorted(set(f for _, f, _, _ in hs))
        print(f"\n[{tname}] 0x{RAM+lo:08x}..0x{RAM+hi:08x}: {len(hs)} ссылок, функций: "
              + ", ".join(f"0x{x:05x}" for x in fs))
        for pc, f, reg, v in sorted(hs):
            print(f"    pc=0x{pc:05x} (func 0x{f:05x}) {reg} <- [pool] = 0x{v:08x}")

    # ---- динамика ----
    if a.dynamic:
        print(f"\n=== ДИНАМИКА: read-taint по {len(funcs)} функциям ===")
        dyn = dynamic_scan(funcs)
        by_t2 = {}
        for f, rec in dyn.items():
            for pc, addr, size in rec:
                tname = target_of(addr - RAM)
                by_t2.setdefault(tname, []).append((f, pc, addr, size))
        print(f"функций с реальными чтениями: {len(dyn)}")
        for tname, lo, hi in TARGETS:
            if only and tname not in only:
                continue
            recs = by_t2.get(tname, [])
            fs = sorted(set(f for f, _, _, _ in recs))
            print(f"\n[{tname}] 0x{RAM+lo:08x}..0x{RAM+hi:08x}: функций-читателей: "
                  + ", ".join(f"0x{x:05x}" for x in fs))
            for f, pc, addr, size in sorted(recs):
                print(f"    func 0x{f:05x} pc=0x{pc:05x} read {size}B @0x{addr:08x}")

    # ---- окна дизассемблера вокруг статических точек чтения ----
    if not a.dynamic:
        print("\n=== ОКНА ДИЗАССЕМБЛЕРА (статические точки) ===")
        seen = set()
        for tname, lo, hi in TARGETS:
            if only and tname not in only:
                continue
            for pc, f, reg, v in sorted(by_t.get(tname, [])):
                key = (f, pc)
                if key in seen:
                    continue
                seen.add(key)
                print(f"\n--- [{tname}] func 0x{f:05x}, точка чтения pc=0x{pc:05x} "
                      f"({reg} <- 0x{v:08x}) ---")
                for line in disasm_window(d, pc, a.win):
                    print(line)


if __name__ == "__main__":
    main()
