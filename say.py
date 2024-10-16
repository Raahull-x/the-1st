import pyttsx3

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Function to convert text to speech."""
    engine.say(text)  # Queue the text to be spoken
    engine.runAndWait()  # Block while processing all currently queued commands

# Example usage
if __name__ == "__main__":
    speak("Hello, I am ready to assist you.")