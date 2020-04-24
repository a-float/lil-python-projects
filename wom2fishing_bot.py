from PIL import Image, ImageGrab
import time
import serial
from datetime import datetime
from pynput.keyboard import Key, Listener
from pynput.mouse import Controller

mouse = Controller()

tries = 0
ser = serial.Serial('COM3', 9600)
print(ser.name)
mark  = (500,307)

def catch():
	global tries
	tries += 1
	time.sleep(1)
	print("Catching ", tries, datetime.now())
	ser.write(b'a')

def on_press(key):
	print('{0} key pressed'.format(key))
	if(key == Key.space):
		pos = mouse.position
		global mark
		mark = (pos[0] + 100, pos[1] + 30)
		print("Mark position set to {}".format(mark))
		listener.stop()

# print("Set up the mark position")
# with Listener(
# 	on_press=on_press) as listener:
# 	listener.join()

print("Starting fishing!")
while True:
	im = ImageGrab.grab(bbox=(0,0,600,590))
	#im.save("test.png")
	r,g,b = im.getpixel(mark)
	mouse.position = (mark[0] - 100, mark[1] - 30)
	#print(r,g,b)
	if(r+g+b > 420):
		print(r,g,b)
		catch()
	time.sleep(0.8)