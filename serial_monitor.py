import serial
import datetime
import httplib2
import urllib
import simplejson as json
import API_keys

h = httplib2.Http()
headers = {'Content-Type': 'application/json'}
server = "http://solarsunflower.herokuapp.com/dc/"
ser = serial.Serial('/dev/ttyUSB0', 57600, timeout=10)

def normalizeDigit(dgt):
    if len(str(dgt)) == 1:
        dgt = str('0' + str(dgt))
    return dgt

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
  return content_dict['rain']['1h']

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
                               'voltage': str(data['voltage'])}]}#,
                               #'rainfall':str(data['rainfall'])}]}
    print packagedData
    body = json.dumps(data)
    resp, content = h.request(server, "POST", body=body, headers=headers)
    # print resp
    # print '\n\n\n\n'
    # print '------------'
    # print '\n\n\n\n'
    # print content
