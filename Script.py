#!/usr/bin/python3
import requests
import json
from datetime import datetime
import os # For getting HOME variable
from tkinter import *
from tkinter.ttk import *
import webbrowser
from PIL import Image
import io
import subprocess
import sys # For determining OS

home = os.path.expanduser(os.getenv('HOME'))
if sys.platform == 'linux':
    openCommand = "xdg-open"
elif sys.platform == 'win32':
    openCommand = "start"
elif sys.platform == 'darwin':
    openCommand = "open"

def mainMenu():  # Main Menu GUI
    menuGUI = Tk()
    menuGUI.title("MI Login Checker")
    frame = Frame(menuGUI, padding=10)
    frame.grid()
    menuGUI.resizable(width=False, height=False)

    loginCheckerBtn = Button(menuGUI, text='Login Checker', command=lambda: loginChecker(menuGUI), width=40)
    loginCheckerBtn.grid(column=0, row=0)

    checkDQBtn = Button(menuGUI, text='Quota Checker', command=lambda: openDQ(), width=40)
    checkDQBtn.grid(column=0, row=1)

    mottoCheckerBtn = Button(menuGUI, text='Check Mottos', command=lambda: mottoChecker(menuGUI), width=40)
    mottoCheckerBtn.grid(column=0, row=2)

    editNamesBtn = Button(menuGUI, text='Edit Names', command=lambda: editNameGUI(menuGUI), width=40)
    editNamesBtn.grid(column=0, row=3)

    getImagesBtn = Button(menuGUI, text='Get Images', command=lambda: getImages(), width=40)
    getImagesBtn.grid(column=0, row=4)

    imagesDirBtn = Button(menuGUI, text='Open Image Directory', command=lambda: openImagesDir(), width=40)
    imagesDirBtn.grid(column=0, row=5)

    exitBtn = Button(menuGUI, text='Exit', command=lambda: menuGUI.destroy(), width=40)
    exitBtn.grid(column=0, row=6)

    menuGUI.mainloop()

def loginChecker(root):  # Checks Last Login Time
    global nameList
    lastLoginStr = []
    onlineStatus = []
    lastAccessTime = []
    profileVisible = []

    readFile()

    for i in range(0, len(nameList)):
        response = requests.get(f"https://www.habbo.com/api/public/users?name={nameList[i]}")
        response = response.json()
        profileVisible.append(response.get('profileVisible'))
        onlineStatus.append(response.get('online'))
        lastAccessTime.append(response.get('lastAccessTime'))

        lastLoginStrFunc(i, lastLoginStr, profileVisible, onlineStatus, lastAccessTime)

def onlineGUI(root):  # GUI for 'Login Checker'
    global nameList
    tryKill(root)
    root = Tk()
    root.title("MI Login Checker")
    root.resizable(width=False, height=False)
    frame = Frame(root, padding=10)
    frame.grid()
    for i in range(0, len(nameList)):
        # print(f"string length is {len(string)}\nstring is {string}\ni is {i}")  # Only for testing
        Label(frame, text=(f"{string[i]}")).grid(column=0, row=i)

    menuButton = Button(root, text="Menu", command=lambda: online2main(root), width=40)
    menuButton.grid(column=0, row=len(nameList)+1)
    refreshButton = Button(root, text="Refresh", command=lambda: refresh(root), width=40)
    refreshButton.grid(column=0, row=2)
    root.mainloop()

def readFile():  # Gets names from file, splitting into an array
    global nameList
    nameList = open(f"{home}/.Habbo-Name-List/habbo-eedb-names.txt")
    nameList = (nameList.read()).split()

def lastLoginStrFunc(i, lastLoginStr, profileVisible, onlineStatus, lastAccessTime):  # Function to determine correct string to show on 'Login Checker' page
    global nameList
    for i in range(0, len(nameList)):
        if onlineStatus[i] == True:
            lastLoginStr.append(f"{nameList[i]} is online")

        elif profileVisible[i] == 'false':
            lastLoginStr.append(f"{nameList[i]}'s profile and online status are private")

        elif lastAccessTime[i] == None:
            lastLoginStr.append(f"{nameList[i]}'s online status is private")

        elif onlineStatus[i] != 'true' and lastAccessTime[i] != None:
            lastLoginStrFunc(i, lastLoginStr)
        else:
            days, hours = calcTimeDelta(str(lastAccessTime[i]).split('.')[0])
            if days == 1 and hours == 1:
                lastLoginStr.append(f"{nameList[i]} last logged in {days} day and {hours} hour ago")
            elif hours == 1:
                lastLoginStr.append(f"{nameList[i]} last logged in {days} days and {hours} hour ago")
            elif days == 1:
                lastLoginStr.append(f"{nameList[i]} last logged in {days} day and {hours} hours ago")
            else:
                lastLoginStr.append(f"{nameList[i]} last logged in {days} days and {hours} hours ago")
            if days > 3:
                lastLoginStr[i] = f"{lastLoginStr[i]} DUE CHECKUP"

def calcTimeDelta(fromDate):  # Calculates time since last online
    fromDate = datetime.strptime(fromDate, '%Y-%m-%dT%H:%M:%S')
    delta = datetime.now() - fromDate
    days = delta.days
    hours = (int(delta.total_seconds()) // 3600) % 24
    return days, hours

def editNameGUI(root):
    global nameList
    root.destroy()
    readFile()
    editRoot = Tk()
    editRoot.title("MI Login Checker")
    editRoot.resizable(width=False, height=False)
    frame = Frame(editRoot, padding=10)
    frame.grid()
    text = Text(editRoot, width=40, height=10)
    text.grid(column=0, row=0)
    # text.insert(1.0, f"this is a test")  # Only for testing
    for i in range(0, len(nameList)):
        text.insert(f'{i+1}.0', f"{nameList[i]}\n")
    done = Button(editRoot, text='Done', command=lambda: doneNameChange(editRoot, text), width=40)
    done.grid(column=0, row=1)
    cancel = Button(editRoot, text='Cancel', command=lambda: edit2main(editRoot), width=40)
    cancel.grid(column=0, row=2)
    editRoot.mainloop()

def edit2main(root):
    tryKill(root)
    mainMenu()

def doneNameChange(editRoot, text):
    global nameList
    # print("doneNameChange()")  # Only for testing
    # temp = text.get(1.0, END)  # Only for testing
    # print(temp) # Only for testing
    nameList = open(f"{home}/.Habbo-Name-List/habbo-eedb-names.txt", 'w')
    nameList.write(text.get(1.0, END))
    nameList.close()
    editRoot.destroy()
    readFile()
    mainMenu()

def openDQ():
    global nameList
    readFile()
    for i in range(0, len(nameList)):
        webbrowser.open(f"https://habbouk.com/dq/stats/{nameList[i]}")

def online2main(root):
    root.destroy()
    mainMenu()

def tryKill(root):
    try:
        root.destroy()
    except:
        print("Tried to kill, failed")

def getImages():
    global nameList
    readFile()
    try:
        os.system(f"rm {home}/.Habbo-Name-List/images/*")
    except:
        print("No images in folder")
    for i in range(0,len(nameList)):
        response = requests.get(f"https://www.habbo.com/habbo-imaging/avatarimage?user={nameList[i]}&action=wav&direction=2&head_direction=2&gesture=sml&size=m&img_format=gif")
        response = io.BytesIO(response.content)
        image = Image.open(response)
        imgPath = f"{home}/.Habbo-Name-List/images/{nameList[i]}.gif"
        image.save(imgPath, format="GIF")
    for i in range(0,len(nameList)):
        response = requests.get(f"https://www.habbo.com/habbo-imaging/avatarimage?user={nameList[i]}&direction=3&head_direction=3&gesture=sml&drk=42&size=l")
        response = io.BytesIO(response.content)
        image = Image.open(response)
        imgPath = f"{home}/.Habbo-Name-List/images/{nameList[i]} forward.png"
        image.save(imgPath, format="PNG")
    for i in range(0,len(nameList)):
        response = requests.get(f"https://www.habbo.com/habbo-imaging/avatarimage?user={nameList[i]}&action=crr=6&direction=&head_direction=2&gesture=sml&size=s&img_format=gif")
        response = io.BytesIO(response.content)
        image = Image.open(response)
        imgPath = f"{home}/.Habbo-Name-List/images/{nameList[i]} classic.png"
        image.save(imgPath, format="GIF")

def openImagesDir():
    global openCommand
    subprocess.Popen([openCommand, f"{home}/.Habbo-Name-List/images/"])

def gitPull():  # Currently disabled by default, kinda broken, will add to enable syncing list between computers
    os.system(f"cd {home}/.Habbo-Name-List/script && git pull")
    os.system(f"cd {home}/.Habbo-Name-List/ && git pull")

def refresh(root):
    onlineMain()
    root.destroy()
    onlineGUI(root)

def refreshMotto(root):
    mottoChecker(root)

def start():
    # gitPull()
    onlineMain()
    onlineGUI()

def mottoChecker(root):
    global nameList, motto
    readFile()
    motto = []
    for i in range(0, len(nameList)):
        response = requests.get(f"https://www.habbo.com/api/public/users?name={nameList[i]}")
        response = response.json()
        # print(f"{nameList[i]}\n{response.get('motto')}")
        motto.append(f"{nameList[i]}: {response.get('motto')}")
        print(motto[i])
    root.destroy()
    root = Tk()
    root.title("MI Login Checker")
    root.resizable(width=False, height=False)
    frame = Frame(root, padding=10)
    frame.grid()
    for i in range(0,len(nameList)):
        Label(frame, text=(motto[i])).grid(column=0, row=i)
    menuButton = Button(root, text="Menu", command=lambda: online2main(root), width=40)
    menuButton.grid(column=0, row=len(nameList)+1)
    refreshButton = Button(root, text="Refresh", command=lambda: refreshMotto(root), width=40)
    refreshButton.grid(column=0, row=2)
    root.mainloop()

mainMenu()
