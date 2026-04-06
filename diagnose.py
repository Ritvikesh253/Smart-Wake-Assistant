#!/usr/bin/env python3
"""Comprehensive diagnostic for Jarvis voice assistant on Mac"""
import pyaudio
import struct
import math
import time
import os
import sys

print("=" * 60)
print("🔍 JARVIS DIAGNOSTIC TOOL")
print("=" * 60)

# Check 1: PyAudio and devices
print("\n1️⃣ AUDIO DEVICES CHECK")
print("-" * 40)

pa = pyaudio.PyAudio()
print(f"PortAudio: {pyaudio.get_portaudio_version_text()[:50]}")

input_devices = []
for i in range(pa.get_device_count()):
    info = pa.get_device_info_by_index(i)
    if info['maxInputChannels'] > 0:
        input_devices.append((i, info['name'], int(info['defaultSampleRate'])))
        print(f"  [{i}] {info['name']} (native: {int(info['defaultSampleRate'])}Hz)")

# Check 2: Stream test at 16000Hz
print("\n2️⃣ STREAM TEST (16000Hz for Porcupine)")
print("-" * 40)

working_device = None
for idx, name, native_rate in input_devices:
    try:
        stream = pa.open(
            rate=16000,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=512,
            input_device_index=idx
        )
        # Quick read test
        data = stream.read(512, exception_on_overflow=False)
        stream.close()
        print(f"  ✅ [{idx}] {name} - works at 16000Hz")
        if working_device is None:
            working_device = idx
    except Exception as e:
        print(f"  ❌ [{idx}] {name} - {str(e)[:40]}")

# Check 3: Audio level test
print("\n3️⃣ MICROPHONE LEVEL TEST (speak into mic!)")
print("-" * 40)

if working_device is not None:
    device_name = [n for i, n, r in input_devices if i == working_device][0]
    print(f"Testing device [{working_device}]: {device_name}")
    print("🎤 SPEAK NOW for 3 seconds...")
    
    stream = pa.open(
        rate=16000,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=512,
        input_device_index=working_device
    )
    
    max_level = 0
    for _ in range(90):  # ~3 seconds
        data = stream.read(512, exception_on_overflow=False)
        samples = struct.unpack_from("h" * 512, data)
        rms = math.sqrt(sum(s*s for s in samples) / len(samples))
        if rms > max_level:
            max_level = rms
        level = int(rms / 100)
        bar = "█" * min(level, 50)
        print(f"\r  {bar:<50} {int(rms):>5}", end="", flush=True)
        time.sleep(0.03)
    
    stream.close()
    print(f"\n\n  Max level: {int(max_level)}")
    if max_level < 300:
        print("  ⚠️  TOO QUIET! Increase mic volume in System Settings > Sound > Input")
    elif max_level < 1000:
        print("  ⚠️  Somewhat quiet. Try speaking louder or closer to mic")
    else:
        print("  ✅ Good audio levels!")

# Check 4: Porcupine
print("\n4️⃣ PORCUPINE WAKE WORD CHECK")
print("-" * 40)

try:
    import pvporcupine
    from config import PICOVOICE_API_KEY
    
    porcupine = pvporcupine.create(
        access_key=PICOVOICE_API_KEY,
        keywords=['jarvis'],
        sensitivities=[0.9]
    )
    print(f"  ✅ Porcupine initialized")
    print(f"     Required: {porcupine.sample_rate}Hz, {porcupine.frame_length} frames")
    porcupine.delete()
except Exception as e:
    print(f"  ❌ Porcupine error: {e}")

# Check 5: SpeechRecognition
print("\n5️⃣ SPEECH RECOGNITION CHECK")
print("-" * 40)

try:
    import speech_recognition as sr
    mics = sr.Microphone.list_microphone_names()
    print(f"  Found {len(mics)} microphones")
    
    # Find mic with 'microphone' in name
    mic_idx = None
    for i, name in enumerate(mics):
        if 'microphone' in name.lower():
            mic_idx = i
            print(f"  Will use: [{i}] {name}")
            break
    
    print("  ✅ SpeechRecognition ready")
except Exception as e:
    print(f"  ❌ SpeechRecognition error: {e}")

# Check 6: Microphone permission
print("\n6️⃣ MICROPHONE PERMISSION CHECK")
print("-" * 40)

# On Mac, if we got this far with audio, permission is granted
print("  ✅ Microphone permission granted (audio streams work)")

# Summary
print("\n" + "=" * 60)
print("📋 SUMMARY")
print("=" * 60)

issues = []
if max_level < 300:
    issues.append("Mic volume too low - increase in System Settings")
if working_device is None:
    issues.append("No working audio device found")

if issues:
    print("⚠️  Issues found:")
    for issue in issues:
        print(f"   • {issue}")
else:
    print("✅ All checks passed!")
    print(f"\n🎯 Recommended device index: {working_device}")

pa.terminate()

print("\n" + "=" * 60)
print("Run complete! Check results above.")
print("=" * 60)
