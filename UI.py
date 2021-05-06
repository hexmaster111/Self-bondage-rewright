import time
from tkinter import *
from tkinter import messagebox


f = ("Arial", 24)

ws = Tk()
ws.geometry("300x250+1500+700")
ws.title("Timer")
ws.config(bg='#345')

hour = StringVar()
minute = StringVar()
second = StringVar()

hour.set("00")
minute.set("00")
second.set("00")

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


def startCountdown():
    try:
        userinput = int(hour.get())*3600 + int(minute.get()) * \
            60 + int(second.get())
        # Time when the user hit the start button
        last_time = 0

    except:
        messagebox.showwarning('', 'Invalid Input!')
    while userinput > -1:
        mins, secs = divmod(userinput, 60)
        hours = 0

        if mins > 60:
            hours, mins = divmod(mins, 60)

        hour.set("{0:2d}".format(hours))
        minute.set("{0:2d}".format(mins))
        second.set("{0:2d}".format(secs))
        ws.update()

        if (userinput == 0):
            messagebox.showinfo("", "Time's Up")
        
        #non blocking way to run the timer down 
        if time.time() - last_time >= 1: 
            userinput -= 1
            last_time = time.time()


start_btn = Button(
    ws,
    text='START',
    bd='5',
    command=startCountdown
)

start_btn.place(x= 120, y = 120)


ws.mainloop()
