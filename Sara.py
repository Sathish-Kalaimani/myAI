import pyttsx3
import datetime
import speech_recognition as sr
import webbrowser
import urllib
import re
import wikipedia
import os
import pathlib
import glob
from weather import Weather, Unit
from Notifier import notify
from Railway import getLiveStatus, getTrainName

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0])

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    
    filepath = pathlib.Path("test.txt")
    
    
    if filepath.exists():
        milliSec = os.path.getctime(os.getcwd()+"/test.txt")
        createDtStr = datetime.datetime.fromtimestamp(milliSec).strftime("%Y-%m-%d")
        createdDt = datetime.datetime.strptime(createDtStr,"%Y-%m-%d")

        if createdDt.date() == datetime.date.today():
            speak(getHour()+". Welcome Back Sir")
        else:
            os.remove(os.getcwd()+"/test.txt")
            speak(getHour()+"Sir")
    else:
        temp_file = open(os.getcwd()+"/test.txt","w")
        temp_file.close()
        speak(getHour()+"Sir")

def getHour():
    
    hour = int(datetime.datetime.now().hour)
    if hour >=0 and hour < 12:
        return "Good Morning"
    elif hour >=12 and hour < 18:
        return "Good Afternoon"
    else:
        return "Good Evening"
    

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

def calculate(audio,method):
    num1 = int(audio.split("calculate")[1].split()[0].strip())
    num2 = int(audio.split(method)[1].strip())

    speak("The {} of {} and {} is {}".format(method,num1, num2,num1+num2))

def speakList(lists):
    for item in lists:
        speak(item)


def readUserCommand():
    query=""
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.adjust_for_ambient_noise(source)
            #r.pause_threshold = 1
            audio = r.listen(source,timeout=10)
    
    
            print("Recognizing")
            query = r.recognize_google(audio,language="en-in")
            print("User: "+query)

    except (sr.WaitTimeoutError,sr.UnknownValueError):
        print("No input")
        
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        speak("I am unable to connect to the internet.")
        
    return query

def processCommands(audio):
    
    if "who are you" in audio:
        speak("I am Sara, your personal assistant")
    
    elif "hi" in audio:
        speak("Hello Sir!!!")

    elif "time" in audio:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak("The time is "+strTime)
        
    elif "open youtube" in audio:
        speak("Opening Youtube")
        webbrowser.open("youtube.com")

    elif "play" in audio or "on youtube" in audio:
        if "on youtube" in audio:
            searchYoutube(audio)
        else:
            name = audio.split("play")[1].strip()
            playSongFromLocal(name)

    elif "who" in audio or "what" in audio:
        checkWiki(audio)
    
    elif "the laptop" in audio or "the system" in audio:
        if "shutdown" in audio or "turn off" in audio:
            speak("Turning off the laptop")
            os.system("shutdown /s /t 1")
        elif "restart" in audio or "reboot" in audio:
            os.system("shutdown /r /t 1")
    
    elif "calculate" in audio:
        if "into" in audio or "multiply":
            calculate(audio,"multiply")
        
    elif "live status" in audio:
            #trainNo = re .sub("[^0-9]+","",audio)
            #print(trainNo)
            trainName = audio.split("of")[1].split("from")[0].strip()
            source = audio.split("from")[1].strip()
            trainNo = getTrainName(trainName,source)
            status = getLiveStatus(trainNo)

            if "None" in status:
                speak("Sorry, I couldn't find any status for the train number "+trainNo)
            else:
                speak("The train is at {}".format(status))

if __name__ == "__main__":
    #notify("Header","Body")

    wishMe()
    
   # while True:
    command = readUserCommand().lower()

    if "none" in command:
        command = readUserCommand().lower()
        processCommands(command)
    else:
        processCommands(command)
        
