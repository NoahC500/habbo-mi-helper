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
    settingsDir = f"{home}/.config/MI Helper Script"
elif sys.platform == 'win32':
    openCommand = "start"
    settingsDir = f"{home}/AppData/Local/MI Helper Script"
elif sys.platform == 'darwin':
    openCommand = "open"
    settingsDir = f"{home}/Library/Application Support/MI Helper Script"
settingsFile = f"{settingsDir}/MI Helper Script.cfg"

def readFile(inFile):  # Splits a file into an array of lines
    outFile = ((open(inFile)).read()).splitlines()
    return outFile

def createFile(inFile):
    try:
        toCreate = open(f"\'{inFile}\'", 'w')
        toCreate.write("")
        toCreate.close()
    except:
        print("Failed creating")

try:
    settings = readFile(settingsFile)
except:
    try:
        createFile(settingsFile)
        settings = readFile(settingsFile)
    except:
        subprocess.run(f"mkdir {settingsDir}", shell=True)
        createFile(settingsFile)
        settings = readFile(settingsFile)

imagesDir = settings[1]
if imagesDir[-1] != '/':
    imagesDir += '/'

def mainMenu(root):  # Main Menu GUI
    if root != "":
        root.destroy()
    root = Tk()
    root.title("MI Login Checker")
    frame = Frame(root, padding=10)
    frame.grid()
    root.resizable(width=False, height=False)

    loginCheckerBtn = Button(root, text='Login Checker', command=lambda: loginChecker(root), width=40)
    loginCheckerBtn.grid(column=0, row=0)

    checkDQBtn = Button(root, text='Quota Checker', command=lambda: openDQ(), width=40)
    checkDQBtn.grid(column=0, row=1)

    mottoCheckerBtn = Button(root, text='Check Mottos', command=lambda: mottoChecker(root), width=40)
    mottoCheckerBtn.grid(column=0, row=2)

    editNamesBtn = Button(root, text='Edit Names', command=lambda: editNamesGUI(root), width=40)
    editNamesBtn.grid(column=0, row=3)

    getImagesBtn = Button(root, text='Get Images', command=lambda: getImages(), width=40)
    getImagesBtn.grid(column=0, row=4)

    imagesDirBtn = Button(root, text='Open Image Directory', command=lambda: openImagesDir(), width=40)
    imagesDirBtn.grid(column=0, row=5)

    settingsBtn = Button(root, text='Settings', command=lambda: settingsGUI(root), width=40)
    settingsBtn.grid(column=0, row=6)

    exitBtn = Button(root, text='Exit', command=lambda: root.destroy(), width=40)
    exitBtn.grid(column=0, row=7)

    root.mainloop()

def loginChecker(root):  # Checks Last Login Time
    lastLoginStr = []
    onlineStatus = []
    lastAccessTime = []
    profileVisible = []

    nameList = readFile()

    for i in range(0, len(nameList)):
        response = requests.get(f"https://www.habbo.com/api/public/users?name={nameList[i]}")
        response = response.json()
        profileVisible.append(response.get('profileVisible'))
        onlineStatus.append(response.get('online'))
        lastAccessTime.append(response.get('lastAccessTime'))

    lastLoginStr= lastLoginStrFunc(lastLoginStr, profileVisible, onlineStatus, lastAccessTime, nameList)

    loginCheckerGUI(root, lastLoginStr, nameList)


def loginCheckerGUI(root, lastLoginStr, nameList):  # GUI for 'Login Checker'
    root.destroy()
    root = Tk()
    root.title("MI Login Checker")
    root.resizable(width=False, height=False)
    frame = Frame(root, padding=10)
    frame.grid()

    for i in range(0, len(nameList)):
        Label(frame, text=(f"{lastLoginStr[i]}")).grid(column=0, row=i)

    refreshBtn = Button(root, text="Refresh", command=lambda: loginChecker(root), width=40)
    refreshBtn.grid(column=0, row=len(nameList))

    menuBtn = Button(root, text="Menu", command=lambda: mainMenu(root), width=40)
    menuBtn.grid(column=0, row=len(nameList)+1)

    root.mainloop()

def lastLoginStrFunc(lastLoginStr, profileVisible, onlineStatus, lastAccessTime, nameList):  # Function to determine correct string to show on 'Login Checker' page
    for i in range(0,len(nameList)):
        if onlineStatus[i] == True:
            lastLoginStr.append(f"{nameList[i]} is online")

        elif profileVisible[i] == 'false':
            lastLoginStr.append(f"{nameList[i]}'s profile and online status are private")

        elif lastAccessTime[i] == None:
            lastLoginStr.append(f"{nameList[i]}'s online status is private")

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
    return lastLoginStr

def calcTimeDelta(fromDate):  # Calculates time since last online
    fromDate = datetime.strptime(fromDate, '%Y-%m-%dT%H:%M:%S')
    delta = datetime.now() - fromDate
    days = delta.days
    hours = (int(delta.total_seconds()) // 3600) % 24
    return days, hours

def editNamesGUI(root):
    global namesFile
    root.destroy()
    nameList = readFile(namesFile)
    root = Tk()
    root.title("MI Login Checker")
    root.resizable(width=False, height=False)
    frame = Frame(root, padding=10)
    frame.grid()
    namesInput = Text(root, width=40, height=10)
    namesInput.grid(column=0, row=0)

    for i in range(0, len(nameList)):
        namesInput.insert(f'{i+1}.0', f"{nameList[i]}\n")

    doneBtn = Button(root, text='Done', command=lambda: saveNames(root, namesInput), width=40)
    doneBtn.grid(column=0, row=1)

    cancelBtn = Button(root, text='Cancel', command=lambda: mainMenu(root), width=40)
    cancelBtn.grid(column=0, row=2)

    root.mainloop()

def saveNames(root, namesInput):
    nameList = open(f"{home}/.Habbo-Name-List/habbo-eedb-names.txt", 'w')
    nameList.write(namesInput.get(1.0, END))
    nameList.close()
    mainMenu(root)

def openDQ():
    nameList = readFile()
    for i in range(0, len(nameList)):
        webbrowser.open(f"https://habbouk.com/dq/stats/{nameList[i]}")

def getImages():
    nameList = readFile()

    subprocess.run(f"rm {imagesDir}*", shell=True) # Deletes all images currently in folder

    for i in range(0,len(nameList)): # Habbo waving
        imgPath = f"{imagesDir}{nameList[i]}.gif"
        (Image.open(io.BytesIO((requests.get(f"https://www.habbo.com/habbo-imaging/avatarimage?user={nameList[i]}&action=wav&direction=2&head_direction=2&gesture=sml&size=m&img_format=gif")).content))).save(imgPath, format="GIF")

    for i in range(0,len(nameList)): # Habbo facing forward
        imgPath = f"{imagesDir}{nameList[i]} forward.png"
        (Image.open(io.BytesIO((requests.get(f"https://www.habbo.com/habbo-imaging/avatarimage?user={nameList[i]}&direction=3&head_direction=3&gesture=sml&drk=42&size=l")).content))).save(imgPath, format="PNG")

    for i in range(0,len(nameList)): # Old-style Habbo w/ Coffee
        imgPath = f"{imagesDir}{nameList[i]} classic & coffee.gif"
        (Image.open(io.BytesIO((requests.get(f"https://www.habbo.com/habbo-imaging/avatarimage?user={nameList[i]}&action=crr=6&direction=&head_direction=2&gesture=sml&size=s&img_format=gif")).content))).save(imgPath, format="GIF")

    for i in range(0,len(nameList)): # Old-style Habbo w/ Coffee
        imgPath = f"{imagesDir}{nameList[i]} classic.gif"
        (Image.open(io.BytesIO((requests.get(f"https://www.habbo.com/habbo-imaging/avatarimage?user={nameList[i]}&direction=&head_direction=2&gesture=sml&size=s&img_format=gif")).content))).save(imgPath, format="GIF")

def openImagesDir():
    global openCommand, imagesDir
    subprocess.run([openCommand, imagesDir])

def mottoChecker(root):
    nameList = readFile()
    motto = []

    for i in range(0, len(nameList)):
        userInfo = (requests.get(f"https://www.habbo.com/api/public/users?name={nameList[i]}")).json()
        motto.append(f"{nameList[i]}: {userInfo.get('motto')}")

    root.destroy()
    root = Tk()
    root.title("MI Login Checker")
    root.resizable(width=False, height=False)
    frame = Frame(root, padding=10)
    frame.grid()

    for i in range(0,len(nameList)):
        Label(frame, text=(motto[i])).grid(column=0, row=i)

    menuButton = Button(root, text="Menu", command=lambda: mainMenu(root), width=40)
    menuButton.grid(column=0, row=len(nameList)+1)

    refreshButton = Button(root, text="Refresh", command=lambda: mottoChecker(root, width=40))
    refreshButton.grid(column=0, row=2)

    root.mainloop()

def settingsGUI(root):
    global settingsFile
    settings = readFile(settingsFile)
    root.destroy()
    root = Tk()
    root.title("MI Login Checker")
    root.resizable(width=False, height=False)
    frame = Frame(root, padding=10)
    frame.grid()

    settingsInput = Text(root, width=40, height=10)
    settingsInput.grid(column=0, row=0)
    for i in range(0,len(settings)):
        settingsInput.insert(f"{i+1}.0", f"{settings[i]}\n")

    cancelBtn = Button(root, text="Cancel", command=lambda: mainMenu(root))
    cancelBtn.grid(column=0, row=1)

    submitBtn = Button(root, text="Submit", command=lambda: submitSettings(root, settingsInput))
    submitBtn.grid(column=0, row=2)

def submitSettings(root, settingsInput):
    global settingsFile
    settings = open(settingsFile, 'w')
    settings.write(settingsInput.get(1.0, END))
    settings.close()
    mainMenu(root)

root = "" # Means there need not be a kill before mainMenu() function
mainMenu(root)
