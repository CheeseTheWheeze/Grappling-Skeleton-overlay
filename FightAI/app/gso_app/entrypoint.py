from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path
import traceback

from gso_app.paths import ensure_data_dir, resolve_config_path, resolve_logs_dir


def _redirect_output(logs_dir: Path) -> None:
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_path = logs_dir / f"launch-{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"
    log_file = log_path.open("a", encoding="utf-8")
    sys.stdout = log_file
    sys.stderr = log_file


def _show_error_dialog(title: str, message: str) -> None:
    if sys.platform.startswith("win"):
        try:
            import ctypes

            ctypes.windll.user32.MessageBoxW(0, message, title, 0x10)
            return
        except Exception:
            pass
    print(f"{title}: {message}", file=sys.stderr)


def main() -> int:
    ensure_data_dir()
    _redirect_output(resolve_logs_dir())
    try:
        from gso_app.gui import launch_gui
    except Exception as exc:
        _show_error_dialog(
            "FightAI Launcher Error",
            "The GUI failed to start. This usually means the embedded Python\n"
            "runtime is missing Tkinter.\n\n"
            "Run FightAI\\\\setup_python.ps1 to install the embedded runtime,\n"
            "or install Python 3.10+ with Tkinter support.\n\n"
            f"Details: {exc}",
        )
        traceback.print_exc()
        return 1
    return launch_gui(config_path=resolve_config_path())


if __name__ == "__main__":
    raise SystemExit(main())
