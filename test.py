from Motor import Stepper
import RPi.GPIO as gpio
# import signal
import time
#
#
# def keyboardInterruptHandler(signal, frame):
#     print("Program interrupted. Cleaning up.")
#     x_motor.switch_off()
#     y_motor.switch_off()
#     z_motor.switch_off()
#     GPIO.cleanup()
#     exit(0)
#
#
# signal.signal(signal.SIGINT, keyboardInterruptHandler)

x_motor = Stepper(11, 12)
# y_motor = Stepper(13, 15)
# z_motor = Stepper(16, 18)

# t = x_motor.rotate_to(9250)
# t.start()
# t.join()
#
# t = x_motor.rotate_to(0)
# t.start()
# t.join()


t = x_motor.rotate_to(2000)
t.start()
t.join()

t = x_motor.rotate_to(0)
t.start()
t.join()




gpio.cleanup()
