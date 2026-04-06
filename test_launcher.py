#!/usr/bin/env python3
# test_launcher.py - Test all modes and audio control
import sys
import os

# Add speak function for testing
def speak(text):
    try:
        safe_text = text.replace('"', '').replace("'", "")
        os.system(f'say "{safe_text}"')
    except:
        pass

print("\n" + "="*50)
print("🧪 TESTING JARVIS MODES")
print("="*50)
print("1 = Test Coding Mode (Terminal + Spotify + AI tabs)")
print("2 = Test Movie Mode (movie sites)")
print("3 = Test Music Mode (chill playlist)")
print("4 = Test Stop Audio (mute + pause)")
print("5 = Test Resume Audio (unmute)")
print("q = Quit")
print("="*50)

from app_launcher import AppLauncher
launcher = AppLauncher()

while True:
    choice = input("\nEnter mode to test (1/2/3/4/5/q): ").strip()
    
    if choice == '1':
        print("\n🧪 Testing Mode 1: Anti-Gravity Coding Mode...")
        speak("Coding mode activated Sir")
        launcher.activate_coding_mode()
    elif choice == '2':
        print("\n🧪 Testing Mode 2: Movie Mode...")
        speak("Movie time activated Sir")
        launcher.activate_movie_mode()
    elif choice == '3':
        print("\n🧪 Testing Mode 3: Chill Music Mode...")
        speak("Chill vibes loading Sir")
        launcher.activate_music_mode()
    elif choice == '4':
        print("\n🧪 Testing Stop Audio...")
        speak("Stopping all audio Sir")
        launcher.stop_all_audio()
    elif choice == '5':
        print("\n🧪 Testing Resume Audio...")
        speak("Resuming audio Sir")
        launcher.resume_audio()
    elif choice.lower() == 'q':
        print("👋 Bye!")
        break
    else:
        print("❌ Invalid choice. Enter 1, 2, 3, 4, 5, or q")
