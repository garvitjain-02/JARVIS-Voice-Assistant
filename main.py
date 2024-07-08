import speech_recognition as sr
import webbrowser
import requests
import pyttsx3
import music_library
import subprocess
import platform
import pyjokes
import datetime
from config import newsapi
from config import weatherapi
import os

recognizer=sr.Recognizer()
engine=pyttsx3.init()

# Function to open any application
def open_application(app_name):
    try:
        if platform.system() == "Windows":
            subprocess.run(["start", app_name], shell=True)
    except Exception as e:
        print(f"An error occurred: {e}")

# function for speaking
def speak(text):
    engine.say(text)
    engine.runAndWait()

# function to get news updates
def get_news():
    r=requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")  
    #  Check if the request was successful
    
    if r.status_code == 200:
        data = r.json()  #  Parse the response as JSON
        articles = data['articles']  #  Extract the articles

    #  Print the headlines
        for i, article in enumerate(articles, 1):
            speak(f"{i}. {article['title']}")
    else:
        speak("Failed to fetch the headlines")    

# Function to get weather updates
def get_weather(city):
    city_name = city
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    complete_url = base_url + "appid=" + weatherapi + "&q=" + city_name + "&units=metric"
    response = requests.get(complete_url)

    if response.status_code == 200:
        data = response.json()
        main = data['main']
        weather_description = data['weather'][0]['description']
        temperature = main['temp']
        humidity = main['humidity']
        pressure = main['pressure']
        speak(f"The weather in {city_name} is {weather_description} with a temperature of {temperature}°C, humidity of {humidity}%, and pressure of {pressure} hPa.")
    else:
        speak("City not found.")

def processCommand(c):

    # To open any website on Internet
    sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"],
             ["google", "https://www.google.com"], ["gmail", "https://gmail.com"],
             ["linkedin", "https://linkedin.com"], ["facebook", "https://facebook.com"], ]
    for site in sites:
        if f"Open {site[0]}".lower() in c.lower():
            speak(f"Opening {site[0]} sir...")
            webbrowser.open(site[1])

    # To get a random joke
    if "joke" in c.lower():
        joke = pyjokes.get_joke()
        print(f"The joke is:- {joke}")
        speak(joke)

    # To repeat anything
    elif c.lower().startswith("say"):
        say=c.lower().replace("say", "")
        print(say)
        speak(say)    

    # To Open any app in your desktop
    elif c.lower().startswith("open"):
        app=c.lower().split(" ")[1]
        open_application(app)

    # To fetch the current time
    elif "the time" in c:
        hour = datetime.datetime.now().strftime("%H")
        mins = datetime.datetime.now().strftime("%M")
        speak(f"Sir time is {hour} bajke {mins} minutes")    
    
    # To play the song from your own library
    elif c.lower().startswith("play"):
        song=c.lower().split(" ")[1]
        speak(f"Playing {song}")
        webbrowser.open(music_library.music[song])  

    # To search something on google
    elif c.lower().startswith("search"):
        item=c.lower().replace("search", "")
        webbrowser.open(f"https://www.google.com/search?q={item}")  

    # To fetch the latest news
    elif "news" in c.lower():
        print("Fetching the news...")
        get_news()

    # To fetch weather updates
    elif "weather" in c.lower():
        city=c.lower().split(" ")[2]
        print("Fetching the weather...")
        get_weather(city)


if __name__=="__main__":
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    speak("Initializing Jarvis...")

    while True:
        #  obtain audio from the microphone
        r = sr.Recognizer()

        #  recognize speech using Google
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source,timeout=2,phrase_time_limit=1)
            print("Recognizing...")    
            word= r.recognize_google(audio)
            if(word.lower()=="jarvis"):
                speak("haa maa lick")

                #  Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Listening Command...")
                    audio = r.listen(source)
                    command= r.recognize_google(audio)
                    processCommand(command)

        except Exception as e:
            print("Error; {0}".format(e))