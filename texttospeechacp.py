# Code with recognising a response or joke

import speech_recognition as sr
import pyttsx3
from deep_translator import GoogleTranslator
import sounddevice as sd
import soundfile as sf 
import numpy as np
import tempfile
import os
# Used for the random nature of the joke order
import random

engine = pyttsx3.init()
engine.setProperty('rate', 150)

# Had to AI these jokes and responses because I couldn't think of any:)
responses = [
    "Interesting! Let me translate that.",
    "Processing your speech now.",
    "I heard you loud and clear.",
    "Working on your translation.",
    "That's a good one!"
]
jokes = [
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "Why did the computer go to therapy? It had too many bytes of emotional baggage.",
    "I would tell you a Python joke, but it might not have enough indentation.",
    "Why was the robot tired? It had a hard drive.",
    "Why did the coder break up with the keyboard? There was no connection."
]

# Function for the commands such as the joke or commands
def handle_commands(text):
    text = text.lower()

    if "tell me a joke" in text:
        joke = random.choice(jokes)
        print(f"😂 {joke}")
        speak(joke)
        return True

    elif "speak faster" in text:
        current_rate = engine.getProperty('rate')
        engine.setProperty('rate', current_rate + 25)
        speak("Speech speed increased.")
        return True

    elif "speak slower" in text:
        current_rate = engine.getProperty('rate')
        engine.setProperty('rate', max(75, current_rate - 25))
        speak("Speech speed decreased.")
        return True

    elif "stop speaking" in text:
        engine.stop()
        print("⏹ Speech stopped.")
        return True
    return False

def speak(text):
    # Convert text to speech
    print(f"🔊 Speaking: {text}")
    engine.say(text)
    engine.runAndWait()

def record_audio(duration= 5, sample_rate= 16000):
    print("🎤 Please speak now in English...")
    audio = sd.rec(int(duration*sample_rate), samplerate= sample_rate, channels= 1, dtype= 'int16')
    sd.wait()
    temp_file = tempfile.NamedTemporaryFile(delete= False, suffix= ".wav")
    sf.write(temp_file.name, audio, sample_rate)
    return temp_file.name

def speech_to_text():
    recognizer = sr.Recognizer()
    try:
        audio_file= record_audio()
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
            print("🔄 Recognizing speech...")
            text= recognizer.recognize_google(audio, language= "en-US")
            print(f"✅ You said: {text}")
            os.remove(audio_file)
            return text
        
    except sr.UnknownValueError:
        print("❌ Could not understand the audio.")
        return ""
    
    except sr.RequestError as e:
        print(f"❌ Speech Recognition Error: {e}")
        return ""

    except Exception as e:
        print(f"❌ Error: {e}")
        return ""
    
def translate_text(text, target_language= "fr"):
    try:
        translated= GoogleTranslator(source= "auto", target= target_language).translate(text)
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
    
    choice = input(
        "\nPlease select the target language number (1-8): "
    )

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
    print("🌐 Speech Translator Plus")
    print("-" * 40)

    target_language = display_language_options()

    while True:
        original_text = speech_to_text()
        if not original_text:
            continue
        if original_text.lower() == "quit":
            speak("Goodbye!")
            break
        if handle_commands(original_text):
            continue
        speak(random.choice(responses))

        translated_text = translate_text(
            original_text,
            target_language
        )

        if translated_text:
            speak(translated_text)
            print("\n✅ Translation completed successfully!")

if __name__ == "__main__":
    main()