from __future__ import annotations

from gso_app.gui import launch_gui
from gso_app.paths import ensure_data_dir, resolve_config_path


def main() -> int:
    ensure_data_dir()
    return launch_gui(config_path=resolve_config_path())


if __name__ == "__main__":
    raise SystemExit(main())
