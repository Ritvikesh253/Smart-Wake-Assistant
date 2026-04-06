#!/usr/bin/env python3
"""Test MacBook Air mic directly"""
import pyaudio
import struct
import math

pa = pyaudio.PyAudio()

# Find MacBook mic
mac_mic = None
for i in range(pa.get_device_count()):
    info = pa.get_device_info_by_index(i)
    if 'MacBook' in info['name'] and info['maxInputChannels'] > 0:
        mac_mic = i
        print(f'Using MacBook mic: [{i}] {info["name"]}')
        break

if mac_mic is None:
    print("MacBook mic not found!")
    pa.terminate()
    exit(1)

print()
print('='*40)
print('🎤 SAY "HELLO JARVIS" INTO LAPTOP MIC')
print('   (NOT earphones - speak into laptop!)')
print('='*40)
print()

stream = pa.open(
    rate=16000,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=512,
    input_device_index=mac_mic
)

max_level = 0
for i in range(60):
    data = stream.read(512, exception_on_overflow=False)
    samples = struct.unpack_from('h' * 512, data)
    rms = math.sqrt(sum(s*s for s in samples) / len(samples))
    if rms > max_level:
        max_level = rms
    level = int(rms / 100)
    bar = '█' * min(level, 50)
    print(f'{bar:<50} {int(rms)}')

stream.close()
pa.terminate()

print()
print(f'Max level: {int(max_level)}')
if max_level > 1000:
    print('✅ Good levels! MacBook mic works!')
else:
    print('⚠️ Still quiet - speak louder into laptop')
