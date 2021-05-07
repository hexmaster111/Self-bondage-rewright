from tkinter import *

def show_entry_fields():
    print("First Name: %s\nLast Name: %s" % (e1.get(), e2.get()))

master = Tk()


e1 = tk.Entry(master)


e1.grid(row=0, column=1)



tk.mainloop()