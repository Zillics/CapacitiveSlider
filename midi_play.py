import mido
import numpy as np
import fit_model
import serial

BAUD = 115200
THRESHOLD = 4500
N_MEAN = 4

def print_ports():
	print("INPUT PORTS:")
	print(mido.get_input_names())
	print("OUTPUT PORTS:")
	print(mido.get_output_names())

def midi_init(input_port, output_port):
	if(input_port == ""):
		inport = mido.open_input()
	else:
		inport = mido.open_input(input_port)
	if(output_port == ""):
		outport = mido.open_output()
	else:
		outport = mido.open_output(output_port)
	return inport, outport

# 48 = C3
def midi_note_on(outport,channel,pitch=48,velocity=100):
	cmd = 0x90 + channel
	outport.send(mido.Message.from_bytes([cmd, pitch+channel, velocity]))


def midi_note_off(outport,channel,pitch=48,velocity=100):
	cmd = 0x80 + channel
	outport.send(mido.Message.from_bytes([cmd, pitch+channel, velocity]))


def pitchbend(outport,value,channel):
	int_16 = to16bit(value)
	msb,lsb = split(int_16)
	msb = to7bit(msb)
	lsb = to7bit(lsb)
	cmd = 0xE0 + channel
	outport.send(mido.Message.from_bytes([cmd, lsb, msb]))

# Turns value x of range (mini,maxi) 16 bit integer
def to16bit(x,mini=0,maxi=30):
	norm_x = int((x/(maxi-mini))*65536)
	return np.uint16(norm_x)

# Convert (default 8 bit) to 7 bit
def to7bit(x,maxi=255):
	return int((x/maxi)*127)


# Splits value of (0 - 65 535) into lsb (0-127) and msb (0-127)
def split(value):
	msb = value >> 8
	mask = np.uint8(0b11111111)
	lsb = value & mask
	return msb, lsb

class Instrument:
	def __init__(self):
		self.sliders = [] # List of Slider objects
		self.inport,self.outport = midi_init("","")

	def add_slider(self,slider_type,model,channel,thresh=THRESHOLD):
		self.sliders.append(Slider(slider_type,model,channel,thresh))

	def update_readings(self,ser,n_mean=N_MEAN):
		#Read from Serial port and convert to string
		reading = ser.readline().decode('utf-8')
		n = len(self.sliders)*2 # Number of raw values from serial to extract
		samples = np.zeros([n_mean,n]) # Initialize matrix for calculating mean values
		for j in range(0,n_mean):
			#Read from Serial port and convert to string
			reading = ser.readline().decode('utf-8')
			#String -> numpy array
			samples[j] = np.fromstring(reading, dtype=int, sep=',')[0:n]
		#Generate mean value of both pad values
		x = np.mean(samples,axis=0)
		
		for slider in self.sliders:
			idx = slider.channel*2
			slider.update_reading(x[idx],x[idx+1])

	def play(self):
		#Initialize Serial port of Teensy
		ser = serial.Serial(port='/dev/ttyACM1', baudrate=BAUD)
		while(True):		
			self.update_readings(ser)
			for slider in self.sliders:
				pos = slider.estimate()
				if(slider.pressed):
					if(slider.over_threshold()):
						pitchbend(self.outport,pos,slider.channel)
					else:
						midi_note_off(self.outport,slider.channel)
						slider.pressed = False
				else:
					if(slider.over_threshold()):
						midi_note_on(self.outport,slider.channel)
						pitchbend(self.outport,pos,slider.channel)
						slider.pressed = True

class Slider:
	def __init__(self,slider_type,model,channel,thresh=THRESHOLD):
		self.slider_type = slider_type
		self.model = model
		self.func, self.params = fit_model.fit_model(slider_type,model)
		self.pressed = False
		self.channel = channel
		self.threshold = thresh
		self.reading = np.zeros(2)
	# threshold() : Condition for activating a note
	# x: np.array of shape (,2)
	def update_reading(self,v1,v2):
		self.reading[0] = v1
		self.reading[1] = v2

	def over_threshold(self):
		ret = (self.reading[0] > self.threshold) & (self.reading[1] > self.threshold)
		return ret

	def estimate(self):
		pos = fit_model.estimate(self.func,self.params,self.reading) # Estimate finger position
		return pos

def main():
	instr = Instrument()
	instr.add_slider('red','model_1',0)
	instr.add_slider('green','model_1',1,2000)
	instr.add_slider('beige','model_1',2)
	instr.play()

if __name__ == '__main__':
	main()