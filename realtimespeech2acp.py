
import speech_recognition as sr
import pyttsx3
from deep_translator import GoogleTranslator
import sounddevice as sd
import soundfile as sf
import numpy as np
import tempfile
import os

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()

def display_language_options():
    print("\n🌐 Available languages:")
    # Added a range of languages and also the proper full form.
    langs = {"1": ("English", "en-US", "en"), "2": ("French", "fr-FR", "fr"), "3": ("German", "de-DE", "de"),
             "4": ("Spanish", "es-ES", "es"), "5": ("Hindi", "hi-IN", "hi"), "6": ("Japanese", "ja-JP", "ja"),
             "7": ("Arabic", "ar-SA", "ar"), "8": ("Dutch", "nl-NL", "nl")}
    for k, v in langs.items(): print(f"{k}. {v[0]} ({v[1]})")
    s = input("Select source language number: "); t = input("Select target language number: ")
    return langs.get(s, langs["1"])[1], langs.get(t, langs["2"])[2]

def record_audio(duration=5, sample_rate=16000):
    print("🎤 Please speak now...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype=np.int16)
    sd.wait()
    temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    sf.write(temp_file.name, recording, sample_rate)
    return temp_file.name

def speech_to_text(source_lang='en-US'):
    recogniser = sr.Recognizer()
    wave_file = record_audio(duration=5)
    try:
        with sr.AudioFile(wave_file) as source:
            audio = recogniser.record(source)
            print("🔄 Recognizing speech...")
            text = recogniser.recognize_google(audio, language=source_lang)
            print(f"✅ You said: {text}")
            return text
        
        # added more exception handling
    except sr.UnknownValueError:
        print("❌ Speech was unclear. Please try again.")
    except sr.RequestError as e:
        print(f"❌ Speech API Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected recognition error: {e}")
    finally:
        if os.path.exists(wave_file): os.remove(wave_file)
    return ""

def translate_text(text, source_language='auto', target_language='fr'):
    try:
        translated = GoogleTranslator(source=source_language, target=target_language).translate(text)
        print(f"🌍 Translated text: {translated}")
        return translated
    except Exception as e:
        print(f"❌ Translation Error: {e}")
        return text

def main():
    source_language, target_language = display_language_options()
    original_text = speech_to_text(source_language)
    if original_text:
        translated_text = translate_text(original_text, source_language=source_language[:2].lower(), target_language=target_language)
        speak(translated_text)
        print("✅ Translation spoken out!")

if __name__ == "__main__":
    main()