#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

python "$SCRIPT_DIR/apps/windows/main.py"
python "$SCRIPT_DIR/tests/day1_validate.py"

echo "Day-1 test complete."
