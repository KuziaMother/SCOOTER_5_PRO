# -*- coding: utf-8 -*-
"""§73.x FOC-интеграция в автономный контур.

Полная цепочка прошивки на каждом шаге (один McuEmu, общий RAM — как на реальном MCU):
  target → PID 0x1d078 → throttle s16[RAM+0x42c]
        → current-ref u16[RAM+0x224] = throttle   (связь найдена эмпирически, §73.x)
        → FOC 0x1a938 (R4=RAM+0x040) → PWM CCR (RAM+0x382/384/386 → 0x40012c44/48/4c)
        → plant(throttle→speed, first-order lag) → SpeedModel(speed→V) → PID ...

FOC в контуре доказывает: реальный FOC исполняется каждый шаг и даёт throttle-коррелированный
PWM (amp ≈ 0.0103·|ref|, center≈1125). Plant абстрагирует МЕХАНИЧЕСКИЙ отклик мотора на ток;
электрический контур (токи→back-EMF) не live-калиброван → не моделируется явно.
"""
import os, struct, sys
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)                                   # func_verify
sys.path.insert(0, os.path.join(_HERE, '..', '..', '..'))   # repo root: emulator
from emulator.mcu_emu import McuEmu, SpeedModel, FLASH0, FLASH1, RAM, STACK_TOP
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (UC_ARM_REG_R0, UC_ARM_REG_R4, UC_ARM_REG_SP, UC_ARM_REG_LR)

FW_LEN = 0x25000


def run_foc(emu, current_ref):
    """Запустить FOC 0x1a938 с current-ref в u16[RAM+0x224]. Возвращает (ccr_a,ccr_b,ccr_c)."""
    uc = emu.uc
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
    ccr = [struct.unpack('<H', uc.mem_read(RAM + o, 2))[0] for o in (0x382, 0x384, 0x386)]
    return tuple(ccr)


def run_pid(emu):
    """Запустить PID 0x1d078. Возвращает throttle s16[RAM+0x42c]."""
    uc = emu.uc
    def stop(uc_, a, s, u):
        aa = a & ~1
        if not (0 <= aa < FW_LEN or FLASH0 <= aa < FLASH0 + FW_LEN or FLASH1 <= aa < FLASH1 + FW_LEN):
            uc_.emu_stop()
    sh = uc.hook_add(UC_HOOK_CODE, stop)
    uc.reg_write(UC_ARM_REG_SP, STACK_TOP - 0x80)
    uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
    for r in (UC_ARM_REG_R0, UC_ARM_REG_R4):
        uc.reg_write(r, 0)
    try:
        uc.emu_start(0x1D078 | 1, 0, count=400000)
    except Exception:
        pass
    uc.hook_del(sh)
    return struct.unpack('<h', uc.mem_read(RAM + 0x42c, 2))[0]


def run_loop(target, v_max=522.0, tau=15.0, tref=28624.0, iters=40, speed0=0.0):
    emu = McuEmu(max_insn=400000)
    uc = emu.uc
    sm = SpeedModel(emu)
    uc.mem_write(RAM, bytes(0x20000))
    uc.mem_write(RAM + 0x229, bytes([3]))                     # mode 3
    uc.mem_write(RAM + 0x326, struct.pack('<H', target))      # target
    uc.mem_write(RAM + 0x339, b'\x00')
    uc.mem_write(RAM + 0x333, b'\x00')                        # skip mode-change block
    uc.mem_write(RAM + 0x263, b'\x00')                        # gate → ramp-core
    uc.mem_write(RAM + 0x1760, struct.pack('<I', 32760))      # u1760 = power enable
    uc.mem_write(RAM + 0x1764, struct.pack('<I', 0))
    uc.mem_write(RAM + 0x388, struct.pack('<I', 0))
    uc.mem_write(RAM + 0x3C8 + 0x28, struct.pack('<H', 1))    # counter → phase B
    speed = speed0
    traj = []
    for it in range(iters):
        sm.set_speed(int(speed))                              # speed → V (вход PID)
        thr = run_pid(emu)                                    # PID (реальный) → throttle
        ccr = run_foc(emu, thr & 0xFFFF)                      # FOC (реальный) → PWM
        center = sum(ccr) / 3.0
        amp = max(abs(c - center) for c in ccr)
        # plant: first-order lag к терминальной скорости для текущего throttle
        tnorm = max(0.0, min(1.0, thr / tref)) if tref else 0.0
        v_term = v_max * tnorm
        speed += (1.0 / tau) * (v_term - speed)
        if speed < 0:
            speed = 0.0
        traj.append((it, round(speed, 1), thr, round(amp, 1)))
    return traj


def main():
    for target in (208, 300):
        print(f'=== target={target} (FOC в контуре) ===')
        traj = run_loop(target, iters=40)
        print('  it   speed  throttle  FOC-amp')
        for it, sp, thr, amp in traj:
            if it % 2 == 0 or it >= len(traj) - 3:
                print(f'  {it:2d}  {sp:8.1f}  {thr:8d}  {amp:7.1f}')
        last = traj[-1]
        print(f'  -> speed={last[1]} (target {target}), thr={last[2]}, FOC-amp={last[3]}')


if __name__ == '__main__':
    main()
