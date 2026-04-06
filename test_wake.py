#!/usr/bin/env python3
"""Test wake word detection"""
import pvporcupine
import pyaudio
import struct
import time
from config import PICOVOICE_API_KEY

print("🎤 Testing wake word detection - Say 'PICOVOICE'...")
print("(Will listen for 15 seconds)")

porcupine = pvporcupine.create(
    access_key=PICOVOICE_API_KEY,
    keywords=['picovoice'],  # Try "picovoice" - their company name
    sensitivities=[1.0]  # Maximum sensitivity
)

pa = pyaudio.PyAudio()

# Use MacBook mic for reliability
device_index = None
device_name = "Unknown"
for i in range(pa.get_device_count()):
    info = pa.get_device_info_by_index(i)
    if 'MacBook' in info['name'] and info['maxInputChannels'] > 0:
        device_index = i
        device_name = info['name']
        break

# Fallback to default if MacBook mic not found
if device_index is None:
    default_device = pa.get_default_input_device_info()
    device_index = default_device['index']
    device_name = default_device['name']

print(f"\\n🎤 Using: {device_name}")

stream = pa.open(
    rate=porcupine.sample_rate,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=porcupine.frame_length,
    input_device_index=device_index
)

print("\n" + "=" * 40)
print("🎙️  LISTENING NOW - Say 'PICOVOICE'...")
print("=" * 40 + "\n")

import math
start = time.time()
detected = False
max_level = 0

while time.time() - start < 15:
    try:
        pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
        pcm_unpacked = struct.unpack_from("h" * porcupine.frame_length, pcm)
        
        # Show audio level
        rms = math.sqrt(sum(s*s for s in pcm_unpacked) / len(pcm_unpacked))
        if rms > max_level:
            max_level = rms
        level = int(rms / 100)
        bar = '█' * min(level, 30)
        print(f'\r{bar:<30} {int(rms):5}', end='', flush=True)
        
        result = porcupine.process(pcm_unpacked)
        if result >= 0:
            print("\n🎯 PICOVOICE DETECTED! It's working!")
            detected = True
            break
    except Exception as e:
        print(f"Error: {e}")
        break

print(f"\n\nMax audio level: {int(max_level)}")

if not detected:
    print("⏰ Timeout - 'picovoice' not detected in 15 seconds")
    print("\nTips:")
    print("  - Say 'PEE-KOH-VOICE'")
    print("  - Make sure mic is not muted")
    print("  - Try speaking closer to mic")

stream.close()
pa.terminate()
porcupine.delete()
