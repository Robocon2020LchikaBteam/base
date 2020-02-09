from __future__ import division
import time
import Adafruit_PCA9685

#from tkinter import *

# pwm = Adafruit_PCA9685.PCA9685()
pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)  #addres 41

pwm.set_pwm_freq(50)

def calcDuty(angle):
	duty = int( float(angle) * 2.17 + 102 )
	return duty

def selectPhase(phase_number,color):
	num = 3
	if phase_number == 0:
		# initialize 0
		pwm.set_pwm(1, 0, calcDuty(0))    # ch,on,duty
		pwm.set_pwm(0, 0, calcDuty(0))
		print("ini")
		pwm.set_pwm(0, 0, calcDuty(7))	# sometimes err??
		time.sleep(1)
	elif phase_number == 1:
		# stop phase 1
		pwm.set_pwm(1, 0, calcDuty(0))    # ch,on,duty
		pwm.set_pwm(0, 0, calcDuty(7))
		print("stop")
		time.sleep(1)
	elif phase_number == 2:
		# judge phase 2 dummy
#		if color == 'null':
#			num = input("blue:0 red:1 ")
#			pwm.set_pwm(1, 0, calcDuty(0))    # ch,on,duty
#			pwm.set_pwm(0, 0, calcDuty(0))
#			print(num)

		# ball carry phase 3
		if int(num) == 0 or color == 'blue':
			pwm.set_pwm(1, 0, calcDuty(0))    # ch,on,duty
			pwm.set_pwm(0, 0, calcDuty(0))
			time.sleep(2)
			print("blue")
			pwm.set_pwm(0, 0, calcDuty(20))
			pwm.set_pwm(1, 0, calcDuty(7))
			pwm.set_pwm(0, 0, calcDuty(80))
			time.sleep(2)
			pwm.set_pwm(1, 0, calcDuty(0))
		elif int(num) == 1 or color == 'red':
			pwm.set_pwm(1, 0, calcDuty(0))    # ch,on,duty
			pwm.set_pwm(0, 0, calcDuty(0))
			time.sleep(2)
			print("red")
			pwm.set_pwm(1, 0, calcDuty(20))
			pwm.set_pwm(0, 0, calcDuty(7))
			pwm.set_pwm(1, 0, calcDuty(80))
			time.sleep(2)
			pwm.set_pwm(1, 0, calcDuty(0))
		pwm.set_pwm(0, 0, calcDuty(7))
		pwm.set_pwm(1, 0, calcDuty(0))

		time.sleep(1)


