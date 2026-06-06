# Instead of the comparing one, I decided to make a better in depth one for the single recording
import threading
import sys
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import speech_recognition as sr
from speech_recognition import AudioData

# Dependency check
try:
    import sounddevice
    import numpy
    import matplotlib
    import speech_recognition
except ImportError as e:
    print(f"❌ Missing library: {e.name}")
    print("\n📦 Install command:")
    print("pip install sounddevice numpy matplotlib SpeechRecognition")
    sys.exit(1)

stop_event = threading.Event()


def wait_for_enter():
    input()
    stop_event.set()


def record_audio(label):
    stop_event.clear()

    sample_rate = 16000
    recording = []

    def callback(indata, frames, time, status):
        if status:
            print(status)
        recording.append(indata.copy())

    print(f"\n🎤 {label}")
    print("   Press Enter to stop...")

    threading.Thread(target=wait_for_enter, daemon=True).start()

    print("🔴 Recording", end="", flush=True)

    with sd.InputStream(
        samplerate=sample_rate,
        channels=1,
        dtype='int16',
        callback=callback
    ):
        while not stop_event.is_set():
            print(".", end="", flush=True)
            sd.sleep(200)

        print(" ✅")

        audio_data = np.concatenate(recording, axis=0)

    return audio_data.tobytes(), sample_rate, 2  # int16 = 2 bytes


def analyze_audio(data, rate):
    samples = np.frombuffer(data, dtype=np.int16)

    return {
        "duration": len(samples) / rate,
        "avg_volume": np.mean(np.abs(samples)),
        "max_volume": np.max(np.abs(samples)),
        # Added for digital samples captured
        "sample_count": len(samples),
        "bit_depth": 16,
        "samples": samples
    }


def transcribe(data, rate, width):
    recognizer = sr.Recognizer()

    try:
        audio = AudioData(data, rate, width)
        return recognizer.recognize_google(audio)

    except sr.UnknownValueError:
        return "[Speech not understood]"

    except sr.RequestError:
        return "[Google Speech service unavailable]"

    except Exception:
        return "[Could not transcribe]"


def display_stats(stats, text):
    print(f"\n{'─' * 40}")
    print("📊 AUDIO ANALYSIS RESULTS")
    print(f"{'─' * 40}")
    print(f"⏱️  Duration:      {stats['duration']:.2f} sec")
    # Printed Sample Rate for reference within the layout
    print(f"🎚️  Sample Rate:   16000 Hz")
    print(f"💾 Bit Depth:     {stats['bit_depth']}-bit")
    print(f"📈 Samples:       {stats['sample_count']:,}")
    print(f"🔊 Avg Volume:    {stats['avg_volume']:.0f}")
    print(f"🔊 Max Volume:    {stats['max_volume']:.0f}")
    print(f"📝 Transcript:    {text}")


def plot_waveform(stats, rate):
    plt.figure(figsize=(10, 4))

    t = np.linspace(
        0,
        len(stats['samples']) / rate,
        len(stats['samples'])
    )

    plt.plot(t, stats['samples'])

    plt.title("Voice Waveform")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude")
    plt.grid(True)

    plt.tight_layout()
    plt.show()


def main():
    print("=" * 45)
    print("🎙️ VOICE CAPTURE & SPEECH RECOGNITION")
    print("=" * 45)

    print("\nThis program demonstrates:")
    print("• Audio Capture")
    print("• Audio Digitization")
    print("• Speech Recognition")
    print("• Waveform Visualization")

    audio, rate, width = record_audio(
        "Record your voice"
    )

    stats = analyze_audio(audio, rate)

    text = transcribe(audio, rate, width)

    display_stats(stats, text)

    plot_waveform(stats, rate)

    print("\n✅ Analysis Complete")


if __name__ == "__main__":
    main()