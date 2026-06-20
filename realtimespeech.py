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

def record_audio(duration=5, sample_rate=16000):
    print("🎤 Please speak now in English...")
    print(f"⏺️ Recording for {duration} seconds...")

    recording= sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels= 1, dtype= np.int16)
    sd.wait()
    temp_file = tempfile.NamedTemporaryFile(suffix= '.wav', delete= False)
    sf.write(temp_file.name, recording, sample_rate)
    return temp_file.name

def speech_to_text():
    recogniser= sr.Recognizer()
    wave_file= record_audio(duration= 5)

    try:
        with sr.AudioFile(wave_file) as source:
            audio = recogniser.record(source)
        print("🔄 Recognizing speech...")
        text= recogniser.recognize_google(audio, language= 'en-US')
        print(f"✅ You said: {text}")
        return text
    
    except sr.UnknownValueError:
        print("❌ Could not understand the audio.")
    
    except sr.RequestError as e:
        print(f"❌ API Error: {e}")
    
    finally:
        if os.path.exists(wave_file):
            os.remove(wave_file)
    return ""

def translate_text(text, target_language= 'fr'):
    try:
        translated= GoogleTranslator(source= 'en', target= target_language).translate(text)
        print(f"🌍 Translated text: {translated}")
        return translated
    
    except Exception as e:
        print(f"❌ Translation Error: {e}")
        return text

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

def main():
    target_language= display_language_options()
    orginal_text= speech_to_text()

    if orginal_text:
        translated_text= translate_text(orginal_text, target_language= target_language)
        speak(translated_text)
        print("✅ Translation spoken out!")

if __name__ == "__main__":
    main()