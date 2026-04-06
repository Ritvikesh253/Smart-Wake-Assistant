# app_launcher.py - Mac Optimized with 3 Custom Modes
import subprocess
import time
import os
from config import (
    CODING_URLS, LEISURE_URLS,
    MODE_1_SPOTIFY_PLAYLIST, MODE_1_CHROME_TABS,
    MODE_2_CHROME_TABS,
    MODE_3_SPOTIFY_PLAYLIST,
    MODE_4_STUDY_VIDEO
)

class AppLauncher:
    def __init__(self):
        self.opened_apps = []
        self.opened_urls = []
    
    def open_app(self, name, app_type):
        """Open a Mac app using 'open -a' command"""
        try:
            print(f"🚀 Opening {name}...")
            # Use 'open -a' which is the most reliable way on Mac
            result = subprocess.run(['open', '-a', name], capture_output=True, text=True)
            if result.returncode == 0:
                self.opened_apps.append(name)
                print(f"✅ Opened {name}")
            else:
                print(f"⚠️ Could not open {name} (may not be installed)")
            time.sleep(0.5)
            return result.returncode == 0
            
        except Exception as e:
            print(f"❌ Failed to open {name}: {e}")
            return False
    
    def open_url(self, url, incognito=False):
        """Open URL in browser (optionally incognito)"""
        try:
            print(f"🌐 Opening {url}..." + (" (incognito)" if incognito else ""))
            
            if incognito:
                # Chrome incognito mode
                subprocess.Popen([
                    'open', '-na', 'Google Chrome', '--args', '--incognito', url
                ])
            else:
                subprocess.Popen(['open', url])
            
            self.opened_urls.append(url)
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
        """Mode 1: Anti-Gravity Coding - Terminal + Chrome with Spotify playlist, Gemini, Qwen"""
        print("\n" + "=" * 50)
        print("💻 ANTI-GRAVITY CODING MODE ACTIVATED!")
        print("=" * 50)
        
        try:
            # 1. Open Terminal
            print("🖥️  Opening Terminal...")
            subprocess.Popen(['open', '-a', 'Terminal'])
            time.sleep(0.5)
            
            # 2. Open Chrome with Spotify playlist + Gemini + Qwen (all in one window)
            print("🎧 Opening Spotify playlist in browser...")
            print("🌐 Opening AI assistants (Gemini + Qwen)...")
            subprocess.Popen([
                'open', '-na', 'Google Chrome', '--args',
                '--new-window', MODE_1_SPOTIFY_PLAYLIST, MODE_1_CHROME_TABS[0], MODE_1_CHROME_TABS[1]
            ])
            
            print("\n✅ Anti-Gravity Coding Mode Ready!")
            print("🚀 Terminal | Spotify Playlist | Gemini | Qwen\n")
            
        except Exception as e:
            print(f"❌ Error activating coding mode: {e}")
    
    def activate_movie_mode(self):
        """Mode 2: Movie Time - Chrome with movie sites"""
        print("\n" + "=" * 50)
        print("🍿 MOVIE TIME ACTIVATED! Enjoy your film.")
        print("=" * 50)
        
        try:
            # Open Chrome with both movie sites in new window
            print("🎬 Opening movie sites...")
            subprocess.Popen([
                'open', '-na', 'Google Chrome', '--args',
                '--new-window', MODE_2_CHROME_TABS[0], MODE_2_CHROME_TABS[1]
            ])
            
            print("\n✅ Movie sites loaded!")
            print("🎥 5movierulz | net22\n")
            
        except Exception as e:
            print(f"❌ Error activating movie mode: {e}")
    
    def activate_music_mode(self):
        """Mode 3: Chill Vibes - Chrome with ONLY the vibe playlist"""
        print("\n" + "=" * 50)
        print("🎧 CHILL MUSIC MODE ACTIVATED! Vibes loading...")
        print("=" * 50)
        
        try:
            # Open Chrome with ONLY the vibe playlist
            print("🎶 Opening chill playlist...")
            subprocess.Popen([
                'open', '-na', 'Google Chrome', '--args',
                '--new-window', MODE_3_SPOTIFY_PLAYLIST
            ])
            
            # Wait for page to load then auto-play
            print("⏳ Waiting for Spotify to load...")
            time.sleep(4)
            
            # Click play button on Spotify web player
            play_script = '''
            tell application "Google Chrome"
                set windowList to every window
                repeat with aWindow in windowList
                    set tabList to every tab of aWindow
                    repeat with aTab in tabList
                        set tabURL to URL of aTab
                        if tabURL contains "spotify.com" or tabURL contains "open.spotify.com" then
                            execute aTab javascript "document.querySelector('[data-testid=play-button]')?.click(); document.querySelector('[data-testid=action-bar-row] button[data-testid=play-button]')?.click();"
                        end if
                    end repeat
                end repeat
            end tell
            '''
            os.system(f"osascript -e '{play_script}' 2>/dev/null")
            
            print("\n✅ Vibes loaded and playing! Enjoy the music.\n")
            
        except Exception as e:
            print(f"❌ Error activating music mode: {e}")
    
    def activate_study_mode(self):
        """Mode 4: Study Mode - Chrome with YouTube study video"""
        print("\n" + "=" * 50)
        print("📚 STUDY MODE ACTIVATED! Focus time...")
        print("=" * 50)
        
        try:
            # Open Chrome with study video
            print("🎓 Opening study video...")
            subprocess.Popen([
                'open', '-na', 'Google Chrome', '--args',
                '--new-window', MODE_4_STUDY_VIDEO
            ])
            
            print("\n✅ Study video loaded! Stay focused.\n")
            
        except Exception as e:
            print(f"❌ Error activating study mode: {e}")
    
    # === AUDIO CONTROL ===
    
    def stop_all_audio(self):
        """Stop all audio - pause Spotify and YouTube videos"""
        print("\n⏸️  PAUSING ALL MEDIA...")
        try:
            # Pause Spotify app if running
            os.system('osascript -e "tell application \"Spotify\" to pause" 2>/dev/null')
            print("✅ Spotify app paused")
            
            # Pause YouTube videos using key simulation (spacebar pauses)
            # First activate Chrome, then send spacebar to pause video
            pause_yt = '''
            tell application "Google Chrome"
                activate
                set windowList to every window
                repeat with aWindow in windowList
                    set tabList to every tab of aWindow
                    repeat with aTab in tabList
                        set tabURL to URL of aTab
                        if tabURL contains "youtube.com" then
                            set active tab index of aWindow to (index of aTab)
                            delay 0.3
                            tell application "System Events" to keystroke "k"
                        end if
                    end repeat
                end repeat
            end tell
            '''
            subprocess.run(['osascript', '-e', pause_yt], capture_output=True, timeout=5)
            print("✅ YouTube paused (k key)")
            
            # Pause Spotify web player using spacebar
            pause_spotify = '''
            tell application "Google Chrome"
                set windowList to every window
                repeat with aWindow in windowList
                    set tabList to every tab of aWindow
                    repeat with aTab in tabList
                        set tabURL to URL of aTab
                        if tabURL contains "spotify.com" then
                            set active tab index of aWindow to (index of aTab)
                            delay 0.3
                            tell application "System Events" to keystroke space
                        end if
                    end repeat
                end repeat
            end tell
            '''
            subprocess.run(['osascript', '-e', pause_spotify], capture_output=True, timeout=5)
            print("✅ Spotify web paused (spacebar)")
            
            print("⏸️  All media paused\n")
        except Exception as e:
            print(f"❌ Error pausing media: {e}")
    
    def resume_audio(self):
        """Resume audio - play Spotify and YouTube videos"""
        print("\n▶️  RESUMING ALL MEDIA...")
        try:
            # Play Spotify app if running
            os.system('osascript -e "tell application \"Spotify\" to play" 2>/dev/null')
            print("✅ Spotify app playing")
            
            # Resume YouTube videos using k key
            play_yt = '''
            tell application "Google Chrome"
                activate
                set windowList to every window
                repeat with aWindow in windowList
                    set tabList to every tab of aWindow
                    repeat with aTab in tabList
                        set tabURL to URL of aTab
                        if tabURL contains "youtube.com" then
                            set active tab index of aWindow to (index of aTab)
                            delay 0.3
                            tell application "System Events" to keystroke "k"
                        end if
                    end repeat
                end repeat
            end tell
            '''
            subprocess.run(['osascript', '-e', play_yt], capture_output=True, timeout=5)
            print("✅ YouTube playing (k key)")
            
            # Resume Spotify web player using spacebar
            play_spotify = '''
            tell application "Google Chrome"
                set windowList to every window
                repeat with aWindow in windowList
                    set tabList to every tab of aWindow
                    repeat with aTab in tabList
                        set tabURL to URL of aTab
                        if tabURL contains "spotify.com" then
                            set active tab index of aWindow to (index of aTab)
                            delay 0.3
                            tell application "System Events" to keystroke space
                        end if
                    end repeat
                end repeat
            end tell
            '''
            subprocess.run(['osascript', '-e', play_spotify], capture_output=True, timeout=5)
            print("✅ Spotify web playing (spacebar)")
            
            print("▶️  All media resumed\n")
        except Exception as e:
            print(f"❌ Error resuming media: {e}")
    
    def close_audio_tabs(self):
        """Close all YouTube and Spotify tabs in Chrome"""
        print("\n🔇 CLOSING AUDIO TABS...")
        try:
            # AppleScript to close tabs with YouTube or Spotify
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
            print("✅ Closed YouTube and Spotify tabs")
            
            # Also pause Spotify app if running
            os.system('osascript -e "tell application \"Spotify\" to pause" 2>/dev/null')
            
            print("🔇 All audio tabs closed\n")
        except Exception as e:
            print(f"❌ Error closing audio tabs: {e}")
    
    def close_all(self):
        """Close all opened apps"""
        print("\n🔒 Closing apps...")
        for app in self.opened_apps:
            try:
                subprocess.run(['pkill', '-f', app], capture_output=True)
            except:
                pass
        self.opened_apps = []
