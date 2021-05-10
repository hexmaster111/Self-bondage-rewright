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


import time, cv2
from tkinter import *
from tkinter import messagebox
import tkinter as tk
import numpy as np





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

def distMap(frame1, frame2):
    """outputs pythagorean distance between two frames"""
    frame1_32 = np.float32(frame1)
    frame2_32 = np.float32(frame2)
    diff32 = frame1_32 - frame2_32
    norm32 = np.sqrt(diff32[:, :, 0]**2 + diff32[:, :, 1] **
                     2 + diff32[:, :, 2]**2)/np.sqrt(255**2 + 255**2 + 255**2)
    dist = np.uint8(norm32*255)
    return dist

cv2.namedWindow('frame')
cv2.namedWindow('dist')
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

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



def countDownLoop():
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
            # @TODO Add a user setable amount of time to time remaning

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

def release():  # Function to run whatever release mech the user selected
    # TODO add user selection to the release script/cd drive
    global release_tested
    release_tested = True
    print("Release workes!!")

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
    command=release
)

test_release.place(x=120, y=150)

# Setup for Sliders
# slider for cam sencitivity
motionSlider = Scale(setupWindow, from_=0, to=50,
                     length=1000, tickinterval=1)
motionSlider.set(15)
motionSlider.pack()

#Entry box


# setting up lables
# timer for tie up time
setupTimer = tk.Label(setupWindow)
setupTimer.place(x=140, y=000)
#


ws.mainloop()
setupWindow.mainloop()
