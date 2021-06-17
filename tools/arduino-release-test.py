#!/usr/bin/python
# This will interact with the arduino to run one or more servos to a set angle



import serial
import time

arduino = serial.Serial('COM9', 9600)
time.sleep(2)

print ("press number to send that byte to the arduino, note the bite has to be set up in the python program first")    

while 1:

    datafromUser = input()

    if datafromUser == '0': #Hold
        arduino.write(b'0')
        print("0 sent")

    if datafromUser == '1': #Release
        arduino.write(b'1')
        print("1 sent")

    if datafromUser == '2': #90 deg
        arduino.write(b'2')
        print("2 sent")

    if datafromUser == '3': #unused
        arduino.write(b'3')
        print("3 sent")

