#slider_printRaw.py
#Just print raw values coming from Teensy via USB

import serial
ser = serial.Serial(port='/dev/ttyACM0', baudrate=9600)
while(True):
	reading = ser.readline().decode('utf-8')
	print(reading)
	