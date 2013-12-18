import serial
import datetime

linenum = 0

while 1:
    ser = serial.Serial('/dev/ttyUSB0', 57600, timeout=9.2)
    now = datetime.datetime.now()
    analog = ser.readline()
    yr = now.year
    mon = now.month
    dy = now.day
    hr = now.hour
    min = now.minute
    sec = now.second

    dte = str(mon) + '/' + str(dy) + '/' + str(yr)
    tme = str(hr) + ':' + str(min) + ':' + str(sec)

    dtme = dte + " " + tme

    if linenum < 10:
        lineprt = analog
    else:
        lineprt = dte + "," + tme + "," + analog

    if analog != "":
        log_file = open("pythonoutput.csv", "w")
        log_file.write(lineprt)
        log_file.flush()
        print lineprt

    linenum = linenum + 1
