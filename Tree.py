#!/usr/bin/env python

from flask import Flask, render_template
import datetime, opc, time, random
from threading import Thread, Event

#remaped lights to fix wiring issue
lightString = [12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,8,9,10,11,4,5,6,7,0,1,2,3,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93]

#set-up old fade array 105 long
rFade = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, 195, 210, 225, 240, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 240, 225, 210, 195, 180, 165, 150, 135, 120, 105, 90, 75, 60, 45, 30, 15, 0]

#set-up fade array 94 long - designed for 94 light tree
rgbString = [0 for i in range(32)]
for i in range(16):
    rgbString.append(i *17)

for i in range(30):
    rgbString.append(255)
    
for i in range(16):
    rgbString.append(255 - i * 17)

#set-up valentines day strings
valGreenString = [0 for i in range(51)]
valBlueString = [0 for i in range(51)]
for i in range(17):
	valBlueString.append((i+1)*15)
	valGreenString.append((i+1)*15)
for i in range(51):
	valGreenString.append(255)
for i in range(17):
	valGreenString.append(255-i*15)
for i in range(68):
	valGreenString.append(0)
for i in range(119):
	valBlueString.append(255)
for i in range(17):
	valBlueString.append(255-i*15)

#set up pattern thread
thread = Thread()
kill_pattern = Event()

class PatternThread(Thread):
	def __init__(self, pattern):
		self.pattern = pattern
		self.delay = 1
		super(PatternThread,self).__init__()

	def wiggleFade(self):
		print('starting wiggleFade')
		wiggleArray = [0 for i in range(numLEDs)]
		string = [black] * numLEDs
		increment = 0
		for i in range(numLEDs):
			wiggleArray[i] = random.randint(-17, 17)        
		while not kill_pattern.isSet():
			for i in range(numLEDs):
				rVal=(wiggleArray[i]+increment) % 105 
				gVal=(wiggleArray[i]+increment+35) % 105 
				bVal=(wiggleArray[i]+increment+70) % 105 
				string[i] = (rFade[rVal],rFade[gVal],rFade[bVal])
			client.put_pixels(string)
			time.sleep(.25)
			increment = increment + 1

	def rainbowFade(self):
		print('starting rainbowFade')
		string = [black] * 94
		increment = 0
		while not kill_pattern.isSet():
			count = 0
			for i in lightString: 
				rVal=(count + increment) % 94 
				gVal=(count + increment + 31) % 94 
				bVal=(count + increment + 62) % 94
				string[i] = (rgbString[rVal],rgbString[gVal],rgbString[bVal])
				count = count + 1
			client.put_pixels(string)
			time.sleep(1)
			increment = increment + 1

	def crazyWiggleFade(self):
		wiggleArray = [0 for i in range(numLEDs)]
		string = [black] * numLEDs
		increment = 0
		while not kill_pattern.isSet():
			for i in range(numLEDs):
				wiggleArray[i] = random.randint(-17,17)
				rVal=(wiggleArray[i]+increment)%105
				gVal=(wiggleArray[i]+increment+35)%105
				bVal=(wiggleArray[i]+increment+70)%105
				string[i] = (rFade[rVal],rFade[gVal],rFade[bVal])
			client.put_pixels(string)
			time.sleep(.25)
			increment = increment + 1

	def ValentinesDayFade(self):
		print('starting Valentines Day Fade')
		wiggleArray = [0 for i in range(numLEDs)]
		string = [black] * numLEDs
		increment = 0
		for i in range(numLEDs):
			wiggleArray[i] = random.randint(0,204)
		while not kill_pattern.isSet():
			for i in range(numLEDs):
				step=(wiggleArray[i]+increment)%204
				string[i] = (255,valGreenString[step],valBlueString[step])
			client.put_pixels(string)
			time.sleep(.25)
			increment = increment + 1

	def redWiggleFade(self):
		print('starting red wiggle fade')
		wiggleArray = [random.randint(0,1000) for i in range(numLEDs)]
		string = [(0,0,0) for i in range(numLEDs)]
		increment = 0
		while not kill_pattern.isSet():
			for i in range(numLEDs):
				if (wiggleArray[i] + increment) % 1000 > 500:
					wiggle = 1000 - ((wiggleArray[i] + increment) % 1000)
				else:
					wiggle = (wiggleArray[i] + increment) % 1000
				if wiggle < 251:
					gVal = wiggle
					bVal = 0
				else:
					gVal = 0
					bVal = wiggle - 250 
				string[i] = (255,gVal,bVal)
			client.put_pixels(string)
			time.sleep(.25)
			if increment > 4000: # prevent crazy overflow
				increment = 0
			increment +=4



	def run(self):
		if self.pattern == 'wiggleFade':
			self.wiggleFade()
		if self.pattern == 'rainbowFade':
			self.rainbowFade()
		if self.pattern == 'crazyWiggle':
			self.crazyWiggleFade()
		if self.pattern == 'valentinesDay':
			self.ValentinesDayFade()
		if self.pattern == 'redWiggleFade':
			self.redWiggleFade()

#set up server
client = opc.Client('localhost:7890')

#generic string set up
numLEDs=94

#Set default settings
settings = {
	'power' : False,
	'mode' : 'color',
	'wiggle' : False,
	'color' : 'red',
	'run_pattern' : False
}
#set up colors
black=(0,0,0)
blue=(0,0,255)
green=(0,255,0)
pink=(255,0,255)
red=(255,0,0)
teal=(0,255,255)
white=(255,255,255)
yellow=(255,255,0)

app = Flask(__name__)



def solidBlack():
	string = [black]*numLEDs
	client.put_pixels(string)
	client.put_pixels(string)

def solidRed():
    string = [red]*numLEDs
    client.put_pixels(string)
    client.put_pixels(string)

def wiggleRed():
    string = [black]*numLEDs
    for i in range(numLEDs):
        wiggle = random.randint(0, 500)
        if wiggle < 251:
            colorOne = wiggle
            colorTwo = 0
        else:
            colorOne = 0
            colorTwo = wiggle - 250
        string[i]= (255,colorOne,colorTwo)
    client.put_pixels(string)
    client.put_pixels(string)

def solidGreen():
	string = [green]*numLEDs
	client.put_pixels(string)
	client.put_pixels(string)

def wiggleGreen():
    string = [black] * numLEDs
    for i in range(numLEDs):
        wiggle = random.randint(0, 500)
        if wiggle < 251:
            colorOne = wiggle
            colorTwo = 0
        else:
            colorOne = 0
            colorTwo = wiggle - 250
        string[i]= (colorOne, 255, colorTwo)
    client.put_pixels(string)
    client.put_pixels(string)

def solidBlue():
    string = [blue]*numLEDs
    client.put_pixels(string)
    client.put_pixels(string)
	
def wiggleBlue():
    string = [black] * numLEDs
    for i in range(numLEDs):
        wiggle = random.randint(0, 500)
        if wiggle < 251:
            colorOne = wiggle
            colorTwo = 0
        else:
            colorOne = 0
            colorTwo = wiggle - 250
        string[i]= (colorOne,colorTwo,255)
    client.put_pixels(string)
    client.put_pixels(string)

def solidPink():
    string = [pink]*numLEDs
    client.put_pixels(string)
    client.put_pixels(string)

def wigglePink():
    string = [black] * numLEDs
    for i in range(numLEDs):
        wiggle = random.randint(0, 160)
        if wiggle < 81:
            colorOne = wiggle
            colorTwo = 0
        else:
            colorOne = 0
            colorTwo = wiggle - 80
        string[i]= (255-colorOne,0,255-colorTwo)
    client.put_pixels(string)
    client.put_pixels(string)

def solidYellow():
    string = [yellow]*numLEDs
    client.put_pixels(string)
    client.put_pixels(string)

def wiggleYellow():
    string = [black] * numLEDs
    for i in range(numLEDs):
        wiggle = random.randint(0, 160)
        if wiggle < 81:
            colorOne = wiggle
            colorTwo = 0
        else:
            colorOne = 0
            colorTwo = wiggle - 80
        string[i]= (255-colorOne,255-colorTwo,0)
    client.put_pixels(string)
    client.put_pixels(string)

def solidTeal():
    string = [teal]*numLEDs
    client.put_pixels(string)
    client.put_pixels(string)

def wiggleTeal():
    string = [black] * numLEDs
    for i in range(numLEDs):
        wiggle = random.randint(0, 160)
        if wiggle < 81:
            colorOne = wiggle
            colorTwo = 0
        else:
            colorOne = 0
            colorTwo = wiggle - 80
        string[i]= (0,255-colorOne,255-colorTwo)
    client.put_pixels(string)
    client.put_pixels(string)	

def solidWhite():
    string = [white]*numLEDs
    client.put_pixels(string)
    client.put_pixels(string)		

def wiggleWhite():
    string = [black] * numLEDs
    for i in range(numLEDs):
        wiggle = random.randint(0, 240)
        if wiggle < 81:
            colorOne = wiggle
            colorTwo = 0
            colorThree = 0
        elif wiggle > 81 and wiggle < 161:
            colorOne = 0
            colorTwo = wiggle - 80
            colorThree = 0
        else:
            colorOne = 0
            colorTwo = 0
            colorThree = wiggle -160
        string[i]= (255-colorOne,255 - colorTwo, 255-colorThree)
    client.put_pixels(string)
    client.put_pixels(string)

def setColor():
	if settings['color'] == 'red':
		if settings['wiggle']==True:
			wiggleRed()
		else:
			solidRed()

	if settings['color'] == 'green':
		if settings['wiggle']==True:
			wiggleGreen()
		else:
			solidGreen()

	if settings['color'] == 'blue':
		if settings['wiggle']==True:
			wiggleBlue()
		else:
			solidBlue()

	if settings['color'] == 'yellow':
		if settings['wiggle']==True:
			wiggleYellow()
		else:
			solidYellow()

	if settings['color'] == 'teal':
		if settings['wiggle']==True:
			wiggleTeal()
		else:
			solidTeal()

	if settings['color'] == 'pink':
		if settings['wiggle']==True:
			wigglePink()
		else:
			solidPink()

	if settings['color'] == 'white':
		if settings['wiggle']==True:
			wiggleWhite()
		else:
			solidWhite()			

@app.route("/")
def main():
	templateData = {
		'settings' : settings
		}
	return render_template('main.html', **templateData)

@app.route("/power/<action>")
def power(action):
	if action == "on":
		# update the dictionary 
		settings['power']=True
		wiggleRed()

	if action == "off":
		# update the dictionary 
		settings['power']=False
		solidBlack()

	templateData = {
	'settings' : settings
	}
	return render_template('main.html', **templateData)

@app.route("/color/<action>")
def changeColor(action):
	settings['color']=action

	setColor()

	templateData = {
	'settings' : settings
	}					
	return render_template('main.html', **templateData)

@app.route("/mode/<action>")
def changeMode(action):
	if action == 'color':
		settings['mode']='color'
		setColor()

	if action == 'pattern':
		settings['mode']='pattern'

	templateData = {
	'settings' : settings
	}					
	return render_template('main.html', **templateData)

@app.route("/wiggle/<action>")
def changeWiggle(action):
	if action == 'on':
		settings['wiggle']=True

	if action == 'off':
		settings['wiggle']=False

	setColor()

	templateData = {
	'settings' : settings
	}					
	return render_template('main.html', **templateData)

@app.route("/pattern/<action>")
def patternToggle(action):
	global thread
	global kill_pattern
	if action == 'wiggleFade':
		settings['run_pattern']=True
		if not thread.isAlive():
			kill_pattern.clear()
			print "Starting Thread"
			thread = PatternThread('wiggleFade')
			thread.start()

	if action == 'rainbowFade':
		settings['run_pattern']=True
		if not thread.isAlive():
			kill_pattern.clear()
			print "Starting Thread"
			thread = PatternThread('rainbowFade')
			thread.start()

	if action == 'crazyWiggle':
		settings['run_pattern']=True
		if not thread.isAlive():
			kill_pattern.clear()
			print "Starting Thread"
			thread = PatternThread('crazyWiggle')
			thread.start()

	if action == 'valentinesDay':
		settings['run_pattern']=True
		if not thread.isAlive():
			kill_pattern.clear()
			print "Starting Thread"
			thread = PatternThread('valentinesDay')
			thread.start()

	if action == 'redWiggleFade':
		settings['run_pattern']=True
		if not thread.isAlive():
			kill_pattern.clear()
			print "Starting Thread"
			thread = PatternThread('redWiggleFade')
			thread.start()

	if action == 'stop':
		print "killing Thread"
		settings['run_pattern']=False
		kill_pattern.set()

	templateData = {
	'settings' : settings
	}					
	return render_template('main.html', **templateData)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)

