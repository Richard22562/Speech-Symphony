import speech_recognition as sr
import pyttsx3
engine=pyttsx3.init()
engine.setProperty("rate",150)
def speak(text):
    engine.say(text)
    engine.runAndWait()
def speech_to_text():
    recognizer=sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak Now....")
        recognizer.adjust_for_ambient_noise(source)
        audio=recognizer.listen(source)
    try:
        print("Recognizing speech....")
        text=recognizer.recognize_google(audio,language="en-US")
        print(f"You said: {text}")
        return text
    except sr.UnkownValueError:
        print("Could not understand the audio")
    except sr.RequestError as e:
        print(f"API Error:{e}")
        return
def main():
    while True:
        print("----Welcome to Voice Recognizer----\n")
        print("1.Speak (speech-to-text)")
        print("2. Type (text-to-speech)")
        print("3. Quit")
        choice=input("choose option (1-3): ")
        if choice=="1":
            spoken_text=speech_to_text()
            if spoken_text:
                print("Speaking back what you said....")
                speak(spoken_text)
        elif choice=="2":
            typed_text=input("Enter text to speak: ")
            if typed_text.strip():
                print("Speaking your text....")
                speak(typed_text)
        elif choice=="3":
            print("Goodbye")
            break
        else:
            print("Invalid Choice, try again")
if __name__=="__main__":
    main()
