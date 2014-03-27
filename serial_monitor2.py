import serial
import datetime
import httplib2
import urllib
import sys
import simplejson as json

print str(sys.argv)

#construct HTTP object
h = httplib2.Http()

#Set defaults for HTTP connection (these won't change unless we rearchitect our system to do actual POST requests)
headers = {'Content-Type': 'application/json'}
body = ''

#defaults for server, USB port, and site_id
port = 'ttyUSB0'
server = 'http://solarsunflower.herokuapp.com/dc'
site_id = '1'

#Look for system argument containing 'http'
#If an argument has it, set that argument to be the value
#for the server
for argument in sys.argv:
  if 'http' in argument:
    server = argument

#Look for system argument containing 'USB'
#If an argument has it, set that argument to be the value
#for the USB port
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


#Try to open port indicated by parameter
try:
  ser = serial.Serial('/dev/'+port, 57600, timeout=10)
#default to ttyUSB0 if it fails
except serial.SerialException:
  print 'connection failed, using ttyUSB0'
  ser = serial.Serial('/dev/ttyUSB0', 57600, timeout=10)

#normalizes digits to be two characters, prepending 0 if necessary.
def normalizeDigit(dgt):
    if len(str(dgt)) == 1:
        dgt = str('0' + str(dgt))
    return dgt

#print out a bunch of network data so we can debug
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

#normalize data for use in POST - remove characters that are not useful, 
#get rid of newlines, split the remainder into an array
def getData(ser):
    serialData = ser.readline().replace('\x00','').rstrip('\r\n').split(',')
    return serialData

#take the data from the serial port and store it in a dictionary
#this makes parsing it into a set of URL parameters easier 
def assignData(analog):
    nodeData = {}
    nodeData['rainfall'] = ''
    try:
      nodeData['soil1'] = analog[0]
      nodeData['soil2'] = analog[1]
      nodeData['soil3'] = analog[2]
      nodeData['temp'] = analog[3]
      nodeData['voltage'] = analog[4]
    except IndexError:
      nodeData = {}
    return nodeData

#generate a time stamp
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

#after everything, set up a repeating loop for getting and POSTing data
while 1:
    dtme = generateTimestamp()
    #get data from the serial port
    analog = getData(ser)
    print analog
    #parse the data and set it up in a dictionary
    data = assignData(analog)
    #If the data hasn't come yet, skip the rest and start all over
    if data == {}:
      continue
    #construct URL parameters for POSTing, using data taken from the serial port
    else:
      packagedData = [{"rainfall":str(data["rainfall"]),
                        "temp": str(data["temp"]),
                        "soil2": str(data["soil2"]),
                        "soil1": str(data["soil1"]),
                        "soil3": str(data["soil3"]),
                        "voltage": str(data["voltage"]),
                        "id": "1"}]
    
    #construct the complete URL with parameters.
    server_url = server + '?node_readings=' + urllib.quote(str(packagedData).replace('\'','\"')) + "&site_id="+site_id
    #send the POST request
    resp, content = h.request(server, "POST", body=body, headers=headers)
    #Uncomment to receive debugging data
    serverResponse(packagedData, body, headers, resp, content, server_url)
