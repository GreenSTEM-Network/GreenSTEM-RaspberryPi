import serial
import datetime
import httplib2
import urllib
import sys
import simplejson as json

print str(sys.argv)

h = httplib2.Http()
headers = {'Content-Type': 'application/json'}
server = 'http://solarsunflower.herokuapp.com/dc'
site_id = '1'
port = 'ttyUSB0'

try:
  ser = serial.Serial('/dev/'+port, 57600, timeout=10)
#default to ttyUSB0 if it fails
except serial.SerialException:
  print 'connection failed, using ttyUSB0'
  ser = serial.Serial('/dev/ttyUSB0', 57600, timeout=10)

def normalizeDigit(dgt):
    if len(str(dgt)) == 1:
        dgt = str('0' + str(dgt))
    return dgt

def serverResponse(packagedData, body, headers, resp, content, server_url):
    print "Packaged Data: "
    print packagedData
    print '------------'
    print "URL: "
    print server_url
    print '------------'
    print "Headers: "
    print headers
    print '------------'
    print "Response: "
    print resp
    print '------------'
    print "Content: "
    print content

def getData(ser):
    serialData = ser.readline().replace('\x00','').rstrip('\r\n').split(',')
    return serialData

def assignData(analog):
    nodeData = {}
    nodeData['rainfall'] = ''
    # nodeData['rainfall'] = getRainfall()
    try:
      nodeData['soil1'] = analog[0]
      nodeData['soil2'] = analog[1]
      nodeData['soil3'] = analog[2]
      nodeData['temp'] = analog[3]
      nodeData['voltage'] = analog[4]
    except IndexError:
      nodeData = {}
    return nodeData

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

while 1:
    dtme = generateTimestamp()
    analog = getData(ser)
    data = assignData(analog)
    #Check nodeData for values
    if data == {}:
      continue
    #construct JSON object
    else:
      packagedData = [{"rainfall":str(data["rainfall"]),
                        "temp": str(data["temp"]),
                        "soil2": str(data["soil2"]),
                        "soil1": str(data["soil1"]),
                        "soil3": str(data["soil3"]),
                        "voltage": str(data["voltage"]),
                        "id": "1"}]
    
    server_url = server + '?node_readings=' + urllib.quote(str(packagedData).replace('\'','\"')) + "&site_id="+site_id
    #body = json.dumps(packagedData)
    body = ''
    #print server
    #print json.dumps(packagedData)
    resp, content = h.request(server_url, "POST", body=body, headers=headers)
    #Uncomment to receive debugging data
    serverResponse(packagedData, body, headers, resp, content, server_url)
