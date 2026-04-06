# clap_detector.py - Mac Optimized
import pyaudio
import numpy as np
import time
import threading
from config import CLAP_THRESHOLD, CLAP_TIMEOUT, MIN_CLAP_GAP, SAMPLE_RATE

class ClapDetector:
    def __init__(self):
        self.threshold = CLAP_THRESHOLD
        self.timeout = CLAP_TIMEOUT
        self.min_clap_gap = MIN_CLAP_GAP
        self.clap_count = 0
        self.pa = pyaudio.PyAudio()
        self.stream = None
        self.listening = False
        
    def detect_clap(self, data):
        """Detect clap based on audio amplitude"""
        audio_data = np.frombuffer(data, dtype=np.int16)
        volume = np.abs(audio_data).mean()
        max_volume = np.abs(audio_data).max()
        
        # Detect clap if volume exceeds threshold
        return max_volume > (self.threshold * 32767)
    
    def count_claps(self):
        """Count claps within timeout period"""
        self.clap_count = 0
        self.last_clap_time = None
        
        try:
            self.stream = self.pa.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=SAMPLE_RATE,
                input=True,
                frames_per_buffer=1024,
                input_device_index=self._get_default_input_device()
            )
            
            print("👂 Listening for claps...")
            start_time = time.time()
            
            while time.time() - start_time < self.timeout:
                try:
                    data = self.stream.read(1024, exception_on_overflow=False)
                    
                    if self.detect_clap(data):
                        current_time = time.time()
                        
                        # Check if enough time passed since last clap
                        if (self.last_clap_time is None or 
                            current_time - self.last_clap_time > self.min_clap_gap):
                            
                            self.clap_count += 1
                            self.last_clap_time = current_time
                            print(f"👏 Clap detected! Count: {self.clap_count}")
                            
                            # Stop if we have 3 claps (max we care about)
                            if self.clap_count >= 3:
                                break
                                
                except Exception as e:
                    print(f"Error reading audio: {e}")
                    break
                    
        except Exception as e:
            print(f"Error opening audio stream: {e}")
        finally:
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
                
        return self.clap_count
    
    def _get_default_input_device(self):
        """Get MacBook mic for reliability, fallback to system default"""
        try:
            # Prioritize MacBook mic
            for i in range(self.pa.get_device_count()):
                info = self.pa.get_device_info_by_index(i)
                if 'MacBook' in info['name'] and info['maxInputChannels'] > 0:
                    return i
            # Fallback to default
            default_device = self.pa.get_default_input_device_info()
            return default_device['index']
        except:
            return None
    
    def wait_for_claps(self):
        """Wait for clap sequence and return count"""
        return self.count_claps()
    
    def cleanup(self):
        """Clean up audio resources"""
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.pa.terminate()
