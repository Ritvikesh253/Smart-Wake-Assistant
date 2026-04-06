#!/usr/bin/env python3
"""Raw audio level test - shows EXACTLY what mic picks up"""
import pyaudio
import struct
import math
import os

print("🎤 RAW AUDIO LEVEL TEST")
print("=" * 50)
print()

pa = pyaudio.PyAudio()

# Find MacBook mic
macbook_mic = None
for i in range(pa.get_device_count()):
    info = pa.get_device_info_by_index(i)
    if 'MacBook' in info['name'] and 'Microphone' in info['name']:
        macbook_mic = i
        print(f"Using: {info['name']}")
        break

if macbook_mic is None:
    print("MacBook mic not found!")
    exit(1)

os.system('say "Say Jarvis NOW"')

stream = pa.open(
    rate=16000,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=512,
    input_device_index=macbook_mic
)

print()
print("Listening for 10 seconds...")
print("=" * 50)

# Record audio levels for 10 seconds
max_level = 0
total_frames = 0
high_frames = 0  # Frames with speech

for i in range(300):  # ~10 seconds at 16000Hz / 512 = ~31 frames/sec
    data = stream.read(512, exception_on_overflow=False)
    samples = struct.unpack_from('h' * 512, data)
    rms = math.sqrt(sum(s*s for s in samples) / len(samples))
    
    if rms > max_level:
        max_level = rms
    
    if rms > 500:  # Speech is usually > 500 RMS
        high_frames += 1
    
    total_frames += 1
    
    # Visual bar
    level = int(rms / 100)
    bar = '█' * min(level, 40)
    print(f'{bar:<40} {int(rms)}')

stream.close()
pa.terminate()

print()
print("=" * 50)
print(f"Max level: {int(max_level)}")
print(f"High frames (>500): {high_frames}/{total_frames} ({high_frames*100//total_frames}%)")
print()

if max_level < 500:
    print("❌ PROBLEM: Mic is barely picking up sound!")
    print("   Try:")
    print("   1. System Preferences > Sound > Input > Check MacBook Air Microphone")
    print("   2. Make sure Input Volume slider is at 100%")
    print("   3. Speak VERY close to keyboard (mic is near the screen hinge)")
elif max_level < 1500:
    print("⚠️ Audio is quiet - speak louder or closer to keyboard")
else:
    print("✅ Audio levels look good!")
    print("   If speech still fails, there might be a network issue with Google API")
