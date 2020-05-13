from __future__ import division
import time
import Adafruit_PCA9685

# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()
# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

# Configure min and max servo pulse lengths
servo_min = 150  # Min pulse length out of 4096
servo_max = 500  # Max pulse length out of 4096

# Helper function to make setting a servo pulse width simpler.
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 50       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

#get pulse from degree
def map(x):
    degree_min = -90
    degree_max = 90
    pulse_min = 150
    pulse_max = 600
    y = (x - degree_min) * (pulse_max - pulse_min) / (degree_max - degree_min) + pulse_min
    return int(y)

# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(50)

def run(delay):
    pwm.set_pwm(0, 0, map(0))
    pwm.set_pwm(1, 0, map(0))
    time.sleep(delay)
    pwm.set_pwm(0, 0, map(-20))
    pwm.set_pwm(1, 0, map(+30))
    time.sleep(delay)
    pwm.set_pwm(0, 1, map(0))
    pwm.set_pwm(1, 1, map(0))
    time.sleep(delay)
    pwm.set_pwm(0, 1, map(+20))
    pwm.set_pwm(1, 1, map(-30))
    time.sleep(delay)
    pwm.set_pwm(0, 1, map(0))
    pwm.set_pwm(1, 1, map(0))
    time.sleep(delay*10)

def scanning(delay):
    for degree in [-30, 20, 0, -20, 30]:
        pwm.set_pwm(0, 0, map(degree))
        for degree2 in [0, -20, 20, -10, 10, 0]:
			pwm.set_pwm(1, 0, map(degree2))
			time.sleep(delay)
			
    for degree in [-40, 30, -20, 10, 0, 40, -30, 20, -10, 0]:
        pwm.set_pwm(0, 0, map(degree))
        time.sleep(delay)
        pwm.set_pwm(1, 0, map(degree))
        time.sleep(delay)

print('Moving servo on channel 0, press Ctrl-C to quit...')
#scanning(0.3)

#parti del corpo
HEAD = 0
NECK = 1
RIGHT_FRONT_SHOULDER=2
RIGHT_FRONT_ARM=3
LEFT_FRONT_SHOULDER=4
LEFT_FRONT_ARM=5
RIGHT_BACK_SHOULDER=6
RIGHT_BACK_ARM=7
LEFT_BACK_SHOULDER=8
LEFT_BACK_ARM=9

#movimento
def move(joint, degree):
	sign = 1
	if(joint in [NECK, LEFT_FRONT_ARM, RIGHT_BACK_ARM, RIGHT_FRONT_SHOULDER, RIGHT_BACK_SHOULDER]): sign = -1
	pwm.set_pwm(joint, 0, map(degree*sign))
	print("pwm.set_pwm("+str(joint)+", 0, map("+str(degree*sign)+"))")

def clear():
	pwm = Adafruit_PCA9685.PCA9685()

def esercise1(joint):
	move(joint, 0)
	time.sleep(0.3)
	for degree in [30, 0, 30, 0, 30, 0]:
		move(joint, degree)
		time.sleep(0.2)
	time.sleep(0.5)
	for degree in [-30, 0, -30, 0, -30, 0]:
		move(joint, degree)
		time.sleep(0.2)
	time.sleep(0.5)	
'''
#posizione iniziale
for degree in [60, 0, 60]:
	move(HEAD, 0)
	move(NECK, 0)
	move(RIGHT_FRONT_SHOULDER, 0)
	move(RIGHT_FRONT_ARM, degree)
	move(LEFT_FRONT_SHOULDER, 0)
	move(LEFT_FRONT_ARM, degree)
	move(RIGHT_BACK_SHOULDER, 0)
	move(RIGHT_BACK_ARM, degree)
	move(LEFT_BACK_SHOULDER, 0)
	move(LEFT_BACK_ARM, degree)
	time.sleep(0.5)

#esercizio1
esercise1(HEAD)
esercise1(NECK)
move(RIGHT_FRONT_ARM, 0)
esercise1(RIGHT_FRONT_SHOULDER)
esercise1(RIGHT_FRONT_ARM)
move(RIGHT_FRONT_ARM, 60)
move(LEFT_FRONT_ARM, 0)
esercise1(LEFT_FRONT_SHOULDER)
esercise1(LEFT_FRONT_ARM)
move(LEFT_FRONT_ARM, 60)
move(RIGHT_BACK_ARM, 0)
esercise1(RIGHT_BACK_SHOULDER)
esercise1(RIGHT_BACK_ARM)
move(RIGHT_BACK_ARM, 60)
move(LEFT_BACK_ARM, 0)
esercise1(LEFT_BACK_SHOULDER)
esercise1(LEFT_BACK_ARM)
move(LEFT_BACK_ARM, 60)
time.sleep(0.5)
'''
move(HEAD, 0)
move(NECK, 0)
move(RIGHT_FRONT_SHOULDER, 0)
move(RIGHT_FRONT_ARM, 50)
move(LEFT_FRONT_SHOULDER, 0)
move(LEFT_FRONT_ARM, 50)
move(RIGHT_BACK_SHOULDER, 0)
move(RIGHT_BACK_ARM, 50)
move(LEFT_BACK_SHOULDER, 0)
move(LEFT_BACK_ARM, 50)
time.sleep(1)


#step
move(RIGHT_FRONT_ARM, -30)
move(LEFT_BACK_ARM, -30)
time.sleep(0.3)
move(RIGHT_FRONT_SHOULDER, 30)
move(LEFT_BACK_SHOULDER, 30)
time.sleep(0.3)
move(RIGHT_FRONT_ARM, 50)
move(LEFT_BACK_ARM, 50)
time.sleep(0.3)
move(RIGHT_FRONT_SHOULDER, -30)
move(LEFT_BACK_SHOULDER, -30)
time.sleep(0.3)
move(LEFT_FRONT_ARM, -30)
move(RIGHT_BACK_ARM, -30)
time.sleep(0.3)
move(LEFT_FRONT_SHOULDER, 30)
move(RIGHT_BACK_SHOULDER, 30)
time.sleep(0.3)
move(LEFT_FRONT_ARM, 50)
move(RIGHT_BACK_ARM, 50)
time.sleep(0.3)
move(LEFT_FRONT_SHOULDER, -30)
move(RIGHT_BACK_ARM, 50)
time.sleep(0.3)


move(HEAD, 0)
move(NECK, 0)
move(RIGHT_FRONT_SHOULDER, 0)
move(RIGHT_FRONT_ARM, 50)
move(LEFT_FRONT_SHOULDER, 0)
move(LEFT_FRONT_ARM, 50)
move(RIGHT_BACK_SHOULDER, 0)
move(RIGHT_BACK_ARM, 50)
move(LEFT_BACK_SHOULDER, 0)
move(LEFT_BACK_ARM, 50)
time.sleep(0.5)

scanning(0.3)

#pulitura
clear()
