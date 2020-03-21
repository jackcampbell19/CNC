from Motor import *
import RPi.GPIO as gpio
import MSTP
from Line import calculate_line_steps


class CNC:

    def __init__(self, spr, error_handler):
        # Motor steps per rotation
        self.SPR = spr
        # Error handler
        self.error_handler = error_handler
        # Dimensions (x, y, z)
        self.dimensions = (0, 0, 0)
        # Loaded mstp data
        self.mstp = None
        # Motors
        self.x_motor = Stepper(11, 12)
        self.y_motor = Stepper(13, 15)
        self.z_motor = Stepper(16, 18)

    def set_mstp(self, mstp):
        self.mstp = mstp

    def load_mstp(self, filename):
        self.mstp = MSTP.load(filename)

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

    def current_position(self):
        return self.x_motor.current_step, self.y_motor.current_step, self.z_motor.current_step

    # Runs the current mstp file.
    def run(self):
        if self.mstp is None:
            self.error_handler('Missing .mstp file.')
        self.return_to_origin()
        current_position = (0, 0, 0)
        for x in range(len(self.mstp['data'])):
            next_position = self.mstp['data'][x]
            sequence = calculate_line_steps(current_position, next_position)
            for dx, dy, dz in sequence:
                if dx == 1:
                    self.x_motor.step(True)
                elif dx == -1:
                    self.x_motor.step(False)
                if dy == 1:
                    self.y_motor.step(True)
                elif dy == -1:
                    self.y_motor.step(False)
                if dz == 1:
                    self.z_motor.step(True)
                elif dz == -1:
                    self.z_motor.step(False)
            current_position = next_position

    def return_to_origin(self):
        if self.x_motor.current_step == 0 \
                and self.y_motor.current_step == 0 \
                and self.z_motor.current_step == 0:
            return
        self.set_position(z=0)
        self.set_position(x=0, y=0)
        self.set_position(z=0)

    # Shuts the cnc down.
    def shutdown(self):
        self.return_to_origin()
        gpio.cleanup()
