import pyttsx3
import datetime
from datetime import date
import speech_recognition
import webbrowser as wb
import os
import requests #weather
import json #weather
import smtplib #email
import wikipedia
from newsapi import NewsApiClient
import pywhatkit as kit #openvideoyoutube
import pyautogui #screenshot
import time
from time import sleep
from win10toast import ToastNotifier
from geopy.geocoders import Nominatim #distance between 2 places
from geopy import distance


nanno = pyttsx3.init()
voice = nanno.getProperty('voices')
nanno.setProperty('voice',voice[1].id)

def speak(audio):
    print("nanno: " + audio)
    nanno.say(audio)
    nanno.runAndWait()
def time():
    Time = datetime.datetime.now().strftime("%I:%M:%p")
    speak(Time)
def today():
    today = date.today()
    current_day = today.strftime("%B %d, %Y")
    speak(current_day)
def welcome():
    hour = datetime.datetime.now().hour
    if hour >= 5 and hour < 12:
        speak("Good morning sir")
    elif hour >=12 and hour < 18:
        speak("Good afternoon sir")
    elif hour >=18 and hour < 24:
        speak("Good night sir")
    speak("How can I help you ?")
def command():
    nanno_ear=speech_recognition.Recognizer()
    with speech_recognition.Microphone() as mic:
        speech_recognition.pause_threshold=5
        audio=nanno_ear.listen(mic)
    try:
        query=nanno_ear.recognize_google(audio,language='en')
        print("You: " + query)
    except speech_recognition.UnknownValueError:
        print("I don't understand what you are saying")
        query = str(input("Your order is: "))
    return query
def current_weather():
    speak("Where do you want to know the weather?")
    ow_url = "http://api.openweathermap.org/data/2.5/weather?"
    city = command()
    if not city:
        pass
    api_key = "5328ae33e2d6ca570d746fb434b87efb"
    call_url = ow_url + "appid=" + api_key + "&q=" + city + "&units=metric"
    response = requests.get(call_url)
    data = response.json()
    print(data)
    if data["cod"] != "404":
        city_res = data["main"]
        current_temperature = city_res["temp"]
        current_pressure = city_res["pressure"]
        current_humidity = city_res["humidity"]
        suntime = data["sys"]
        sunrise = datetime.datetime.fromtimestamp(suntime["sunrise"])
        sunset = datetime.datetime.fromtimestamp(suntime["sunset"])
        wthr = data["weather"]
        weather_description = wthr[0]["description"]
        now = datetime.datetime.now()
        content = """
        Today is {day} month {month} year {year}
         The sun rises at {hourrise} hour {minrise} minutes
         The sun sets at {hourset} hour {minset} minutes
         Average temperature is {temp} degrees C
         The air pressure is {pressure} Pascals
         Humidity is {humidity}%
         The sky is clear today. Scattered rain forecast in some places.""".format(day = now.day,month = now.month, year= now.year, hourrise = sunrise.hour, minrise = sunrise.minute,
                                                                           hourset = sunset.hour, minset = sunset.minute,
                                                                           temp = current_temperature, pressure = current_pressure, humidity = current_humidity)
        speak(content)

    else:
        speak("Can't find your address")

def knowledge():
    try:
        speak("What do you want to know ?")
        text = command()
        contents = wikipedia.summary(text).split('\n')
        speak(contents[0])
        print(contents[0])

        speak("Thank you for listening !")
    except:
        speak("I have no knowledge of this subject")
def send_email():
    speak("Who do you want to send your email? Please type recipient's name")
    recipient = input("name :").strip()

    if recipient == "huy":
        speak("Please type the content")
        content = input("content:")
        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.ehlo()
        mail.starttls()
        mail.login('huyhua1322@gmail.com', 'jkhg1432##@')
        mail.sendmail('huyhua1322@gmail.com',
                       '19104017@student.hcmute.edu.vn', content.encode('utf-8'))
        mail.close()
        speak('Your email has just been sent')
    else:
        speak(f"I don't know who is {recipient}")

def end_program():
    speak("Goodbye sir ! See you later")
def news():
        newsapi = NewsApiClient(api_key='5840b303fbf949c9985f0e1016fc1155')
        speak("What topic you need the news about")
        topic = command()
        data = newsapi.get_top_headlines(
            q=topic, language="en", page_size=4)
        newsData = data["articles"]
        for y in newsData:
            speak(y["description"])
def location():
    speak ("What is the location")
    location = command()
    url = 'https://google.nl/maps/place/' +  location + '/&amp;'
    wb.get().open(url)
    print("here is the location of " + location)
def screenshot():
    sleep(5)
    pyautogui.screenshot(str("picture") + ".png").show()
def covid():
    r=requests.get("https://coronavirus-19-api.herokuapp.com/all")
    data = r.json()
    text = f'Cases: {data["cases"]} \nDeaths : {data["deaths"]}\nRecovered :{data["recovered"]}'

    while True:
        t = ToastNotifier()
        t.show_toast("Covid 19 update",text,duration=30)
        sleep(10)
def calculate():
    # Initialize Nominatim API
    geolocator = Nominatim(user_agent="geoapiExcercies")
    speak("Please input 2 places which you want to calculate the distance")

    # place input
    input_place1 = input("place1: ")
    input_place2 = input("place2: ")

    # get locations of the input strings
    place1 = geolocator.geocode(input_place1)
    place2 = geolocator.geocode(input_place2)
    print(place1)
    print(place2)

    # get latitude and longitude
    Loc1_lat, Loc1_lon = (place1.latitude), (place2.longitude)
    Loc2_lat, Loc2_lon = (place2.latitude), (place2.longitude)

    location1 = (Loc1_lat, Loc1_lon)
    location2 = (Loc2_lat, Loc2_lon)

    # calculate the distance
    print(distance.distance(location1, location2).km, "kms")

if __name__ == "__main__":
    welcome()
    while True:
        query = command().lower()
        if "google" in query:
            speak("What should I search boss ? ")
            search = command().lower()
            url = f"https://www.google.com/search?q={search}"
            wb.get().open(url)
            speak(f"Here is your {search} on google")
        elif "youtube" in query:
            speak("What should I search boss ? ")
            search = command().lower()
            url = f"https://www.youtube.com/search?q={search}"
            wb.get().open(url)
            speak(f"Here is your {search} on youtube")
            kit.playonyt(f"{search}")
        elif "open video" in query:
            beat= r"C:\Users\Admin\Desktop\beat\beat.mp4"
            os.startfile(beat)
        elif "time" in query:
            time()
        elif "today" in query:
            today()

        elif "weather" in query:
            current_weather()

        elif "define" in query:
            knowledge()
        elif "email" in query:
            send_email()
        elif "news" in query:
            news()
        elif "picture" in query:
            screenshot()
        elif "virus" in query:
            covid()
        elif "location" in query:
            location()
        elif "calculate" in query:
            calculate()

        elif "goodbye" in query:
            end_program()
            break










