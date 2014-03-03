import serial
import datetime
import httplib2
import sys
import simplejson as json
import API_keys

print str(sys.argv)

h = httplib2.Http()
headers = {'Content-Type': 'application/json'}
port = 'ttyUSB0'
server = 'http://solarsunflower.herokuapp.com/dc/'

#Look for system argument containing 'http'
#If an argument has it, set that argument to be the value
#for the server
for argument in sys.argv:
  if 'http' in argument:
    server = argument

#Same with 'USB' for specifying the port
for argument in sys.argv:
  if 'USB' in argument:
    port = argument

#!!!! Eventually I'd like to change the above to something like this, but it's not working
#
# if any('http' in argument for argument in sys.argv):
#   server = argument
# else:
#   server = 'ttyUSB0'
#   print 'no server specified, using ' + server

# if any('tty' in argument for argument in sys.argv):
#   port = argument
# else:
#   port = 'ttyUSB0'
#   print 'no port specified, using ' + port


#Try to open port, default to ttyUSB0 if it fails
try:
  ser = serial.Serial('/dev/'+port, 57600, timeout=10)
except serial.SerialException:
  print 'connection failed, using ttyUSB0'
  ser = serial.Serial('/dev/ttyUSB0', 57600, timeout=10)

def normalizeDigit(dgt):
    if len(str(dgt)) == 1:
        dgt = str('0' + str(dgt))
    return dgt

def serverResponse(resp, content):
    print resp
    print '\n\n\n\n'
    print '------------'
    print '\n\n\n\n'
    print content

def getData(ser):
    serialData = ser.readline().replace('\x00','').rstrip('\r\n').split(',')
    return serialData

def getRainfall():
  http = httplib2.Http()
  url_base = 'http://api.openweathermap.org/data/2.5/weather'
  url = '?q=Philadelphia,PA&APPID=3545f6916c462e0c8f2e273c87c09fd4'
  rainHeaders = {'Content-type': 'application/x-www-form-urlencoded'}
  response, content = http.request(url_base+url, 'GET', headers=rainHeaders, body='')
  #print str(response) + '\n'
  content_dict = json.loads(content)
  print content_dict['rain']
  try:
    return content_dict['rain']['1h']
  except KeyError:
    try:
      return content_dict['rain']['3h']
    except KeyError:
      return 'not found'

def assignData(analog):
    nodeData = {}
    nodeData['rainfall'] = getRainfall()
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
      packagedData = {'site_id': '1',
            'node_readings': [{'id': '1',
                               'timestamp': str(dtme),
                               'channel': '001',
                               'soil1': str(data['soil1']),
                               'soil2': str(data['soil2']),
                               'soil3': str(data['soil3']),
                               'temp': str(data['temp']),
                               'voltage': str(data['voltage']),
                               'rainfall':str(data['rainfall'])}]}
    print packagedData
    body = json.dumps(data)
    resp, content = h.request(server, "POST", body=body, headers=headers)
    serverResponse(resp, content)
