import socket
from pynput.keyboard import Key, Controller

keyboard = Controller()

HOST = '192.168.137.1'  # Standard loopback interface address (localhost)
PORT = 65432	# Port to listen on (non-privileged ports are > 1023)

leftw=97
rightw=1004
upw=119
downw=115
lefts=276
rights=275
ups=273
downs=274

arrows = {lefts:Key.left, rights:Key.right, ups:Key.up, downs:Key.down}

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.bind((HOST, PORT))
	s.listen()
	conn, addr = s.accept()
	with conn:
		print('Connected by', addr)
		while True:
			data = conn.recv(1024)
			if data:
				d = data.decode('utf-8')
				words = d.split(" ")
				for i in range(1,len(words),2):
					key, switch = int(words[i-1]), words[i]
					if(switch == 'u'):
						if key in arrows.keys():
							keyboard.release(arrows[key])
						else:
							keyboard.release(chr(key))
						print(chr(key)+" up")
					elif(switch == 'd'):
						if key in arrows.keys():
							keyboard.press(arrows[key])
						else:
							keyboard.press(chr(key))
						print(chr(key)+" down")
			else:
				break;