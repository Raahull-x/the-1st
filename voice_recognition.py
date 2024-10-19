import speech_recognition as sr
import webbrowser
import os
import subprocess
import platform
import random
import pygame  # Library to handle music playback
import pyttsx3 # convert word to speak
import threading
import urllib.parse
import requests
from pytube import YouTube

WAKE_WORD = "you"  # Define the wake word
MUSIC_FOLDER = r"D:\python\Voice_Recognition\musiclibrary"  # Update this with your music folder path

API_KEY = "fd760dd103c8406fa0eb798f9e909a88"
BASE_URL = "https://newsapi.org/v2/top-headlines?"

# Initialize pygame mixer for music playback
pygame.mixer.init() 
engine = pyttsx3.init()
# Get available voices
voices = engine.getProperty('voices')

# Set the voice to female
# On most systems, voices[1] is the female voice (index might differ depending on system)
engine.setProperty('voice', voices[1].id)

# Optional: Adjust the rate of speech if needed
engine.setProperty('rate', 150)  # You can increase or decrease the speed of speech# Get available voices

# Global variable to track the current song being played
current_song = None
paused = False

def speak(text):
    engine.say(text)
    engine.runAndWait()


def recognize_speech():
    recognizer = sr.Recognizer()

    while True:  # Loop to continuously listen for the wake word
         
         with sr.Microphone() as source:
            print("Listening for the wake word 'you'...")
            speak("Listening for the wake word 'you'...")

            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source)

            try:
                text = recognizer.recognize_google(audio)
                text = text.lower()
                print(f"You said: {text}")

                if WAKE_WORD in text:
                    print("Wake word detected!")
                    speak("What's your command?")  # System response
                    process_commands(recognizer)  # Call function to process command
                else:
                    print("Wake word not detected. Listening again...")
            
            except sr.UnknownValueError:
                print("Could not understand audio.")
            except sr.RequestError:
                print("Could not request results; check your network connection.")

def process_commands(recognizer):
    with sr.Microphone() as source:
        print("Listening for your command...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

        try:
            # Recognize the spoken command
            command = recognizer.recognize_google(audio)
            command = command.lower()
            print(f"Command recognized: {command}")
            speak(f"Command recognized: {command}")

            # Check the command and perform the corresponding action
            if "open youtube" in command:
                print("Opening YouTube...")
                speak("Opening YouTube...")
                webbrowser.open("https://www.youtube.com")
            elif "open google" in command:
                print("Opening Google...")
                speak("Opening Google...")
                webbrowser.open("https://www.google.com")
            elif "open github" in command:
                print("Opening GitHub...")
                speak("Opening GitHub...")
                webbrowser.open("https://www.github.com")
            elif "open chatgpt" in command:
                print("Opening Chatgpt...")
                speak("Opening Chatgpt...")
                webbrowser.open("https://chatgpt.com")
            elif "Open Movies" in command:
                print("Opening the Movies..")
                speak("Opening the Movies..")
                webbrowser.open("https://modlist.in")
            elif "Open News" in command:
                print("Opening the News..")
                speak("Opening the News..")
                webbrowser.open("")
            
            elif "open notepad" in command:
                print("Opening Notepad...")
                speak("Opening Notepad...")
                open_application("notepad")
            elif "open calculator" in command:
                print("Opening Calculator...")
                speak("Opening Calculator...")
                open_application("calc")
            elif "shut down" in command:
                print("Shutting down the system...")
                speak("Shutting down the system...")
                shut_down_system()
            elif "increase volume" in command:
                print("Increasing volume...")
                change_volume("up")
            elif "decrease volume" in command:
                print("Decreasing volume...")
                change_volume("down")
            elif "play music" in command:
                print("Playing music...")
                speak("Playing music...")
                play_music()
            elif "next song" in command:
                print("Skipping to the next song...")
                next_song()
            elif "pause music" in command:
                print("Pausing music...")
                pause_music()
            elif "resume music" in command:
                print("Resuming music...")
                resume_music()
            elif "stop music" in command:
                print("Stopping music...")
                speak("Stopping music...")
                stop_music()

            elif "play song" in command:
                song_name = command.replace("play song", "").strip()  # Get the song name from the command
                if song_name:
                    print(f"Playing {song_name} on YouTube...")
                    speak(f"Playing {song_name} on YouTube...")
                    play_music_from_youtube(song_name)
                else:
                    print("No song name provided.")
                    speak("Please provide the name of the song to play.")
            else:
                print("Command not recognized or not supported.")

        except sr.UnknownValueError:
            print("Could not understand command.")
        except sr.RequestError:
            print("Error processing command.")


# Helper function to play music from YouTube

def play_music_from_youtube(song_query):
    try:
        search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(song_query)}"
        webbrowser.open(search_url)  # This will open YouTube search results in the browser
        speak(f"Searching for {song_query} on YouTube and playing the first result.")
        
        # Fetch the first video URL from the search results using pytube
        yt_search = YouTube(f'https://www.youtube.com/results?search_query={urllib.parse.quote(song_query)}')
        video_url = yt_search.streams.filter(only_audio=True).first().url

        # Open the video in the browser
        webbrowser.open(video_url)
        speak(f"Playing {song_query} on YouTube.")
    
    except Exception as e:
        print(f"Error playing music: {e}")
        speak("Sorry, I couldn't play the music. Please try again.")

def get_news(query):
    url = f"{BASE_URL}q={query}&apiKey={API_KEY}"
    response = requests.get(url)
    news_data = response.json()
    return news_data

# Helper functions for system-level commands

def open_application(app_name):
    try:
        if platform.system() == "Windows":
            subprocess.run([app_name])
        elif platform.system() == "Linux":
            subprocess.run([app_name])
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", "-a", app_name])
        else:
            print("Unsupported Operating System.")
    except Exception as e:
        print(f"Error opening {app_name}: {e}")

def shut_down_system():
    try:
        if platform.system() == "Windows":
            os.system("shutdown /s /t 1")
        elif platform.system() == "Linux" or platform.system() == "Darwin":
            os.system("sudo shutdown now")
        else:
            print("Shutdown command not supported for this OS.")
    except Exception as e:
        print(f"Error shutting down: {e}")

def change_volume(direction):
    try:
        if platform.system() == "Windows":
            if direction == "up":
                os.system("nircmd.exe changesysvolume 5000")
            elif direction == "down":
                os.system("nircmd.exe changesysvolume -5000")
        elif platform.system() == "Linux":
            if direction == "up":
                os.system("amixer set Master 5%+")
            elif direction == "down":
                os.system("amixer set Master 5%-")
        elif platform.system() == "Darwin":  # macOS
            if direction == "up":
                os.system("osascript -e 'set volume output volume (output volume of (get volume settings) + 10)'")
            elif direction == "down":
                os.system("osascript -e 'set volume output volume (output volume of (get volume settings) - 10)'")
        else:
            print("Volume control not supported for this OS.")
    except Exception as e:
        print(f"Error changing volume: {e}")

# Music control functions

def play_music():
    global current_song
    if not pygame.mixer.music.get_busy():
        song = get_random_song()  # Get a random song from the music folder
        if song:
            current_song = song
            print(f"Playing {current_song}...")
            pygame.mixer.music.load(current_song)
            pygame.mixer.music.play()

def next_song():
    global current_song
    pygame.mixer.music.stop()  # Stop the current song
    song = get_random_song()  # Get a new random song
    if song:
        current_song = song
        print(f"Playing {current_song}...")
        pygame.mixer.music.load(current_song)
        pygame.mixer.music.play()

def pause_music():
    global paused
    if pygame.mixer.music.get_busy() and not paused:
        pygame.mixer.music.pause()
        paused = True
        print("Music paused.")

def resume_music():
    global paused
    if paused:
        pygame.mixer.music.unpause()
        paused = False
        print("Music resumed.")

def stop_music():
    pygame.mixer.music.stop()
    print("Music stopped.")

def get_random_song():
    try:
        songs = [os.path.join(MUSIC_FOLDER, song) for song in os.listdir(MUSIC_FOLDER) if song.endswith(('.mp3', '.wav'))]
        if songs:
            return random.choice(songs)
        else:
            print("No music files found in the specified folder.")
            return None
    except Exception as e:
        print(f"Error accessing music folder: {e}")
        return None
    
def main():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say the topic you want news on...")
        speak("Say the topic you want news on...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

        try:
            query = recognizer.recognize_google(audio).lower()
            print(f"You asked for news about: {query}")
            speak(f"You asked for news about: {query}")

            news_data = get_news(query)
            if news_data['status'] == 'ok':
                for article in news_data['articles']:
                    print(f"Title: {article['title']}")
                    print(f"Description: {article['description']}\n")
                    speak(f"Title: {article['title']}. Description: {article['description']}")
            else:
                print("No news found on this topic.")
                speak("No news found on this topic.")
        except sr.UnknownValueError:
            print("Could not understand your request.")
            speak("Sorry, I couldn't understand your request.")
        except sr.RequestError:
            print("Error in processing the request.")
            speak("There was an error in processing your request.")

if __name__ == "__main__":
    recognize_speech()