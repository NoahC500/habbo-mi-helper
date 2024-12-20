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

appTitle = "Habbo MI Helper"
home = os.path.expanduser(os.getenv('HOME'))
if sys.platform == 'linux':
    openCommand = "xdg-open"
    nameLoc = f"{home}/.config/habbo-mi-helper/names"
    baseDir = f"{home}/.config/habbo-mi-helper/"
    rmdirCmd = "rm -rf"
elif sys.platform == 'win32':
    openCommand = "start"
    nameLoc = f"{home}/Documents/habbo-mi-helper/names"
    baseDir = f"{home}/Documents/habbo-mi-helper/"
    rmdirCmd = "rmdir"
elif sys.platform == 'darwin':
    openCommand = "open"
    nameLoc = f"{home}/.config/habbo-mi-helper/names"
    baseDir = f"{home}/.config/habbo-mi-helper/"
    rmdirCmd = "rm -rf"
else:
    sys.exit("Can't ID OS")
baseImgDir = f"{home}/Pictures/habbo-mi-helper/"

def mainMenu(root):  # Main Menu GUI
    if root != "":
        root.destroy()
    menuGUI = Tk()
    menuGUI.title(appTitle)
    frame = Frame(menuGUI, padding=10)
    frame.grid()
    menuGUI.resizable(width=False, height=False)

    loginCheckerBtn = Button(menuGUI, text='Login Checker', command=lambda: loginChecker(menuGUI), width=40)
    loginCheckerBtn.grid(column=0, row=0)

    checkDQBtn = Button(menuGUI, text='Quota Checker', command=lambda: openDQ(), width=40)
    checkDQBtn.grid(column=0, row=1)

    mottoCheckerBtn = Button(menuGUI, text='Motto Checker', command=lambda: mottoChecker(menuGUI), width=40)
    mottoCheckerBtn.grid(column=0, row=2)

    mottoCheckerBtn = Button(menuGUI, text='Badge Checker', command=lambda: badgeChecker(menuGUI), width=40)
    mottoCheckerBtn.grid(column=0, row=3)

    editNamesBtn = Button(menuGUI, text='Edit Names', command=lambda: editNamesGUI(menuGUI), width=40)
    editNamesBtn.grid(column=0, row=4)

    getImagesBtn = Button(menuGUI, text='Get Images', command=lambda: getImages(getImagesBtn), width=40)
    getImagesBtn.grid(column=0, row=5)

    imagesDirBtn = Button(menuGUI, text='Open Image Directory', command=lambda: openImagesDir(), width=40)
    imagesDirBtn.grid(column=0, row=6)

    ecatCommitBtn = Button(menuGUI, text='Commit ECAT Update', command=lambda: ecatCommit(menuGUI), width=40)
    ecatCommitBtn.grid(column=0, row=7)

    exitBtn = Button(menuGUI, text='Exit', command=lambda: menuGUI.destroy(), width=40)
    exitBtn.grid(column=0, row=8)

    menuGUI.mainloop()

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
    root.title(appTitle)
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

def readFile():  # Gets names from file, then splits into an array
    for i in range(0,2):
        try:
            nameList = ((open(nameLoc)).read()).split()
        except:
            os.system(f"mkdir {baseDir}")
            os.system(f"echo 'NoahC500' > {nameLoc}")
    return nameList

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
    root.destroy()
    nameList = readFile()
    root = Tk()
    root.title(appTitle)
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
    nameList = open(nameLoc, 'w')
    nameList.write(namesInput.get(1.0, END))
    nameList.close()
    mainMenu(root)

def openDQ():
    nameList = readFile()
    for i in range(0, len(nameList)):
        webbrowser.open(f"https://habbouk.com/dq/stats/{nameList[i]}")

def getImages(getImagesBtn):
    getImagesBtn.text = "Loading..."
    nameList = readFile()
    subprocess.run(f"{rmdirCmd} {baseImgDir}", shell=True)
    subprocess.run(f"mkdir {baseImgDir}", shell=True)

    for i in range(0,len(nameList)): # Habbo waving
        imgPath = f"{baseImgDir}{nameList[i]}.gif"
        (Image.open(io.BytesIO((requests.get(f"https://www.habbo.com/habbo-imaging/avatarimage?user={nameList[i]}&action=wav&direction=2&head_direction=2&gesture=sml&size=m&img_format=gif")).content))).save(imgPath, format="GIF")

    for i in range(0,len(nameList)): # Habbo facing forward
        imgPath = f"{baseImgDir}{nameList[i]} forward.png"
        (Image.open(io.BytesIO((requests.get(f"https://www.habbo.com/habbo-imaging/avatarimage?user={nameList[i]}&direction=3&head_direction=3&gesture=sml&drk=42&size=l")).content))).save(imgPath, format="PNG")

    for i in range(0,len(nameList)): # Old-style Habbo w/ Coffee
        imgPath = f"{baseImgDir}{nameList[i]} classic & coffee.gif"
        (Image.open(io.BytesIO((requests.get(f"https://www.habbo.com/habbo-imaging/avatarimage?user={nameList[i]}&action=crr=6&direction=&head_direction=2&gesture=sml&size=s&img_format=gif")).content))).save(imgPath, format="GIF")

    for i in range(0,len(nameList)): # Old-style Habbo w/ Coffee
        imgPath = f"{baseImgDir}{nameList[i]} classic.gif"
        (Image.open(io.BytesIO((requests.get(f"https://www.habbo.com/habbo-imaging/avatarimage?user={nameList[i]}&direction=&head_direction=2&gesture=sml&size=s&img_format=gif")).content))).save(imgPath, format="GIF")

def openImagesDir():
    global openCommand
    subprocess.run([openCommand, f"{baseImgDir}"])

def gitPull():  # Currently disabled by default, ~~kinda~~ very broken :P, will add to enable syncing list between computers; this will be toggleable
    os.system(f"cd {home}/.Habbo-Name-List/script && git pull")
    os.system(f"cd {home}/.Habbo-Name-List/ && git pull")

def mottoChecker(root):
    nameList = readFile()
    motto = []

    for i in range(0, len(nameList)):
        userInfo = (requests.get(f"https://www.habbo.com/api/public/users?name={nameList[i]}")).json()
        motto.append(f"{nameList[i]}: {userInfo.get('motto')}")

    root.destroy()
    root = Tk()
    root.title(appTitle)
    root.resizable(width=False, height=False)
    frame = Frame(root, padding=10)
    frame.grid()

    for i in range(0,len(nameList)):
        Label(frame, text=(motto[i])).grid(column=0, row=i)

    menuButton = Button(root, text="Menu", command=lambda: mainMenu(root), width=40)
    menuButton.grid(column=0, row=len(nameList)+1)

    refreshButton = Button(root, text="Refresh", command=lambda: mottoChecker(root), width=40)
    refreshButton.grid(column=0, row=2)

    root.mainloop()

def badgeChecker(root):
    root.destroy()
    root = Tk()
    root.title(appTitle)
    root.resizable(width=False, height=False)
    frame = Frame(root, padding=10)
    frame.grid()

    miAccessBtn = Button(root, text="MI Access ID", command=lambda: badgeCheckerMain(root, 'lr'), width=40)
    miAccessBtn.grid(column=0, row=0)

    miBtn = Button(root, text="Training ID", command=lambda: badgeCheckerMain(root, 'mi'), width=40)
    miBtn.grid(column=0, row=1)

    hocBtn = Button(root, text="HoC ID", command=lambda: badgeCheckerMain(root, 'hoc'), width=40)
    hocBtn.grid(column=0, row=2)

    judiBtn = Button(root, text="Judiciary ID", command=lambda: badgeCheckerMain(root, 'judi'), width=40)
    judiBtn.grid(column=0, row=3)

    cabBtn = Button(root, text="Cabinet ID", command=lambda: badgeCheckerMain(root, 'cab'), width=40)
    cabBtn.grid(column=0, row=4)

    menuButton = Button(root, text="Menu", command=lambda: mainMenu(root), width=40)
    menuButton.grid(column=0, row=5)


def badgeCheckerMain(root, badge):
    global i
    i = 0
    if badge == 'lr':
        data = requests.get("https://www.habbo.com/api/public/groups/g-hhus-1532b1b5605132a130a9bcc48da9ca96/members?pageIndex=0").json()
    elif badge == 'mi':
        data = requests.get("https://www.habbo.com/api/public/groups/g-hhus-7fa90a65814f7d7dadcfaa99b74cc46a/members?pageIndex=0").json()
    elif badge == 'hoc':
        data = requests.get("https://www.habbo.com/api/public/groups/g-hhus-1ced7dc74a0a5828c6c7a80e2233080c/members?pageIndex=0").json()
    elif badge == 'judi':
        data = requests.get("https://www.habbo.com/api/public/groups/g-hhus-16ea38d9abce2bf63fa12d8d41e41f94/members?pageIndex=0").json()
    elif badge == 'cab':
        data = requests.get("https://www.habbo.com/api/public/groups/g-hhus-2114ea67eb859501ecd3b3192d66bbf3/members?pageIndex=0").json()
    drawNameBadge(data, root)

def nextNameBadge(data, root):
    global i
    i+=1
    drawNameBadge(data, root)

def prevNameBadge(data, root):
    global i
    i-=1
    drawNameBadge(data, root)

def drawNameBadge(data, root):
    global i
    root.destroy()
    root = Tk()
    root.title(appTitle)
    root.resizable(width=False, height=False)
    frame = Frame(root, padding=10)
    frame.grid()

    label = Button(frame, text=f"{data[i].get('name')}: {data[i].get('motto')}", command=lambda: copyUsername(data, root)).grid(column=0, row=0)

    if i < len(data)-1:
        nextBtn = Button(root, text="-> Next ->", command=lambda: nextNameBadge(data, root), width=40)
        nextBtn.grid(column=0, row=1)
    else:
        nextBtn = Button(root, text="End of List", width=40)
        nextBtn.grid(column=0, row=1)

    if i != 0:
        prevBtn = Button(root, text="<- Previous <-", command=lambda: prevNameBadge(data, root), width=40)
        prevBtn.grid(column=0, row=2)
    else:
        prevBtn = Button(root, text="Start of List", width=40)
        prevBtn.grid(column=0, row=2)

    menuBtn = Button(root, text="Menu", command=lambda: badgeChecker(root), width=40)
    menuBtn.grid(column=0, row=3)

    root.mainloop()

def copyUsername(data, root):
#   To copy usernames on the badge screen, currently non-functional
    global i
    root.withdraw()
    root.clipboard_clear()
    root.clipboard_append(data[i].get('name'))
    root.update()

def ecatCommit(root):
    root.destroy()
    subprocess.run("python '/pmt/Files/Habbo/ECAT Updates/Git Script.py'", shell=True, cwd="/pmt/Files/Habbo/ECAT Updates/") # This should be replaced with your local script; I use it for committing training script files; a future update will make this editable and toggleable with the GUI

root = "" # Means there need not be a kill before mainMenu() function
mainMenu(root)
