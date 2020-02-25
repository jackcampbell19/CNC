from Motor import Stepper
import RPi.GPIO as GPIO
import signal
import time


def keyboardInterruptHandler(signal, frame):
    print("Program interrupted. Cleaning up.")
    y_motor.switch_off()
    x_motor.switch_off()
    GPIO.cleanup()
    exit(0)


signal.signal(signal.SIGINT, keyboardInterruptHandler)


y_motor = Stepper(13, 11, 15, 12, 1.8, Stepper.FULL_STEP_SEQUENCE)
x_motor = Stepper(22, 18, 24, 16, 1.8, Stepper.FULL_STEP_SEQUENCE)


print("Running x_motor forward.")
for _ in range(200):
    x_motor.step(True)
    time.sleep(0.01)

print("Running x_motor backward.")
for _ in range(200):
    x_motor.step(False)
    time.sleep(0.01)

print("Running y_motor forward.")
for _ in range(200):
    y_motor.step(True)
    time.sleep(0.01)

print("Running y_motor backward.")
for _ in range(200):
    y_motor.step(False)
    time.sleep(0.01)

print("Running both forward.")
for _ in range(200):
    x_motor.step(True)
    y_motor.step(True)
    time.sleep(0.01)

print("Running both backward.")
for _ in range(200):
    x_motor.step(False)
    y_motor.step(False)
    time.sleep(0.01)

GPIO.cleanup()