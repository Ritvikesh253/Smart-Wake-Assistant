#!/bin/bash
# start_jarvis.sh - Mac Startup Script

# Navigate to project directory
cd "$HOME/Desktop/Agravity/Jarvis_wakeup"

# Activate virtual environment
source venv/bin/activate

# Start Jarvis
echo "🚀 Starting Jarvis Assistant..."
python main.py
