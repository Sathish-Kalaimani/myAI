import pyttsx3
import datetime
import speech_recognition as sr
import webbrowser
import urllib
import re
import wikipedia
import os
import glob
from weather import Weather, Unit

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0])

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >=0 and hour < 12:
        speak("Good Morning")
    elif hour >=12 and hour < 18:
        speak("Good Afternoon")
    else:
        speak("Good Evening")
    speak("I am Siri, how may I help you today")


def searchYoutube(video):
    searchText = video.split("play")[1].split(" on")[0].strip()
    #re.sub("play","",video).replace("on youtube","").strip()
    query = urllib.parse.urlencode({"search_query":searchText})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?"+query)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    speak("Launching browser to play the song")
    webbrowser.open("http://www.youtube.com/watch?v=" + search_results[0])

def checkWiki(query):
    keyWord = query.split("is"or"are")[1].split()[0].strip()
    result = wikipedia.summary(keyWord,sentences=2)
    speak("According to Wikipedia "+result)
    
def playSongFromLocal(songName):
    music_dir = "E:\\"
    songList=[]
    count=0
    for dir,subdir,files in os.walk(music_dir):
        for file in (name.lower() for name in files):
            song = re.sub("[^a-zA-Z0-9]+"," ",file)
            if glob.fnmatch.fnmatch(file,"*.mp3"):
                if songName in song:
                    count = count+1
                    songList.append(file)
                    
    
    if count >1:
        speak("There are {} songs in the directory, which one would you want to play?".format(count))
        speakList(songList)
    else:
        try:
            os.startfile(os.path.join(music_dir,songList[0]))
            speak("Playing {}".format(songName))
        except Exception as e:
            speak("Could not find the song in the system.")
        
            
    # allSongs = os.listdir(music_dir)
    # count=0
    # songList=[]
    # songs = {song.lower() for song in allSongs}
    # for songName in songs:
    #     if songName in songs:
    #         count = count + 1
    #         songList.append(songName)
    
    #if count >1:
        #speak("There are {} songs in the directory, which one would you want to play?".format(count))
        #speakList(songList)
    #else:
    #    os.startfile(os.path.join(music_dir,songList[0]))

def speakList(lists):
    for item in lists:
        speak(item)

def readUserCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        #r.pause_threshold = 1
        audio = r.listen(source)
            
    try:
        print("Recognizing")
        query = r.recognize_google(audio,language="en-in")
        print("User: "+query)
    except Exception as e:
        print(e)
        speak("I am unable to connect to the internet.")
        return "None"
    return query

if __name__ == "__main__":
    wishMe()
    command = readUserCommand().lower()

    if "who are you" in command:
        speak("I am Siri, your personal assistant")

    elif "time" in command:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak("The time is "+strTime)
        
    elif "open youtube" in command:
        speak("Opening Youtube")
        webbrowser.open("youtube.com")

    elif "play" in command or "on youtube" in command:
        if "on youtube" in command:
            searchYoutube(command)
        else:
            name = command.split("play")[1].strip()
            playSongFromLocal(name)

    elif "who" in command or "what" in command:
        checkWiki(command)
    
    elif "the laptop" in command or "the system" in command:
        if "shutdown" in command or "turn off" in command:
            os.system("shutdown /s /t 1")
        elif "restart" in command or "reboot" in command:
            os.system("shutdown /r /t 1")
        
    else:
        speak("Hmmmm.. I missed what you said. Could you please repeat?")
