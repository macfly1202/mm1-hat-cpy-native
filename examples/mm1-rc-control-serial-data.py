# CircuitPython Test for Robotics Masters MM1
#
# Notes:
#   This is to be run using CircuitPython 4.0
#   Date: 15/05/2019
#
import time
import board
import busio

#from analogio import AnalogIn
from digitalio import DigitalInOut, Direction

from pulseio import PWMOut, PulseIn, PulseOut
from array import array
#from adafruit_motor import servo

## set up on-board LED
led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
led.value = 1

## set up serial UART
# note UART(TX, RX, baudrate)
uart = busio.UART(board.UART_TX, board.UART_RX, baudrate=115200)

## set up servos and radio control channels
steering_pwm = PWMOut(board.SERVO1, duty_cycle=2 ** 15, frequency=50)
throttle_pwm = PWMOut(board.SERVO2, duty_cycle=2 ** 15, frequency=50)

steering_channel = PulseIn(board.RCH1, maxlen=64, idle_state=0)
throttle_channel = PulseIn(board.RCH2, maxlen=64, idle_state=0)

## Set some other variables
SMOOTHING_INTERVAL_IN_S = 0.025
DEBUG = False
last_update = time.monotonic()


class Control:
     def __init__(self, name, servo, channel, value):
	self.name = name
	self.servo = servo
	self.channel = channel
	self.value = value
	self.servo.duty_cycle = servo_duty_cycle(value)

## Hardware Notification: starting
print("preparing to start..")
for i in range(0, 2):
	led.value = True
	time.sleep(0.5)
	led.value = False
	time.sleep(0.5)

## GO TO: main()

## functions
def get_voltage(pin):
	return (pin.value * 3.3) / 65536

def servo_duty_cycle(pulse_ms, frequency = 50):
	period_ms = 1.0 / frequency * 1000.0
	duty_cycle = int(pulse_ms / 1000 / (period_ms / 65535.0))
	return duty_cycle

def get_angle(time):
	# TODO: 1000ms==0°, 2000ms==270°. So: (ms-999)*1001/270
	return (time)/(18) + 7.5

def state_changed(control):
	control.channel.pause()
	for i in range(0, len(control.channel)):
		val = control.channel[i]
		if(val < 1000 or val > 2000):
			continue
		control.value = (control.value + val) /2
#		print(control.channel[i])

	if DEBUG:
		print("%f\t%s (%i): %i (%i)" % (time.monotonic(), control.name, len(control.channel), control.value, servo_duty_cycle(control.value)))
	control.channel.clear()
	control.channel.resume()

steering = Control("Steering", steering_pwm, steering_channel, 1500)
throttle = Control("Throttle", throttle_pwm, throttle_channel, 1000)

def main():
	global last_update
	while True:
    # TODO: serial send data
		if(last_update + SMOOTHING_INTERVAL_IN_S > time.monotonic()):
			continue
		last_update = time.monotonic()

		if(len(throttle.channel) != 0):
			state_changed(throttle)

		if(len(steering.channel) != 0):
			state_changed(steering)

		print("%i, %i" % (int(steering.value), int(throttle.value)))
		steering.servo.duty_cycle = servo_duty_cycle(steering.value)
		throttle.servo.duty_cycle = servo_duty_cycle(throttle.value)


## Run
print("Run!")
main()
