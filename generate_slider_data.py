import serial
from time import sleep
import inspect
import numpy as np
import sys
#Initialize Serial port of Teensy
ser = serial.Serial(port='/dev/ttyACM0', baudrate=9600)
#Set max limit for number of datapoints
n_max = 200
#Number of samples that are used for generating a mean value of both values
n_mean = 30
#Store user arguments in list
arguments = sys.argv
#Check whether user used correct arguments
if(len(arguments) <= 1):
	raise ValueError("Name of log file not specified!")
else:
	if(len(arguments) == 2):
		raise ValueError("Position of finger not specified!")
	else:
		if(not(1 <= int(arguments[2]) <= 28)):
			raise ValueError("Position needs to be between 1 and 28!")
#Store arguments
filename = arguments[1]
pos = arguments[2] #position of finger (1 - 28)
#initialize temporary matrix for storing one set of samples
samples = np.zeros([n_mean,2])
#Open file where data will be stored
with open('sliderData/' + filename + pos,'w') as f:
	for i in range(0,n_max):
		for j in range(0,n_mean):
			#Read from Serial port and convert to string
			reading = ser.readline().decode('utf-8')
			#String -> numpy array
			samples[j] = np.fromstring(reading, dtype=int, sep=',')
		#Generate mean value of both pad values
		means = np.mean(samples,axis=0).astype(int)
		#Generate one string line to write to file
		line = pos + ',' + str(means[0]) + ',' + str(means[1]) + '\n'
		#Write to file
		f.write(line)
		print(line)