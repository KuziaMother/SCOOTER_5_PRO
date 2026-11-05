#!/usr/bin/env python3
"""
Compatibility launcher: legacy entry point `python probes/spec_listen_web.py` now
starts the modular web UI from `webui/app.py` (see `webui/README.md`).
Legacy monolithic implementation (frames/baseline/live endpoints)
is replaced by the read-only dashboard in webui/app.py — same port 8321.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "webui"))

from app import main

if __name__ == "__main__":
    main()
