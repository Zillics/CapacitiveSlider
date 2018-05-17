import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import sys
import serial
#Own functions
import slider_models
from slider_models import model_1
from slider_models import model_2
from slider_models import model_3
from slider_models import model_4
n = 10000
#Function for reading raw values
def read_raw(n,serial_port):
	#Initialize matrix for calculating mean values
	samples = np.zeros([n,2])
	for j in range(0,n):
		#Read from Serial port and convert to string
		reading = serial_port.readline().decode('utf-8')
		#String -> numpy array
		samples[j] = np.fromstring(reading, dtype=int, sep=',')[0:2]
	#Generate mean value of both pad values
	x = np.mean(samples,axis=0).astype(int)
	return x

#Store user arguments in list
arguments = sys.argv
#Check whether user inputted argument

#Initialize Serial port of Teensy
ser = serial.Serial(port='/dev/ttyACM0', baudrate=9600)
#Define number of samples taken for calculating mean
n_mean = 60

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
#ax1.autoscale(enable=False)
#ax1.set_yticks(range(0,30,30))

if(len(arguments) <= 1):
	bar = ax1.bar(['model_1','model_2','model_3','model_4'],[0,0,0,0])	
else:
	function = arguments[1]
	bar = ax1.bar([function],[0,0,0,0])

#Function used for visualizing estimated position
def animate_all(n_frame):	
	for i in range(0,n):
		x = read_raw(n_mean,ser)
		#pos1 = getattr(slider_models, function)(x[0],x[1])
		pos1 = model_1(x[0],x[1])
		pos2 = model_2(x[0],x[1])
		pos3 = model_3(x[0],x[1])
		pos4 = model_4(x[0],x[1])
		ax1.clear()
		ax1.set_ylim([0,30])
		#ax1.autoscale(enable=False)
		return ax1.bar(['model_1','model_2','model_3','model_4'],[pos1,pos2,pos3,pos4])
def animate(n_frame):	
	for i in range(0,n):
		x = read_raw(n_mean,ser)
		pos = getattr(slider_models, function)(x[0],x[1])
		ax1.clear()
		ax1.set_ylim([0,30])
		#ax1.autoscale(enable=False)
		return ax1.bar([function],pos)

if(len(arguments) <= 1):
	ani = animation.FuncAnimation(fig, animate_all, frames = 100, interval=1)
else:
	ani = animation.FuncAnimation(fig, animate, frames = 100, interval=1)


#x = read_raw(n_mean,ser)
#pos = getattr(slider_models, function)(x[0],x[1])
#ax1.bar([1],pos)
plt.show()

