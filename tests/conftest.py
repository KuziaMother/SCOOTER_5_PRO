"""Shared sys.path for tests — project modules are not packaged as a single module
(project convention: scripts prepend root and subfolders to sys.path on launch),
so required directories are injected once here."""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _p in (ROOT, os.path.join(ROOT, "core"), os.path.join(ROOT, "probes"),
           os.path.join(ROOT, "webui"), os.path.join(ROOT, "emulator"),
           os.path.join(ROOT, "research", "scripts", "ble")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
