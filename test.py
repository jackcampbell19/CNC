from Motor import Stepper
import RPi.GPIO as GPIO
import signal
import time


def keyboardInterruptHandler(signal, frame):
    print("Program interrupted. Cleaning up.")
    x_motor.switch_off()
    y_motor.switch_off()
    z_motor.switch_off()
    GPIO.cleanup()
    exit(0)


signal.signal(signal.SIGINT, keyboardInterruptHandler)


x_motor = Stepper(11, 12, 13, 15, 16)
y_motor = Stepper(21, 19, 22, 23, 18)
z_motor = Stepper(29, 31, 36, 37, 32)






x_motor.switch_off()
y_motor.switch_off()
z_motor.switch_off()
GPIO.cleanup()
