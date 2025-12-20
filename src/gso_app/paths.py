from __future__ import annotations

import os
from pathlib import Path


DATA_ENV_VARS = ("FIGHTAI_DATA_DIR", "GSO_DATA_DIR")


def resolve_data_dir() -> Path:
    for env_var in DATA_ENV_VARS:
        value = os.environ.get(env_var)
        if value:
            return Path(value).expanduser()
    return Path.home() / ".config" / "gso"


def ensure_data_dir() -> Path:
    data_dir = resolve_data_dir()
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def resolve_config_path() -> Path:
    return resolve_data_dir() / "config.json"


def resolve_logs_dir() -> Path:
    return resolve_data_dir() / "logs"
