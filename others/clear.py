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
while True:
    #scanning(0.3)
    time.sleep(0.3)
