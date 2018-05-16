import serial
from time import sleep
import inspect
import numpy as np

ser = serial.Serial(port='/dev/ttyACM0', baudrate=9600)
n = 100
#matrix = np.zeros([100,2])
values = []
while(True):
	for i in range(0,n):
		reading = ser.readline().decode('utf-8')
		matrix = np.fromstring(reading, dtype=int, sep=',')
		#matrix[i] = np.asarray(values)
		#print(values)
	#matrix = np.asarray(values)
		print(matrix)
	#sleep(1)
	