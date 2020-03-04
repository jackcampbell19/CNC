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





import SVG
import MSTP
# svg = SVG.SVG(200)
# svg.parse('svg/e.svg')
# svg.export('mstp/e.mstp')

e = MSTP.load('mstp/e.mstp')
print(e)

# import Visualization
# Visualization.visualize_mstp(s)