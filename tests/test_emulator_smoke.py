"""Integration smoke test: runs emulator/run_emulator.py in full —
all 7 scenarios against REAL dreame_auth.py/dreame_flasher.py/probes/spec_read.py,
without BLE and without a physical device (see emulator/README.md). Longest test in
the suite (channel 18-byte frame reassembly is paced, ~2-3 minutes) — this is
the end-to-end check ensuring protocol is not broken after changes."""
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

    assert proc.returncode == 0, f"emulator crashed with code {proc.returncode}:\n{out[-3000:]}"
    assert "Traceback" not in out, f"unhandled exception in run:\n{out[-3000:]}"

    results = [ln for ln in out.splitlines() if ln.startswith("RESULT")]
    assert len(results) == 7, f"expected 7 RESULT lines, got {len(results)}:\n{out[-3000:]}"
    failed = [ln for ln in results if "❌" in ln]
    assert not failed, "failed scenarios:\n" + "\n".join(failed)
