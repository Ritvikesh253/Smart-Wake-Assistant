#!/usr/bin/env python3
# main.py - Jarvis Voice Assistant for Mac
# PRIVACY: Wake detection uses speech recognition (no Picovoice API key needed)
# Only AFTER "Jarvis" is detected, Google Speech is used for command
import pyaudio
import sys
import os
import time
import subprocess
import speech_recognition as sr
from clap_detector import ClapDetector
from app_launcher import AppLauncher

# NO LOGGING - Privacy first
# Nothing you say is stored anywhere

# === SCREEN LOCK DETECTION ===
def is_screen_locked():
    """Check if Mac screen is locked or display is asleep"""
    try:
        # Check if screen is locked using ioreg
        result = subprocess.run(
            ['ioreg', '-n', 'Root', '-d1'],
            capture_output=True, text=True, timeout=2
        )
        if 'CGSSessionScreenIsLocked' in result.stdout and '= Yes' in result.stdout:
            return True
        
        # Also check if display is asleep
        result2 = subprocess.run(
            ['pmset', '-g', 'powerstate', 'IODisplayWrangler'],
            capture_output=True, text=True, timeout=2
        )
        # Power state 4 = display on, less than 4 = display off/dim
        if 'IODisplayWrangler' in result2.stdout:
            lines = result2.stdout.strip().split('\n')
            for line in lines:
                if 'IODisplayWrangler' in line:
                    # Get the power state number
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if part.isdigit():
                            power_state = int(part)
                            if power_state < 4:
                                return True
                            break
        return False
    except:
        return False  # Assume not locked if check fails

# === VOICE FEEDBACK (TTS) ===
def speak(text):
    """Speak text using Mac's built-in say command"""
    try:
        safe_text = text.replace('"', '').replace("'", "")
        os.system(f'say "{safe_text}"')
    except:
        pass

class JarvisAssistant:
    def __init__(self):
        self.clap_detector = ClapDetector()
        self.app_launcher = AppLauncher()
        self.running = True
        self.pa = pyaudio.PyAudio()
        self.wake_recognizer = sr.Recognizer()
        self.wake_recognizer.energy_threshold = 350
        self.wake_recognizer.dynamic_energy_threshold = True
        
        # Find MacBook mic index for PyAudio
        self.mic_index = None
        for i in range(self.pa.get_device_count()):
            info = self.pa.get_device_info_by_index(i)
            if 'MacBook' in info['name'] and 'Microphone' in info['name']:
                self.mic_index = i
                break
        
        print("✅ Jarvis initialized (No Picovoice key required)")
    
    def listen_for_wake_word(self):
        """
        Wake word detection using speech recognition.
        - No Picovoice dependency or API key required
        - Waits for the word "Jarvis"
        """
        print("\n" + "=" * 50)
        print("🎙️  JARVIS IS LISTENING (Privacy Mode)")
        print("=" * 50)
        print("🌐 Wake word detection: Speech recognition service (no API key)")
        print("📝 Available Modes:")
        print("   🔹 Say 'Jarvis' + 2 claps → Coding Mode")
        print("   🔹 Say 'Jarvis' + 'Movie Time' → Movie Mode")
        print("   🔹 Say 'Jarvis' + 'Vibe/Songs' → Music Mode")
        print("   🔹 Say 'Jarvis' + 'Study Mode/Time' → Study Mode")
        print("   🔹 Say 'Jarvis' + 'Stop/Quiet' → Mute Audio")
        print("   🔹 Say 'Jarvis' + 'Play/Resume' → Unmute Audio")
        print("   🔹 Say 'Jarvis' + 'Stop Forever' → Close audio tabs")
        print("=" * 50)
        print("\n🎧 Waiting for 'Jarvis'... (your speech is private)\n")
        
        # Track sleep state
        was_sleeping = False
        
        while self.running:
            try:
                # Check if Mac is locked/sleeping - pause to save battery
                if is_screen_locked():
                    if not was_sleeping:
                        print("💤 Mac locked/sleeping - Jarvis paused (saving battery)")
                        was_sleeping = True
                    time.sleep(2)  # Check every 2 seconds
                    continue
                
                # Mac is awake - resume if we were sleeping
                if was_sleeping:
                    print("☕ Mac awake - Jarvis resuming!")
                    was_sleeping = False
                    os.system('afplay /System/Library/Sounds/Pop.aiff &')

                if self.detect_wake_word(timeout=2):
                    # "Jarvis" detected!
                    print("🎯 Jarvis detected!")

                    speak("Yes Sir")

                    # Use clap and command flow after wake word
                    self.handle_activation()

                    time.sleep(0.5)

                    print("\n🎧 Waiting for 'Jarvis'... (your speech is private)\n")
                    os.system('afplay /System/Library/Sounds/Pop.aiff &')
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(0.5)

    def detect_wake_word(self, timeout=2):
        """Listen briefly and return True if wake word is detected."""
        try:
            with sr.Microphone(device_index=self.mic_index, sample_rate=44100) as source:
                self.wake_recognizer.adjust_for_ambient_noise(source, duration=0.2)
                audio = self.wake_recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=2,
                )

            text = self.wake_recognizer.recognize_google(audio, language='en-IN').lower()
            return 'jarvis' in text
        except sr.WaitTimeoutError:
            return False
        except sr.UnknownValueError:
            return False
        except sr.RequestError:
            print("⚠️ Speech recognition unavailable. Check internet connection.")
            time.sleep(1)
            return False
        except Exception:
            return False
    
    def handle_activation(self):
        """Handle activation: check for claps first, then voice command with retry"""
        try:
            # Step 1: Quick clap check (0.8 sec)
            print("👂 Listening for claps...")
            clap_count = self.clap_detector.wait_for_claps()
            
            if clap_count == 2:
                # Mode 1: Anti-Gravity Coding Mode
                speak("Coding mode activated Sir")
                self.app_launcher.activate_coding_mode()
            elif clap_count < 2:
                # No claps - listen for voice command with 3 retries
                for attempt in range(1, 4):
                    print(f"🎤 Listening for command (attempt {attempt}/3)...")
                    command = self.listen_for_voice_command()
                    
                    if command and self.handle_voice_command(command):
                        # Valid command executed
                        break
                    else:
                        # Retry messages
                        if attempt == 1:
                            speak("I didn't catch that, say that again sir")
                        elif attempt == 2:
                            speak("I didn't get it sir")
                        else:
                            speak("Try again with Jarvis")
                            break
            else:
                print(f"⚠️ Detected {clap_count} claps. Use exactly 2 claps for Coding Mode.")
            
        except Exception as e:
            print(f"Error: {e}")
    
    def listen_for_voice_command(self):
        """Listen for voice command using speech recognition"""
        recognizer = sr.Recognizer()
        recognizer.energy_threshold = 400  # Higher threshold
        recognizer.dynamic_energy_threshold = True  # Let it adapt
        
        try:
            # Find MacBook mic for speech recognition
            macbook_mic_index = None
            for i, mic_name in enumerate(sr.Microphone.list_microphone_names()):
                if 'MacBook' in mic_name and 'Microphone' in mic_name:
                    macbook_mic_index = i
                    break
            
            # Use 44100Hz (Mac's native rate) for best compatibility
            with sr.Microphone(device_index=macbook_mic_index, sample_rate=44100) as source:
                print("🎤 Speak now...")
                recognizer.adjust_for_ambient_noise(source, duration=0.3)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                
            # Use Indian English locale for better accent recognition
            command = recognizer.recognize_google(audio, language='en-IN')
            # Privacy: Don't log what user says
            print("✅ Command received")
            return command
            
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            return None
        except Exception as e:
            return None
    
    def handle_voice_command(self, command):
        """Handle voice commands after wake word. Returns True if valid command."""
        if not command:
            return False
        
        command_lower = command.lower()
        
        # Audio Control Commands
        if "stop forever" in command_lower or "forever" in command_lower:
            speak("Closing all audio tabs Sir")
            self.app_launcher.close_audio_tabs()
            return True
        elif any(word in command_lower for word in ["stop", "quiet", "mute", "silence", "shut", "pause"]):
            speak("Stopping all audio Sir")
            self.app_launcher.stop_all_audio()
            return True
        elif any(word in command_lower for word in ["play", "resume", "unmute", "start", "unpause"]):
            speak("Resuming audio Sir")
            self.app_launcher.resume_audio()
            return True
        # Mode Commands
        elif any(word in command_lower for word in ["movie", "movies", "film", "watch"]):
            # Mode 2: Movie Mode
            speak("Movie time activated Sir")
            self.app_launcher.activate_movie_mode()
            return True
        elif any(word in command_lower for word in ["vibe", "vibes", "wibe", "wibes", "vype", "song", "songs", "music", "chill", "tune", "tunes", "spotify", "playlist"]):
            # Mode 3: Chill Music Mode
            speak("Chill vibes loading Sir")
            self.app_launcher.activate_music_mode()
            return True
        elif any(word in command_lower for word in ["study", "focus", "work", "concentrate"]):
            # Mode 4: Study Mode
            speak("Study mode activated Sir")
            self.app_launcher.activate_study_mode()
            return True
        else:
            # Unknown command - let retry logic handle it
            return False
    
    def handle_clap_sequence(self):
        """Legacy method - redirects to handle_activation"""
        self.handle_activation()
    
    def _get_default_input_device(self):
        """Get the best available input device - prioritize MacBook mic for reliability"""
        try:
            # First, try to find MacBook Air Microphone (most reliable)
            for i in range(self.pa.get_device_count()):
                info = self.pa.get_device_info_by_index(i)
                if 'MacBook' in info['name'] and info['maxInputChannels'] > 0:
                    print(f"\n🎤 Microphone: {info['name']}")
                    print("   ✅ Using MacBook built-in mic for best reliability\n")
                    return i
            
            # Fallback to system default if MacBook mic not found
            default_device = self.pa.get_default_input_device_info()
            print(f"\n🎤 Microphone: {default_device['name']}")
            print("   (Change in System Settings > Sound > Input if needed)\n")
            return default_device['index']
        except Exception as e:
            print(f"❌ No microphone found! Check System Settings > Sound > Input")
            return None
    
    def start(self):
        """Start the assistant"""
        print("\n" + "=" * 50)
        print("🤖 JARVIS VOICE ASSISTANT FOR MAC")
        print("=" * 50)
        print("🔒 Privacy Mode: No logging, no data stored")
        print("=" * 50 + "\n")
        
        try:
            self.listen_for_wake_word()
        except KeyboardInterrupt:
            print("\n👋 Shutting down...")
        finally:
            self.stop()
    
    def stop(self):
        """Stop the assistant and cleanup"""
        self.running = False
        
        try:
            self.clap_detector.cleanup()
            if hasattr(self, 'pa'):
                self.pa.terminate()
        except Exception as e:
            pass  # Privacy: No logging
        
        print("\n👋 Jarvis stopped. Goodbye!")

if __name__ == "__main__":
    try:
        jarvis = JarvisAssistant()
        jarvis.start()
    except KeyboardInterrupt:
        print("\n👋 Interrupted by user")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
