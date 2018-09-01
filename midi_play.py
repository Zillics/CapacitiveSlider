import mido

def print_ports():
	print("INPUT PORTS:")
	print(mido.get_input_names())
	print("OUTPUT PORTS:")
	print(mido.get_output_names())

def midi_init(input_port, output_port):
	input_port = mido.open_input(input_port)
	output_port = mido.open_output(output_port)
	return input_port, output_port

# 48 = C3
def midi_note_on(outport,pitch=48,velocity=100):
	outport.send(mido.Message.from_bytes([0x90, pitch, velocity]))

def midi_note_off(outport,pitch=48,velocity=100):
	outport.send(mido.Message.from_bytes([0x80, pitch, velocity]))

def pitchbend(outport,lsb,msb):
	outport.send(mido.Message.from_bytes([0xE0, lsb, msb]))

# Turns value x of range (mini,maxi) to range (0,16 384)s
def normalize(x,mini=0,maxi=30):
	norm_x = (x/(maxi-mini))*16384
	return int(norm_x)

# Splits value of (0 - 16 384) into lsb (0-127) and msb (0-127)
def split(value):
	msb = value >> 8
	lsb = (value << 8) >> 8  
	return lsb, msb
