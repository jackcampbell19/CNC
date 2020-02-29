from Motor import *
import RPi.GPIO as GPIO
import json
import math

class CNC:

    MODE_CALIBRATE = 'mode-calibrate'
    MODE_DRAW_2D = 'mode-draw-2d'
    MODE_MILL_3D = 'mode-mill-3d'

    def __init__(self, spr, error_handler):
        # Motor steps per rotation
        self.SPR = spr
        # Error handler
        self.error_handler = error_handler
        # X size in number of steps
        self.XSIZE = 0
        # Y size in number of steps
        self.YSIZE = 0
        # Z size in number of steps
        self.ZSIZE = 0
        # Loaded mstp data
        self.mstp = None
        # Mode
        self.mode = None
        # Motors
        self.x_motor = Stepper(11, 12, 13, 15, 16)
        self.y_motor = Stepper(21, 19, 22, 23, 18)
        self.z_motor = Stepper(29, 31, 36, 37, 32)

    def load_mstp(self, filename):
        with open(filename) as mstp_file:
            self.mstp = json.load(mstp_file)

    # Position the pen up for drawing mstp.
    def pen_down(self):
        t = self.z_motor.rotate_to(0)
        t.start()
        t.join()

    # Sets the position to the given xy coordinate. DO NOT USE FOR ACCURATE STEPPING.
    def set_position(self, x=None, y=None, z=None):
        threads = []
        if x:
            threads.append(self.x_motor.rotate_to(x))
        if y:
            threads.append(self.y_motor.rotate_to(y))
        if z:
            threads.append(self.z_motor.rotate_to(z))
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    # Draw the loaded 2D sequence.
    def draw_2d(self):
        for [(x, y, z), sequence] in self.mstp:
            self.set_position(z=20)
            self.set_position(x, y)
            self.set_position(z=0)
            for [dx, dy, _] in sequence:
                if dx == -1:
                    self.x_motor.step(False)
                elif dx == 1:
                    self.x_motor.step(True)
                if dy == -1:
                    self.y_motor.step(False)
                elif dy == 1:
                    self.y_motor.step(True)
                sleep(Stepper.SHORTEST_DELAY)

    # Runs the current mstp file.
    def run(self):
        if not self.mstp:
            self.error_handler('Missing .mstp file.')
            return
        if not self.mode:
            self.error_handler('Mode has not been set.')
            return
        if self.mode == self.MODE_CALIBRATE:
            pass
        elif self.mode == self.MODE_DRAW_2D:
            self.draw_2d()
        elif self.mode == self.MODE_MILL_3D:
            pass

    # Shuts the cnc down.
    def shutdown(self):
        self.x_motor.switch_off()
        self.y_motor.switch_off()
        self.z_motor.switch_off()
        GPIO.cleanup()