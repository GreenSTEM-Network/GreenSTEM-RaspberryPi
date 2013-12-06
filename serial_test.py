import serial
import datetime

linenum = 0

while 1:
    ser = serial.Serial('/dev/ttyUSB0', 57600, timeout=10)
    analog = ser.readlines()
    print analog
