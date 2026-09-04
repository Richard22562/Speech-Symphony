import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt
FORMAT=pyaudio.paInt16
CHANNELS=3
RATE=44100
CHUNK=1024
RECORD_SECONDS=5
WAVE_OUTPUT_FILENAME="output.wav"
audio=pyaudio.PyAudio()
stream=audio.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True, frames_per_buffer=CHUNK)
print("Recording........")
frames=[]
for i in range(int(RATE/CHUNK * RECORD_SECONDS)):
    data=stream.read(CHUNK)
    frames.append(data)
print("Recording Stopped")
stream.stop_stream()
stream.close()
audio.terminate()
wf=wave.open(WAVE_OUTPUT_FILENAME,"wb")
wf.setnchannels(CHANNELS)
wf.setsampwidth(audio.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b"".join(frames))
wf.close()
audio_data=np.frombuffer(b"".join(frames),dtype=np.int16)
plt.figure(figsize=(10,4))
plt.plot(audio_data)
plt.title("Recorded Audio Waveform")
plt.xlabel("Sample Index")
plt.ylabel("Amplitude")
plt.show()