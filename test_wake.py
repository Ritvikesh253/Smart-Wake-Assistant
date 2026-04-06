#!/usr/bin/env python3
"""Test wake word detection without Picovoice/API key."""
import speech_recognition as sr

print("🎤 Testing wake word detection - Say 'JARVIS'...")
print("(Will listen for up to 20 seconds)")

recognizer = sr.Recognizer()
recognizer.energy_threshold = 350
recognizer.dynamic_energy_threshold = True

# Prefer MacBook microphone when available
device_index = None
device_name = "Default"
for i, name in enumerate(sr.Microphone.list_microphone_names()):
    if 'MacBook' in name and 'Microphone' in name:
        device_index = i
        device_name = name
        break

print(f"\n🎤 Using: {device_name}")
print("\n" + "=" * 40)
print("🎙️  LISTENING NOW - Say 'JARVIS'...")
print("=" * 40 + "\n")

try:
    with sr.Microphone(device_index=device_index, sample_rate=44100) as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.3)
        audio = recognizer.listen(source, timeout=20, phrase_time_limit=3)

    text = recognizer.recognize_google(audio, language='en-IN').lower()
    print(f"\n🗣️ Heard: '{text}'")

    if 'jarvis' in text:
        print("✅ JARVIS DETECTED! Wake word test passed.")
    else:
        print("❌ Wake word not detected in recognized speech.")
except sr.WaitTimeoutError:
    print("⏰ Timeout - no speech detected")
except sr.UnknownValueError:
    print("❌ Could not understand speech")
except sr.RequestError as e:
    print(f"❌ Speech recognition service error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
