"""Cross-platform launcher for macOS, Windows, and Linux."""
import os
import platform
import shutil
import subprocess
import time
import webbrowser

from config import (
    CODING_URLS,
    LEISURE_URLS,
    MODE_1_CHROME_TABS,
    MODE_1_SPOTIFY_PLAYLIST,
    MODE_2_CHROME_TABS,
    MODE_3_SPOTIFY_PLAYLIST,
    MODE_4_STUDY_VIDEO,
)

class AppLauncher:
    def __init__(self):
        self.os_name = platform.system()
        self.opened_apps = []
        self.opened_urls = []

    def _open_terminal(self):
        """Open system terminal using OS-specific command."""
        try:
            if self.os_name == "Darwin":
                subprocess.Popen(["open", "-a", "Terminal"])
                return True

            if self.os_name == "Windows":
                subprocess.Popen(["cmd", "/c", "start", "", "cmd"], shell=False)
                return True

            for cmd in ["x-terminal-emulator", "gnome-terminal", "konsole", "xterm"]:
                if shutil.which(cmd):
                    subprocess.Popen([cmd])
                    return True
        except Exception as e:
            print(f"⚠️ Could not open terminal: {e}")

        print("⚠️ Could not open terminal automatically on this OS.")
        return False

    def _chrome_command(self):
        """Return an available Chrome/Chromium executable."""
        candidates = [
            "google-chrome",
            "google-chrome-stable",
            "chromium-browser",
            "chromium",
            "chrome",
            "chrome.exe",
            "msedge",
            "msedge.exe",
        ]
        for exe in candidates:
            path = shutil.which(exe)
            if path:
                return path
        return None

    def _open_urls_new_window(self, urls, incognito=False):
        """Open URLs in a browser window, with fallback to default browser tabs."""
        browser_cmd = self._chrome_command()

        if browser_cmd:
            try:
                args = [browser_cmd]
                if incognito:
                    args.append("--incognito")
                args.append("--new-window")
                args.extend(urls)
                subprocess.Popen(args)
                self.opened_urls.extend(urls)
                return True
            except Exception as e:
                print(f"⚠️ Browser command failed, using fallback: {e}")

        for url in urls:
            try:
                webbrowser.open_new_tab(url)
                self.opened_urls.append(url)
            except Exception as e:
                print(f"❌ Failed to open {url}: {e}")
                return False
        return True
    
    def open_app(self, name, app_type):
        """Open app with platform-aware launch commands."""
        try:
            print(f"🚀 Opening {name}...")

            if self.os_name == "Darwin":
                result = subprocess.run(["open", "-a", name], capture_output=True, text=True)
                success = result.returncode == 0
            elif self.os_name == "Windows":
                result = subprocess.run(["cmd", "/c", "start", "", name], capture_output=True, text=True)
                success = result.returncode == 0
            else:
                cmd = shutil.which(name.lower().replace(" ", "-")) or shutil.which(name.lower())
                if cmd:
                    subprocess.Popen([cmd])
                    success = True
                else:
                    success = False

            if success:
                self.opened_apps.append(name)
                print(f"✅ Opened {name}")
            else:
                print(f"⚠️ Could not open {name} (may not be installed)")

            time.sleep(0.5)
            return success
            
        except Exception as e:
            print(f"❌ Failed to open {name}: {e}")
            return False
    
    def open_url(self, url, incognito=False):
        """Open URL in browser (optionally incognito)"""
        try:
            print(f"🌐 Opening {url}..." + (" (incognito)" if incognito else ""))

            self._open_urls_new_window([url], incognito=incognito)
            time.sleep(0.3)
            return True
        except Exception as e:
            print(f"❌ Failed to open {url}: {e}")
            return False
    
    def open_coding_mode(self, app_dict):
        """Open coding apps and URLs"""
        print("\n💻 ACTIVATING CODING MODE")
        print("=" * 40)
        
        # Open apps
        for name, app_type in app_dict.items():
            self.open_app(name, app_type)
        
        # Wait a bit for apps to load
        time.sleep(1)
        
        # Open coding URLs (regular browser)
        print("\n📑 Opening coding resources...")
        for url in CODING_URLS:
            self.open_url(url, incognito=False)
        
        print("\n✅ Coding mode activated!\n")
    
    def open_leisure_mode(self, app_dict):
        """Open leisure apps and URLs (with incognito)"""
        print("\n🎮 ACTIVATING LEISURE MODE")
        print("=" * 40)
        
        # Open apps
        for name, app_type in app_dict.items():
            self.open_app(name, app_type)
        
        # Wait a bit
        time.sleep(1)
        
        # Open leisure URLs in INCOGNITO
        print("\n📺 Opening entertainment (incognito)...")
        for url in LEISURE_URLS:
            self.open_url(url, incognito=True)
        
        print("\n✅ Leisure mode activated!\n")
    
    # === CUSTOM USER MODES ===
    
    def activate_coding_mode(self):
        """Mode 1: Coding - open terminal plus coding/music tabs."""
        print("\n" + "=" * 50)
        print("💻 ANTI-GRAVITY CODING MODE ACTIVATED!")
        print("=" * 50)
        
        try:
            print("🖥️  Opening Terminal...")
            self._open_terminal()
            time.sleep(0.5)

            print("🎧 Opening Spotify playlist in browser...")
            print("🌐 Opening AI assistants (Gemini + Qwen)...")
            self._open_urls_new_window([MODE_1_SPOTIFY_PLAYLIST, MODE_1_CHROME_TABS[0], MODE_1_CHROME_TABS[1]])
            
            print("\n✅ Anti-Gravity Coding Mode Ready!")
            print("🚀 Terminal | Spotify Playlist | Gemini | Qwen\n")
            
        except Exception as e:
            print(f"❌ Error activating coding mode: {e}")
    
    def activate_movie_mode(self):
        """Mode 2: Movie Time - open movie sites in a new browser window."""
        print("\n" + "=" * 50)
        print("🍿 MOVIE TIME ACTIVATED! Enjoy your film.")
        print("=" * 50)
        
        try:
            print("🎬 Opening movie sites...")
            self._open_urls_new_window([MODE_2_CHROME_TABS[0], MODE_2_CHROME_TABS[1]])
            
            print("\n✅ Movie sites loaded!")
            print("🎥 5movierulz | net22\n")
            
        except Exception as e:
            print(f"❌ Error activating movie mode: {e}")
    
    def activate_music_mode(self):
        """Mode 3: Chill Vibes - open chill playlist."""
        print("\n" + "=" * 50)
        print("🎧 CHILL MUSIC MODE ACTIVATED! Vibes loading...")
        print("=" * 50)
        
        try:
            print("🎶 Opening chill playlist...")
            self._open_urls_new_window([MODE_3_SPOTIFY_PLAYLIST])
            print("\n✅ Vibes loaded!\n")
            
        except Exception as e:
            print(f"❌ Error activating music mode: {e}")
    
    def activate_study_mode(self):
        """Mode 4: Study Mode - open study video."""
        print("\n" + "=" * 50)
        print("📚 STUDY MODE ACTIVATED! Focus time...")
        print("=" * 50)
        
        try:
            print("🎓 Opening study video...")
            self._open_urls_new_window([MODE_4_STUDY_VIDEO])
            
            print("\n✅ Study video loaded! Stay focused.\n")
            
        except Exception as e:
            print(f"❌ Error activating study mode: {e}")
    
    # === AUDIO CONTROL ===
    
    def stop_all_audio(self):
        """Stop media where possible. Full control is currently macOS-only."""
        print("\n⏸️  PAUSING ALL MEDIA...")
        try:
            if self.os_name == "Darwin":
                os.system('osascript -e "tell application \"Spotify\" to pause" 2>/dev/null')
                print("✅ Spotify app paused")
                print("⏸️  Media pause command sent\n")
            else:
                print("⚠️ Global media pause automation is not yet available on this OS.")
                print("   Please use your media keys/browser controls.\n")
        except Exception as e:
            print(f"❌ Error pausing media: {e}")
    
    def resume_audio(self):
        """Resume media where possible. Full control is currently macOS-only."""
        print("\n▶️  RESUMING ALL MEDIA...")
        try:
            if self.os_name == "Darwin":
                os.system('osascript -e "tell application \"Spotify\" to play" 2>/dev/null')
                print("✅ Spotify app playing")
                print("▶️  Media resume command sent\n")
            else:
                print("⚠️ Global media resume automation is not yet available on this OS.")
                print("   Please use your media keys/browser controls.\n")
        except Exception as e:
            print(f"❌ Error resuming media: {e}")
    
    def close_audio_tabs(self):
        """Close audio tabs where possible. Full control is currently macOS-only."""
        print("\n🔇 CLOSING AUDIO TABS...")
        try:
            if self.os_name == "Darwin":
                script = '''
                tell application "Google Chrome"
                    set windowList to every window
                    repeat with aWindow in windowList
                        set tabList to every tab of aWindow
                        repeat with i from (count tabList) to 1 by -1
                            set aTab to item i of tabList
                            set tabURL to URL of aTab
                            if tabURL contains "youtube.com" or tabURL contains "spotify.com" or tabURL contains "open.spotify.com" then
                                close aTab
                            end if
                        end repeat
                    end repeat
                end tell
                '''
                os.system(f"osascript -e '{script}'")
                os.system('osascript -e "tell application \"Spotify\" to pause" 2>/dev/null')
                print("✅ Closed YouTube and Spotify tabs")
                print("🔇 All audio tabs closed\n")
            else:
                print("⚠️ Closing specific browser audio tabs is not yet available on this OS.\n")
        except Exception as e:
            print(f"❌ Error closing audio tabs: {e}")
    
    def close_all(self):
        """Close all opened apps"""
        print("\n🔒 Closing apps...")
        for app in self.opened_apps:
            try:
                if self.os_name == "Windows":
                    subprocess.run(["taskkill", "/F", "/IM", app], capture_output=True)
                else:
                    subprocess.run(["pkill", "-f", app], capture_output=True)
            except:
                pass
        self.opened_apps = []
