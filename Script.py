#!/usr/bin/python3
import requests
import json
from datetime import datetime
import os
from tkinter import *
from tkinter.ttk import *
import webbrowser
from PIL import Image
import io
import subprocess

# os.system("nano /home/noah/.Habbo-Name-List/habbo-eedb-names.txt") # Only for testing

home = os.path.expanduser(os.getenv('HOME'))


def mainMenu():  # Initial Menu
    menuGUI = Tk()
    menuGUI.title("MI Login Checker")
    frame = Frame(menuGUI, padding=10)
    frame.grid()

    loginChecker = Button(menuGUI, text='Login Checker', command=lambda: startLoginChecker(menuGUI, loginChecker), width=40)
    loginChecker.grid(column=0, row=0)

    checkDQ = Button(menuGUI, text='Quota Checker', command=lambda: openDQ(), width=40)
    checkDQ.grid(column=0, row=10)

    mottoCheckerBtn = Button(menuGUI, text='Check Mottos', command=lambda: mottoChecker(menuGUI), width=40)
    mottoCheckerBtn.grid(column=0, row=15)

    editNames = Button(menuGUI, text='Edit Names', command=lambda: editNameGUI(menuGUI), width=40)
    editNames.grid(column=0, row=20)

    getImagesButton = Button(menuGUI, text='Get Images', command=lambda: getImages(), width=40)
    getImagesButton.grid(column=0, row=30)

    openImagesDirButton = Button(menuGUI, text='Open Image Directory', command=lambda: openImagesDir(), width=40)
    openImagesDirButton.grid(column=0, row=40)

    exitButton = Button(menuGUI, text='Exit', command=lambda: menuGUI.destroy(), width=40)
    exitButton.grid(column=0, row=99)

    menuGUI.mainloop()

def calcDelta(fromDate):  # Calculates time since last online
    fromDate = datetime.strptime(fromDate, '%Y-%m-%dT%H:%M:%S')
    delta = datetime.now() - fromDate
    days = delta.days
    hours = (int(delta.total_seconds()) // 3600) % 24
    return days, hours

def readFile():  # Gets names from file, splitting into an array
    global nameList
    nameList = open(f"{home}/.Habbo-Name-List/habbo-eedb-names.txt")
    nameList = (nameList.read()).split()

def onlineMain():  # 'Login Checker'
    global onlineStatus, lastAccessTime, nameList, string
    string = []
    onlineStatus = []
    lastAccessTime = []
    profileVisible = []
    response = ""

    readFile()

    for i in range(0, len(nameList)):
        response = requests.get(f"https://www.habbo.com/api/public/users?name={nameList[i]}")
        response = response.json()
        profileVisible.append(response.get('profileVisible'))
        onlineStatus.append(response.get('online'))
        lastAccessTime.append(response.get('lastAccessTime'))


    for i in range(0, len(nameList)):
        # print(f"{nameList[i]}: {onlineStatus[i]} {profileVisible[i]}")  # for testing only
        if onlineStatus[i] == True:
            string.append(f"{nameList[i]} is online")

        elif profileVisible[i] == 'false':
            string.append(f"{nameList[i]}'s profile and online status are private")

        elif lastAccessTime[i] == None:
            string.append(f"{nameList[i]}'s online status is private")

        elif onlineStatus[i] != 'true' and lastAccessTime[i] != None:
            lastLoginStr(i)

def lastLoginStr(i):  # Function to determine applicable string to show on 'Login Checker' page
    global onlineStatus, lastAccessTime, nameList, string
    # print(f"{lastAccessTime[i]}\n{lastAccessTime}\n")  # Only for testing
    temp = str(lastAccessTime[i])
    # print(f"lastAccessTime is {lastAccessTime}")  # Only for testing
    days, hours = calcDelta(temp.split('.')[0])
    if days == 1 and hours == 1:
        string.append(f"{nameList[i]} last logged in {days} day and {hours} hour ago")
    elif hours == 1:
        string.append(f"{nameList[i]} last logged in {days} days and {hours} hour ago")
    elif days == 1:
        string.append(f"{nameList[i]} last logged in {days} day and {hours} hours ago")
    else:
        string.append(f"{nameList[i]} last logged in {days} days and {hours} hours ago")
    if days > 3:
        string[i] = f"{string[i]} DUE CHECKUP"

def onlineGUI(root):  # GUI for 'Login Checker'
    global onlineStatus, lastAccessTime, nameList, string
    tryKill(root)
    root = Tk()
    root.title("MI Login Checker")
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

def editNameGUI(root):
    global nameList
    root.destroy()
    readFile()
    editRoot = Tk()
    editRoot.title("MI Login Checker")
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

def openImagesDir():
    subprocess.Popen(['dolphin', f"{home}/.Habbo-Name-List/images/"])

def startLoginChecker(root, loadingText):
    loadingText.config(text="Loading...")
    onlineMain()
    onlineGUI(root)

def gitPull():  # Currently disabled by default, kinda broken, will add to enable syncing list between computers
    os.system(f"cd {home}/.Habbo-Name-List/script && git pull")
    os.system(f"cd {home}/.Habbo-Name-List/ && git pull")

def refresh(root):
    onlineMain()
    root.destroy()
    onlineGUI(root)

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
    frame = Frame(root, padding=10)
    frame.grid()
    for i in range(0,len(nameList)):
        Label(frame, text=(motto[i])).grid(column=0, row=i)
    root.mainloop()

# editNameGUI()  # Used when debugging this menu
# start()  # Old, bypasses menu and goes straight to 'Login Checker'
mainMenu()
