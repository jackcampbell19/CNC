from Motor import *
import RPi.GPIO as gpio
import Line
from CoordinateTrace import CoordinateTrace


class CNC:

    def __init__(self, spr, error_handler):
        # Motor steps per rotation
        self.SPR = spr
        # Error handler
        self.error_handler = error_handler
        # Dimensions (x, y, z)
        self.dimensions = (0, 0, 0)
        # Loaded mstp data
        self.ct = None
        # Motors
        self.x_motor = Stepper(11, 12)
        self.y_motor = Stepper(13, 15)
        self.z_motor = Stepper(16, 18)

    def set_mstp(self, ct):
        self.ct = ct

    def load_mstp(self, filename):
        self.ct = CoordinateTrace.load(filename)

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
        if self.ct is None:
            self.error_handler('Missing .ct file.')
        self.return_to_origin()
        current_position = (0, 0, 0)
        sequences = []
        l = len(self.ct.coordinates)
        for x in range(l):
            next_position = self.ct.coordinates[x]
            sequence = Line.calculate_motor_sequence(current_position, next_position)
            sequences += sequence
            current_position = next_position
            print(str(x) + '/' + str(l), end='\r')
        for dx, dy, dz in sequences:
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
            sleep(Stepper.SHORTEST_DELAY)

    def return_to_origin(self):
        if self.x_motor.current_step == 0 \
                and self.y_motor.current_step == 0 \
                and self.z_motor.current_step == 0:
            return
        if self.ct is not None:
            self.set_position(z=self.ct.safe_height)
        self.set_position(x=0, y=0)
        self.set_position(z=0)

    # Shuts the cnc down.
    def shutdown(self):
        self.return_to_origin()
        gpio.cleanup()
