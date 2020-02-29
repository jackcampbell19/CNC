# from Motor import Stepper
# import RPi.GPIO as GPIO
# import signal
# import time
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
#
#
# x_motor = Stepper(11, 12, 13, 15, 16)
# y_motor = Stepper(21, 19, 22, 23, 18)
# z_motor = Stepper(29, 31, 36, 37, 32)
#
#
#
# t = x_motor.rotate_to(200)
# t.start()
# t.join()
# t = y_motor.rotate_to(400)
# t.start()
# t.join()
# t1 = x_motor.rotate_to(0)
# t2 = y_motor.rotate_to(0)
# t1.start()
# t2.start()
# t1.join()
# t2.join()
# t = z_motor.rotate_to(50)
# t.start()
# t.join()
# t3 = z_motor.rotate_to(0)
# t3.start()
# t3.join()
#
#
#
#
# x_motor.switch_off()
# y_motor.switch_off()
# z_motor.switch_off()
# GPIO.cleanup()

import SVG
svg = SVG.SVG(200)
s = svg.parse('svg/void-01.svg')
svg.export(s, 'text.mstp')
import Visualization
Visualization.visualize_mstp(s)