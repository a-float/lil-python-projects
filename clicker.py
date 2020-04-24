from pynput import mouse, keyboard
import time
working = True
mousecon = mouse.Controller()
print('its on')
times = 100
def on_press(key):
    try:
    	print(key.char)
    	if(key.char == 'x'):
    		print('will click '+str(times) + " times")
    		#for i in range(times):
    		mousecon.click(mouse.Button.left,times)
    			#time.sleep(0.02)
    		print('done')
    		return False
    	elif(key.char == 'q'):
    		global working
    		working = False
    		return False
    except AttributeError:
        print('special key {0} pressed'.format(key))

def on_release(key):
	pass

while working:
	with keyboard.Listener(
	        on_press=on_press,
	        on_release=on_release) as listener:
	    listener.join()

