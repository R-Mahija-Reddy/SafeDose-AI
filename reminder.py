import pyttsx3

def play_reminder(medicine):
    engine = pyttsx3.init()
    engine.say(f"Time to take your {medicine}")
    engine.runAndWait()