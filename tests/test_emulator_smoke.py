"""Интеграционный smoke-тест: прогоняет emulator/run_emulator.py целиком —
все 7 сценариев против НАСТОЯЩИХ dreame_auth.py/dreame_flasher.py/probes/spec_read.py,
без BLE и без живого устройства (см. emulator/README.md). Самый долгий тест в
пакете (реассемблинг канальных 18-байтных кадров пейсится, ~2-3 минуты) — это
единственная сквозная проверка, что протокол не сломан после правок."""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_run_emulator_all_scenarios_pass():
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    proc = subprocess.run(
        [sys.executable, os.path.join(ROOT, "emulator", "run_emulator.py")],
        cwd=ROOT, env=env, capture_output=True, text=True, encoding="utf-8",
        errors="replace", timeout=300,
    )
    out = proc.stdout + proc.stderr

    assert proc.returncode == 0, f"эмулятор упал с кодом {proc.returncode}:\n{out[-3000:]}"
    assert "Traceback" not in out, f"необработанное исключение в прогоне:\n{out[-3000:]}"

    results = [ln for ln in out.splitlines() if ln.startswith("РЕЗУЛЬТАТ")]
    assert len(results) == 7, f"ожидалось 7 строк РЕЗУЛЬТАТ, получено {len(results)}:\n{out[-3000:]}"
    failed = [ln for ln in results if "❌" in ln]
    assert not failed, "провалившиеся сценарии:\n" + "\n".join(failed)
