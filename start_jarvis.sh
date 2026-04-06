#!/bin/bash
# start_jarvis.sh - Linux/macOS startup script

# Navigate to project directory (script location)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Activate virtual environment
source venv/bin/activate

# Start Jarvis
echo "🚀 Starting Jarvis Assistant..."
python main.py
