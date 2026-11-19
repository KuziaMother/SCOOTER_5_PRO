# ruff: noqa: F405
"""§94 (Phase ②): main-loop tick-harness — виртуальное время + реальный планировщик.

MainLoopHarness (emulator/mcu_emu.py): виртуальные часы (u64 "now" @0x1E0) +
реальный планировщик 0x1f600 на каждый tick + опц. комм-тик 0x1dfd8.
**Контракт планировщика (live verified):** elapsed = now − last (u64 @0x198);
  elapsed <= 432 → idle (ранний return); elapsed > 432 И tail != head →
  **main-путь**: slot_idx(tail)++, last := now; tail==head → стоп (кольцо 4 слота,
  head@0x2C1 продюсер / tail@0x2C2 потребитель). cap < slot_counter+1 → overflow
  (межбайтовый 8-тик). Это расширяет автономный прогон с ~45% (ControlLoop PID+FOC)
  к реальному main-loop на виртуальном времени (НЕ cold-boot — §74.1 потолок).
"""

from fv_core import *  # noqa: F401,F403
from emulator.mcu_emu import MainLoopHarness, SCHED_PERIOD  # noqa: E402


@t(0x1F600, 'Phase② §94: MainLoopHarness — контракт планировщика: 432 тика → 0 dispatch (elapsed<=432 → idle); 433 тика → 1 dispatch (t=433, tail 0→1, last→433); head=2/870 тиков → 2 dispatch (t=433 slot→1, t=866 slot→2, tail==head→стоп). Период = 432 тика (межслотовый)')
def _(run, rng):
    """Emulator test @ 0x1f600: Phase② §94: MainLoopHarness — контракт планировщика: 432 тика → 0 dispatch (elapsed<=432 → idle); 433 тика → 1 dispatch (t=433, tail 0→1, last→433); head=2/870 тиков → 2 dispatch (t=433 slot→1, t=866 slot→2, tail==head→стоп). Период = 432 тика (межслотовый).
    Тест эмулятора @ 0x1f600: Phase② §94: MainLoopHarness — контракт планировщика: 432 тика → 0 dispatch (elapsed<=432 → idle); 433 тика → 1 dispatch (t=433, tail 0→1, last→433); head=2/870 тиков → 2 dispatch (t=433 slot→1, t=866 slot→2, tail==head→стоп). Период = 432 тика (межслотовый).
    """
    assert SCHED_PERIOD == 432
    # 432 тика → нет dispatch
    h = MainLoopHarness(cap=1, run_comm=False)
    h.reset(now=0, head=1)
    states = h.run(432)
    assert h.dispatches == 0, f"432 тика: dispatches={h.dispatches} ждём 0"
    assert all(s['sched'] == 'idle' for s in states), 'все 432 тика должны быть idle'
    # 433 тика → 1 dispatch при t=433
    h2 = MainLoopHarness(cap=1, run_comm=False)
    h2.reset(now=0, head=1)
    st = h2.run(433)
    mains = [s for s in st if s['sched'] == 'main']
    assert len(mains) == 1, f"433 тика: {len(mains)} dispatch ждём 1"
    assert mains[0]['t'] == 433, f"dispatch t={mains[0]['t']} ждём 433"
    assert mains[0]['slot_idx'] == 1, f"slot_idx={mains[0]['slot_idx']} ждём 1"
    assert mains[0]['last'] == 433, f"last={mains[0]['last']} ждём 433"
    # head=2 → 2 dispatch (t=433, t=866), tail→2==head
    h3 = MainLoopHarness(cap=1, run_comm=False)
    h3.reset(now=0, head=2)
    st3 = h3.run(870)
    mains3 = [s for s in st3 if s['sched'] == 'main']
    assert len(mains3) == 2, f"head=2: {len(mains3)} dispatch ждём 2"
    assert mains3[0]['t'] == 433 and mains3[1]['t'] == 866, \
        f"dispatch t={[m['t'] for m in mains3]} ждём [433, 866]"
    assert h3.dispatches == 2 and h3._read_slot_idx() == 2


@t(0x1DFD8, 'Phase② §94: MainLoopHarness + комм-тик 0x1dfd8 — run_comm=True: harness на 1200 тиков (comm_period=1000 → комм-тик при t=1000) не падает, comm_ticks инкрементится, планировщик диспатчит (t=433). Автономный прогон main-loop (scheduler + комм-тик) на виртуальном времени')
def _(run, rng):
    """Emulator test @ 0x1dfd8: Phase② §94: MainLoopHarness + комм-тик 0x1dfd8 — run_comm=True: harness на 1200 тиков (comm_period=1000 → комм-тик при t=1000) не падает, comm_ticks инкрементится, планировщик диспатчит (t=433). Автономный прогон main-loop (scheduler + комм-тик) на виртуальном времени.
    Тест эмулятора @ 0x1dfd8: Phase② §94: MainLoopHarness + комм-тик 0x1dfd8 — run_comm=True: harness на 1200 тиков (comm_period=1000 → комм-тик при t=1000) не падает, comm_ticks инкрементится, планировщик диспатчит (t=433). Автономный прогон main-loop (scheduler + комм-тик) на виртуальном времени.
    """
    h = MainLoopHarness(cap=1, run_comm=True, comm_period=1000)
    h.reset(now=0, head=1)
    states = h.run(1200)
    assert h.comm_ticks == 1, f"comm_ticks={h.comm_ticks} ждём 1 (t=1000)"
    assert h.dispatches >= 1, f"dispatches={h.dispatches} ждём >=1"
    mains = [s for s in states if s['sched'] == 'main']
    assert mains and mains[0]['t'] == 433, f"первый dispatch t={[m['t'] for m in mains]}"
    # последний тик валиден (harness не сломан)
    assert states[-1]['t'] == 1200


@t(0x1A2A4, 'Phase② §94: FOC-ISR по timer-update — MainLoopHarness.run_foc: 0x1a2a4 (реальный TIM1-IRQ) на каждый timer-update. Контракт: bit7 [TIM1+0x1C]=update-событие (lsls #0x18=<<24 тестит bit7); bit7 set → handler-путь (~39 insn: clear flag, set bit7 [base+0x20]); bit7 clr → быстрый return (6 insn). harness: foc_period=10/100 тиков → foc_runs=10, foc_handler=10. **Коррекция:** 0x7875 НЕ ISR-entry в образе (нет полной векторной таблицы, OTA; 0x7875 = середина state-machine блока, изоляция уходит в 0x7992); реальный TIM1-IRQ = 0x1a2a4')
def _(run, rng):
    # FOC-ISR через harness: foc_period=10 → 10 runs за 100 тиков
    """Emulator test @ 0x1a2a4: Phase② §94: FOC-ISR по timer-update — MainLoopHarness.run_foc: 0x1a2a4 (реальный TIM1-IRQ) на каждый timer-update. Контракт: bit7 [TIM1+0x1C]=update-событие (lsls #0x18=<<24 тестит bit7); bit7 set → handler-путь (~39 insn: clear flag, set bit7 [base+0x20]); bit7 clr → быстрый return (6 insn). harness: foc_period=10/100 тиков → foc_runs=10, foc_handler=10. **Коррекция:** 0x7875 НЕ ISR-entry в образе (нет полной векторной таблицы, OTA; 0x7875 = середина state-machine блока, изоляция уходит в 0x7992); реальный TIM1-IRQ = 0x1a2a4.
    Тест эмулятора @ 0x1a2a4: Phase② §94: FOC-ISR по timer-update — MainLoopHarness.run_foc: 0x1a2a4 (реальный TIM1-IRQ) на каждый timer-update. Контракт: bit7 [TIM1+0x1C]=update-событие (lsls #0x18=<<24 тестит bit7); bit7 set → handler-путь (~39 insn: clear flag, set bit7 [base+0x20]); bit7 clr → быстрый return (6 insn). harness: foc_period=10/100 тиков → foc_runs=10, foc_handler=10. **Коррекция:** 0x7875 НЕ ISR-entry в образе (нет полной векторной таблицы, OTA; 0x7875 = середина state-machine блока, изоляция уходит в 0x7992); реальный TIM1-IRQ = 0x1a2a4.
    """
    h = MainLoopHarness(cap=1, run_comm=False, run_foc=True, foc_period=10)
    h.reset(now=0, head=1)
    h.run(100)
    assert h.foc_runs == 10, f"foc_runs={h.foc_runs} ждём 10 (100/10)"
    assert h.foc_handler == 10, f"foc_handler={h.foc_handler} ждём 10 (bit7 set → handler)"
    # foc_period=1 → каждый тик
    h2 = MainLoopHarness(cap=1, run_comm=False, run_foc=True, foc_period=1)
    h2.reset(now=0, head=1)
    h2.run(20)
    assert h2.foc_runs == 20 and h2.foc_handler == 20
    # run_foc=False → 0 runs
    h3 = MainLoopHarness(cap=1, run_comm=False, run_foc=False)
    h3.reset(now=0, head=1)
    h3.run(20)
    assert h3.foc_runs == 0, f"run_foc=False: foc_runs={h3.foc_runs} ждём 0"
