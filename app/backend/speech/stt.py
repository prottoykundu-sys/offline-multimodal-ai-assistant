import speech_recognition as sr

def listen_once():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        return r.recognize_google(audio)  # This is not offline
    except Exception:
        return "Speech recognition unavailable offline. Use text input."
