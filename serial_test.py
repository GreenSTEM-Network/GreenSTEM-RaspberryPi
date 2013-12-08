import serial
import datetime
import httplib2
import simplejson as json

h = httplib2.Http()
headers = {'Content-Type': 'application/json'}
server = "http://solarsunflower.herokuapp.com/dc/"

while 1:
	now = datetime.datetime.now()
	yr = now.year
	mon = now.month
	dy = now.day
	hr = now.hour
	mnt = now.minute
	sec = now.second
	if len(str(sec)) == 1:
		sec = str('0' + str(sec))
	if len(str(dy)) == 1:
		dy = str('0' + str(dy))
	if len(str(mnt)) == 1:
		mnt = str('0' + str(mnt))

	dte = str(yr) + '-' + str(mon) + '-' + str(dy)
	tme = str(hr) + ':' + str(mnt) + ':' + str(sec)

	dtme = dte + " " + tme

	ser = serial.Serial('/dev/ttyUSB0', 57600, timeout=9.3)
	analog = ser.readlines()
	sensorData = analog[1].rstrip('\r\n')
	data = {'site_id':'1','node_readings':[{'id':'1','timestamp':str(dtme),'channel':'001','soil1':str(sensorData),'soil2':'1.3','soil3':'1.4','temp':'58','voltage':'1.4'}]}
	print data
	body = json.dumps(data)
	resp, content = h.request(server, "POST", body=body, headers=headers)
