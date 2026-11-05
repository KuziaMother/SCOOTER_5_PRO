# -*- coding: utf-8 -*-
"""§73.x motor dynamics: experimental closed-loop sim.

target → PID 0x1d078 → throttle(u16[RAM+0x42c]) → plant(throttle→speed) →
SpeedModel(speed->V) -> PID ...  Find plant parameters where speed
converges to target.
"""
import os, struct, sys
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)                                   # func_verify
sys.path.insert(0, os.path.join(_HERE, '..', '..', '..'))   # repo root: emulator
from emulator.mcu_emu import McuEmu, SpeedModel, RAM
from func_verify import Run, _s16, _sdiv


def s16u(x):
    return x & 0xFFFF


def run_loop(target, v_max, tau, throttle_ref, iters=40, speed0=0.0):
    run = Run()
    sm = SpeedModel(run.emu)
    uc = run.uc
    # initial state: target (mode=3 -> u16[RAM+0x326]), ramp-core gates, zero integrators
    uc.mem_write(RAM, bytes(0x20000))
    uc.mem_write(RAM + 0x229, bytes([3]))
    uc.mem_write(RAM + 0x326, struct.pack('<H', target))
    uc.mem_write(RAM + 0x339, b'\x00')
    uc.mem_write(RAM + 0x333, b'\x00')          # skip mode-change block
    uc.mem_write(RAM + 0x263, b'\x00')          # gate → ramp-core
    uc.mem_write(RAM + 0x1760, struct.pack('<I', 32760))  # u1760=power enabled (not reset)
    uc.mem_write(RAM + 0x1764, struct.pack('<I', 0))
    uc.mem_write(RAM + 0x388, struct.pack('<I', 0))
    uc.mem_write(RAM + 0x224, struct.pack('<I', 0))
    uc.mem_write(RAM + 0x3C8 + 0x28, struct.pack('<H', 1))  # counter → ramp-core
    speed = speed0
    traj = []
    for it in range(iters):
        sm.set_speed(int(speed))
        run.call(0x1D078, (), max_insn=400000)
        thr = struct.unpack('<h', uc.mem_read(RAM + 0x42c, 2))[0]
        cnt = struct.unpack('<H', uc.mem_read(RAM + 0x3C8 + 0x28, 2))[0]
        # plant: first-order lag to terminal speed for current throttle
        tnorm = max(0.0, min(1.0, thr / throttle_ref)) if throttle_ref else 0.0
        v_term = v_max * tnorm
        speed += (1.0 / tau) * (v_term - speed)
        if speed < 0:
            speed = 0.0
        traj.append((it, round(speed, 1), thr, cnt))
    return traj


def main():
    for target in (208,):
        print(f'=== target={target} ===')
        for (v_max, tau, tref) in [(520, 15.0, 4000), (520, 25.0, 4000),
                                   (520, 40.0, 6000), (300, 20.0, 3000)]:
            traj = run_loop(target, v_max, tau, tref, iters=30)
            last = traj[-1]
            print(f'v_max={v_max} tau={tau} tref={tref}: '
                  f'speed: {traj[0][1]} -> {traj[len(traj)//2][1]} -> {last[1]} '
                  f'(target {target}); thr_last={last[2]}')
        # detailed trajectory for best set
        traj = run_loop(target, 520, 15.0, 4000, iters=40)
        print('detailed (v_max=520 tau=15 tref=4000):')
        for it, sp, thr, cnt in traj:
            print(f'  it={it:2d} speed={sp:8.1f} throttle={thr:6d} cnt={cnt}')


if __name__ == '__main__':
    main()
