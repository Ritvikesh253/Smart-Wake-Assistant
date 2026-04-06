#!/bin/bash
# Jarvis Startup Script
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"
./venv/bin/python main.py
echo ""
echo "Jarvis stopped. Press any key to close..."
read -n 1
