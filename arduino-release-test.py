#!/usr/bin/python
# This will interact with the arduino to run one or more servos to a set angle



import serial
import time

arduino = serial.Serial('COM9', 9600)
time.sleep(2)

print("Enter 1 to turn ON LED and 0 to turn OFF LED")

teaseToggle = False

def tease():
    global teaseToggle
    if teaseToggle:
        arduino.write(b'0')
        teaseToggle = False
    else:
        arduino.write(b'2')
        teaseToggle = True

while 1:
    # time.sleep(1000)
    tease()
    

# while 1:

#     datafromUser = input()

#     if datafromUser == '0': #Hold
#         arduino.write(b'0')
#         print("0 sent")

#     if datafromUser == '1': #Release
#         arduino.write(b'1')
#         print("1 sent")

#     if datafromUser == '2': #90 deg
#         arduino.write(b'2')
#         print("2 sent")

#     if datafromUser == '3': #unused
#         arduino.write(b'3')
#         print("3 sent")

