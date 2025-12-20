from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Iterable

from gso_app.paths import resolve_data_dir

DEFAULT_MIN_PYTHON = (3, 9)
DEFAULT_CONFIG_DIR = resolve_data_dir()
DEFAULT_REQUIREMENTS_PATH = Path(__file__).resolve().parents[2] / "requirements.txt"
DEFAULT_DESKTOP_DIR = Path.home() / "Desktop"
DEFAULT_DESKTOP_ENTRY_NAME = "GSO Analyzer"
DEFAULT_WHEELHOUSE_DIR = Path(__file__).resolve().parents[2] / "vendor" / "wheels"


def _format_version(version: Iterable[int]) -> str:
    return ".".join(str(part) for part in version)


def verify_python_version(min_version: tuple[int, int] = DEFAULT_MIN_PYTHON) -> None:
    current = sys.version_info[:2]
    if current < min_version:
        raise RuntimeError(
            "Python {required}+ is required. Detected {current}.".format(
                required=_format_version(min_version),
                current=_format_version(current),
            )
        )


def install_requirements(
    requirements_path: Path = DEFAULT_REQUIREMENTS_PATH,
    python_executable: str | None = None,
) -> None:
    if not requirements_path.exists():
        raise RuntimeError(f"Requirements file not found: {requirements_path}")
    requirements_text = requirements_path.read_text(encoding="utf-8").strip()
    if not requirements_text:
        return
    python_executable = python_executable or sys.executable
    command = [
        python_executable,
        "-m",
        "pip",
        "install",
        "--no-index",
        "-r",
        str(requirements_path),
    ]
    if DEFAULT_WHEELHOUSE_DIR.exists():
        command.extend(["--find-links", str(DEFAULT_WHEELHOUSE_DIR)])
    result = subprocess.run(command, check=False)
    if result.returncode != 0:
        raise RuntimeError(
            "Requirement installation failed. Command: "
            + " ".join(command)
        )


def _resolve_desktop_dir() -> Path | None:
    xdg_dirs = Path.home() / ".config" / "user-dirs.dirs"
    if xdg_dirs.exists():
        for line in xdg_dirs.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped.startswith("XDG_DESKTOP_DIR"):
                continue
            _, _, value = stripped.partition("=")
            value = value.strip().strip('"')
            value = os.path.expandvars(value.replace("$HOME", str(Path.home())))
            candidate = Path(value).expanduser()
            return candidate
    return DEFAULT_DESKTOP_DIR


def _next_available_path(directory: Path, stem: str, suffix: str) -> Path:
    candidate = directory / f"{stem}{suffix}"
    if not candidate.exists():
        return candidate
    counter = 2
    while True:
        candidate = directory / f"{stem} ({counter}){suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def create_desktop_launcher(
    *,
    config_dir: Path = DEFAULT_CONFIG_DIR,
    requirements_path: Path = DEFAULT_REQUIREMENTS_PATH,
    python_executable: str | None = None,
) -> Path | None:
    desktop_dir = _resolve_desktop_dir()
    if desktop_dir is None:
        return None
    desktop_dir.mkdir(parents=True, exist_ok=True)
    config_dir.mkdir(parents=True, exist_ok=True)

    python_executable = python_executable or sys.executable
    launcher_script = config_dir / "gso_gui_launcher.py"
    launcher_contents = "\n".join(
        [
            f"#!{python_executable}",
            "from __future__ import annotations",
            "",
            "import sys",
            "from pathlib import Path",
            "",
            "from gso_app import cli",
            "from gso_app.gui import launch_gui",
            "",
            "def main() -> int:",
            f"    requirements_path = Path(r\"{requirements_path}\")",
            f"    config_dir = Path(r\"{config_dir}\")",
            "    exit_code = cli.run_install(requirements_path, config_dir)",
            "    if exit_code != 0:",
            "        return exit_code",
            "    return launch_gui()",
            "",
            "if __name__ == \"__main__\":",
            "    raise SystemExit(main())",
            "",
        ]
    )
    launcher_script.write_text(launcher_contents, encoding="utf-8")
    launcher_script.chmod(0o755)

    desktop_entry_path = _next_available_path(
        desktop_dir,
        DEFAULT_DESKTOP_ENTRY_NAME,
        ".desktop",
    )
    desktop_entry_name = desktop_entry_path.stem
    desktop_entry_contents = "\n".join(
        [
            "[Desktop Entry]",
            "Type=Application",
            f"Name={desktop_entry_name}",
            f"Exec={launcher_script}",
            "Terminal=false",
            "Categories=Utility;",
            "",
        ]
    )
    desktop_entry_path.write_text(desktop_entry_contents, encoding="utf-8")
    desktop_entry_path.chmod(0o755)
    return desktop_entry_path


def initialize_assets(config_dir: Path = DEFAULT_CONFIG_DIR) -> Path:
    config_dir.mkdir(parents=True, exist_ok=True)
    config_path = config_dir / "config.json"
    if not config_path.exists():
        config_payload = {
            "version": "1.0",
            "analysis_output_dir": str(Path.cwd() / "artifacts"),
        }
        config_path.write_text(
            json.dumps(config_payload, indent=2) + "\n",
            encoding="utf-8",
        )
    return config_dir
