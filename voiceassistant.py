import speech_recognition as sr
from speech_recognition import AudioData
from deep_translator import GoogleTranslator
import sounddevice as sd
import soundfile as sf
import numpy as np
import tempfile
import subprocess
import os

# Record audio without PyAudio
def record_audio(duration=5, samplerate=16000):
    print(f"\n🎤 Speak now... Recording for {duration} seconds")

    recording = sd.rec(
        int(duration * samplerate),
        samplerate=samplerate,
        channels=1,
        dtype='int16'
    )

    sd.wait()

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".wav"
    )

    sf.write(
        temp_file.name,
        recording,
        samplerate
    )

    return temp_file.name

# Convert speech to text
def speech_to_text():
    recognizer = sr.Recognizer()

    audio_file = record_audio()

    try:
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(
            audio,
            language="en-US"
        )

        print(f"\n✅ You said: {text}")

        return text

    except sr.UnknownValueError:
        print("❌ Could not understand audio")
        return ""

    except sr.RequestError as e:
        print(f"❌ Speech API error: {e}")
        return ""

    finally:
        if os.path.exists(audio_file):
            os.remove(audio_file)

# Translate text
def translate_text(text, target_lang):
    try:
        translated = GoogleTranslator(
            source='auto',
            target=target_lang
        ).translate(text)

        print(f"\n🌍 Translation: {translated}")

        return translated

    except Exception as e:
        print(f"❌ Translation Error: {e}")
        return ""

# Speak using macOS built-in TTS
def speak_mac(text):
    try:
        subprocess.run(["say", text])
    except Exception as e:
        print(f"❌ Speech Error: {e}")

# Language menu
def display_language_options():
    print("\n🌐 Available translation languages:")
    print("1. French (fr)")
    print("2. German (de)")
    print("3. Latin (la)")
    print("4. Spanish (es)")
    print("5. Hindi (hi)")
    print("6. Japanese (ja)")
    print("7. Arabic (ar)")
    print("8. Dutch (nl)")
    
    choice = input("\nPlease select the target language number: ")

    language_dict = {
        "1": "fr",
        "2": "de",
        "3": "la",
        "4": "es",
        "5": "hi",
        "6": "ja",
        "7": "ar",
        "8": "nl"
    }

    return language_dict.get(choice, "fr")

# Main program
def main():
    print("🎙️ MacBook Speech Translator")
    print("=" * 35)

    target_lang = display_language_options()

    original_text = speech_to_text()

    if original_text:
        translated_text = translate_text(
            original_text,
            target_lang
        )

        if translated_text:
            print("\n🔊 Speaking translation...")
            speak_mac(translated_text)
            print("✅ Done!")

if __name__ == "__main__":
    main()