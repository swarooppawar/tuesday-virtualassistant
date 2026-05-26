# !apt-get update
# !apt-get install -y portaudio19-dev
# !pip install pyaudio
# !pip install SpeechRecognition pyaudio pyttsx3 setuptools

# Required packages:
# pip install SpeechRecognition pyaudio pyttsx3 setuptools

import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import musiclibrary
import wikipedia
import os

recognizer = sr.Recognizer()     # Use a single recognizer
engine = pyttsx3.init()     #Retrieves voices

def speak(text):        #Activating the speaker
    engine.say(text)    #Saying it out loud
    engine.runAndWait()   #Waiting for it to finish

#Greeting Code
def wishme():
    hour = int(datetime.datetime.now().hour)    #Fetching current hour
    if hour>=0 and hour<12:
        speak("Good Morning")
    elif hour>=12 and hour<18:
        speak("Good Afternoon")
    else:
        speak("Good Evening")
    speak("I am Tuesday, How can I help you?")


def processCommand(c):
    print("Command received:", c)
    # Example: open Google if user says "open google"
    if "open google" in c.lower():
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "open youtube" in c.lower():
        speak("Opening Youtube")
        webbrowser.open("https://www.youtube.com")

    elif "open Linkedin" in c.lower():
        speak("Opening Linkedin")
        webbrowser.open("https://www.linkedin.com")
    
    elif "open instagram" in c.lower():
        speak("Opening Instagram")
        webbrowser.open("https://www.instagram.com")


    elif c.lower().startswith("play"):
        # Strip "play " prefix and remove spaces to match library keys
        song = c.lower().replace("play", "", 1).strip().replace(" ", "")
        if song in musiclibrary.music:
            link = musiclibrary.music[song]
            speak(f"Playing {song}")
            webbrowser.open(link)
        else:
            speak(f"Sorry, I couldn't find {song} in the music library")


    elif "the time" in c.lower():
        # Formats time to e.g. "04:22 PM"
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")


    elif "wikipedia" in c.lower():
        speak("Searching on Wikipedia")
        # Strip all common filler words to isolate the actual search topic
        query = c.lower()
        for filler in ["search", "wikipedia", "on", "about", "for", "tell me", "who is", "what is"]:
            query = query.replace(filler, "")
        query = query.strip()

        if not query:
            speak("Please tell me what you want to search on Wikipedia.")
        else:
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                speak(results)
            except wikipedia.exceptions.DisambiguationError as e:
                speak(f"There are multiple results for {query}. Please be more specific.")
                print(f"Disambiguation options: {e.options[:5]}")
            except wikipedia.exceptions.PageError:
                speak(f"Sorry, I couldn't find a Wikipedia page for {query}.")
            except Exception as e:
                speak("Sorry, I ran into an error while searching Wikipedia.")
                print(f"Wikipedia error: {e}")

    
    elif "open vs code" in c.lower():
        codepath= "/Users/swarooppawar/Downloads/Visual Studio Code.app"
        os.system(f"open '{codepath}'")
        speak("Opening V S Code")
        
if __name__ == "__main__":
    wishme() #Calls the greeting code


    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=3)  # Helps with background noise
                print("Listening for wake word 'Tuesday'...")
                audio = recognizer.listen(source)   # Keeps listening until silence
                word = recognizer.recognize_google(audio) #Stimulates Google Speech Recognition

            print("Heard:", word)

            if "tuesday" in word.lower():   # More flexible check
                speak("Yes")

                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=1)
                    print("Tuesday Active... Say your command")
                    audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)

                command = recognizer.recognize_google(audio) #Stimulates Google Speech Recognition
                processCommand(command) 

        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.") #If the audio is not understood
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            print("Error:", e)
