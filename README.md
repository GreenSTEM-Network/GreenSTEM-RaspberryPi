RaspberryPi
===========

Code for accepting data from the sensors, packaging it, and uploading it to the server.

Launch with the command 'python serial_monitor.py <USB-PORT-OF-JEELINK> <server>

The USB Port will default to 'ttyUSB0' if none is specified or the USB port specified is invalid.
The server will default to 'http://solarsunflower.herokuapp.com/dc/' if none is specified 

While the listener is running, it reacts every time the JeeNode sends data successfully. It takes the data, converts it into a set of URL parameters, and sends a POST request to the URL.

Example URL: http://solarsunflower.herokuapp.com/dc?node_readings=[{"rainfall": "", "temp": "45", "soil2": "26", "soil3": "34", "soil1": "1", "voltage": "56", "id": "1"}]&site_id=1

(this will be encoded in a URL parameter-safe format).

To quit, Ctrl + C.

To set the site_id, modify the variable in the defaults section at the top of the file.

Useful Pi Links
---------------

* Getting Arduino IDE workign on PI: http://www.quilix.com/node/103
* Advice for Wifi with Edimax USB stick: http://www.savagehomeautomation.com/projects/raspberry-pi-installing-the-edimax-ew-7811un-usb-wifi-adapte.html
* Make My Pi;  project that sets up SD card image: https://github.com/mholt/makemypi
