#slider_generate_data.py
#Generates labeled training data for capacitive slider. Stores it in csv file
#Arguments: LOG_FILENAME FINGER_POSITION
import serial
from time import sleep
import inspect
import numpy as np
import sys

#Store user arguments in list
arguments = sys.argv
#Store arguments
n = int(arguments[1]) # number of samples
filename = arguments[2]
#Initialize Serial port of Teensy
ser = serial.Serial(port='/dev/ttyACM0', baudrate=9600)
samples = np.zeros((n,2))
for j in range(0,n):
	#Read from Serial port and convert to string
	reading = ser.readline().decode('utf-8')
	#String -> numpy array
	samples[j,:] = np.fromstring(reading, dtype=int, sep=',')
print(samples[100:110,:])
print("Writing to file....")
with open('sliderData/' + filename + '.csv','w') as f:
	for i in range(0,n):
		#Generate one string line to write to file
		line = str(samples[i,0]) + ',' + str(samples[i,1]) + '\n'
		#Write to file
		f.write(line)
		#print(line)