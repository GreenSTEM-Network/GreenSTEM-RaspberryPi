RaspberryPi
===========

Code for accepting data from the sensors, packaging it, and uploading it to the server.

Launch with the command 'python serial_monitor.py <USB-PORT-OF-JEELINK> <server>

The USB Port will default to 'ttyUSB0' if none is specified or the USB port specified is invalid.
The server will default to 'http://solarsunflower.herokuapp.com/dc/' if none is specified 


Useful Pi Links
---------------

* Getting Arduino IDE workign on PI: http://www.quilix.com/node/103
* Advice for Wifi with Edimax USB stick: http://www.savagehomeautomation.com/projects/raspberry-pi-installing-the-edimax-ew-7811un-usb-wifi-adapte.html
* Make My Pi;  project that sets up SD card image: https://github.com/mholt/makemypi
