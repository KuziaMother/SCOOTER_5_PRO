#!/usr/bin/env python3
"""
Совместимый launcher: старый вход `python probes/spec_listen_web.py` теперь
запускает модульный web UI из `webui/app.py` (см. `webui/README` в todo.md
раздел A0). Старая монолитная реализация (frames/baseline/live-эндпоинты)
заменена read-only dashboard'ом webui/app.py — тот же порт 8321.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "webui"))

from app import main  # noqa: E402

if __name__ == "__main__":
    main()
