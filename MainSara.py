from Sara import wishMe, assistant, textToAssistant, speak
from tkinter import *

#wishMe()

def takeCommand():
    try:
        print(getCommand.get().lower())
        textToAssistant(getCommand.get().lower())
    except Exception as e:
        print(e)
        speak("There was an Error process your request")

appWindow = Tk()
appWindow.geometry("450x100")
appWindow.title("Sara")

startSaraBtn = Button(appWindow,text="Sara",width=4, height=1, bg="blue",fg="white",font=("bold",10), command=assistant)
startSaraBtn.place(x=200,y=5)

label1= Label(appWindow,text="Text to Sara",font=("bold",10))
label1.place(x=1,y=40)

getCommand = Entry(appWindow,width=50)
getCommand.place(x=80,y=40)


sendBtn = Button(appWindow,text="Send",width=4,height=1,bg="green",font=("bold",10),command=takeCommand)
sendBtn.place(x=400,y=38)

#assistant()

appWindow.mainloop()
