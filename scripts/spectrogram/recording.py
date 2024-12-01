import socket
import time

import pyaudio
import wave

#record
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 60 * 60 * 3  #60 minutes

p = pyaudio.PyAudio()
frames = []

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                input_device_index=0)

print("*recording")
start_time = time.time()

try:
    while time.time() - start_time < RECORD_SECONDS:
        data = stream.read(CHUNK)
        frames.append(data)
except KeyboardInterrupt:
    print("*done recording")
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("*closed")

    wf = wave.open("output.wav", 'wb')
    wf.setnchannels(2)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(44100)
    wf.writeframes(b''.join(frames))
    wf.close()
    exit(1)

print("*done recording")
stream.stop_stream()
stream.close()
p.terminate()
print("*closed")

wf = wave.open("output.wav", 'wb')
wf.setnchannels(2)
wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
wf.setframerate(44100)
wf.writeframes(b''.join(frames))
wf.close()
