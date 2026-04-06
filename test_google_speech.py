#!/usr/bin/env python3
"""Test Jarvis detection using Google Speech Recognition (works with any accent!)"""
import speech_recognition as sr

print("🎤 Testing voice detection using Google Speech...")
print("   Say 'JARVIS' loudly into your laptop!")
print()

recognizer = sr.Recognizer()
recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = False

# Find MacBook mic
macbook_mic = None
for i, name in enumerate(sr.Microphone.list_microphone_names()):
    if 'MacBook' in name and 'Microphone' in name:
        macbook_mic = i
        print(f"🎤 Using: {name}")
        break

print("\n" + "=" * 40)
print("🎙️  SAY 'JARVIS' NOW...")
print("=" * 40 + "\n")

try:
    with sr.Microphone(device_index=macbook_mic, sample_rate=16000) as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.3)
        print("Listening...")
        audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
    
    print("Processing speech...")
    text = recognizer.recognize_google(audio).lower()
    print(f"\n🗣️ You said: '{text}'")
    
    if 'jarvis' in text:
        print("✅ JARVIS DETECTED! Google Speech works!")
    elif 'travis' in text or 'service' in text or 'davis' in text:
        print(f"⚠️ Close! Heard '{text}' - Google gets it, we can filter for this")
    else:
        print(f"❓ Didn't hear 'jarvis' but heard: '{text}'")
        
except sr.WaitTimeoutError:
    print("❌ No speech detected - speak louder!")
except sr.UnknownValueError:
    print("❌ Couldn't understand speech - speak clearer!")
except sr.RequestError as e:
    print(f"❌ Google API error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
