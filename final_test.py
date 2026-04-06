#!/usr/bin/env python3
"""Final test - say JARVIS when it says Listening"""
import speech_recognition as sr
import time

print()
print("=" * 50)
print("🎤 JARVIS VOICE TEST")
print("=" * 50)
print()
print("When you see 'LISTENING NOW', say 'JARVIS' loudly")
print("into your LAPTOP MICROPHONE (not earphones)")
print()

# Countdown
for i in [3, 2, 1]:
    print(f"   Starting in {i}...")
    time.sleep(1)

recognizer = sr.Recognizer()
recognizer.energy_threshold = 300

# Find MacBook mic
macbook_mic = 2  # MacBook Air Microphone is typically index 2
for i, name in enumerate(sr.Microphone.list_microphone_names()):
    if 'MacBook' in name and 'Microphone' in name:
        macbook_mic = i
        break

print()
print("=" * 50)
print("🎙️  LISTENING NOW - SAY 'JARVIS'!")
print("=" * 50)
import os
os.system('say "Speak now"')  # Audio cue so you know when to speak!
print()

try:
    with sr.Microphone(device_index=macbook_mic, sample_rate=16000) as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.3)
        audio = recognizer.listen(source, timeout=15, phrase_time_limit=8)
    
    print("Processing...")
    text = recognizer.recognize_google(audio).lower()
    print(f"\n🗣️ Google heard: '{text}'")
    
    # Check for jarvis or similar
    if 'jarvis' in text:
        print()
        print("🎉🎉🎉 SUCCESS! JARVIS DETECTED! 🎉🎉🎉")
        print()
    elif any(x in text for x in ['travis', 'service', 'davis', 'jarvin', 'java', 'jar']):
        print(f"\n⚠️ Close match! We can make this work.")
    else:
        print(f"\n📝 You said: '{text}' (not jarvis)")
        
except sr.WaitTimeoutError:
    print("❌ Timeout - you didn't speak in time")
except sr.UnknownValueError:
    print("❌ Couldn't understand - speak louder/clearer")
except Exception as e:
    print(f"❌ Error: {e}")
