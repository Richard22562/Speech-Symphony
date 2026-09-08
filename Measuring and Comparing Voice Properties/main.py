# pyrefly: ignore [missing-import]
from pyaudio import Stream
import threading,sys
# pyrefly: ignore [missing-import]
import pyaudio, numpy as np, matplotlib.pyplot as plt

# pyrefly: ignore [missing-import]
#from speech_recognition import AudioData

stop_event=threading.Event()

def wait_enter():
    input()
    stop_event.set()

def record_audio(label, rate=16000, chunk=1024):
    stop_event.clear()
    p=pyaudio.PyAudio()
    stream=p.open(format=pyaudio.paInt16, channels=1, rate=rate,input=True, frames_per_buffer=chunk)
    frame=[]
    print(f"\n🎙️ {label}\n Press Enter to stop...")
    threading.Thread(target=wait_enter, daemon=True).start()

    print("📍Recording....",end="",flush=True)
    while not stop_event.is_set():
        frame.append(stream.read(chunk, exception_on_overflow=False))
        print(".", end="", flush=True)
    print("✅")
    stream.stop_stream()
    stream.close()
    p.terminate()
    width=p.get_sample_size(pyaudio.paInt16)
    return b''.join(frame), rate, width


def analyze_audio(data,rate):
    sample=np.frombuffer(data, dtype=np.int16)
    return {
        'duration': len(sample) / rate,
        'avg_volume': np.mean(np.abs(sample)),
        'max_volume': np.max(np.abs(sample)),
        'samples': sample
    }

def display_stats(stats, label):
    print(f"\n{'─'*40}\n📊 {label}\n{'─'*40}")
    print(f"⏱️ Duration: {stats['duration']:.2f}s")
    print(f"🔉 Avg Amplitude: {stats['avg_volume']:.0f}")
    print(f"🔊 Max Amplitude: {stats['max_volume']:.0f}")

def compare(stats1, stats2):
    print("\n" + "="*40 + "\n📈 COMPARISON RESULTS\n" + "="*40)
    def diff(val1, val2): return ((val1 - val2) / val2) * 100
    longer = "Recording 1" if stats1['duration'] > stats2['duration'] else "Recording 2"
    louder = "Recording 1" if stats1['avg_volume'] > stats2['avg_volume'] else "Recording 2"
    dur_diff = diff(stats1['duration'], stats2['duration']) if longer=="Recording 1" else diff(stats2['duration'], stats1['duration'])
    vol_diff = diff(stats1['avg_volume'], stats2['avg_volume']) if louder=="Recording 1" else diff(stats2['avg_volume'], stats1['avg_volume'])
    print(f"⏱️ {longer} is longer by {dur_diff:.1f}%")
    print(f"🔊 {louder} is louder by {vol_diff:.1f}%")
def plot_both(stats1, stats2, rate):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6))
    for ax, stats, color, title in [
        (ax1, stats1, 'blue', "Recording 1 (Normal)"),
        (ax2, stats2, 'red', "Recording 2 (Modified)")
    ]:
        t = np.linspace(0, len(stats['samples'])/rate, len(stats['samples']))
        ax.plot(t, stats['samples'], color=color, linewidth=0.5)
        ax.set_title(f"{title} - {stats['duration']:.2f}s, Avg: {stats['avg_volume']:.0f}")
        ax.set_ylabel("Amplitude"); ax.grid(True, alpha=0.3); ax.set_ylim(-35000, 35000)
    ax2.set_xlabel("Time (seconds)")
    plt.tight_layout(); plt.show()
def main():
    print("="*40 + "\n🎤 VOICE ANALYSIS LAB\n" + "="*40)
    print("Record twice and compare your voice!")

    audio1, rate, width = record_audio("Recording 1: Speak NORMALLY")
    stats1 = analyze_audio(audio1, rate)
    display_stats(stats1, "Recording 1 Results")

    input("\n➡️ Press Enter, then speak LOUDER or FASTER...")
    audio2, _, _ = record_audio("Recording 2: CHANGE your voice!")
    stats2 = analyze_audio(audio2, rate)
    display_stats(stats2, "Recording 2 Results")

    compare(stats1, stats2)
    plot_both(stats1, stats2, rate)

if __name__ == "__main__":
    main()