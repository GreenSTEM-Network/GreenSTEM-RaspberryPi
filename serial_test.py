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
server = "http://solarsunflower.herokuapp.com/dc/"
ser = serial.Serial('/dev/ttyUSB0', 57600, timeout=10)
#try to grab and discard the first few data updates - the help text, etc.
#Still doesn't work. We need to remove all the extraneous Serial.println() statements from the JeeLink code.
analog = ser.readline()
analog = ser.readline()


while 1:
  #Set up default variables for each pass
    #for storing extracted data from JeeLink
    data = []
    #constant representing number of lines sent each update
    NUMBER_OF_LINES = 6
    #generate timestamp
    dtme = generateTimestamp()
    #set up a loop for the total number of lines in the update. For each line...
    for x in range(0,NUMBER_OF_LINES):
      #read the line
      analog = ser.readline().rstrip('\r\n')
      #add it to the list
      data.append(analog)
    #assign the data - this is based on the order defined in the JeeLink Receive sketch  
    soil1 = data[0]
    soil2 = data[1]
    soil3 = data[2]
    temp = data[3]
    voltage = data[4]
    #construct JSON object
    data = {'site_id': '1',
            'node_readings': [{'id': '1',
                               'timestamp': str(dtme),
                               'channel': '001',
                               'soil1': str(soil1),
                               'soil2': str(soil2),
                               'soil3': str(soil3),
                               'temp': str(temp),
                               'voltage': str(voltage)}]}
    print data
#    body = json.dumps(data)
#    resp, content = h.request(server, "POST", body=body, headers=headers)
