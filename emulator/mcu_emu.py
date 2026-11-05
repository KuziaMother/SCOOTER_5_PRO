#!/usr/bin/env python3
"""
MCU firmware instruction emulator (Unicorn) — executes REAL mcu_0007.bin code.

Unlike emulator/ (behavioral protocol model), this executes real
ARM Thumb instructions of controller. Purpose — penetrate runtime RAM wall: run code,
allow it to initialize tables in RAM and/or intercept USART3 writes
(real command IDs/frames absent in static analysis).

Boundaries: we only have the OTA APP region (no vector table/boot), peripherals
are stubbed (status registers return "ready"), so this is FUNCTIONAL emulation
(calling a specific function with initialized state) rather than boot-from-reset.

Usage:   python emulator/mcu_emu.py --func 0x1f600 [--max 200000] [--trace]
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

FLASH0 = 0x00000000          # base 0 (address == offset in file)
FLASH1 = 0x08000000          # mirror (some literals may expect this base)
RAM = 0x20000000
RAM_SIZE = 0x20000           # 128K
PERIPH = 0x40000000
PERIPH_SIZE = 0x00100000
# §59.3: extended chip peripheral region (blocks 0x48000400 DMA-like,
# 0x48000C00 GPIO-like; used by 0x1D640/0x1BF48/0x1C040)
PERIPH2 = 0x48000000
PERIPH2_SIZE = 0x00020000
SYS = 0xE0000000             # Cortex-M NVIC/SCB
SYS_SIZE = 0x00100000
STACK_TOP = 0x20018000

USART3_DR = 0x40004804       # destination where 0x1f1c0 writes command byte
USART3_BASE = 0x40004800

# §73: PWM motor timer = "TIMER_A" from catalog §60/§60.2 (FOC subfunctions
# 0x1be1c/0x1bd88). Discovered/confirmed via full trace of FOC entry 0x1a938
# (block @0x1bde0-0x1bdfc). Register block 0x40012c00..0x40012c54; data/status —
# at sub-base 0x40012c40 (catalog "TIMER_A"), CTRL at base+0x30.
MOTOR_TIM_BASE = 0x40012c00
MOTOR_TIM_CTRL = MOTOR_TIM_BASE + 0x30    # FOC: ldr/ands #0xDFFF/str -> clear bit 13
MOTOR_TIM_DATA0 = MOTOR_TIM_BASE + 0x44   # = TIMER_A+4;  ← u16[RAM+0x386] (PWM duty)
MOTOR_TIM_DATA1 = MOTOR_TIM_BASE + 0x48   # = TIMER_A+8;  ← u16[RAM+0x384]
MOTOR_TIM_DATA2 = MOTOR_TIM_BASE + 0x4c   # = TIMER_A+0xc;← u16[RAM+0x382]
MOTOR_TIM_STAT = MOTOR_TIM_BASE + 0x54    # = TIMER_A+0x14; read (bit15 low16 = FOC gate)

# A1: custom GPIO "ports" block (§39.1): 4 ports * stride, F4-like layout.
# Empirical from _gpio_layout_probe.py + driver 0x22000 disasm (port/pin/mode validation).
GPIO_PORT_BASE = 0x48000000
GPIO_PORT_STRIDE = 0x400        # ports: 0x48000000/0400/0800/0C00
GPIO_NPORTS = 4
GPIO_MODER = 0x2c               # modes for ALL 16 pins, 2 bits/pin: pin N -> bits [2N+1:2N]
                                # (observed: port0=0x666 [pins 0-5], port1=0x66660000 [pins 12-15])
GPIO_MODER_HI = 0x28            # secondary field (AF/dir) — in motor-init = 0
GPIO_OUTSEL = 0x10              # output/select (large values — mask in high bits)
GPIO_BIT_REGS = (0x14, 0x18, 0x1c, 0x20, 0x24)   # bit registers (cleared to 0 in init)

# USART3 scheduler descriptors (from REPORT §MCU)
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
        self.ram_writes = []          # (pc, addr, size, val) in descriptor region
        # --- peripherals: diagnostics + exact values (§73) ---
        self.periph_overrides = {}    # {addr: u32} exact register values (after fill)
        self.periph_writes = []       # [(pc, addr, size, value)] all writes to peripherals
        self.periph_reads = {}        # {addr: [pc,...]} read trace (trace_periph)
        self.trace_periph = False     # enable peripheral read logging
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
            self.stopped = f"instruction limit {self.max_insn}"
            uc.emu_stop()
            return
        # hang detection: single PC executed too many times = spin-loop
        if getattr(self, "broad", False):
            c = self.pc_hits.get(address, 0) + 1
            self.pc_hits[address] = c
            if c > self.spin_limit:
                uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR) or 1)
                self.spins += 1
                # if completely stuck (too many different spins) — stop
                if self.spins > 400:
                    self.stopped = f"too many spin loops (last @0x{address:05x})"
                    uc.emu_stop()
        if self.trace and self.insn <= 60:
            print(f"    [{self.insn:>5}] pc=0x{address:05x}")

    def _h_write(self, uc, access, address, size, value, user):
        if address == USART3_DR or (USART3_BASE <= address < USART3_BASE + 0x20 and size == 1):
            self.usart_out.append(value & 0xFF)
            pc = uc.reg_read(UC_ARM_REG_PC)
            print(f"    >>> USART3 write @pc=0x{pc:05x}: 0x{value & 0xFF:02x}")
        if 0x20000A00 <= address < 0x20000C10:      # descriptor/state region
            pc = uc.reg_read(UC_ARM_REG_PC)
            self.ram_writes.append((pc, address, size, value))
        # write to peripherals (TIM/ADC/GPIO) — log for motor loop analysis
        if (PERIPH <= address < PERIPH + PERIPH_SIZE or
                PERIPH2 <= address < PERIPH2 + PERIPH2_SIZE):
            pc = uc.reg_read(UC_ARM_REG_PC)
            self.periph_writes.append((pc, address, size, value))

    def _h_read(self, uc, access, address, size, value, user):
        # peripherals: status registers return "ready" (all bits) so poll loops
        # do not hang. This is rough, but allows code to progress.
        if self.trace_periph:
            pc = uc.reg_read(UC_ARM_REG_PC)
            self.periph_reads.setdefault(address, []).append(pc)
        return

    def _h_unmapped(self, uc, access, address, size, value, user):
        # BROAD mode: map zero page on demand and continue
        if getattr(self, "broad", False):
            page = address & ~0xFFF
            try:
                uc.mem_map(page, 0x1000)
                self.mapped_pages = getattr(self, "mapped_pages", 0) + 1
                return True
            except UcError:
                return True
        pc = uc.reg_read(UC_ARM_REG_PC)
        self.stopped = f"access to unmapped 0x{address:08x} @pc=0x{pc:05x} (access={access})"
        return False       # stop

    def hook_periph_ready(self):
        """Read peripherals as 0xFFFFFFFF (all ready bits) — via dedicated
        mechanism: Unicorn does not allow altering values in READ hooks directly,
        so prefill region with ones."""
        self.uc.mem_write(PERIPH, b"\xff" * PERIPH_SIZE)
        self.uc.mem_write(PERIPH2, b"\x00" * PERIPH2_SIZE)
        self.uc.mem_write(SYS, b"\x00" * SYS_SIZE)

    # --- §73: exact peripheral register values + access report ---
    def set_periph(self, addr, value):
        """Set exact value for 32-bit peripheral register (instead of blanket
        0xFF/0x00). Applied after hook_periph_ready/run_broad fill."""
        self.periph_overrides[addr] = value & 0xFFFFFFFF

    def apply_periph_overrides(self):
        """Apply periph_overrides into memory (call after fill)."""
        for addr, val in self.periph_overrides.items():
            try:
                self.uc.mem_write(addr, struct.pack('<I', val))
            except Exception:
                pass

    def report_periph(self, max_addrs=40):
        """Report of peripheral accesses (writes + reads grouped by address)."""
        addrs = set(a for _, a, _, _ in self.periph_writes) | set(self.periph_reads)
        if not addrs:
            print("[periph] no peripheral accesses recorded")
            return
        print(f"[periph] registers accessed: {len(addrs)} "
              f"(writes: {len(self.periph_writes)}, reads in {len(self.periph_reads)} addrs)")
        for a in sorted(addrs)[:max_addrs]:
            ws = [w for _, aa, _, w in self.periph_writes if aa == a]
            rs = self.periph_reads.get(a, [])
            wvals = sorted(set(ws))
            wstr = ('[' + ','.join(hex(v) for v in wvals[:6]) + ']') if ws else ''
            print(f"  0x{a:08x}: W×{len(ws)} {wstr} R×{len(rs)}")

    # --- E2: periph-write-trace facility (capture periph-writes per function) ---
    def periph_write_map(self):
        """E2: periph-writes grouped by address {addr: [value,...]} (order of writes).
        Facility for verifying "function X writes value Z to register Y" — enhances all
        A-models (GPIO/USART/SPI/TIM). Source: self.periph_writes [(pc,addr,size,value)]."""
        m = {}
        for _, addr, size, value in self.periph_writes:
            m.setdefault(addr, []).append(value)
        return m

    def periph_writes_since(self, mark):
        """E2: periph-writes after mark=len(periph_writes) snapshot — window of a single call."""
        return self.periph_writes[mark:]

    def seed_scheduler(self):
        """Preconditions for scheduler 0x1f600 (from literal pool):
        - [0x200002c2]=0 (slot 0), [0x200002c1]=1 (!= -> not beq);
        - timer 'now' 0x200001e0 large, 'last' 0x20000198 = 0 (elapsed>432);
        - slot 0 descriptor (0x20000a43, 150B) — markers to trace path to USART3."""
        self.uc.mem_write(0x200002c2, b"\x00")            # slot 0
        self.uc.mem_write(0x200002c1, b"\x01")            # != -> not beq
        self.uc.mem_write(0x200001e0, struct.pack("<Q", 0x00100000))  # timer now
        self.uc.mem_write(0x20000198, struct.pack("<Q", 0))           # timer last
        # interbyte timer [0x20000170+0x30/+0x34] > 8 (otherwise waits 8 ticks)
        self.uc.mem_write(0x200001a0, struct.pack("<II", 100, 0))
        # slot 0 descriptor: recognizable bytes D0 D1 D2 ... (first = frame length)
        self.uc.mem_write(DESC_BASE, bytes((0xD0 + i) & 0xFF for i in range(150)))
        # USART3 SR [0x40004828] bit14 = 0 -> "not busy", transmission path open

    def run_broad(self, addr, budget=2000000, spin_limit=3000):
        """Broad emulation: run init function allowing runtime pointers to be established.
        On-demand mapping, spin-loop detection, peripheral fault tolerance."""
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
        print(f"[broad] starting init 0x{addr:05x}, budget {budget}")
        try:
            self.uc.emu_start(addr | 1, 0, count=budget + 5)
        except UcError as e:
            if self.stopped is None:
                self.stopped = f"UcError {e} @pc=0x{self.uc.reg_read(UC_ARM_REG_PC):05x}"
        print(f"[broad] instructions: {self.insn}, spin-loops: {self.spins}, "
              f"mapped pages: {self.mapped_pages}")
        print(f"[broad] stopped: {self.stopped or 'completed execution'}")
        return self

    def dump_ram(self, addr, size, label=""):
        try:
            r = self.uc.mem_read(addr, size)
        except Exception:
            return
        nz = any(r)
        print(f"[ram] 0x{addr:08x}..+0x{size:x} {label} {'(has data)' if nz else '(empty)'}:")
        if nz:
            for i in range(0, len(r), 16):
                print(f"      +{i:03x}: {r[i:i+16].hex(' ')}")

    def run_func(self, addr, args=(), fill_desc=None, seed_sched=False):
        if seed_sched:
            self.uc.mem_write(PERIPH, bytes(PERIPH_SIZE))   # status bits cleared
            self.uc.mem_write(PERIPH2, bytes(PERIPH2_SIZE))
            self.uc.mem_write(SYS, bytes(SYS_SIZE))
            self.seed_scheduler()
        else:
            self.hook_periph_ready()
        self.apply_periph_overrides()      # exact register values (§73)
        # optionally seed descriptors with markers to trace path to USART3
        if fill_desc is not None:
            self.uc.mem_write(DESC_BASE, fill_desc)
        # stack
        self.uc.reg_write(UC_ARM_REG_SP, STACK_TOP)
        # arguments r0..r3
        regs = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3]
        for r, v in zip(regs, args):
            self.uc.reg_write(r, v)
        # magic return address, caught in code hook as exit condition
        ret_magic = 0x00000001                      # BX to odd Thumb address 0 -> intercepted
        self.uc.reg_write(UC_ARM_REG_LR, ret_magic)

        start = addr | 1                            # Thumb bit
        print(f"[emu] running function 0x{addr:05x} (Thumb), max {self.max_insn} insn.")
        try:
            self.uc.emu_start(start, 0, count=self.max_insn + 5)
        except UcError as e:
            pc = self.uc.reg_read(UC_ARM_REG_PC)
            if self.stopped is None:
                self.stopped = f"UcError {e} @pc=0x{pc:05x}"
        self._report()

    def _report(self):
        print(f"\n[emu] instructions executed: {self.insn}")
        print(f"[emu] stopped: {self.stopped or 'completed execution'}")
        print(f"[emu] bytes written to USART3: {len(self.usart_out)}")
        if self.usart_out:
            print(f"      data: {bytes(self.usart_out).hex(' ')}")
        if self.ram_writes:
            print(f"[emu] writes to descriptor region 0x20000A00..0C10: {len(self.ram_writes)}")
            for pc, addr, size, val in self.ram_writes[:20]:
                print(f"      @pc=0x{pc:05x} [0x{addr:08x}] <- 0x{val:0{size*2}x} ({size}B)")
        # dump RAM descriptor region after execution
        try:
            region = self.uc.mem_read(STATE_BASE, 0x60)
            print(f"[emu] RAM 0x{STATE_BASE:08x}..+0x60 after execution:")
            for i in range(0, len(region), 16):
                print(f"      +{i:02x}: {region[i:i+16].hex(' ')}")
        except Exception:
            pass


class TimModel:
    """§73: behavioral timer model — scoped view into Uc memory region + write log
    + named access. Firmware writes land directly in memory (source of truth);
    model mirrors them for inspection and provides extension point for clock/status flags
    (tick() method — clock model hook)."""
    def __init__(self, emu, base=MOTOR_TIM_BASE, size=0x100, period=0x8000, step=1):
        self.emu = emu
        self.base = base
        self.size = size
        self.writes = []      # [(pc, offset, size, value)] writes to this timer
        # --- clock model (§73.x): free-running counter + update event ---
        self.period = period  # counter wrap value (ARR)
        self.step = step      # increment per tick
        self.cnt = 0          # current counter value
        self.update = False   # update event flag (wrap)
        self.ticks = 0        # elapsed ticks count
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
        """Current values of key registers: {name: u32}."""
        return {
            'ctrl': self.read(0x30),
            'data0': self.read(0x44),
            'data1': self.read(0x48),
            'data2': self.read(0x4c),
            'stat': self.read(0x54),
        }

    def tick(self, n=1):
        """Advance clock model by n ticks. Returns count of update events.

        Free-running counter cnt += step, wrapping around period; on wrap (cnt <= prev)
        self.update is set (analogous to TIM update / capture event).
        For motor block 0x40012xxx, one "tick" = one control loop period;
        update event corresponds to firmware STAT bit15 (FOC mode gate).
        Exact hardware event source and period are not statically determined ->
        model is parameterized (period/step provided by caller).
        """
        updates = 0
        for _ in range(n):
            self.ticks += 1
            prev = self.cnt
            self.cnt = (self.cnt + self.step) % self.period
            if self.cnt <= prev:          # wrap (or step=0)
                self.update = True
                updates += 1
        return updates

    def set_status_bits(self, addr, mask):
        """Set mask bits in peripheral register addr (RMW, 32-bit)."""
        cur = struct.unpack('<I', self.emu.uc.mem_read(addr, 4))[0]
        self.emu.uc.mem_write(addr, struct.pack('<I', cur | mask))

    def clear_status_bits(self, addr, mask):
        """Clear mask bits in peripheral register addr (RMW, 32-bit)."""
        cur = struct.unpack('<I', self.emu.uc.mem_read(addr, 4))[0]
        self.emu.uc.mem_write(addr, struct.pack('<I', cur & ~mask))


# §73.x ADC: capture registers of phase current measurement (ADC-inject PWM). 0x1be1c
# reads T28/T2C/T30 and reconstructs currents: phase = (T-C)<<4, third phase = -sum
# of measured two (Kirchhoff's law), final clamp [-30000, 30000]. Mode gate:
# STAT bit15 (u32[0x40012c54]): =1 -> capture, =0 -> skip (clamp only).
ADC_CAP_BASE = 0x40012440
ADC_CAP_T28 = ADC_CAP_BASE + 0x28    # 0x40012468
ADC_CAP_T2C = ADC_CAP_BASE + 0x2c    # 0x4001246c
ADC_CAP_T30 = ADC_CAP_BASE + 0x30    # 0x40012470
# sector -> handler (catalog convention §60, empirically verified §73.x):
# 0→null, 1→B, 2/3→C, 4/5→A, 6→B.
ADC_SECTOR_HANDLER = {0: None, 1: 'B', 2: 'C', 3: 'C', 4: 'A', 5: 'A', 6: 'B'}
# handler -> measured phases: (t_reg_off, c_struct_off, out_struct_off).
# C-references (zero-current refs) in struct FOC: C18=+0x18, C1A=+0x1a, C1C=+0x1c;
# outputs: o_c=+0xc, o_10=+0x10, o_14=+0x14.
ADC_HANDLER_MEASURED = {
    'A': [(0x28, 0x18, 0xc), (0x2c, 0x1a, 0x10)],   # T28→o_c, T2C→o_10; o_14=−sum
    'B': [(0x2c, 0x1a, 0x10), (0x30, 0x1c, 0x14)],   # T2C→o_10, T30→o_14; o_c=−sum
    'C': [(0x28, 0x18, 0xc), (0x30, 0x1c, 0x14)],    # T28→o_c, T30→o_14; o_10=−sum
}


class AdcModel:
    """§73.x: ADC/phase current capture channel model (FOC input).

    Hardware: ADC-inject PWM — ADC samples current, timer captures compare event;
    0x1be1c reads T28/T2C/T30 (periph) and reconstructs currents.
    Model provides app access to T registers (set_captures) and convenience set_currents
    (inject desired currents relative to C-references). Current quantized *16 (<<4 scale).
    """
    def __init__(self, emu):
        self.emu = emu

    def _w(self, off, val):
        self.emu.uc.mem_write(ADC_CAP_BASE + off,
                              struct.pack('<I', val & 0xFFFFFFFF))

    def set_captures(self, t28, t2c, t30):
        """Write raw capture values T28/T2C/T30 (periph)."""
        self._w(0x28, t28)
        self._w(0x2c, t2c)
        self._w(0x30, t30)

    def get_captures(self):
        """Read current (T28, T2C, T30) as u32."""
        return (struct.unpack('<I', self.emu.uc.mem_read(ADC_CAP_T28, 4))[0],
                struct.unpack('<I', self.emu.uc.mem_read(ADC_CAP_T2C, 4))[0],
                struct.unpack('<I', self.emu.uc.mem_read(ADC_CAP_T30, 4))[0])

    def set_currents(self, r0, currents, sector):
        """Inject desired pre-clamp currents, setting capture relative to C-refs from r0.

        currents = {0xc: o_c, 0x10: o_10, 0x14: o_14}. For two measured phases
        (per sector->handler) T = C + (current>>4); third phase = -sum (automatically).
        Current is quantized *16; sector determines which 2 phases are measured.
        """
        h = ADC_SECTOR_HANDLER.get(sector & 7)
        if h is None:
            return
        for t_off, c_off, out_off in ADC_HANDLER_MEASURED[h]:
            cref = struct.unpack('<h', self.emu.uc.mem_read(r0 + c_off, 2))[0]
            target = currents[out_off]
            self._w(t_off, (cref + (target >> 4)) & 0xFFFFFFFF)


# §73.x speed: V=u32[RAM+0x158]=timer-capture period; F=byte[RAM+0x100] gate;
# val=s16(48000/V) if F!=0 else 0 (0x1d874). val -> u16[RAM+0x1768], read by PID 0x1d078.
SPEED_V_OFF = 0x158        # u32 period (RAM+0x158)
SPEED_F_OFF = 0x100        # byte gate (RAM+0x100): 0 -> val=0
SPEED_SP0_OFF = 0x1768     # u16 computed val (RAM+0x1768) — speed for PID
SPEED_DIV = 48000          # divisor: val = s16(48000/V)


class SpeedModel:
    """§73.x: speed measurement model (PID 0x1d078 input), closes loop.

    Hardware: timer-capture period between encoder pulses -> V; speed proportional to 1/V.
    Firmware: val = s16(48000/V) if F=byte[RAM+0x100]!=0 else 0 (0x1d874),
    val -> u16[RAM+0x1768]. Model sets V/F (set_period / set_speed / stop).
    Exact ISR writer is gated by hardware state (pulse/pending) and in
    isolated emulation is not triggered (writer-sweep: 0 hits) -> model
    is parameterized (app provides measured speed).
    """
    def __init__(self, emu):
        self.emu = emu

    def set_period(self, v):
        """Write period V (u32[RAM+0x158]) + open gate F=1."""
        self.emu.uc.mem_write(RAM + SPEED_V_OFF,
                              struct.pack('<I', v & 0xFFFFFFFF))
        self.emu.uc.mem_write(RAM + SPEED_F_OFF, bytes([1]))

    def set_speed(self, val):
        """Inject desired measured speed val: V = max(1, 48000 // val).

        val<=0 -> stop() (F=0). val>48000 is capped (V=1 -> val=48000).
        """
        if val <= 0:
            self.stop()
            return
        v = max(1, SPEED_DIV // int(val))
        self.set_period(v)

    def stop(self):
        """Stop: F=0 -> val=0."""
        self.emu.uc.mem_write(RAM + SPEED_F_OFF, bytes([0]))

    def get_val(self):
        """Read computed val (s16 u16[RAM+0x1768]) after PID execution."""
        return struct.unpack('<h', self.emu.uc.mem_read(RAM + SPEED_SP0_OFF, 2))[0]


class MotorModel:
    """motor dynamics model (plant): throttle -> speed over time.

    First-order lag toward terminal speed for current throttle:
      v_term = v_max * clamp(throttle/throttle_ref, 0, 1)
      speed += (dt/tau) * (v_term - speed)
    Terminal speed at full throttle = v_max; tau — time constant
    (inertia + drag). Parameters are NOT determined by firmware
    (physics of specific scooter) -> model is parameterized. Speed units = internal
    val (§71): ~20.8 units/(km/h); target 125~6 km/h, 208~10 km/h, 522~25 km/h (EU).
    v_max=522 default = max target (~25 km/h). Closes AUTONOMOUS simulation:
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
        """Single step: throttle (PID output) -> new speed (val). Returns speed."""
        tnorm = max(0.0, min(1.0, throttle / self.throttle_ref))
        v_term = self.v_max * tnorm
        self.speed += (self.dt / self.tau) * (v_term - self.speed)
        if self.speed < 0.0:
            self.speed = 0.0
        return self.speed

    def reset(self, speed=0.0):
        self.speed = float(speed)


# §73.x battery: SoC% = u16[RAM+0x306] (from i16@0x17a0 [415..535]->[0..100]%, §25).
# FOC reads SoC@0x306 with thresholds 90/10, clamp 100; gate byte@0x22e. Protection: 4150
# (max 4.15 V), 3000 (cutoff 3.0 V). Loop: ADC buf[2]->IIR/256->*410+calib(BLE)
# ->block 0x40023c00->i16@0x17a0->[0..100]%->u16@0x306.
BATT_SOC_OFF = 0x306        # u16 SoC % (RAM+0x306)
BATT_RAW_OFF = 0x17A0       # i16 raw value [415..535] (RAM+0x17a0)
BATT_RAW_MIN = 415          # → 0%
BATT_RAW_MAX = 535          # → 100%


class BatteryModel:
    """§73.x: battery model. SoC% -> u16[RAM+0x306] (+ raw i16@0x17a0).

    Loop (§25): ADC buf[2] -> IIR/256 (i16@0x272) -> *410 + calibration u16@0x1ec
    (from BLE, raw*41/48) -> block 0x40023c00 -> i16@0x17a0 [415..535] -> [0..100]% ->
    u16[RAM+0x306]. FOC reads SoC@0x306 with 90/10 thresholds (gate byte@0x22e — in isolation
    does not trigger, verified). Model sets SoC (set_soc) and simulates discharge
    (discharge: SoC drops with load over time). Discharge parameters are parameterized.
    """
    def __init__(self, emu, soc=100.0):
        self.emu = emu
        self.soc = float(soc)

    @staticmethod
    def _raw(pct):
        """[0..100]% -> raw [415..535]."""
        return BATT_RAW_MIN + int(round(pct * (BATT_RAW_MAX - BATT_RAW_MIN) / 100.0))

    def set_soc(self, pct):
        """Write SoC% (u16[RAM+0x306]) + synchronized raw i16@0x17a0."""
        pct = max(0, min(100, int(pct)))
        self.soc = float(pct)
        self.emu.uc.mem_write(RAM + BATT_SOC_OFF, struct.pack('<H', pct))
        self.emu.uc.mem_write(RAM + BATT_RAW_OFF, struct.pack('<h', self._raw(pct)))
        return pct

    def get_soc(self):
        """Read SoC% (u16[RAM+0x306])."""
        return struct.unpack('<H', self.emu.uc.mem_read(RAM + BATT_SOC_OFF, 2))[0]

    def discharge(self, throttle, dt=1.0, full_throttle=32760.0, rate=0.05):
        """Discharge: SoC drops proportionally to load (throttle as current proxy).

        rate — %/step at full throttle (parameterized; match to live measurement).
        Float accumulator in self.soc (§74: set_soc truncates to int and cleared fractional
        part -> discharge was exactly 1%/tick at any load>0); RAM receives int.
        Returns new SoC (int).
        """
        load = max(0.0, min(1.0, throttle / full_throttle))
        self.soc = max(0.0, self.soc - rate * load * dt)
        pct = max(0, min(100, int(self.soc)))
        self.emu.uc.mem_write(RAM + BATT_SOC_OFF, struct.pack('<H', pct))
        self.emu.uc.mem_write(RAM + BATT_RAW_OFF, struct.pack('<h', self._raw(pct)))
        return pct


# §73.x range estimation (0x1d898): reads i16@RAM+0x27A (battery, ADC region §25),
# writes struct(RAM+0x3C8, shared with PID/FOC): +0x20 = X=(8000*v)>>16;
# +0x40 = 10000*X/(500-X) (divisor 0x19994, div-by-zero->-1, negative denom->negative).
# Constants: SCALE=8000, REF=500, K=10000 (=scale/100% from §25). Formula verified 400/400 (v>=0).
RANGE_VAL_OFF = 0x27A       # i16 input (battery)
RANGE_CTX_OFF = 0x3C8       # struct context (shared with PID/FOC)
RANGE_SCALE = 8000          # ×8000>>16
RANGE_REF = 500             # full-scale (div-by-zero when X==500)
RANGE_K = 10000             # numerator divisor scale
# accumulator 0x1d898 (leaky integrator): new_0x3c=(old_0x3c+delta-prev_0x14)&0xFFFFFFFF;
# new_0x14=asr(new_0x3c,10)[i16]. delta=i16@RAM+0x26E. Verified 250/250.
RANGE_ACC_OFF = 0x404       # u32 accumulator (struct+0x3c)
RANGE_ACC_SCALED_OFF = 0x3DC  # i16 = acc>>10 (struct+0x14)
RANGE_DELTA_OFF = 0x26E     # i16 delta input


class RangeModel:
    """§73.x: range estimator (firmware 0x1d898).

    v = i16@RAM+0x27A (battery) -> X = (8000*v)>>16; R = 10000*X/(500-X).
    Formula verified via random-sweep 400/400 (v>=0, including div-by-zero->-1 and
    negative denominator) against firmware. estimate() is closed-form; to verify,
    call firmware directly: run.call(0x1D898, (0,0,0,0), max_insn=300000) ->
    X=u16[RAM+0x3E8], R=i32[RAM+0x408]. Physical unit of R is not statically determined
    (requires live correlation); with v in [415..535] (SoC), R~1111..1494.
    """
    def __init__(self, emu):
        self.emu = emu

    def set_value(self, v):
        """Write input i16@RAM+0x27A. Returns v."""
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
        """Write accumulator delta input i16@RAM+0x26E. Returns d."""
        d = max(-32768, min(32767, int(d)))
        self.emu.uc.mem_write(RAM + RANGE_DELTA_OFF, struct.pack('<h', d))
        return d

    def acc_step(self, old_acc, old_scaled, delta):
        """Leaky integrator (0x1d898): returns (new_acc u32, new_scaled i16).

        new_acc = (old_acc + delta - old_scaled) & 0xFFFFFFFF
        new_scaled = asr(new_acc, 10) as i16 (low 16 bits of arithmetic shift).
        Verified via stateful-sweep 250/250 against firmware.
        """
        new_acc = (old_acc + delta - old_scaled) & 0xFFFFFFFF
        s = new_acc if new_acc < 0x80000000 else new_acc - 0x100000000
        asr = s >> 10                      # Python arithmetic shift == ARM asr
        ns = asr & 0xFFFF
        new_scaled = ns if ns < 0x8000 else ns - 0x10000
        return new_acc, new_scaled


# §74 Autonomous motor loop (time-driven warm-start control loop).
PID_OFF = 0x1D078          # PID / speed-limit state machine
FOC_OFF = 0x1A938          # FOC routine
THROTTLE_OFF = 0x42C       # s16 PID output (throttle)
CURR_REF_OFF = 0x224       # u16 FOC current-ref (upstream command, §73.15)
FOC_CTX_OFF = 0x040        # R4 FOC context
FOC_CCR_OFFS = (0x382, 0x384, 0x386)   # PWM CCR A/B/C (RAM+off)


class GpioModel:
    """A1: behavioral model of custom GPIO "ports" block (§39.1) — scoped view onto
    region 0x48000000..+4*0x400 + write log + pin mode decoder (2 bits/pin in
    MODER_LO/HI). Firmware writes land directly in memory (source of truth); model
    mirrors them for pin-config inspection and provides extension point for input-state.
    (input register is read-only, not written in init; see extension.)"""
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
        """Pin mode (2 bits) from MODER (+0x2c): pin N -> bits [2N+1:2N]."""
        return (self.read(port, GPIO_MODER) >> (pin * 2)) & 0x3

    def output(self, port):
        """Value of output/select register +0x10."""
        return self.read(port, GPIO_OUTSEL)

    def config_report(self):
        """{port: {pin: mode}} — only pins with non-zero mode (final state)."""
        rep = {}
        for p in range(self.nports):
            pins = {pin: self.pin_mode(p, pin) for pin in range(16)
                    if self.pin_mode(p, pin)}
            if pins:
                rep[p] = pins
        return rep


# A2: push frames 'a'/'a1' (collector 0x211f8 -> TX ring @0x10b5, frame from 0x10b6).
PUSH_RING_OFF = 0x10B5          # TX ring base
PUSH_FRAME_HDR = 0x61
PUSH_FRAME_TRAILER = 0x9E


def decode_push_frames(data):
    """Parse byte stream into valid push frames `61 [sub] [len] data[len] chk 9E`
    (chk=SUM(bytes before chk)&0xFF). Returns [(raw, sub, fields)]. Pure function —
    works for emulator and live capture alike (ported from probes/mcu_push_decode.py)."""
    out = []
    i, n = 0, len(data)
    while i < n:
        if data[i] != PUSH_FRAME_HDR:
            i += 1
            continue
        if n - i < 3:
            break
        ln = data[i + 2]
        e = i + ln + 5
        if ln > 200 or e > n:
            i += 1
            continue
        if data[e - 1] != PUSH_FRAME_TRAILER or (sum(data[i:e - 2]) & 0xFF) != data[e - 2]:
            i += 1
            continue
        f = bytes(data[i:e])
        sub = f[1]
        if sub == 0x30:      # 'a0' telemetry (LEN=10)
            fields = {'mode': f[3], 'mask': f[5], 'cur_biased': f[6],
                      'abs_i290': f[7], 'status': f[8], 'pct_0x236': (f[9] << 8) | f[10],
                      'flag': f[11], 'bit3_0x244': f[12]}
        elif sub == 0x31:    # 'a1' battery (LEN=9)
            fields = {'v_0x2e6': f[3], 'batt_pct': f[4], 'u16_0x308': (f[5] << 8) | f[6],
                      'u16_0x30a': (f[7] << 8) | f[8], 'temp_c': f[9],
                      'range': (f[10] << 8) | f[11]}
        else:
            fields = {}
        out.append((f, sub, fields))
        i = e
    return out


class UsartTxModel:
    """A2: push-TX pipeline model (ASSEMBLY stage). Runs REAL collector 0x211f8
    (without arguments — reads fixed RAM telemetry fields), reads TX ring @0x10b5,
    and decodes frames via decode_push_frames. Delivery to USART3_DR is performed by a separate
    TX sender (usart_out) — this model simulates frame assembly specifically."""
    def __init__(self, emu):
        self.emu = emu

    def assemble(self, run_off=0x211F8, window=(0x10B0, 0x140)):
        """Run collector with current RAM state -> list of [(raw, sub, fields)]."""
        uc = self.emu.uc

        def _st(uc_, a, s, u):
            aa = a & ~1
            if not (FLASH0 <= aa < FLASH0 + 0x23680 or
                    FLASH1 <= aa < FLASH1 + 0x23680):
                uc_.emu_stop()
        sh = uc.hook_add(UC_HOOK_CODE, _st)
        try:
            uc.reg_write(UC_ARM_REG_SP, STACK_TOP - 0x80)
            uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
            self.emu.insn = 0
            try:
                uc.emu_start(run_off | 1, 0, count=300_000)
            except UcError:
                pass
        finally:
            uc.hook_del(sh)
        lo, size = window
        data = bytes(uc.mem_read(RAM + lo, size))
        return decode_push_frames(data)


# A3: external SPI flash (NVM). SPI1 @0x40013000; NVM <= 4KB (addr validation in 0x221e6).
SPI_FLASH_BASE = 0x40013000   # SPI1 (MOSI/MISO to external flash with NVM)
NVM_SIZE = 0x1000             # ≤4KB

class SpiFlashModel:
    """A3: virtual buffer for external SPI flash (NVM) + set/get. NVM content is
    device runtime data (config/calibration); without live dump, values are unknown ->
    default 0xFF (erased flash), buffer is settable. SPI protocol: write-enable 0x221a4
    (cmd 0x06) + page-program 0x221e6 (addr<0x1000, slot step 4B); NVRAM-save 0x21A08
    persists 7+18B of config. Full modeling of SPI transactions (MISO return) —
    future work: SPI context = struct in RAM (gate [ctx+0x14] bit31), base/state
    needs reconstruction for live."""
    def __init__(self, emu, size=NVM_SIZE):
        self.emu = emu
        self.size = size
        self.flash = bytearray(b'\xff' * size)   # virtual NVM content

    def set(self, addr, data):
        """Write data into NVM at addr (emulates page-program)."""
        if addr < 0 or addr + len(data) > self.size:
            raise ValueError(f'NVM address out of range: {addr}+{len(data)} > {self.size}')
        self.flash[addr:addr + len(data)] = data

    def get(self, addr, n=1):
        """Read n bytes from NVM at addr (emulates read)."""
        return bytes(self.flash[addr:addr + n])

    def seed(self, mapping):
        """Seed NVM with dict of {addr: int_or_bytes} (for tests/simulation)."""
        for addr, val in mapping.items():
            if isinstance(val, (bytes, bytearray)):
                self.set(addr, bytes(val))
            else:
                self.set(addr, val.to_bytes(max(1, (val.bit_length() + 7) // 8), 'little'))


# B1: custom command control block @0x40021000 (u32 fields +0x10/+0x18/+0x1c).
CMD_CTRL_BASE = 0x40021000
CMD_CTRL_FIELDS = (0x10, 0x18, 0x1c)


class CmdControlModel:
    """B1: scoped view into custom control block @0x40021000 — captures set/clear/pulse
    bits in fields +0x10/+0x18/+0x1c (primitives 0xc664/0xc684/0xc6a4; dispatcher 0x2e0c,
    handler 0x97f4). Firmware writes land in memory; model mirrors them for inspecting
    "which control bits were touched by command". Exact ID->bit mapping is resolved via
    command-ID from RX parser (B2) / live."""
    def __init__(self, emu, base=CMD_CTRL_BASE):
        self.emu = emu
        self.base = base
        self.ops = []      # [(pc, offset, value)] writes to block fields
        self._hook = emu.uc.hook_add(UC_HOOK_MEM_WRITE, self._on_w,
                                     None, base, base + 0x40)

    def _on_w(self, uc, access, address, size, value, user):
        self.ops.append((uc.reg_read(UC_ARM_REG_PC) & 0xFFFFF, address - self.base, value))

    def read(self, off):
        return struct.unpack('<I', bytes(self.emu.uc.mem_read(self.base + off, 4)))[0]

    def set(self, off, val):
        self.emu.uc.mem_write(self.base + off, struct.pack('<I', val & 0xFFFFFFFF))


# B2: USART3 RX protocol (BLE->MCU) — ASCII command-IDs. Parser 0x1e9e0 (1914 B).
# 15 commands (ASCII characters), 2 categories:
#   cat=2 (@ G K c)      — response/status commands;
#   cat=0xa (others)     — SET-params (copy [d+2] to [r0+3]).
# RX frame: [+1]=cmd(ASCII), [+2]=len/param, [+3..]=payload. Response frames are built
# with sub 'd'(0x64)/'K'(0x4b) + sum-chk. Field semantics derived from handler addresses.
USART_RX_PARSER = 0x1E9E0
USART_RX_COMMANDS = {
    '@': (0x1EB92, 2,   'complement-param: val=0xFF-[d+?], store [r0+6]'),
    'G': (0x1EBAA, 2,   'response build: [f+1]=5, [f+2]=0x14, sub="K", chk5'),
    'K': (0x1EBDE, 2,   'response build: [f+2]=0x1b, sub="K", chk5'),
    'c': (0x1EC14, 2,   'response build: [f+2]=0x53, sub="K", chk5'),
    'A': (0x1EC74, 0xA, 'multi-param SET (bit-extract lsrs#4/#7/#1f/#1a) + resp "d"/0x20'),
    'B': (0x1ED90, 0xA, 'SET: [d+3..d+8] -> RAM bytes'),
    'C': (0x1EDBA, 0xA, 'SET: [d+3..d+8] -> RAM bytes'),
    'F': (0x1EE86, 0xA, 'variable-length data copy (len=[d+2], <=0x14) -> buffer'),
    'D': (0x1EEB4, 0xA, 'SET with clamps ([d+3]<=0xfe,[d+4]<=0x64) + u16 pairs'),
    'E': (0x1EF08, 0xA, 'bulk u16 SET (6 pairs from [d+3..d+0xf])'),
    'H': (0x1EF58, 0xA, 'SET 4B + resp "d"/0x2c len=4'),
    'I': (0x1EFC8, 0xA, 'variable-length copy + resp 0x2e'),
    'J': (0x1F036, 0xA, 'variable-length copy + resp 0x2f'),
    '`': (0x1F0CA, 0xA, 'variable-length copy + resp "d"/0x50'),
    'a': (0x1F112, 0xA, 'variable-length copy + resp "d"/0x51'),
}


def usart_rx_cmd(cmd_byte):
    """B2: identify USART3-RX command by byte (ASCII). Returns
    (handler_off, cat, desc) or None for unknown cmd."""
    if isinstance(cmd_byte, int):
        cmd_byte = chr(cmd_byte)
    return USART_RX_COMMANDS.get(cmd_byte)


# C1: LUT blocks of range estimator 0x1d898 (u32 words, step 4; values from NVM/live).
RANGE_LUT0_OFF = 0x614    # block0: 0x614..0x6c4
RANGE_LUT0_WORDS = 45
RANGE_LUT1_OFF = 0x738    # block1: 0x738..0x808
RANGE_LUT1_WORDS = 53
RANGE_FLAG_OFFS = (0x286, 0x290, 0x294, 0x29e, 0x2a8, 0x2ac)   # status gates (§73.13)


class LutModel:
    """C1: scoped view onto range estimator LUT blocks @RAM+0x614 / RAM+0x738 (u32 words,
    step 4). Captures firmware READS (which offsets 0x1d898 scanned), seed/get for
    synthetic/live values. Real values come from NVM (live dump); default 0. 0x1d898
    scans both blocks, reading each word once (table traversal)."""
    def __init__(self, emu):
        self.emu = emu
        self.reads = set()   # RAM-relative offsets read by firmware
        self._hooks = []
        for off, words in ((RANGE_LUT0_OFF, RANGE_LUT0_WORDS),
                           (RANGE_LUT1_OFF, RANGE_LUT1_WORDS)):
            h = emu.uc.hook_add(UC_HOOK_MEM_READ, self._on_r,
                                None, RAM + off, RAM + off + words * 4)
            self._hooks.append(h)

    def _on_r(self, uc, access, address, size, value, user):
        self.reads.add(address - RAM)

    def get_word(self, off):
        return struct.unpack('<I', bytes(self.emu.uc.mem_read(RAM + off, 4)))[0]

    def set_word(self, off, val):
        self.emu.uc.mem_write(RAM + off, struct.pack('<I', val & 0xFFFFFFFF))

    def seed_block(self, off, words):
        """words: list[int] (or int = constant across entire block)."""
        if isinstance(words, int):
            words = [words]
        for i, w in enumerate(words):
            self.set_word(off + i * 4, w)

    def scanned(self, off, words):
        """True if firmware read all words of block @off."""
        return all((off + i * 4) in self.reads for i in range(words))


# C2: FOC routine 0x1a938 — value-gated pipeline (not discrete FSM).
FOC_ROUTINE = 0x1A938
FOC_REF_OFF = 0x224        # u16 current-reference (upstream input)
FOC_P_OFF = 0x388          # u32 P = [ref] (1:1, §73.15)
FOC_PHASE_OFFS = (0x382, 0x384, 0x386)   # u16 PWM phases (final FOC output)
FOC_PHASE_CENTER = 1125    # center (idle): all phases = 1125


class FocPipelineModel:
    """C2: scoped view onto FOC routine 0x1a938 as value-gated pipeline (TIM capture ->
    cross/dot -> inline -> fixed-point -> 2D rotate -> sector -> PWM). NOT a discrete FSM:
    branches on values (currents/thresholds), not state register (§60.3; single byte
    flags do not alter path). Captures OUTPUTS (P@0x388, PWM phases @0x382/4/6); seed for
    current-ref @0x224. Transfer: phases = 1125 +/- ~0.0103*|ref| (2-phase split, §73.14)."""
    def __init__(self, emu):
        self.emu = emu
        self.writes = {}   # RAM-off -> last value
        lo, hi = FOC_P_OFF - 0x10, max(FOC_PHASE_OFFS) + 8
        self._h = emu.uc.hook_add(UC_HOOK_MEM_WRITE, self._on_w,
                                  None, RAM + lo, RAM + hi)

    def _on_w(self, uc, access, address, size, value, user):
        self.writes[address - RAM] = value

    def set_ref(self, v):
        self.emu.uc.mem_write(RAM + FOC_REF_OFF, struct.pack('<H', v & 0xFFFF))

    def get_p(self):
        return struct.unpack('<I', bytes(self.emu.uc.mem_read(RAM + FOC_P_OFF, 4)))[0]

    def get_phases(self):
        return tuple(struct.unpack('<H', bytes(self.emu.uc.mem_read(RAM + o, 2)))[0]
                     for o in FOC_PHASE_OFFS)


# D1: main-loop dispatcher 0x1f600 — round-robin across N slots (ceiling §74.1).
SCHEDULER_FN = 0x1F600
SCHED_SLOT_INDEX_OFF = 0x2C2   # byte current slot (wrap 0..3)
SCHED_SLOT_TABLE_OFF = 0xA43   # base of slot-descriptors, stride 0x96 (§74)
SCHED_SLOT_STRIDE = 0x96
SCHED_N_SLOTS = 4
SCHED_TICK_WORDS_OFF = 0x17F78   # u32 words tick/last (empirical D1)


class SchedulerModel:
    """D1: scoped view onto main-loop dispatcher 0x1f600 (round-robin across N slots). Captures
    READS/WRITES of state (slot_index @0x2C2, slot-table @0xA43 stride 0x96, tick-words
    @0x17F78+); seed for slot_index. **LIMITATION §74.1:** task function pointers reside in runtime
    RAM (set during init); in zero RAM dispatch hits unmapped fetch (jump to 0) BEFORE
    completing rotation, because 0x1f600 reads byte from slot-descriptor and calls 0x1f1c0
    (store-byte), while execution is detached and requires runtime pointers."""
    def __init__(self, emu):
        self.emu = emu
        self.reads = set()   # RAM-relative offsets read
        self.writes = {}     # RAM-off -> last value
        self._hr = emu.uc.hook_add(UC_HOOK_MEM_READ, self._on_r,
                                   None, RAM, RAM + 0x20000)
        self._hw = emu.uc.hook_add(UC_HOOK_MEM_WRITE, self._on_w,
                                   None, RAM, RAM + 0x20000)

    def _on_r(self, uc, access, address, size, value, user):
        if RAM <= address < RAM + 0x20000:
            self.reads.add(address - RAM)

    def _on_w(self, uc, access, address, size, value, user):
        if RAM <= address < RAM + 0x20000:
            self.writes[address - RAM] = value

    def set_slot_index(self, v):
        self.emu.uc.mem_write(RAM + SCHED_SLOT_INDEX_OFF, bytes([v & 0xFF]))

    def get_slot_index(self):
        return bytes(self.emu.uc.mem_read(RAM + SCHED_SLOT_INDEX_OFF, 1))[0]

    def touched(self, off):
        """True if dispatcher read or wrote offset @off."""
        return off in self.reads or off in self.writes


class ControlLoop:
    """§74 Autonomous motor loop — time-driven warm-start.

    Virtual clock + real firmware PID/FOC on each tick + behavioral models of
    plant/speed/battery/range. NOT a boot-from-reset and NOT a complete scheduler (slot-table
    is populated at runtime, boot-blocked §73.15) — PID/FOC are invoked directly at their
    actual rates (valid control loop abstraction: speed controller -> torque -> FOC).

    Tick pipeline:
      measured_speed -> SpeedModel.set_speed (V)          [PID input]
      target -> PID 0x1d078 -> throttle s16[RAM+0x42c]     [real firmware]
      throttle -> current-ref u16[RAM+0x224] -> FOC 0x1a938 -> PWM CCR  [real firmware]
      throttle → MotorModel.step → speed                 [plant, first-order lag]
      throttle -> BatteryModel.discharge -> SoC            [battery discharge]
      SoC -> RangeModel.estimate -> remaining range        [closed-form]
    """
    def __init__(self, emu=None, v_max=522.0, tau=15.0, throttle_ref=28624.0,
                 batt_rate=0.05, run_foc=True):
        # throttle_ref = full-scale PID output (0x42c ~28624..32760), NOT 4000 (§73.9 default
        # caused plant saturation: speed diverged to v_max instead of converging to target).
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
        """Seed RAM: mode, target, power-enable, gates, battery (see §73.9-73.15)."""
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
        """Real PID 0x1d078 -> throttle s16[RAM+0x42c]."""
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
        """Real FOC 0x1a938 (R4=RAM+0x040, ref=u16[RAM+0x224]) -> PWM CCR."""
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
        """Single loop step. Returns state dict."""
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
        v_batt = BatteryModel._raw(int(soc))           # SoC -> raw [415..535]
        X, R = self.rm.estimate(v_batt)                # range estimation (closed-form)
        self.now += 1
        return dict(t=self.now, speed=round(self.mm.speed, 1), throttle=thr,
                    pwm_amp=round(amp, 1), soc=round(soc, 2), range=R)

    def run(self, ticks):
        """Run ticks steps. Returns list of states."""
        return [self.tick() for _ in range(ticks)]


def find_func_starts():
    """Function entries = push {..,lr} (0xB5xx) prologue in code sections."""
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
    """Run each function and identify those writing to descriptor region.
    Dynamic taint analysis — uncovers runtime base pointers absent in static code."""
    starts = find_func_starts()
    print(f"[sweep] functions: {len(starts)}, searching writes to 0x{target_lo:08x}..0x{target_hi:08x}")
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
    print(f"\n[sweep] functions writing to descriptor region: {len(hits)}")
    for addr, recs in sorted(hits.items(), key=lambda kv: -len(kv[1]))[:25]:
        addrs = sorted(set(r[1] for r in recs))
        print(f"  func 0x{addr:05x}: {len(recs)} writes, addresses "
              f"{[hex(a) for a in addrs[:8]]}{' …' if len(addrs) > 8 else ''}")
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--func", default="0x1f600")
    ap.add_argument("--max", type=int, default=200000)
    ap.add_argument("--trace", action="store_true")
    ap.add_argument("--seed-desc", action="store_true",
                    help="seed descriptors with markers 0xA0..0xAF")
    ap.add_argument("--seed-sched", action="store_true",
                    help="set up preconditions for scheduler 0x1f600")
    ap.add_argument("--find-writers", action="store_true",
                    help="sweep all functions to find descriptor writers")
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
