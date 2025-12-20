from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

from gso_app.gui import launch_gui
from gso_app.paths import ensure_data_dir, resolve_config_path, resolve_logs_dir


def _redirect_output(logs_dir: Path) -> None:
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_path = logs_dir / f"launch-{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"
    log_file = log_path.open("a", encoding="utf-8")
    sys.stdout = log_file
    sys.stderr = log_file


def main() -> int:
    ensure_data_dir()
    _redirect_output(resolve_logs_dir())
    return launch_gui(config_path=resolve_config_path())


if __name__ == "__main__":
    raise SystemExit(main())
