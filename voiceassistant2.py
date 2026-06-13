import speech_recognition as sr
import pyttsx3
import sounddevice as sd
import numpy as np
import tempfile
import os
from scipy.io.wavfile import write
from datetime import datetime

engine = pyttsx3.init()
# FIRST WORD is lowercase; Second WORD is uppercase
engine.setProperty('rate', 150)

def speak(text):
    print(f"🤖 {text}")
    engine.say(text)
    engine.runAndWait()

def get_audio():
    recogniser= sr.Recognizer()
    sample_rate= 16000
    duration= 5
    
    print("🎤 Speak now...")
    recording= sd.rec(int(duration * sample_rate), samplerate= sample_rate, channels= 1, dtype= 'int16')
    sd.wait()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
        write(temp_wav, sample_rate, recording)

        try:
            with sr.AudioFile(temp_wav.name) as source:
                audio= recogniser.record(source)

            command= recogniser.recognize_google(audio)
            print(f"✅ You said: {command}")
            return command.lower()
        
        except sr.UnknownValueError:
            print("❌ Could not understand.")

        except sr.RequestError as e:
            print(f"❌ API Error: {e}.")
        
        finally:
            os.unlink(temp_wav.name)

    return ""

def respond_to_command(command):

    if "hello" in command:
        speak("Hi there! How can I help you there?")

    elif "your name" in command:
        speak("I am your Python Voice Assistant")
    
    elif "time" in command:
        now= datetime.now().strftime("%H:%M")
        speak(f"Time is {now}")
    
    elif "exit" in command or "stop" in command:
        speak("Goodbye!")
        return False
    
    else:
        speak("I'm not sure how to help you with that.")

    return True

def main():
    speak("Voice Assistant Activated. Say something!")

    while True:
        command = get_audio()
        if command and not respond_to_command(command):
            break

if __name__ == "__main__":
    main()