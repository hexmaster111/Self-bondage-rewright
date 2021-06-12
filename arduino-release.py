#!/usr/bin/python
# This will interact with the arduino to run one or more servos to a set angle

import serial
import time

arduino=serial.Serial('COM9', 9600)
time.sleep(2)

print("Enter 1 to turn ON LED and 0 to turn OFF LED")

while 1:
    
    datafromUser=input()

    if datafromUser == '1':
        arduino.write(b'1')
        print("LED  turned ON")
    elif datafromUser == '0':
        arduino.write(b'0')
        print("LED turned OFF")