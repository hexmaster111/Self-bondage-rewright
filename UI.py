# TODO Add labes for the timer
# TODO on the setup window, there will be hiddent timer for setup time
# with a start in 1 min button and a add 1 min button

import time
from tkinter import *
from tkinter import messagebox
import tkinter as tk
import numpy as np
import cv2


# Window Setups
f = ("Arial", 24)
ws = Tk()
ws.geometry("300x250")  # l*w+lat+lon
ws.title("Selfbondage Stream Window")
ws.config(bg='#345')

setupWindow = Tk()
setupWindow.title("Selfbondage Setup")
setupWindow.config(bg='#345')

# Define our globals
release_tested = False
hour = StringVar()
minute = StringVar()
second = StringVar()

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

def startWith1Min(): #Used for setup time
    if(release_tested == False):  # if the user didnt test the release mech, we need to not run
        messagebox.showwarning('', 'YOU MUST TEST THAT YOUR RELESE METHOD WORKS AS INTENDED\
 SESSION WILL NOT START UNTEL YOU CHECK IT WORKS')
        return
    print("Starting with one minute setup")
    timeToStart_min = 1 #@TODO make this a user definable number, time in munutes
    timeToStart_ms = timeToStart_min * 1000
    last_time = time.time()
    display_time=timeToStart_min*60
    while display_time > -1:
        #update the window
        setupWindow.update()
        ws.update()

        setupTimer['text'] = display_time
        
        if time.time() - last_time >= 1:
            display_time -= 1
            last_time = time.time()
    countDownLoop() 


# Where we place all the buttons
start_btn = Button(
    setupWindow,
    text='Start',
    bd='5',
    command=countDownLoop
)

start_btn.place(x=120, y=120)

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

##setting up lables
#timer for tie up time
setupTimer = tk.Label(setupWindow)
setupTimer.place(x=140, y=000)
#


ws.mainloop()
setupWindow.mainloop()