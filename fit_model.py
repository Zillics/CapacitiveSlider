import glob
import numpy as np
from scipy.optimize import curve_fit
import serial
import inspect
import sys

import midi_play
# Global constants
DATA_DIR = 'sliderData/'
N_MEAN = 20
BAUD = 115200
THRESHOLD = 5000

def main():
	#Store user arguments in list
	arguments = sys.argv
	#Check whether user inputted argument
	if(len(arguments) <= 1):
		raise ValueError("Missing arguments: (1) slider type and (2) model name")
	else:
		slider_type = arguments[1]
	if(len(arguments) <= 2):
		raise ValueError("Missing argument: model name")
	else:
		model = arguments[2]
	#Initialize Serial port of Teensy
	ser = serial.Serial(port='/dev/ttyACM0', baudrate=BAUD)
	func, params = fit_model(DATA_DIR,slider_type,model)
	inport, outport = midi_play.midi_init('Midi Through:Midi Through Port-0 14:0','Midi Through:Midi Through Port-0 14:0')
	midi_play.midi_note_on(outport)
	while(True):
		try:
			x = read_serial(ser)
		except KeyboardInterrupt as e:
			raise
		except Exception as e:
			print("%s -> Whoops! Skipping one datapoint...." % (e))
		if(threshold(x)):
			pos = estimate(func,params,x)
			norm_x = midi_play.to16bit(pos)
			msb,lsb = midi_play.split(norm_x)
			msb_7 = midi_play.to7bit(msb)
			lsb_7 = midi_play.to7bit(lsb)
			midi_play.pitchbend(outport,msb_7,lsb_7)
			#print("{0:d} , {1:d} , {2:d}".format(norm_x,msb_7bit,lsb_7bit))
			#print(norm_x)
			#print(pos)

# x: np.array of shape (,2)
def threshold(x,thr=THRESHOLD):
	ret = (x[0] > thr) & (x[1] > thr)
	return ret


# data_dir: location of csv files
def readData(csv_location):
	files = glob.glob(csv_location + '/*')
	data = np.zeros((0,3))
	for file in files:
		data_i = np.loadtxt(open(file, "rb"), delimiter=",", skiprows=1)
		data = np.append(data,data_i,axis=0)
	return data

# data_dir: location of data folders, model: string
# returns function of model + parameters
def fit_model(data_dir,slider_type,model):
	csv_location = DATA_DIR + str(slider_type)
	# Import training data from csv
	data = readData(csv_location)

	# Preprocess training data
	X = data[:,1:3].transpose()
	y = data[:,0].transpose()

	thismodule = sys.modules[__name__]
	func = getattr(thismodule, model)

	popt, pcov = curve_fit(func, X, y)

	return func, popt

# ser: serial.Serial, n_mean: int
def read_serial(ser,n_mean=N_MEAN):
	#Read from Serial port and convert to string
	reading = ser.readline().decode('utf-8')
	samples = np.zeros([n_mean,2]) # Initialize matrix for calculating mean values
	for j in range(0,n_mean):
		#Read from Serial port and convert to string
		reading = ser.readline().decode('utf-8')
		#String -> numpy array
		samples[j] = np.fromstring(reading, dtype=int, sep=',')[0:2]
	#Generate mean value of both pad values
	x = np.mean(samples,axis=0)
	return x

# model: string, sider_type: string, x: np.array of shape (,2), n_mean: int
def estimate(func,params,x):
	pos = func(x,*params)
	return pos

# Define your models below
def model_1(X,w1,w2):
	return w1*((X[0]-X[1])/(X[0]+X[1])) + w2

def model_2(X,w1,w2,w3):
	return w1*((X[0]-X[1])/(X[0]+X[1])) + w2 + w3

if __name__ == '__main__':
	main()