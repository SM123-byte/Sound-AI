import os
import subprocess
import tempfile

import sounddevice as sd  
import soundfile as sf
import speech_recognition as sr  
from deep_translator import GoogleTranslator

LANGUAGE_OPTIONS = {
    "1": ("French", "fr"),
    "2": ("German", "de"),
    "3": ("Latin", "la"),
    "4": ("Spanish", "es"),
    "5": ("Hindi", "hi"),
    "6": ("Japanese", "ja"),
    "7": ("Arabic", "ar"),
    "8": ("Dutch", "nl"),
}

def record_audio(duration: float = 5.0, samplerate: int = 16_000) -> str | None:
    print(f"\n🎤 Speak now... Recording for {duration} seconds")
    try:
        recording = sd.rec(
            int(duration * samplerate),
            samplerate=samplerate,
            channels=1,
            dtype="int16",
        )
        sd.wait()
    except Exception as e:
        print(f"❌ Recording failed: {e}")
        return None
    try:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        sf.write(temp_file.name, recording, samplerate)
        return temp_file.name
    except Exception as e:
        print(f"❌ Failed to save recording: {e}")
        return None
    
def speech_to_text(duration: float = 5.0, language: str = "en-US") -> str:
    recognizer = sr.Recognizer()
    audio_file = record_audio(duration)
    if not audio_file:
        return ""

    try:
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio, language=language)  # returns most likely transcription [web:3][web:4]
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

def translate_text(text: str, target_lang: str) -> str:
    if not text.strip():
        return ""
    try:
        translator = GoogleTranslator(source="auto", target=target_lang)
        translated = translator.translate(text)  # GoogleTranslator supports language codes like 'en', 'de' [web:6]
        print(f"\n🌍 Translation ({target_lang}): {translated}")
        return translated
    except Exception as e:
        print(f"❌ Translation error: {e}")
        return ""

def speak_mac(text: str) -> None:
    if not text.strip():
        return
    try:
        subprocess.run(["say", text], check=False)
    except Exception as e:
        print(f"❌ Speech error: {e}")

def display_language_options() -> str:
    print("\n🌐 Available translation languages:")
    for key, (name, code) in LANGUAGE_OPTIONS.items():
        print(f"{key}. {name} ({code})")

    choice = input("\nPlease select the target language number (default 1): ").strip() or "1"
    lang_name, lang_code = LANGUAGE_OPTIONS.get(choice, LANGUAGE_OPTIONS["1"])
    print(f"➡️ Target language: {lang_name} ({lang_code})")
    return lang_code

def main() -> None:
    print("🎙️ MacBook Speech Translator")
    print("=" * 35)

    try:
        duration_input = input("⏱️ Recording duration in seconds (default 5): ").strip()
        duration = float(duration_input) if duration_input else 5.0
    except ValueError:
        print("⚠️ Invalid duration. Using 5 seconds.")
        duration = 5.0

    target_lang = display_language_options()

    original_text = speech_to_text(duration=duration)
    if not original_text:
        print("⚠️ No recognized speech. Exiting.")
        return

    translated_text = translate_text(original_text, target_lang)
    if not translated_text:
        print("⚠️ No translation produced. Exiting.")
        return

    print("\n🔊 Speaking translation...")
    speak_mac(translated_text)
    print("✅ Done!")

if __name__ == "__main__":
    main()