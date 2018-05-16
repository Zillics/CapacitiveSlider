#HOW TO USE: 
#if n is model number that you want to use:
#python slider_estimate.py model_n
import serial
from time import sleep
import inspect
import numpy as np
import sys
import inspect
#Own functions
import slider_models
from slider_models import model_1
from slider_models import model_2
from slider_models import model_3
from slider_models import model_4

#Store user arguments in list
arguments = sys.argv
#Check whether user inputted argument
if(len(arguments) <= 1):
	raise ValueError("Model name not specified")
else:
	function = arguments[1]
#Initialize Serial port of Teensy
ser = serial.Serial(port='/dev/ttyACM0', baudrate=9600)
#Define number of samples taken for calculating mean
n_mean = 30
#Initialize matrix for calculating mean values
samples = np.zeros([n_mean,2])
#Get function from user argument
while(True):
	for j in range(0,n_mean):
		#Read from Serial port and convert to string
		reading = ser.readline().decode('utf-8')
		#String -> numpy array
		samples[j] = np.fromstring(reading, dtype=int, sep=',')
	#Generate mean value of both pad values
	x = np.mean(samples,axis=0).astype(int)
	pos = getattr(slider_models, function)(x[0],x[1])
	print(pos)


