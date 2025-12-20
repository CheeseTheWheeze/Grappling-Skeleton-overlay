from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Iterable

DEFAULT_MIN_PYTHON = (3, 9)
DEFAULT_CONFIG_DIR = Path.home() / ".gso"
DEFAULT_REQUIREMENTS_PATH = Path(__file__).resolve().parents[2] / "requirements.txt"


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
    python_executable = python_executable or sys.executable
    command = [python_executable, "-m", "pip", "install", "-r", str(requirements_path)]
    result = subprocess.run(command, check=False)
    if result.returncode != 0:
        raise RuntimeError(
            "Requirement installation failed. Command: "
            + " ".join(command)
        )


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
