import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import sys
import serial
#Own functions
import fit_model

BAUD = 115200
N = 10000
#Define number of samples taken for calculating mean
N_MEAN = 10

#Store user arguments in list
arguments = sys.argv
if(len(arguments) > 1):
	SLIDER_TYPE = arguments[1]
else:
	raise ValueError("Missing argument: slider type")
if(len(arguments) > 2):
	MODELS = arguments[2:len(arguments)]
else:
	raise ValueError("Missing argument(s): model name(s)")

#Initialize Serial port of Teensy
SER = serial.Serial(port='/dev/ttyACM0', baudrate=BAUD)

FIG = plt.figure()
AX1 = FIG.add_subplot(1,1,1)
BAR = AX1.bar(MODELS,[0,0,0,0])



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

def animate(n_frame):
	pos = np.zeros(len(MODELS))	
	for i in range(0,N):
		for i, model in enumerate(MODELS,start=0):
			pos[i] = fit_model.estimate(model,SLIDER_TYPE,SER,N_MEAN)
		AX1.clear()
		AX1.set_ylim([0,30])
		#ax1.autoscale(enable=False)
		return AX1.bar(MODELS,pos)

#Function used for visualizing estimated position
def animate_all(n_frame):	
	for i in range(0,N):
		x = read_raw(N_MEAN,SER)
		#pos1 = getattr(slider_models, function)(x[0],x[1])
		pos1 = model_1(x[0],x[1])
		pos2 = model_2(x[0],x[1])
		pos3 = model_3(x[0],x[1])
		pos4 = model_4(x[0],x[1])
		ÄX1.clear()
		AX1.set_ylim([0,30])
		#ax1.autoscale(enable=False)
		return AX1.bar(['model_1','model_2','model_3','model_4'],[pos1,pos2,pos3,pos4])

#if(len(arguments) <= 1):
#	ani = animation.FuncAnimation(fig, animate_all, frames = 100, interval=1)
#else:
#	ani = animation.FuncAnimation(fig, animate, frames = 100, interval=1)

def main():

	ani = animation.FuncAnimation(FIG,animate,frames = 100,interval=1)
	plt.show()

if __name__ == '__main__':
	main()
