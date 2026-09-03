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
                               UC_ARM_REG_R3, UC_ARM_REG_R4)

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

# §73: моторный таймер PWM = «TIMER_A» из каталога §60/§60.2 (подфункции FOC
# 0x1be1c/0x1bd88). Обнаружен/подтверждён трассой полного входа FOC 0x1a938
# (блок @0x1bde0-0x1bdfc). Блок регистров 0x40012c00..0x40012c54; данные/статус —
# на sub-base 0x40012c40 (это и есть «TIMER_A» каталога), CTRL — на base+0x30.
MOTOR_TIM_BASE = 0x40012c00
MOTOR_TIM_CTRL = MOTOR_TIM_BASE + 0x30    # FOC: ldr/ands #0xDFFF/str → clear бит 13
MOTOR_TIM_DATA0 = MOTOR_TIM_BASE + 0x44   # = TIMER_A+4;  ← u16[RAM+0x386] (PWM duty)
MOTOR_TIM_DATA1 = MOTOR_TIM_BASE + 0x48   # = TIMER_A+8;  ← u16[RAM+0x384]
MOTOR_TIM_DATA2 = MOTOR_TIM_BASE + 0x4c   # = TIMER_A+0xc;← u16[RAM+0x382]
MOTOR_TIM_STAT = MOTOR_TIM_BASE + 0x54    # = TIMER_A+0x14; read (бит15 low16 = гейт FOC)

# A1: кастомный GPIO-блок «портов» (§39.1): 4 порта × stride, F4-подобный layout.
# Эмпирика _gpio_layout_probe.py + дизасм драйвера 0x22000 (валидация port/pin/mode).
GPIO_PORT_BASE = 0x48000000
GPIO_PORT_STRIDE = 0x400        # порты: 0x48000000/0400/0800/0C00
GPIO_NPORTS = 4
GPIO_MODER = 0x2c               # режимы ВСЕХ 16 пинов, по 2 бита/пин: pin N → биты [2N+1:2N]
                                # (наблюдено: порт0=0x666 [пины 0-5], порт1=0x66660000 [пины 12-15])
GPIO_MODER_HI = 0x28            # вторичное поле (AF/напр.) — в motor-init = 0
GPIO_OUTSEL = 0x10              # output/select (большие значения — mask в high-битах)
GPIO_BIT_REGS = (0x14, 0x18, 0x1c, 0x20, 0x24)   # битовые регистры (сброс 0 в init)

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
        # --- периферия: диагностика + точные значения (§73) ---
        self.periph_overrides = {}    # {addr: u32} точные значения регистров (после fill)
        self.periph_writes = []       # [(pc, addr, size, value)] все записи в периферию
        self.periph_reads = {}        # {addr: [pc,...]} трассировка чтений (trace_periph)
        self.trace_periph = False     # включить логирование чтений периферии
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
        self.uc.hook_add(UC_HOOK_MEM_READ, self._h_read, None, PERIPH2, PERIPH2 + PERIPH2_SIZE)
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
        # запись в периферию (TIM/ADC/GPIO) — логируем для анализа моторного контура
        if (PERIPH <= address < PERIPH + PERIPH_SIZE or
                PERIPH2 <= address < PERIPH2 + PERIPH2_SIZE):
            pc = uc.reg_read(UC_ARM_REG_PC)
            self.periph_writes.append((pc, address, size, value))

    def _h_read(self, uc, access, address, size, value, user):
        # периферия: status-регистры отдают «готов» (все биты), чтобы poll-циклы
        # не зависали. Это грубо, но позволяет коду двигаться.
        if self.trace_periph:
            pc = uc.reg_read(UC_ARM_REG_PC)
            self.periph_reads.setdefault(address, []).append(pc)
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

    # --- §73: точные значения регистров периферии + отчёт по обращениям ---
    def set_periph(self, addr, value):
        """Задать точное значение 32-битного регистра периферии (вместо blanket
        0xFF/0x00). Применяется после hook_periph_ready/run_broad-заполнения."""
        self.periph_overrides[addr] = value & 0xFFFFFFFF

    def apply_periph_overrides(self):
        """Пропитать periph_overrides в память (вызывать после заполнения fill)."""
        for addr, val in self.periph_overrides.items():
            try:
                self.uc.mem_write(addr, struct.pack('<I', val))
            except Exception:
                pass

    def report_periph(self, max_addrs=40):
        """Отчёт по обращениям к периферии (записи + чтения, сгруппировано по адресу)."""
        addrs = set(a for _, a, _, _ in self.periph_writes) | set(self.periph_reads)
        if not addrs:
            print("[periph] обращений к периферии не было")
            return
        print(f"[periph] регистров затронуто: {len(addrs)} "
              f"(записей {len(self.periph_writes)}, чтений в {len(self.periph_reads)} адр)")
        for a in sorted(addrs)[:max_addrs]:
            ws = [w for _, aa, _, w in self.periph_writes if aa == a]
            rs = self.periph_reads.get(a, [])
            wvals = sorted(set(ws))
            wstr = ('[' + ','.join(hex(v) for v in wvals[:6]) + ']') if ws else ''
            print(f"  0x{a:08x}: W×{len(ws)} {wstr} R×{len(rs)}")

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
        self.apply_periph_overrides()      # точные значения регистров (§73)
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


class TimModel:
    """§73: поведенческая модель таймера — scoped-вид на регион в памяти Uc + реестр
    записей + named-доступ. Записи firmware уже попадают в память (источник истины);
    модель зеркалирует их для инспекции и даёт точку расширения под clock/status-флаги
    (метод tick() — заглушка под будущую тактовую модель)."""
    def __init__(self, emu, base=MOTOR_TIM_BASE, size=0x100, period=0x8000, step=1):
        self.emu = emu
        self.base = base
        self.size = size
        self.writes = []      # [(pc, offset, size, value)] записи в этот таймер
        # --- тактовая модель (§73.x): свободно-ходный счётчик + update-событие ---
        self.period = period  # wrap-значение счётчика (ARR)
        self.step = step      # приращение за такт
        self.cnt = 0          # текущее значение счётчика
        self.update = False   # флаг update-события (wrap)
        self.ticks = 0        # число продвинутых тактов
        self._hook = emu.uc.hook_add(UC_HOOK_MEM_WRITE, self._on_w,
                                     None, base, base + size)

    def _on_w(self, uc, access, address, size, value, user):
        self.writes.append((uc.reg_read(UC_ARM_REG_PC) & 0xFFFFF,
                            address - self.base, size, value))

    def read(self, off):
        return struct.unpack('<I', bytes(self.emu.uc.mem_read(self.base + off, 4)))[0]

    def set(self, off, val):
        self.emu.uc.mem_write(self.base + off, struct.pack('<I', val & 0xFFFFFFFF))

    def snapshot(self):
        """Текущие значения ключевых регистров: {имя: u32}."""
        return {
            'ctrl': self.read(0x30),
            'data0': self.read(0x44),
            'data1': self.read(0x48),
            'data2': self.read(0x4c),
            'stat': self.read(0x54),
        }

    def tick(self, n=1):
        """Продвинуть тактовую модель на n тактов. Возвращает число update-событий.

        Свободно-ходный счётчик cnt += step, wrap по period; при wrap (cnt <= prev)
        устанавливается self.update (аналог TIM update-события / события захвата).
        Для моторного блока 0x40012xxx «такт» = один период контура управления;
        update-событие соответствует тому, что firmware видит как STAT бит15 (гейт
        режима FOC). Точный hardware-источник события и период статически не
        определяются → модель параметризована (period/step задаёт вызывающий).
        """
        updates = 0
        for _ in range(n):
            self.ticks += 1
            prev = self.cnt
            self.cnt = (self.cnt + self.step) % self.period
            if self.cnt <= prev:          # wrap (или step=0)
                self.update = True
                updates += 1
        return updates

    def set_status_bits(self, addr, mask):
        """Задать биты mask в периферийном регистре addr (RMW, 32-bit)."""
        cur = struct.unpack('<I', self.emu.uc.mem_read(addr, 4))[0]
        self.emu.uc.mem_write(addr, struct.pack('<I', cur | mask))

    def clear_status_bits(self, addr, mask):
        """Сбросить биты mask в периферийном регистре addr (RMW, 32-bit)."""
        cur = struct.unpack('<I', self.emu.uc.mem_read(addr, 4))[0]
        self.emu.uc.mem_write(addr, struct.pack('<I', cur & ~mask))


# §73.x ADC: capture-регистра измерения фазных токов (ADC-inject PWM). 0x1be1c
# читает T28/T2C/T30 и реконструирует токи: фаза = (T−C)<<4, третья фаза = −сумма
# двух измеренных (закон Кирхгофа), финальный clamp [−30000,30000]. Гейт режима —
# STAT бит15 (u32[0x40012c54]): =1 → capture, =0 → skip (только clamp).
ADC_CAP_BASE = 0x40012440
ADC_CAP_T28 = ADC_CAP_BASE + 0x28    # 0x40012468
ADC_CAP_T2C = ADC_CAP_BASE + 0x2c    # 0x4001246c
ADC_CAP_T30 = ADC_CAP_BASE + 0x30    # 0x40012470
# sector → handler (конвенция каталога §60, поведение эмпирически верифицировано §73.x):
# 0→null, 1→B, 2/3→C, 4/5→A, 6→B.
ADC_SECTOR_HANDLER = {0: None, 1: 'B', 2: 'C', 3: 'C', 4: 'A', 5: 'A', 6: 'B'}
# handler → измеренные фазы: (t_reg_off, c_struct_off, out_struct_off).
# C-ссылки (zero-current refs) в struct FOC: C18=+0x18, C1A=+0x1a, C1C=+0x1c;
# выходы: o_c=+0xc, o_10=+0x10, o_14=+0x14.
ADC_HANDLER_MEASURED = {
    'A': [(0x28, 0x18, 0xc), (0x2c, 0x1a, 0x10)],   # T28→o_c, T2C→o_10; o_14=−sum
    'B': [(0x2c, 0x1a, 0x10), (0x30, 0x1c, 0x14)],   # T2C→o_10, T30→o_14; o_c=−sum
    'C': [(0x28, 0x18, 0xc), (0x30, 0x1c, 0x14)],    # T28→o_c, T30→o_14; o_10=−sum
}


class AdcModel:
    """§73.x: модель ADC/capture-канала фазных токов (вход FOC).

    Hardware: ADC-inject PWM — ADC сэмплирует ток, таймер захватывает момент
    сравнения; 0x1be1c читает T28/T2C/T30 (periph) и реконструирует токи.
    Модель даёт app доступ к T-регистрам (set_captures) и convenience set_currents
    (инжект желаемых токов под C-ссылки). Ток квантуется ×16 (масштаб <<4).
    """
    def __init__(self, emu):
        self.emu = emu

    def _w(self, off, val):
        self.emu.uc.mem_write(ADC_CAP_BASE + off,
                              struct.pack('<I', val & 0xFFFFFFFF))

    def set_captures(self, t28, t2c, t30):
        """Записать сырые capture-значения T28/T2C/T30 (periph)."""
        self._w(0x28, t28)
        self._w(0x2c, t2c)
        self._w(0x30, t30)

    def get_captures(self):
        """Прочитать текущие (T28, T2C, T30) как u32."""
        return (struct.unpack('<I', self.emu.uc.mem_read(ADC_CAP_T28, 4))[0],
                struct.unpack('<I', self.emu.uc.mem_read(ADC_CAP_T2C, 4))[0],
                struct.unpack('<I', self.emu.uc.mem_read(ADC_CAP_T30, 4))[0])

    def set_currents(self, r0, currents, sector):
        """Инжект желаемых pre-clamp токов, задав capture под C-ссылки из r0.

        currents = {0xc: o_c, 0x10: o_10, 0x14: o_14}. Для двух измеренных фаз
        (по sector→handler) T = C + (ток>>4); третья фаза = −сумма (автоматически).
        Ток квантуется ×16; sector определяет, какие 2 фазы измеряются.
        """
        h = ADC_SECTOR_HANDLER.get(sector & 7)
        if h is None:
            return
        for t_off, c_off, out_off in ADC_HANDLER_MEASURED[h]:
            cref = struct.unpack('<h', self.emu.uc.mem_read(r0 + c_off, 2))[0]
            target = currents[out_off]
            self._w(t_off, (cref + (target >> 4)) & 0xFFFFFFFF)


# §73.x скорость: V=u32[RAM+0x158]=timer-capture период; F=byte[RAM+0x100] гейт;
# val=s16(48000/V) if F!=0 else 0 (0x1d874). val → u16[RAM+0x1768], читается PID 0x1d078.
SPEED_V_OFF = 0x158        # u32 период (RAM+0x158)
SPEED_F_OFF = 0x100        # byte гейт (RAM+0x100): 0 → val=0
SPEED_SP0_OFF = 0x1768     # u16 вычисленный val (RAM+0x1768) — скорость для PID
SPEED_DIV = 48000          # делитель: val = s16(48000/V)


class SpeedModel:
    """§73.x: модель замера скорости (вход PID 0x1d078), замыкает контур.

    Hardware: timer-capture период между импульсами энкодера → V; скорость ∝ 1/V.
    Firmware: val = s16(48000/V) if F=byte[RAM+0x100]!=0 else 0 (0x1d874),
    val → u16[RAM+0x1768]. Модель задаёт V/F (set_period / set_speed / stop).
    Точный ISR-писатель гейтится по аппаратному состоянию (импульс/pending) и в
    изолированной эмуляции не триггерится (writer-sweep: 0 хитов) → модель
    параметризована (app даёт измеренную скорость).
    """
    def __init__(self, emu):
        self.emu = emu

    def set_period(self, v):
        """Записать период V (u32[RAM+0x158]) + открыть гейт F=1."""
        self.emu.uc.mem_write(RAM + SPEED_V_OFF,
                              struct.pack('<I', v & 0xFFFFFFFF))
        self.emu.uc.mem_write(RAM + SPEED_F_OFF, bytes([1]))

    def set_speed(self, val):
        """Инжект желаемой измеренной скорости val: V = max(1, 48000//val).

        val<=0 → stop() (F=0). val>48000 кэпится (V=1 → val=48000).
        """
        if val <= 0:
            self.stop()
            return
        v = max(1, SPEED_DIV // int(val))
        self.set_period(v)

    def stop(self):
        """Останов: F=0 → val=0."""
        self.emu.uc.mem_write(RAM + SPEED_F_OFF, bytes([0]))

    def get_val(self):
        """Прочитать вычисленный val (s16 u16[RAM+0x1768]) после прогона PID."""
        return struct.unpack('<h', self.emu.uc.mem_read(RAM + SPEED_SP0_OFF, 2))[0]


class MotorModel:
    """§73.x: модель динамики мотора (plant): throttle → скорость во времени.

    Первый-порядковый lag к терминальной скорости для текущего throttle:
      v_term = v_max * clamp(throttle/throttle_ref, 0, 1)
      speed += (dt/tau) * (v_term - speed)
    Терминальная скорость при full throttle = v_max; tau — постоянная времени
    (инерция + сопротивление). Параметры НЕ определяются firmware (физика
    конкретного самоката) → модель параметризована. Единицы скорости = внутренние
    val (§71): ~20.8 units/(км/ч); target 125≈6 км/ч, 208≈10 км/ч, 522≈25 км/ч (EU).
    v_max=522 по умолчанию = максимальный target (~25 км/ч). Замыкает АВТОНОМНЫЙ симул:
      target → PID 0x1d078 → throttle(u16[RAM+0x42c]) → [MotorModel] → speed →
      SpeedModel.set_speed (V) → PID ...
    """
    def __init__(self, emu, v_max=522.0, tau=15.0, throttle_ref=4000.0, dt=1.0):
        self.emu = emu
        self.v_max = float(v_max)
        self.tau = float(tau)
        self.throttle_ref = float(throttle_ref)
        self.dt = float(dt)
        self.speed = 0.0

    def step(self, throttle):
        """Один шаг: throttle (PID-вывод) → новая скорость (val). Возвращает speed."""
        tnorm = max(0.0, min(1.0, throttle / self.throttle_ref))
        v_term = self.v_max * tnorm
        self.speed += (self.dt / self.tau) * (v_term - self.speed)
        if self.speed < 0.0:
            self.speed = 0.0
        return self.speed

    def reset(self, speed=0.0):
        self.speed = float(speed)


# §73.x батарея: SoC% = u16[RAM+0x306] (из i16@0x17a0 [415..535]→[0..100]%, §25).
# FOC читает SoC@0x306 с порогами 90/10, clamp 100; гейт byte@0x22e. Защита: 4150
# (max 4.15 В), 3000 (cutoff 3.0 В). Контур: ADC buf[2]→IIR÷256→×410+калибровка(BLE)
# →блок 0x40023c00→i16@0x17a0→[0..100]%→u16@0x306.
BATT_SOC_OFF = 0x306        # u16 SoC % (RAM+0x306)
BATT_RAW_OFF = 0x17A0       # i16 сырое значение [415..535] (RAM+0x17a0)
BATT_RAW_MIN = 415          # → 0%
BATT_RAW_MAX = 535          # → 100%


class BatteryModel:
    """§73.x: модель аккумулятора. SoC% → u16[RAM+0x306] (+ сырое i16@0x17a0).

    Контур (§25): ADC buf[2] → IIR÷256 (i16@0x272) → ×410 + калибровка u16@0x1ec
    (из BLE, raw×41/48) → блок 0x40023c00 → i16@0x17a0 [415..535] → [0..100]% →
    u16[RAM+0x306]. FOC читает SoC@0x306 с порогами 90/10 (гейт byte@0x22e — в изоляции
    не срабатывает, проверено). Модель задаёт SoC (set_soc) и моделирует разряд
    (discharge: SoC падает с нагрузкой во времени). Параметры разряда параметризованы.
    """
    def __init__(self, emu, soc=100.0):
        self.emu = emu
        self.soc = float(soc)

    @staticmethod
    def _raw(pct):
        """[0..100]% → сырое [415..535]."""
        return BATT_RAW_MIN + int(round(pct * (BATT_RAW_MAX - BATT_RAW_MIN) / 100.0))

    def set_soc(self, pct):
        """Записать SoC% (u16[RAM+0x306]) + согласованное сырое i16@0x17a0."""
        pct = max(0, min(100, int(pct)))
        self.soc = float(pct)
        self.emu.uc.mem_write(RAM + BATT_SOC_OFF, struct.pack('<H', pct))
        self.emu.uc.mem_write(RAM + BATT_RAW_OFF, struct.pack('<h', self._raw(pct)))
        return pct

    def get_soc(self):
        """Прочитать SoC% (u16[RAM+0x306])."""
        return struct.unpack('<H', self.emu.uc.mem_read(RAM + BATT_SOC_OFF, 2))[0]

    def discharge(self, throttle, dt=1.0, full_throttle=32760.0, rate=0.05):
        """Разряд: SoC падает пропорционально нагрузке (throttle как прокси тока).

        rate — %/шаг при full throttle (параметризовано; подгонять под live-замер).
        Float-накопление в self.soc (§74: set_soc тринкует до int и обнулял дробную
        часть → разряд был ровно 1%/tick при любой нагрузке>0); в RAM пишется int.
        Возвращает новый SoC (int).
        """
        load = max(0.0, min(1.0, throttle / full_throttle))
        self.soc = max(0.0, self.soc - rate * load * dt)
        pct = max(0, min(100, int(self.soc)))
        self.emu.uc.mem_write(RAM + BATT_SOC_OFF, struct.pack('<H', pct))
        self.emu.uc.mem_write(RAM + BATT_RAW_OFF, struct.pack('<h', self._raw(pct)))
        return pct


# §73.x запас хода (0x1d898): читает i16@RAM+0x27A (батарея, ADC-регион §25),
# пишет struct(RAM+0x3C8, общий с PID/FOC): +0x20 = X=(8000·v)>>16;
# +0x40 = 10000·X/(500−X) (делитель 0x19994, div-by-zero→-1, отриц. знаменатель→отриц.).
# Константы: SCALE=8000, REF=500, K=10000 (=scale/100% из §25). Формула вериф. 400/400 (v≥0).
RANGE_VAL_OFF = 0x27A       # i16 вход (батарея)
RANGE_CTX_OFF = 0x3C8       # struct-контекст (общий с PID/FOC)
RANGE_SCALE = 8000          # ×8000>>16
RANGE_REF = 500             # full-scale (div-by-zero при X==500)
RANGE_K = 10000             # масштаб числителя делителя
# аккумулятор 0x1d898 (leaky integrator): new_0x3c=(old_0x3c+delta−prev_0x14)&0xFFFFFFFF;
# new_0x14=asr(new_0x3c,10)[i16]. delta=i16@RAM+0x26E. Вериф. 250/250.
RANGE_ACC_OFF = 0x404       # u32 аккумулятор (struct+0x3c)
RANGE_ACC_SCALED_OFF = 0x3DC  # i16 = acc>>10 (struct+0x14)
RANGE_DELTA_OFF = 0x26E     # i16 delta-вход


class RangeModel:
    """§73.x: оценщик запаса хода (firmware 0x1d898).

    v = i16@RAM+0x27A (батарея) → X = (8000·v)>>16; R = 10000·X/(500−X).
    Формула верифицирована random-sweep 400/400 (v≥0, включая div-by-zero→-1 и
    отрицательный знаменатель) против firmware. estimate() — closed-form; для сверки
    вызывайте firmware напрямую: run.call(0x1D898, (0,0,0,0), max_insn=300000) →
    X=u16[RAM+0x3E8], R=i32[RAM+0x408]. Физическая единица R не определена статически
    (нужна live-корреляция); при v∈[415..535] (SoC) R≈1111..1494.
    """
    def __init__(self, emu):
        self.emu = emu

    def set_value(self, v):
        """Записать входной i16@RAM+0x27A. Возвращает v."""
        v = max(-32768, min(32767, int(v)))
        self.emu.uc.mem_write(RAM + RANGE_VAL_OFF, struct.pack('<h', v))
        return v

    def estimate(self, v):
        """Closed-form: (X, R). X=(8000·v)>>16; R=10000·X/(500−X), div-by-zero→-1."""
        X = (RANGE_SCALE * v) >> 16
        denom = RANGE_REF - X
        if denom == 0:
            return X, -1
        num = RANGE_K * X
        q = abs(num) // abs(denom)
        R = -q if (num < 0) != (denom < 0) else q
        return X, R

    def set_delta(self, d):
        """Записать delta-вход аккумулятора i16@RAM+0x26E. Возвращает d."""
        d = max(-32768, min(32767, int(d)))
        self.emu.uc.mem_write(RAM + RANGE_DELTA_OFF, struct.pack('<h', d))
        return d

    def acc_step(self, old_acc, old_scaled, delta):
        """Leaky integrator (0x1d898): возвращает (new_acc u32, new_scaled i16).

        new_acc = (old_acc + delta − old_scaled) & 0xFFFFFFFF
        new_scaled = asr(new_acc, 10) как i16 (низкие 16 бит арифметического сдвига).
        Верифицировано stateful-sweep 250/250 против firmware.
        """
        new_acc = (old_acc + delta - old_scaled) & 0xFFFFFFFF
        s = new_acc if new_acc < 0x80000000 else new_acc - 0x100000000
        asr = s >> 10                      # Python arithmetic shift == ARM asr
        ns = asr & 0xFFFF
        new_scaled = ns if ns < 0x8000 else ns - 0x10000
        return new_acc, new_scaled


# §74 Автономный моторный контур (time-driven warm-start control loop).
PID_OFF = 0x1D078          # PID / speed-limit state machine
FOC_OFF = 0x1A938          # FOC routine
THROTTLE_OFF = 0x42C       # s16 PID-вывод (throttle)
CURR_REF_OFF = 0x224       # u16 FOC current-ref (upstream command, §73.15)
FOC_CTX_OFF = 0x040        # R4 контекст FOC
FOC_CCR_OFFS = (0x382, 0x384, 0x386)   # PWM CCR A/B/C (RAM+off)


class GpioModel:
    """A1: поведенческая модель кастомного GPIO-блока «портов» (§39.1) — scoped-вид на
    регион 0x48000000..+4×0x400 + реестр записей + декод режима пинов (2 бита/пин в
    MODER_LO/HI). Записи firmware уже попадают в память (источник истины); модель
    зеркалирует их для инспекции pin-config и даёт точку расширения под input-state.
    (input-регистр — чтение, в init не пишется; см. расширение.)"""
    def __init__(self, emu, base=GPIO_PORT_BASE, nports=GPIO_NPORTS, stride=GPIO_PORT_STRIDE):
        self.emu = emu
        self.base = base
        self.nports = nports
        self.stride = stride
        self.writes = []      # [(pc, port, offset, size, value)]
        self._hook = emu.uc.hook_add(UC_HOOK_MEM_WRITE, self._on_w,
                                     None, base, base + nports * stride)

    def _on_w(self, uc, access, address, size, value, user):
        off = address - self.base
        self.writes.append((uc.reg_read(UC_ARM_REG_PC) & 0xFFFFF,
                            off // self.stride, off % self.stride, size, value))

    def read(self, port, off):
        return struct.unpack('<I',
                             bytes(self.emu.uc.mem_read(self.base + port * self.stride + off, 4)))[0]

    def set(self, port, off, val):
        self.emu.uc.mem_write(self.base + port * self.stride + off,
                              struct.pack('<I', val & 0xFFFFFFFF))

    def pin_mode(self, port, pin):
        """Режим пина (2 бита) из MODER (+0x2c): pin N → биты [2N+1:2N]."""
        return (self.read(port, GPIO_MODER) >> (pin * 2)) & 0x3

    def output(self, port):
        """Значение output/select-регистра +0x10."""
        return self.read(port, GPIO_OUTSEL)

    def config_report(self):
        """{port: {pin: mode}} — только пины с ненулевым режимом (итоговое состояние)."""
        rep = {}
        for p in range(self.nports):
            pins = {pin: self.pin_mode(p, pin) for pin in range(16)
                    if self.pin_mode(p, pin)}
            if pins:
                rep[p] = pins
        return rep


class ControlLoop:
    """§74 Автономный моторный контур — time-driven warm-start.

    Виртуальные часы + реальный firmware PID/FOC на каждом tick + поведенческие модели
    plant/speed/battery/range. НЕ boot от reset и НЕ полный scheduler (slot-table
    устанавливается runtime, boot-blocked §73.15) — PID/FOC вызываются напрямую на их
    реальной частоте (валидная абстракция контура: speed-controller → torque → FOC).

    Цепочка на tick:
      measured_speed → SpeedModel.set_speed (V)          [вход PID]
      target → PID 0x1d078 → throttle s16[RAM+0x42c]     [реальный firmware]
      throttle → current-ref u16[RAM+0x224] → FOC 0x1a938 → PWM CCR  [реальный firmware]
      throttle → MotorModel.step → speed                 [plant, first-order lag]
      throttle → BatteryModel.discharge → SoC            [разряд]
      SoC → RangeModel.estimate → запас хода             [closed-form]
    """
    def __init__(self, emu=None, v_max=522.0, tau=15.0, throttle_ref=28624.0,
                 batt_rate=0.05, run_foc=True):
        # throttle_ref = full-scale PID-вывода (0x42c ~28624..32760), НЕ 4000 (§73.9 дефолт
        # дал насыщение plant: speed не сходится к target, а уходит в v_max).
        self.emu = emu or McuEmu(max_insn=400000)
        self.sm = SpeedModel(self.emu)
        self.mm = MotorModel(self.emu, v_max=v_max, tau=tau,
                             throttle_ref=throttle_ref, dt=1.0)
        self.bm = BatteryModel(self.emu)
        self.rm = RangeModel(self.emu)
        self.batt_rate = float(batt_rate)
        self.run_foc = bool(run_foc)
        self.now = 0

    def setup(self, target, mode=3, soc=100.0):
        """Засеять RAM: режим, target, power-enable, гейты, батарея (см. §73.9-73.15)."""
        uc = self.emu.uc
        uc.mem_write(RAM, bytes(0x20000))
        uc.mem_write(RAM + 0x229, bytes([mode]))                          # mode
        uc.mem_write(RAM + 0x326, struct.pack('<H', target & 0xFFFF))     # target
        uc.mem_write(RAM + 0x339, b'\x00')
        uc.mem_write(RAM + 0x333, b'\x00')                                # skip mode-change
        uc.mem_write(RAM + 0x263, b'\x00')                                # gate → ramp-core
        uc.mem_write(RAM + 0x1760, struct.pack('<I', 32760))              # power enable
        uc.mem_write(RAM + 0x3C8 + 0x28, struct.pack('<H', 1))            # counter → phase B
        self.bm.set_soc(soc)
        self.mm.reset(0.0)
        self.now = 0

    def _in_flash(self, aa):
        L = self.emu.fw_len
        return (FLASH0 <= aa < FLASH0 + L) or (FLASH1 <= aa < FLASH1 + L)

    def _run_pid(self):
        """Реальный PID 0x1d078 → throttle s16[RAM+0x42c]."""
        uc = self.emu.uc
        sh = uc.hook_add(UC_HOOK_CODE,
                         lambda u, a, s, ud: u.emu_stop() if not self._in_flash(a & ~1) else None)
        uc.reg_write(UC_ARM_REG_SP, STACK_TOP - 0x80)
        uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        for r in (UC_ARM_REG_R0, UC_ARM_REG_R4):
            uc.reg_write(r, 0)
        try:
            uc.emu_start(PID_OFF | 1, 0, count=400000)
        except Exception:
            pass
        uc.hook_del(sh)
        return struct.unpack('<h', uc.mem_read(RAM + THROTTLE_OFF, 2))[0]

    def _run_foc(self, current_ref):
        """Реальный FOC 0x1a938 (R4=RAM+0x040, ref=u16[RAM+0x224]) → PWM CCR."""
        uc = self.emu.uc
        r4 = RAM + FOC_CTX_OFF
        uc.mem_write(r4, bytes(0x80))
        uc.mem_write(r4 + 2, struct.pack('<h', 16384))
        uc.mem_write(RAM + CURR_REF_OFF, struct.pack('<H', current_ref & 0xFFFF))
        sh = uc.hook_add(UC_HOOK_CODE,
                         lambda u, a, s, ud: u.emu_stop() if not self._in_flash(a & ~1) else None)
        uc.reg_write(UC_ARM_REG_SP, STACK_TOP - 0x80)
        uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        uc.reg_write(UC_ARM_REG_R4, r4)
        uc.reg_write(UC_ARM_REG_R0, 0)
        try:
            uc.emu_start(FOC_OFF | 1, 0, count=200000)
        except Exception:
            pass
        uc.hook_del(sh)
        return tuple(struct.unpack('<H', uc.mem_read(RAM + o, 2))[0] for o in FOC_CCR_OFFS)

    def tick(self):
        """Один шаг контура. Возвращает dict состояния."""
        self.sm.set_speed(int(self.mm.speed))          # measured speed → PID input
        thr = self._run_pid()                          # real firmware: PID → throttle
        if self.run_foc:
            ccr = self._run_foc(thr & 0xFFFF)          # real firmware: FOC → PWM
            center = sum(ccr) / 3.0
            amp = max(abs(c - center) for c in ccr)
        else:
            amp = 0.0
        self.mm.step(thr)                              # plant: throttle → speed
        self.bm.discharge(thr, dt=1.0, rate=self.batt_rate)   # battery
        soc = self.bm.get_soc()
        v_batt = BatteryModel._raw(int(soc))           # SoC → сырое [415..535]
        X, R = self.rm.estimate(v_batt)                # запас хода (closed-form)
        self.now += 1
        return dict(t=self.now, speed=round(self.mm.speed, 1), throttle=thr,
                    pwm_amp=round(amp, 1), soc=round(soc, 2), range=R)

    def run(self, ticks):
        """Прогнать ticks шагов. Возвращает список состояний."""
        return [self.tick() for _ in range(ticks)]


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
