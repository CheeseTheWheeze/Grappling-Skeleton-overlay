#!/bin/bash
set -e
cd "$(dirname "$0")"
python3 install_gso.py
echo ""
echo "Installer finished. Press Enter to close."
read -r
