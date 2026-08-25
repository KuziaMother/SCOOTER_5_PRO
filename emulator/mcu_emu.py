#!/usr/bin/env python3
"""
Инструкционный эмулятор прошивки MCU (Unicorn) — исполняет РЕАЛЬНЫЙ код mcu_0007.bin.

В отличие от emulator/ (поведенческая модель протокола), это исполнение настоящих
ARM Thumb-инструкций контроллера. Цель — пробить «стену рантайм-RAM»: запустить код,
дать ему инициализировать свои таблицы в RAM и/или перехватить, что он пишет в USART3
(реальные ID/кадры команд, которых нет в статике).

Границы честно: у нас только APP-регион OTA (нет вектор-таблицы/boot), периферия
заглушена (status-регистры отдают «готов»), поэтому это ФУНКЦИОНАЛЬНАЯ эмуляция
(вызов конкретной функции с поднятым состоянием), а не boot-from-reset.

Запуск:  python emulator/mcu_emu.py --func 0x1f600 [--max 200000] [--trace]
"""
import argparse
import os
import struct

from unicorn import (Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_HOOK_CODE,
                     UC_HOOK_MEM_WRITE, UC_HOOK_MEM_READ,
                     UC_HOOK_MEM_UNMAPPED, UcError)
from unicorn.arm_const import (UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC,
                               UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2,
                               UC_ARM_REG_R3)

HERE = os.path.dirname(os.path.abspath(__file__))
FW = os.path.join(os.path.dirname(HERE), "research", "images", "mcu_0007.bin")

FLASH0 = 0x00000000          # база 0 (адрес == смещение в файле)
FLASH1 = 0x08000000          # зеркало (некоторые литералы могут ждать эту базу)
RAM = 0x20000000
RAM_SIZE = 0x20000           # 128K
PERIPH = 0x40000000
PERIPH_SIZE = 0x00100000
# §59.3: расширенная область периферии чипа (блоки 0x48000400 DMA-подобный,
# 0x48000C00 GPIO-подобный; используют 0x1D640/0x1BF48/0x1C040)
PERIPH2 = 0x48000000
PERIPH2_SIZE = 0x00020000
SYS = 0xE0000000             # Cortex-M NVIC/SCB
SYS_SIZE = 0x00100000
STACK_TOP = 0x20018000

USART3_DR = 0x40004804       # куда 0x1f1c0 пишет байт команды
USART3_BASE = 0x40004800

# дескрипторы планировщика USART3 (из REPORT §MCU)
DESC_BASE = 0x20000A43
STATE_BASE = 0x20000A40


def align(x, a=0x1000):
    return (x + a - 1) & ~(a - 1)


class McuEmu:
    def __init__(self, trace=False, max_insn=200000):
        self.trace = trace
        self.max_insn = max_insn
        self.insn = 0
        self.usart_out = bytearray()
        self.ram_writes = []          # (pc, addr, size, val) в области дескрипторов
        self.stopped = None
        self.uc = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
        self._map()
        self._hooks()

    def _map(self):
        fw = open(FW, "rb").read()
        fsz = align(len(fw))
        for base in (FLASH0, FLASH1):
            self.uc.mem_map(base, fsz)
            self.uc.mem_write(base, fw)
        self.uc.mem_map(RAM, RAM_SIZE)
        self.uc.mem_map(PERIPH, PERIPH_SIZE)
        self.uc.mem_map(PERIPH2, PERIPH2_SIZE)
        self.uc.mem_map(SYS, SYS_SIZE)
        self.fw_len = len(fw)

    def _hooks(self):
        self.uc.hook_add(UC_HOOK_CODE, self._h_code)
        self.uc.hook_add(UC_HOOK_MEM_WRITE, self._h_write)
        self.uc.hook_add(UC_HOOK_MEM_READ, self._h_read, None, PERIPH, PERIPH + PERIPH_SIZE)
        self.uc.hook_add(UC_HOOK_MEM_UNMAPPED, self._h_unmapped)

    def _h_code(self, uc, address, size, user):
        self.insn += 1
        if self.insn > self.max_insn:
            self.stopped = f"лимит инструкций {self.max_insn}"
            uc.emu_stop()
            return
        # детект зависания: один PC исполнен слишком много раз = spin-loop
        if getattr(self, "broad", False):
            c = self.pc_hits.get(address, 0) + 1
            self.pc_hits[address] = c
            if c > self.spin_limit:
                uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR) or 1)
                self.spins += 1
                # если совсем застряли (много разных спинов) — стоп
                if self.spins > 400:
                    self.stopped = f"слишком много spin-loop'ов (последний @0x{address:05x})"
                    uc.emu_stop()
        if self.trace and self.insn <= 60:
            print(f"    [{self.insn:>5}] pc=0x{address:05x}")

    def _h_write(self, uc, access, address, size, value, user):
        if address == USART3_DR or (USART3_BASE <= address < USART3_BASE + 0x20 and size == 1):
            self.usart_out.append(value & 0xFF)
            pc = uc.reg_read(UC_ARM_REG_PC)
            print(f"    >>> USART3 write @pc=0x{pc:05x}: 0x{value & 0xFF:02x}")
        if 0x20000A00 <= address < 0x20000C10:      # область дескрипторов/стейта
            pc = uc.reg_read(UC_ARM_REG_PC)
            self.ram_writes.append((pc, address, size, value))

    def _h_read(self, uc, access, address, size, value, user):
        # периферия: status-регистры отдают «готов» (все биты), чтобы poll-циклы
        # не зависали. Это грубо, но позволяет коду двигаться.
        return

    def _h_unmapped(self, uc, access, address, size, value, user):
        # ШИРОКИЙ режим: маппим нулевую страницу по требованию и продолжаем
        if getattr(self, "broad", False):
            page = address & ~0xFFF
            try:
                uc.mem_map(page, 0x1000)
                self.mapped_pages = getattr(self, "mapped_pages", 0) + 1
                return True
            except UcError:
                return True
        pc = uc.reg_read(UC_ARM_REG_PC)
        self.stopped = f"обращение к незамапленному 0x{address:08x} @pc=0x{pc:05x} (access={access})"
        return False       # остановить

    def hook_periph_ready(self):
        """Периферию читаем как 0xFFFFFFFF (все ready-биты) — через отдельный
        механизм: Unicorn не даёт менять значение в READ-хуке напрямую, поэтому
        предзаполняем регион единицами."""
        self.uc.mem_write(PERIPH, b"\xff" * PERIPH_SIZE)
        self.uc.mem_write(PERIPH2, b"\x00" * PERIPH2_SIZE)
        self.uc.mem_write(SYS, b"\x00" * SYS_SIZE)

    def seed_scheduler(self):
        """Предусловия планировщика 0x1f600 (из литерального пула):
        - [0x200002c2]=0 (слот 0), [0x200002c1]=1 (!= -> не beq);
        - таймер 'сейчас' 0x200001e0 велик, 'послед.' 0x20000198 = 0 (elapsed>432);
        - дескриптор слота 0 (0x20000a43, 150Б) — маркеры, чтобы увидеть путь в USART3."""
        self.uc.mem_write(0x200002c2, b"\x00")            # слот 0
        self.uc.mem_write(0x200002c1, b"\x01")            # != -> не beq
        self.uc.mem_write(0x200001e0, struct.pack("<Q", 0x00100000))  # таймер now
        self.uc.mem_write(0x20000198, struct.pack("<Q", 0))           # таймер last
        # межбайтовый таймер [0x20000170+0x30/+0x34] > 8 (иначе ждёт 8 тиков)
        self.uc.mem_write(0x200001a0, struct.pack("<II", 100, 0))
        # дескриптор слота 0: узнаваемые байты D0 D1 D2 ... (первый = длина кадра)
        self.uc.mem_write(DESC_BASE, bytes((0xD0 + i) & 0xFF for i in range(150)))
        # USART3 SR [0x40004828] бит14 = 0 -> «не занято», путь отправки открыт

    def run_broad(self, addr, budget=2000000, spin_limit=3000):
        """Широкая эмуляция: прогнать init-функцию, дав рантайм-указателям поставиться.
        Маппинг по требованию, детект spin-loop, толерантность к периферии."""
        self.broad = True
        self.max_insn = budget
        self.spin_limit = spin_limit
        self.pc_hits = {}
        self.spins = 0
        self.mapped_pages = 0
        self.uc.mem_write(PERIPH, bytes(PERIPH_SIZE))
        self.uc.mem_write(PERIPH2, bytes(PERIPH2_SIZE))
        self.uc.mem_write(SYS, bytes(SYS_SIZE))
        self.uc.reg_write(UC_ARM_REG_SP, STACK_TOP)
        self.uc.reg_write(UC_ARM_REG_LR, 1)
        print(f"[broad] запуск init 0x{addr:05x}, бюджет {budget}")
        try:
            self.uc.emu_start(addr | 1, 0, count=budget + 5)
        except UcError as e:
            if self.stopped is None:
                self.stopped = f"UcError {e} @pc=0x{self.uc.reg_read(UC_ARM_REG_PC):05x}"
        print(f"[broad] инструкций: {self.insn}, spin-loop'ов: {self.spins}, "
              f"домапплено страниц: {self.mapped_pages}")
        print(f"[broad] останов: {self.stopped or 'дошёл до конца'}")
        return self

    def dump_ram(self, addr, size, label=""):
        try:
            r = self.uc.mem_read(addr, size)
        except Exception:
            return
        nz = any(r)
        print(f"[ram] 0x{addr:08x}..+0x{size:x} {label} {'(есть данные)' if nz else '(пусто)'}:")
        if nz:
            for i in range(0, len(r), 16):
                print(f"      +{i:03x}: {r[i:i+16].hex(' ')}")

    def run_func(self, addr, args=(), fill_desc=None, seed_sched=False):
        if seed_sched:
            self.uc.mem_write(PERIPH, bytes(PERIPH_SIZE))   # status-биты сброшены
            self.uc.mem_write(PERIPH2, bytes(PERIPH2_SIZE))
            self.uc.mem_write(SYS, bytes(SYS_SIZE))
            self.seed_scheduler()
        else:
            self.hook_periph_ready()
        # опционально засеять дескрипторы маркерами, чтобы увидеть их путь в USART3
        if fill_desc is not None:
            self.uc.mem_write(DESC_BASE, fill_desc)
        # стек
        self.uc.reg_write(UC_ARM_REG_SP, STACK_TOP)
        # аргументы r0..r3
        regs = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3]
        for r, v in zip(regs, args):
            self.uc.reg_write(r, v)
        # адрес возврата — «магический», ловим его в code-хуке как конец
        ret_magic = 0x00000001                      # BX к нечётному Thumb-адресу 0 -> поймаем
        self.uc.reg_write(UC_ARM_REG_LR, ret_magic)

        start = addr | 1                            # Thumb bit
        print(f"[emu] запуск функции 0x{addr:05x} (Thumb), макс {self.max_insn} инстр.")
        try:
            self.uc.emu_start(start, 0, count=self.max_insn + 5)
        except UcError as e:
            pc = self.uc.reg_read(UC_ARM_REG_PC)
            if self.stopped is None:
                self.stopped = f"UcError {e} @pc=0x{pc:05x}"
        self._report()

    def _report(self):
        print(f"\n[emu] инструкций выполнено: {self.insn}")
        print(f"[emu] останов: {self.stopped or 'дошёл до конца'}")
        print(f"[emu] байт записано в USART3: {len(self.usart_out)}")
        if self.usart_out:
            print(f"      данные: {bytes(self.usart_out).hex(' ')}")
        if self.ram_writes:
            print(f"[emu] записей в область дескрипторов 0x20000A00..0C10: {len(self.ram_writes)}")
            for pc, addr, size, val in self.ram_writes[:20]:
                print(f"      @pc=0x{pc:05x} [0x{addr:08x}] <- 0x{val:0{size*2}x} ({size}B)")
        # дамп RAM-области дескрипторов после прогона
        try:
            region = self.uc.mem_read(STATE_BASE, 0x60)
            print(f"[emu] RAM 0x{STATE_BASE:08x}..+0x60 после прогона:")
            for i in range(0, len(region), 16):
                print(f"      +{i:02x}: {region[i:i+16].hex(' ')}")
        except Exception:
            pass


def find_func_starts():
    """Начала функций = пролог push {..,lr} (0xB5xx) в кодовых секциях."""
    import struct as _s
    d = open(FW, "rb").read()
    CODE = [(0x01200, 0x02400), (0x02600, 0x10200), (0x10400, 0x10e00),
            (0x11000, 0x12400), (0x12800, 0x13e00), (0x14200, 0x14400),
            (0x14600, 0x17a00), (0x18e00, 0x19200), (0x19a00, 0x24200),
            (0x24400, 0x24600)]
    starts = []
    for a, b in CODE:
        for o in range(a, b, 2):
            if (_s.unpack_from("<H", d, o)[0] & 0xFF00) == 0xB500:
                starts.append(o)
    return starts


def sweep_writers(target_lo=0x20000A00, target_hi=0x20000C10, cap=8000):
    """Прогнать каждую функцию и найти те, что пишут в область дескрипторов.
    Динамический taint — то, чего статика не даёт (база указателя в рантайме)."""
    starts = find_func_starts()
    print(f"[sweep] функций: {len(starts)}, ищу запись в 0x{target_lo:08x}..0x{target_hi:08x}")
    hits = {}
    for idx, addr in enumerate(starts):
        emu = McuEmu(trace=False, max_insn=cap)
        emu.uc.mem_write(PERIPH, bytes(PERIPH_SIZE))
        emu.uc.mem_write(SYS, bytes(SYS_SIZE))
        recorded = []

        def on_w(uc, access, address, size, value, user):
            if target_lo <= address < target_hi:
                pc = uc.reg_read(UC_ARM_REG_PC)
                recorded.append((pc, address, size, value))
        from unicorn import UC_HOOK_MEM_WRITE as _W
        emu.uc.hook_add(_W, on_w)
        emu.uc.reg_write(UC_ARM_REG_SP, STACK_TOP)
        emu.uc.reg_write(UC_ARM_REG_LR, 1)
        try:
            emu.uc.emu_start(addr | 1, 0, count=cap)
        except UcError:
            pass
        if recorded:
            hits[addr] = recorded
        del emu
    print(f"\n[sweep] функций, пишущих в область дескрипторов: {len(hits)}")
    for addr, recs in sorted(hits.items(), key=lambda kv: -len(kv[1]))[:25]:
        addrs = sorted(set(r[1] for r in recs))
        print(f"  func 0x{addr:05x}: {len(recs)} записей, адреса "
              f"{[hex(a) for a in addrs[:8]]}{' …' if len(addrs) > 8 else ''}")
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--func", default="0x1f600")
    ap.add_argument("--max", type=int, default=200000)
    ap.add_argument("--trace", action="store_true")
    ap.add_argument("--seed-desc", action="store_true",
                    help="засеять дескрипторы маркерами 0xA0..0xAF")
    ap.add_argument("--seed-sched", action="store_true",
                    help="поднять предусловия планировщика 0x1f600")
    ap.add_argument("--find-writers", action="store_true",
                    help="прогнать все функции, найти пишущих в дескрипторы")
    a = ap.parse_args()
    if a.find_writers:
        sweep_writers()
        return
    addr = int(a.func, 16)
    emu = McuEmu(trace=a.trace, max_insn=a.max)
    seed = bytes(range(0xA0, 0xB0)) * 20 if a.seed_desc else None
    emu.run_func(addr, fill_desc=seed, seed_sched=a.seed_sched)


if __name__ == "__main__":
    main()
