# Smart Wake Assistant

A privacy-first, Python-based wake assistant that listens for the wake word "Jarvis", then triggers clap/voice-driven automation flows for coding, media, and study modes.

## Highlights

- Wake word detection without API keys
- Clap and voice command activation flows
- Cross-platform runtime support (macOS, Windows, Linux)
- Modular architecture with diagnostics and test scripts
- Startup scripts for quick launch

## How It Works

1. Wake word detection listens for "Jarvis" using speech recognition.
2. After wake word detection, the assistant checks for clap patterns.
3. If claps are not detected, it listens for a short voice command.
4. The command maps to a mode and launches configured apps/tabs.

## Project Structure

- `main.py`: Main assistant runtime and wake pipeline
- `app_launcher.py`: Mode-specific app and browser launch logic
- `clap_detector.py`: Clap detection and timing rules
- `audio_level.py`: Audio input level checks/utilities
- `config.py`: Runtime configuration and mode URLs
- `diagnose.py`: Diagnostics for setup and runtime issues
- `debug_speech.py`: Speech debug helper
- `voice_test_v2.py`: Voice pipeline test utility
- `start_jarvis.sh`: Linux/macOS shell startup script
- `start_jarvis.command`: macOS double-click launch script
- `start_jarvis.bat`: Windows startup script

## Requirements

- macOS, Windows, or Linux
- Python 3.10+
- Microphone access enabled for your terminal/Python process
- Internet connection (speech recognition backend)

Install dependencies:

```bash
pip install -r requirements.txt
```

## Quick Start

1. Create virtual environment (recommended).

macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows (PowerShell):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Install dependencies.

```bash
pip install -r requirements.txt
```

3. Run assistant.

macOS/Linux:

```bash
python main.py
```

Windows:

```bat
python main.py
```

Or run startup script:

```bash
./start_jarvis.sh
```

Windows startup script:

```bat
start_jarvis.bat
```

## Example Commands

- "Jarvis" + 2 claps: Coding mode
- "Jarvis" + "movie time": Movie mode
- "Jarvis" + "vibe" or "songs": Music mode
- "Jarvis" + "study mode": Study mode

## Testing and Diagnostics

Useful scripts in this repository:

- `test_wake.py`
- `test_google_speech.py`
- `test_macbook_mic.py`
- `test_launcher.py`
- `diagnose.py`

## Security and Privacy Notes

- No Picovoice API key is required.
- Wake-word recognition currently uses an online speech recognition service.
- Review `config.py` before sharing to confirm app URLs and behavior.

## Cross-Platform Notes

- App and browser launching works on macOS, Windows, and Linux.
- Advanced media control commands (`stop`, `resume`, `stop forever`) are fully automated on macOS.
- On Windows/Linux, those audio control commands currently fall back to manual media keys/browser controls.

## Roadmap

- Better command intent handling
- Config profiles for multiple users
- Optional structured logging and telemetry controls
- Cross-platform startup support improvements

## License

This project currently has no root-level license file.
If you plan to open-source it publicly, add a standard license (for example, MIT).
