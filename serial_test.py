import serial
import datetime
import httplib2
import simplejson as json


def normalizeDigit(dgt):
    if len(str(dgt)) == 1:
        dgt = str('0' + str(dgt))
    return dgt


def generateTimestamp():
    now = datetime.datetime.now()
    yr = normalizeDigit(now.year)
    mon = normalizeDigit(now.month)
    dy = normalizeDigit(now.day)
    hr = normalizeDigit(now.hour)
    mnt = normalizeDigit(now.minute)
    sec = normalizeDigit(now.second)

    dte = str(yr) + '-' + str(mon) + '-' + str(dy)
    tme = str(hr) + ':' + str(mnt) + ':' + str(sec)

    dtme = dte + " " + tme

    return dtme

h = httplib2.Http()
headers = {'Content-Type': 'application/json'}
#server = "http://localhost:3000/dc/"
server = "http://solarsunflower.herokuapp.com/dc/"

while 1:
    data = []
    NUMBER_OF_LINES = 6
    dtme = generateTimestamp()
    ser = serial.Serial('/dev/ttyUSB0', 57600, timeout=10)
    for x in range(0,NUMBER_OF_LINES):
      analog = ser.readline()
      analog = analog.rstrip('\r\n')
      data.append(analog)
    soil1 = data[1]
    soil2 = data[2]
    soil3 = data[3]
    data = {'site_id': '1',
            'node_readings': [{'id': '1',
                               'timestamp': str(dtme),
                               'channel': '001',
                               'soil1': str(soil1),
                               'soil2': str(soil2),
                               'soil3': str(soil3),
                               'temp': '58',
                               'voltage': '1.4'}]}
    print data
#    body = json.dumps(data)
#    resp, content = h.request(server, "POST", body=body, headers=headers)
