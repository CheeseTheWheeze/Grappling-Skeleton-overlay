from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def main() -> int:
    repo_root = Path(__file__).resolve().parent
    python = sys.executable
    env = os.environ.copy()
    env["PIP_NO_INDEX"] = "1"

    install_cmd = [python, "-m", "pip", "install", "--no-index", "-e", str(repo_root)]
    install_result = subprocess.run(install_cmd, check=False, env=env)
    if install_result.returncode != 0:
        print("Installer error: unable to install the app.")
        return install_result.returncode

    install_flow = [python, "-m", "gso_app.cli", "install"]
    flow_result = subprocess.run(install_flow, check=False)
    return flow_result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
