import speech_recognition as sr
import pyttsx3

print("Starting voice command program...", flush=True)
engine = pyttsx3.init()

def speak(text):
    print(f"Robot says: {text}", flush=True)
    engine.say(text)
    engine.runAndWait()

def listen_and_respond():
    recognizer = sr.Recognizer()
    print("Initializing microphone...", flush=True)
    try:
        with sr.Microphone() as source:
            print(
                "[Listening] Say 'move forward', 'stop', or 'turn left' "
                "within 5 seconds...",
                flush=True,
            )
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
    except sr.WaitTimeoutError:
        print("No speech detected. Run the program again and try speaking.", flush=True)
        return
    except (OSError, AttributeError) as error:
        print(f"Microphone error: {error}", flush=True)
        return

    try:
        print("Recognizing speech...", flush=True)
        command = recognizer.recognize_google(audio).lower()
        print(f"User Command: '{command}'")
        
        if "forward" in command:
            speak("Moving forward at half speed.")
        elif "stop" in command:
            speak("Emergency stop executed!")
        elif "left" in command:
            speak("Turning left 90 degrees.")
        else:
            speak(f"Command '{command}' not recognized.")
    except sr.UnknownValueError:
        speak("Sorry, I could not understand the speech.")
    except sr.RequestError as error:
        print(f"Speech recognition service error: {error}", flush=True)

if __name__ == "__main__":
    listen_and_respond()
