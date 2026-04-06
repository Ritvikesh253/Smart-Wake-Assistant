# config.py - Cross-platform configuration
import os
from dotenv import load_dotenv
import platform

# Load environment variables
load_dotenv()

# Wake word configuration
WAKE_WORD = "jarvis"

# Audio Configuration
SAMPLE_RATE = 16000
FRAME_LENGTH = 512
CLAP_THRESHOLD = 0.6  # Adjust if too sensitive/not sensitive
CLAP_TIMEOUT = 0.8  # Seconds to wait for claps (fast check)
MIN_CLAP_GAP = 0.2  # Minimum gap between claps (seconds)

# Platform info
OS_NAME = platform.system()

# Apps to open
CODING_APPS = {
    "Visual Studio Code": "app",
    "Terminal": "app",
}

LEISURE_APPS = {
    "Spotify": "app",
}

if OS_NAME == "Windows":
    CODING_APPS = {
        "Code": "app",
        "cmd": "app",
    }
elif OS_NAME == "Linux":
    CODING_APPS = {
        "code": "app",
        "x-terminal-emulator": "app",
    }

# URLs to open in coding mode (regular browser)
CODING_URLS = [
    "https://github.com",
    "https://stackoverflow.com",
    "https://chat.openai.com",
]

# URLs to open in leisure mode (optionally incognito)
LEISURE_URLS = [
    "https://youtube.com",
    "https://reddit.com",
    "https://netflix.com",
]

# Use incognito for leisure mode
USE_INCOGNITO_FOR_LEISURE = True

# Logging
LOG_FILE = os.path.expanduser("~/jarvis-assistant/logs/jarvis.log")
DEBUG = True

# === USER MODES ===
# Mode 1: Anti-Gravity Coding Mode (2 claps)
MODE_1_SPOTIFY_PLAYLIST = "https://open.spotify.com/playlist/6ZjWzRDyi43b5dlyT1eTuV?highlight=spotify%3Atrack%3A4WmB04GBqS4xPMYN9dHgBw&utm_source=openai&utm_medium=chatgpt&nap_web=1&context=spotify%3Aplaylist%3A6ZjWzRDyi43b5dlyT1eTuV&redirectUrl=https%3A%2F%2Fchatgpt.com%2Fc%2F69ac2098-57e8-8322-89ed-5db2928ecd59"
MODE_1_CHROME_TABS = ["https://gemini.google.com", "https://chat.qwen.ai"]

# Mode 2: Movie Mode (voice: "movie time")
MODE_2_CHROME_TABS = ["https://www.5movierulz.claims/", "https://net22.cc/home"]

# Mode 3: Chill Music Mode (voice: "vibe" or "songs")
MODE_3_SPOTIFY_PLAYLIST = "https://open.spotify.com/playlist/792epnXmUM4PlMMEPCYmei?utm_source=openai&utm_medium=chatgpt&nap_web=1&redirect_uri=com.openai.chat%3A%2F%2F&redirectUrl=https%3A%2F%2Fchatgpt.com%2Fc%2F69ac2098-57e8-8322-89ed-5db2928ecd59"

# Mode 4: Study Mode (voice: "study mode" or "study time")
MODE_4_STUDY_VIDEO = "https://www.youtube.com/watch?v=74cOUSKXMz0&t=2s"

