import serial
import datetime
import httplib2
import simplejson as json

h = httplib2.Http()
linenum = 0

#while 1:
#    ser = serial.Serial('/dev/ttyUSB0', 57600, timeout=10)
#    analog = ser.readlines()
#    print analog

headers = {'Content-Type': 'application/json'}
data = {'site_id':'1','node_readings':[{'id':'1','timestamp':'2013-12-07 04:05:06','channel':'001','soil1':'1.02','soil2':'1.3','soil3':'1.4','temp':'58','voltage':'1.4'}]}
body = json.dumps(data)
uri = "http://solarsunflower.herokuapp.com/dc/"
resp, content = h.request(uri, "POST", body=body, headers=headers)
