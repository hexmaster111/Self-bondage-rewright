#!/usr/bin/python
# TODO Add labes for the timer
# TODO on the setup window, there will be hiddent timer for setup time
# TODO add a way to check the cam even if we arnt running a timer
# TODO get the display updating when sitting idle
#
# TODO Beep druing countdown option
# TODO random time between min and max
# TODO option to show time or not
# TODO Amount of minutes to be added when motion is detected
# TODO add a random teasing timer with probbablilty adjustment
# TODO play sound when random teasing


import time
import cv2
import serial
import warnings
import serial.tools.list_ports
from tkinter import *
from tkinter import messagebox
import tkinter as tk
import numpy as np
from platform import system as platform_name
import os as system
import ctypes


# Window Setups
f = ("Arial", 24)
ws = Tk()
ws.geometry("300x250")  # l*w+lat+lon
ws.title("Selfbondage Stream Window")
ws.config(bg='#345')

setupWindow = Tk()
setupWindow.geometry("800x400")  # l*w+lat+lon
setupWindow.title("Selfbondage Setup")
setupWindow.config(bg='#345')

# Open CV Setup
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cv2.namedWindow('frame')
cv2.namedWindow('dist')

# Define our globals
release_tested = False
hour = StringVar()
minute = StringVar()
second = StringVar()

# The var to determin how much movement is ok
sdThresh = 10
font = cv2.FONT_HERSHEY_SIMPLEX

hour.set("00")
minute.set("00")
second.set("00")

# Placing Text boxes for timer
hour_tf = Entry(
    ws,
    width=3,
    font=f,
    textvariable=hour
)

hour_tf.place(x=80, y=20)

mins_tf = Entry(
    ws,
    width=3,
    font=f,
    textvariable=minute)

mins_tf.place(x=130, y=20)

sec_tf = Entry(
    ws,
    width=3,
    font=f,
    textvariable=second)

sec_tf.place(x=180, y=20)

platforms_dictionary = {
    "Windows": {
        "open": 'ctypes.windll.WINMM.mciSendStringW(u"set cdaudio door open", None, 0, None)',
        "close": 'ctypes.windll.WINMM.mciSendStringW(u"open L: type CDAudio alias L_drive", None, 0, None); ctypes.windll.WINMM.mciSendStringW(u"set L_drive door closed", None, 0, None)'
    },
    "Darwin":  {
        "open": 'system("drutil tray open")',
        "close": 'system("drutil tray closed")'
    },
    "Linux":   {
        "open": 'system("eject cdrom")',
        "close": 'system("eject -t cdrom")'
    },
    "NetBSD":  {
        "open": 'system("eject cd")',
        "close": 'system("eject -t cd")'
    },
    "FreeBSD": {
        "open": 'system("sudo cdcontrol eject")',
        "close": 'system("sudo cdcontrol close")'
    }
}

teaseToggle = False


def tease():
    global teaseToggle
    if teaseToggle:
        if arduino_enabled:
            arduino.write(b'0')
        teaseToggle = False
    else:
        if arduino_enabled:
            arduino.write(b'2')
        teaseToggle = True


def distMap(frame1, frame2):
    """outputs pythagorean distance between two frames"""
    frame1_32 = np.float32(frame1)
    frame2_32 = np.float32(frame2)
    diff32 = frame1_32 - frame2_32
    norm32 = np.sqrt(diff32[:, :, 0]**2 + diff32[:, :, 1] **
                     2 + diff32[:, :, 2]**2)/np.sqrt(255**2 + 255**2 + 255**2)
    dist = np.uint8(norm32*255)
    return dist


def prossessVideo():
    _, frame1 = cap.read()
    _, frame2 = cap.read()

    _, frame3 = cap.read()
    rows, cols, _ = np.shape(frame3)
    cv2.imshow('dist', frame3)
    dist = distMap(frame1, frame3)

    frame1 = frame2
    frame2 = frame3

    # apply Gaussian smoothing
    mod = cv2.GaussianBlur(dist, (9, 9), 0)

    # apply thresholding
    _, thresh = cv2.threshold(mod, 100, 255, 0)

    # calculate st dev test
    _, stDev = cv2.meanStdDev(mod)

    cv2.imshow('dist', mod)
    cv2.putText(frame2, "Movement Score - {}".format(
        round(stDev[0][0], 0)), (70, 70), font, 1, (255, 0, 255), 1, cv2.LINE_AA)
    cv2.imshow('frame', frame2)
    return(stDev)


timesMovedCurrently = 0

def countDownLoop():
    global timesMovedCurrently
    try:
        userinput = int(hour.get())*3600 + int(minute.get()) * \
            60 + int(second.get())
        # Time when the user hit the start button
        last_time = 0

    except:
        messagebox.showwarning('', 'Invalid Input!')
    while userinput > -1:
        if(release_tested == False):  # if the user didnt test the release mech, we need to not run
            messagebox.showwarning('', 'YOU MUST TEST THAT YOUR RELESE METHOD WORKS AS INTENDED\
 SESSION WILL NOT START UNTEL YOU CHECK IT WORKS')
            return

        movementVal = prossessVideo()

        if movementVal > motionSlider.get():
            print("movement")
            if teaseEnable:
                tease()


            if addTimeOnMovement and timesMovedCurrently <= int(timeaddCountBox.get()): #add more time per a user settable ammount to the timer 
                #@TODO add a max amount of times to be teased and make it user setable
                timeToAdd = int(timePerMovementBox.get())
                print("adding time...")
                userinput = userinput+timeToAdd
                timesMovedCurrently = timesMovedCurrently + 1
                print(timesMovedCurrently)
            

        mins, secs = divmod(userinput, 60)
        hours = 0

        if mins > 60:
            hours, mins = divmod(mins, 60)

        hour.set("{0:2d}".format(hours))
        minute.set("{0:2d}".format(mins))
        second.set("{0:2d}".format(secs))
        ws.update()

        if (userinput == 0):
            release()
            messagebox.showinfo("", "Time's Up")

        # non blocking way to run the timer down
        if time.time() - last_time >= 1:
            userinput -= 1
            last_time = time.time()


def release_test():
    global release_tested
    global arduino_enabled
    global DiskDrive_enabled
    global arduino
    global teaseEnable

    if not arduino_enabled and not DiskDrive_enabled:
        messagebox.showwarning(
            '', 'No Release Methid selected\nYou may still start the program')

    if teaseEnable and not arduino_enabled:
        messagebox.showwarning(
            '', 'Arduino must be enabled in order to use the arduino tease')
        return

# Find arduino on first run
    if arduino_enabled and not release_tested:
        arduino_ports = [
            p.device
            for p in serial.tools.list_ports.comports()
            if 'USB-SER' in p.description  # may need tweaking to match new arduinos
        ]
        if not arduino_ports:
            messagebox.showwarning(
                '', 'No Arduino Found, check cable and that drivers are installed')
        if len(arduino_ports) > 1:
            messagebox.showwarning(
                '', 'Multiple Arduinos found, using the first')

        arduino = serial.Serial(arduino_ports[0])

        print(arduino)

    if arduino_enabled:

        print("Trying Arduino")

# Jog Servo to positions
        messagebox.showwarning(
            '', 'press ok to\n Move Servo to HOLD KEY Position')
        arduino.write(b'1')  # Hold
        messagebox.showwarning(
            '', 'press ok to\nMove Servo to RELEASE KEY Position')
        arduino.write(b'0')  # Release
        if teaseEnable:
            messagebox.showwarning(
                '', 'press ok to\nMove Servo to TEASE Position')
            arduino.write(b'2')  # Tease
        messagebox.showwarning(
            '', 'press ok to\nMove Servo back to HOLD KEY Position')
        arduino.write(b'1')  # Hold

# Pop open disk drive

    if DiskDrive_enabled:
        print("Trying Disk Drive")
        print(platform_name())
        if platform_name() in platforms_dictionary:
            messagebox.showwarning('', 'Press OK to open Disk Drive')
            exec(platforms_dictionary[platform_name()]["open"])
        else:
            messagebox.showwarning(
                '', 'OS not supported\n Open an issue on github and we can try!!')

    release_tested = True


def release():  # Function to run whatever release mech the user selected
    global release_tested
    global arduino_enabled

    if arduino_enabled:
        print("Releasing with arduino")
        arduino.write(b'0')  # Release
        time.sleep(5)
        arduino.write(b'1')  # Hold

    if DiskDrive_enabled:
        print(platform_name())
        if platform_name() in platforms_dictionary:
            print('Releasing with Disk Drive')
            exec(platforms_dictionary[platform_name()]["open"])


def startWith1Min():  # Used for setup time
    if(release_tested == False):  # if the user didnt test the release mech, we need to not run
        messagebox.showwarning('', 'YOU MUST TEST THAT YOUR RELESE METHOD WORKS AS INTENDED\
 SESSION WILL NOT START UNTEL YOU CHECK IT WORKS')
        return
    print("Starting with one minute setup")
    timeToStart_min = 1  # @TODO make this a user definable number, time in munutes
    timeToStart_ms = timeToStart_min * 1000
    last_time = time.time()
    display_time = timeToStart_min*60
    while display_time > -1:
        # update the window
        setupWindow.update()
        ws.update()

        setupTimer['text'] = display_time

        if time.time() - last_time >= 1:
            display_time -= 1
            last_time = time.time()
    countDownLoop()


def quit():
    cap.release()
    cv2.destroyAllWindows()
    ws.destroy()
    setupWindow.destroy()
    exit()


arduino_enabled = False
DiskDrive_enabled = False
teaseEnable = False
addTimeOnMovement = False

def arduinoEnabledToggle():
    global arduino_enabled
    arduino_enabled = not arduino_enabled
    print("Arduino enabled = ")
    print(arduino_enabled)


def DiskDrive_enabledToggle():
    global DiskDrive_enabled
    DiskDrive_enabled = not DiskDrive_enabled
    print("DiskDriveEnable enabled = ")
    print(DiskDrive_enabled)


def teaseEnable_enabledToggle():
    global teaseEnable
    teaseEnable = not teaseEnable
    print("Teasing is = ")
    print(teaseEnable)

def timeOnMovementToggle():
    global addTimeOnMovement
    addTimeOnMovement = not addTimeOnMovement
    print("Adding Time On Tease is = ")
    print(addTimeOnMovement)


uslessVarNO1 = BooleanVar()
uslessVarNO2 = BooleanVar()
uslessVarNO3 = BooleanVar()
uslessVarNO4 = BooleanVar()

# Checkbox Deffs
arduinoCheckBox = tk.Checkbutton(setupWindow, text='Use Arduino', variable=uslessVarNO1, onvalue=True, offvalue=False,
                                 command=arduinoEnabledToggle)
arduinoCheckBox.pack(side=tk.LEFT)

keyJiggleCheck = tk.Checkbutton(setupWindow, text='Arduino Servo Key Jiggle Tease', variable=uslessVarNO3, onvalue=True, offvalue=False,
                                   command=teaseEnable_enabledToggle)
keyJiggleCheck.pack(side=tk.LEFT)

DiskDriveCheckBox = tk.Checkbutton(setupWindow, text='Use Disk Eject', variable=uslessVarNO2, onvalue=True, offvalue=False,
                                   command=DiskDrive_enabledToggle)
DiskDriveCheckBox.pack(side=tk.LEFT)

addTimeOnTeaseCheck = tk.Checkbutton(setupWindow, text='Add Time On Movement', variable=uslessVarNO4, onvalue=True, offvalue=False,
                                   command=timeOnMovementToggle)
addTimeOnTeaseCheck.pack(side=tk.LEFT)


#Number Input stuffs
timePerMovementVar = IntVar()
timePerMovementBox = Entry(setupWindow)
timePerMovementBox.insert(0, "Add time sec")
timePerMovementBox.pack(side=tk.LEFT)


timeaddCountVar = IntVar()
timeaddCountBox = Entry(setupWindow)
timeaddCountBox.insert(0, "Max times to add")
timeaddCountBox.pack(side=tk.LEFT)


# Where we place all the buttons
start_btn = Button(
    setupWindow,
    text='Start',
    bd='5',
    command=countDownLoop
)

start_btn.place(x=120, y=120)

quit_button = Button(
    setupWindow,
    text='Exit',
    bd='5',
    command=quit
)

quit_button.place(x=0, y=150)

start_with_setup_time = Button(
    setupWindow,
    text='Start With 1 Min Setup',
    bd='5',
    command=startWith1Min
)

start_with_setup_time.place(x=000, y=000)

test_release = Button(
    setupWindow,
    text='Test Release',
    bd='5',
    command=release_test
)

test_release.place(x=120, y=150)

# Setup for Sliders
# slider for cam sencitivity
motionSlider = Scale(setupWindow, from_=0, to=50,
                     length=1000, tickinterval=1)
motionSlider.set(15)
motionSlider.pack()

# setting up lables
# timer for tie up time
setupTimer = tk.Label(setupWindow)
setupTimer.place(x=140, y=000)


ws.mainloop()
setupWindow.mainloop()
