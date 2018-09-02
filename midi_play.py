import mido
import numpy as np

def print_ports():
	print("INPUT PORTS:")
	print(mido.get_input_names())
	print("OUTPUT PORTS:")
	print(mido.get_output_names())

def midi_init(input_port, output_port):
	inport = mido.open_input(input_port)
	outport = mido.open_output(output_port)
	return inport, outport

# 48 = C3
def midi_note_on(outport,pitch=48,velocity=100):
	outport.send(mido.Message.from_bytes([0x90, pitch, velocity]))

def midi_note_off(outport,pitch=48,velocity=100):
	outport.send(mido.Message.from_bytes([0x80, pitch, velocity]))

def pitchbend(outport,msb,lsb):
	outport.send(mido.Message.from_bytes([0xE0, lsb, msb]))

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
