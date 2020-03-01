from Motor import *
import RPi.GPIO as GPIO
import json
import math

class CNC:

    MODE_CALIBRATE = 'calibrate'
    MODE_DRAW_2D = 'draw-2d'
    MODE_MILL_2D = 'mill-2d'
    MODE_MILL_3D = 'mill-3d'
    MODE_PRINT_3D = 'print-3d'

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
        self.mstp_data = None
        self.safe_height = 200
        self.step_down = None
        # Mode
        self.mode = None
        # Motors
        self.x_motor = Stepper(11, 12, 13, 15, 16)
        self.y_motor = Stepper(21, 19, 22, 23, 18)
        self.z_motor = Stepper(29, 31, 36, 37, 32)

    def load_mstp(self, filename):
        with open(filename) as mstp_file:
            mstp = json.load(mstp_file)
            self.mstp_data = mstp['data']
            sh = mstp['meta']['safe-height']
            if sh:
                self.safe_height = sh
            sd = mstp['meta']['step-down']
            if sd:
                self.step_down = sd
            m = mstp['meta']['mode']
            if m == self.MODE_DRAW_2D:
                self.mode = self.MODE_DRAW_2D
            elif m == self.MODE_MILL_3D:
                self.mode = self.MODE_MILL_3D
            elif m == self.MODE_MILL_2D:
                self.mode = self.MODE_MILL_2D
            elif m == self.MODE_PRINT_3D:
                self.mode = self.MODE_PRINT_3D

    # Sets the position to the given xy coordinate. DO NOT USE FOR ACCURATE STEPPING.
    def set_position(self, x=None, y=None, z=None):
        threads = []
        if x is not None:
            threads.append(self.x_motor.rotate_to(x))
        if y is not None:
            threads.append(self.y_motor.rotate_to(y))
        if z is not None:
            threads.append(self.z_motor.rotate_to(z))
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    # Draw the loaded 2D sequence.
    def draw_2d(self):
        if not self.mstp_data:
            self.error_handler('Missing .mstp file.')
            return
        for [(x, y, _), sequence] in self.mstp_data:
            self.set_position(z=self.safe_height)
            self.set_position(x=x, y=y)
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
        self.return_to_origin()

    # Runs the current mstp file.
    def run(self):
        if not self.mode:
            self.error_handler('Mode has not been set.')
            return
        if self.mode == self.MODE_CALIBRATE:
            pass
        elif self.mode == self.MODE_DRAW_2D:
            self.draw_2d()
        elif self.mode == self.MODE_MILL_3D:
            pass

    def return_to_origin(self):
        self.set_position(z=self.safe_height)
        self.set_position(x=0, y=0)
        self.set_position(z=0)

    # Shuts the cnc down.
    def shutdown(self):
        self.return_to_origin()
        self.x_motor.switch_off()
        self.y_motor.switch_off()
        self.z_motor.switch_off()
        GPIO.cleanup()
