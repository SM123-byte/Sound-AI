#pip install sounddevice scipy SpeechRecognition matplotlib numpy
import threading
import sys
import time
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
import speech_recognition as sr
from speech_recognition import AudioData

stop_event = threading.Event()

RATE = 16000
CHANNELS = 1

audio_frames = []


def wait_for_enter():
    input("\n🎤 Press Enter to stop recording...\n")
    stop_event.set()


def spinner():
    chars = '|/-\\'
    i = 0
    while not stop_event.is_set():
        sys.stdout.write(f'\r🔴 Recording... {chars[i % 4]}')
        sys.stdout.flush()
        i += 1
        time.sleep(0.1)

    print("\r✅ Recording complete!          ")


def callback(indata, frames, time_info, status):
    if status:
        print(status)

    audio_frames.append(indata.copy())

    if stop_event.is_set():
        raise sd.CallbackStop()


def record_audio():
    print("\nSpeak into your microphone...")

    threading.Thread(target=wait_for_enter, daemon=True).start()
    threading.Thread(target=spinner, daemon=True).start()

    with sd.InputStream(
        samplerate=RATE,
        channels=CHANNELS,
        dtype='int16',
        callback=callback
    ):
        while not stop_event.is_set():
            sd.sleep(100)

    audio_data = np.concatenate(audio_frames, axis=0)

    return audio_data


def save_audio(data, filename="recording.wav"):
    write(filename, RATE, data)
    print(f"💾 Saved: {filename}")


def transcribe(data):
    recognizer = sr.Recognizer()

    audio_bytes = data.tobytes()
    audio = AudioData(audio_bytes, RATE, 2)

    try:
        text = recognizer.recognize_google(audio)
        print(f"📝 Transcription: {text}")

    except sr.UnknownValueError:
        print("❌ Could not understand audio")

    except sr.RequestError as e:
        print(f"❌ API Error: {e}")


def plot_waveform(data):
    samples = data.flatten()

    time_axis = np.linspace(0, len(samples) / RATE, len(samples))

    plt.figure(figsize=(10, 4))
    plt.plot(time_axis, samples)

    plt.title("Your Voice Waveform")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude")

    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def main():
    print("=" * 40)
    print("🎙️ HELLO AI, CAN YOU HEAR ME?")
    print("=" * 40)

    audio_data = record_audio()

    save_audio(audio_data)

    transcribe(audio_data)

    plot_waveform(audio_data)


if __name__ == "__main__":
    main()