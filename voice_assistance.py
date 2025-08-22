import asyncio
from mistralai import Mistral
import pyttsx3
import speech_recognition as sr

client = Mistral(api_key="9ylVIZ5MlbWpkrU7vn8GXtRrZdoGpVEP")

recognizer = sr.Recognizer()

def speak(text: str):
    if not text:
        return
    print(f"Assistant: {text}")
    engine = pyttsx3.init()  
    engine.say(str(text))
    engine.runAndWait()
    engine.stop()

async def ask_mistral(prompt: str):
    print("Generating response...")
    try:
        response = client.chat.complete(
            model="mistral-small",
            messages=[{"role": "user", "content": prompt}]
        )
        text = response.choices[0].message.content
        return str(text).strip()
    except Exception as e:
        print("⚠️ Error with Mistral:", e)
        return "Sorry, I couldn't process that right now."

def listen():
    with sr.Microphone() as source:
        print("🎤 Speak now...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"User: {text}")
            return text
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            print("⚠️ Error with Speech Recognition:", e)
            return None

async def main():
    speak("Hello Quivir! I am your voice assistant. How can I help you today?")
    while True:
        user_input = listen()
        if user_input:
            if user_input.lower() in ["quit", "exit", "stop"]:
                speak("Goodbye!")
                break

            response = await ask_mistral(user_input)
            speak(response)

if __name__ == "__main__":
    asyncio.run(main())
