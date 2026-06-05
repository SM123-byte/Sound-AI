import threading
import sys
import time
import wave

import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import speech_recognition as sr
from speech_recognition import AudioData

RATE = 16000
CHANNELS = 1

stop_event = threading.Event()


def wait_for_enter():
    input("\n🎤 Press Enter to stop recording...\n")
    stop_event.set()

def spinner():
    chars = "|/-\\"
    i = 0

    while not stop_event.is_set():
        sys.stdout.write(f"\r🔴 Recording... {chars[i % 4]}")
        sys.stdout.flush()
        i += 1
        time.sleep(0.1)

    print("\r✅ Recording complete!          ")

# Changed the recording function 

def record_audio():
    # Changed 
    recorded_chunks = []

    def callback(indata, frames, time_info, status):
        if status:
            print(status)

        recorded_chunks.append(indata.copy())

        if stop_event.is_set():
            raise sd.CallbackStop

    threading.Thread(target=wait_for_enter, daemon=True).start()
    threading.Thread(target=spinner, daemon=True).start()

    with sd.InputStream(samplerate=RATE, channels=CHANNELS, dtype='int16', callback=callback
    ):
        while not stop_event.is_set():
            time.sleep(0.1)

    # Convert audio into chunks
    audio_array = np.concatenate(recorded_chunks, axis=0)

    return (audio_array.tobytes(), RATE, 2)

def save_audio(data, rate, width, filename="recording.wav"):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(width)
        wf.setframerate(rate)
        wf.writeframes(data)

    print(f"💾 Saved: {filename}")

def transcribe(data, rate, width):
    recognizer = sr.Recognizer()
    audio = AudioData(data, rate, width)

    try:
        text = recognizer.recognize_google(audio)
        print(f"\n📝 Transcription:\n{text}")

    except sr.UnknownValueError:
        print("❌ Could not understand audio")

    except sr.RequestError as e:
        print(f"❌ API Error: {e}")

def plot_waveform(data, rate):

    samples = np.frombuffer(data, dtype=np.int16)
    time_axis = np.linspace(0, len(samples) / rate, len(samples))

    plt.figure(figsize=(12, 4))
    plt.plot(time_axis, samples, color="royalblue")
    plt.fill_between(time_axis, samples, alpha=0.2)

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
    print("\nSpeak into your microphone...")

    audio_data, rate, width = record_audio()
    save_audio(audio_data, rate, width)
    transcribe(audio_data, rate, width)
    plot_waveform(audio_data, rate)

if __name__ == "__main__":
    main()