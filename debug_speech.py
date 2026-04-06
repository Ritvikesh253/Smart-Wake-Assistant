#!/usr/bin/env python3
"""Debug Google Speech Recognition"""
import speech_recognition as sr
import time

print("🔍 Debug Google Speech Recognition")
print()

recognizer = sr.Recognizer()

# Find MacBook mic
macbook_mic = None
mics = sr.Microphone.list_microphone_names()
print(f"Available microphones: {len(mics)}")
for i, name in enumerate(mics):
    print(f"  [{i}] {name}")
    if 'MacBook' in name and 'Microphone' in name:  # Need BOTH keywords!
        macbook_mic = i

print(f"\n🎤 Using mic index: {macbook_mic}")

print("\n" + "=" * 40)
print("🎙️  SAY ANYTHING - any word, name, etc...")
print("=" * 40 + "\n")

try:
    with sr.Microphone(device_index=macbook_mic, sample_rate=16000) as source:
        print("📊 Calibrating for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print(f"   Energy threshold: {recognizer.energy_threshold}")
        
        print("\n🎤 Listening now - SPEAK!")
        start = time.time()
        audio = recognizer.listen(source, timeout=8, phrase_time_limit=5)
        duration = time.time() - start
        
        print(f"   Captured {len(audio.frame_data)} bytes in {duration:.1f}s")
        print(f"   Sample rate: {audio.sample_rate} Hz")
        print(f"   Sample width: {audio.sample_width} bytes")
    
    print("\n📤 Sending to Google...")
    try:
        # Try with show_all to see raw response
        result = recognizer.recognize_google(audio, show_all=True)
        print(f"Raw result type: {type(result)}")
        print(f"Raw result: {result}")
        
        if result:
            text = recognizer.recognize_google(audio)
            print(f"\n✅ Google heard: '{text}'")
    except sr.RequestError as e:
        print(f"❌ Request error: {e}")
    except sr.UnknownValueError:
        print("❌ Could not understand audio")

except sr.WaitTimeoutError:
    print("❌ No speech detected before timeout")
except Exception as e:
    print(f"❌ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
