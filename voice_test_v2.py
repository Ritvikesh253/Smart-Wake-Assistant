#!/usr/bin/env python3
"""Test with FLAC encoding for Google - works better"""
import speech_recognition as sr
import os

print("🎤 IMPROVED VOICE TEST")
print("=" * 50)
print()

recognizer = sr.Recognizer()
recognizer.energy_threshold = 400  # Higher threshold
recognizer.dynamic_energy_threshold = True  # Let it adapt
recognizer.operation_timeout = 15

# Find MacBook mic
macbook_mic = None
for i, name in enumerate(sr.Microphone.list_microphone_names()):
    if 'MacBook' in name and 'Microphone' in name:
        macbook_mic = i
        print(f"🎤 Using: {name} (index {i})")
        break

if macbook_mic is None:
    print("❌ MacBook mic not found!")
    print("Available mics:")
    for i, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"  [{i}] {name}")
    exit(1)

print()
os.system('say "Say hello world now"')

print("=" * 50)
print("🎙️  LISTENING - SAY 'HELLO WORLD'!")
print("=" * 50)
print()

try:
    # Try with 44100Hz (native Mac rate) then let SR convert
    with sr.Microphone(device_index=macbook_mic, sample_rate=44100) as source:
        print("📊 Calibrating ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print(f"   Energy threshold: {recognizer.energy_threshold}")
        print()
        print("🎤 Speak now (10 sec timeout)...")
        audio = recognizer.listen(source, timeout=10, phrase_time_limit=8)
        print(f"   Captured: {len(audio.frame_data)} bytes")
        print(f"   Sample rate: {audio.sample_rate} Hz")
    
    print()
    print("📤 Sending to Google API...")
    text = recognizer.recognize_google(audio, language='en-IN')  # Indian English!
    print(f"\n✅ Google heard: '{text}'")
    
    if 'jarvis' in text.lower():
        print("\n🎉 JARVIS DETECTED!")
    
except sr.WaitTimeoutError:
    print("❌ No speech detected in 10 seconds")
except sr.UnknownValueError:
    print("❌ Google couldn't understand audio")
    print("   Try speaking clearer or check internet connection")
except sr.RequestError as e:
    print(f"❌ Google API error: {e}")
except Exception as e:
    print(f"❌ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
