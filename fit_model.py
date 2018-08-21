import glob
import numpy as np
from scipy.optimize import curve_fit
import serial
import inspect
import sys
# Global constants
DATA_DIR = 'sliderData/'
N_MEAN = 30

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
	#Define number of samples taken for calculating mean
	estimate(model,slider_type)


def readData(data_dir):
	files = glob.glob(data_dir + '/*')
	data = np.zeros((0,3))
	for file in files:
		data_i = np.loadtxt(open(file, "rb"), delimiter=",", skiprows=1)
		data = np.append(data,data_i,axis=0)
	return data

def fit_model(data,model):
	X = data[:,1:3].transpose()
	y = data[:,0].transpose()
	popt, pcov = curve_fit(model, X, y)
	return popt

def estimate(model,slider_type):
	data = readData(DATA_DIR + str(slider_type))
	thismodule = sys.modules[__name__]
	func = getattr(thismodule, model)
	popt = fit_model(data,func)
	samples = np.zeros([N_MEAN,2]) # Initialize matrix for calculating mean values
	#Initialize Serial port of Teensy
	ser = serial.Serial(port='/dev/ttyACM0', baudrate=9600)
	while(True):
		for j in range(0,N_MEAN):
			#Read from Serial port and convert to string
			reading = ser.readline().decode('utf-8')
			#String -> numpy array
			samples[j] = np.fromstring(reading, dtype=int, sep=',')[0:2]
		#Generate mean value of both pad values
		x = np.mean(samples,axis=0).astype(int)
		pos = func(x,*popt)
		print(pos)

# Define your models here:
def model_1(X,w1,w2):
	return w1*((X[0]-X[1])/(X[0]+X[1])) + w2

def model_2(X,w1,w2,w3):
	return w1*((X[0]-X[1])/(X[0]+X[1])) + w2 + w3

if __name__ == '__main__':
	main()