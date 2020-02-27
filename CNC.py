from SVG import *
from Visualization import visualize_sequences
from Motor import *


class CNC:

    def __init__(self, spr):
        # Motor steps per rotation
        self.SPR = spr
        # X size in number of steps
        self.XSIZE = 0
        # Y size in number of steps
        self.YSIZE = 0
        # Z size in number of steps
        self.ZSIZE = 0
        # Parser
        self.svg_parser = SVG(StepsPerRotation=self.SPR)
        # Sequences
        self.sequences = None
        # Motors
        self.x_motor = Stepper(11, 12, 13, 15, 16)
        self.y_motor = Stepper(21, 19, 22, 23, 18)
        self.z_motor = Stepper(29, 31, 36, 37, 32)

    # Calculates sequence of steps to take to draw a line with a given x,y coordinates.
    # Sequence returned is array of tuples where each value specifies if the associated motor
    # should be stepped forward, backward, or stay still.
    def calculate_line_steps(self, x0, y0, x1, y1):
        if x0 == x1:
            f = lambda x: y1
        else:
            m = (y1 - y0) / (x1 - x0)
            b = -(m * x0) + y0
            f = lambda x: m * x + b
        sequence = []
        direction = 1 if x1 > x0 else -1
        current_y = y0
        dx = 0
        for current_x in range(x0, x1 + direction, direction):
            expected_y = int(f(current_x))
            subsequence = [dx, 0]
            while current_y != expected_y:
                if current_y < expected_y:
                    current_y += 1
                    subsequence[1] = 1
                elif current_y > expected_y:
                    current_y -= 1
                    subsequence[1] = -1
                sequence.append(subsequence)
                subsequence = [0, 0]
            if dx == 0:
                dx = direction
            if subsequence[0] != 0:
                sequence.append(subsequence)
        return sequence

    # Loads an svg file, calculates motor movements using line steps algorithm.
    # Saves the sequences to the 'sequences' variable.
    def load_svg(self, filename):
        paths = self.svg_parser.parse(filename)
        sequences = []
        for path in paths:
            sequence = []
            for [x0, y0, x1, y1] in path:
                if len(sequence) == 0:
                    sequence = [(x0, y0), []]
                sequence[1] += self.calculate_line_steps(x0, y0, x1, y1)
            sequences.append(sequence)
        self.sequences = sequences

    # Visualizes the sequence loaded.
    def visualize_sequences(self):
        visualize_sequences(self.sequences)

    # Position the pen up for drawing sequences.
    def pen_up(self):
        t = self.z_motor.rotate_to(20)
        t.start()
        t.join()

    # Position the pen up for drawing sequences.
    def pen_down(self):
        t = self.z_motor.rotate_to(0)
        t.start()
        t.join()

    # Sets the position to the given xy coordinate. DO NOT USE FOR ACCURATE STEPPING.
    def set_position(self, x, y):
        t1 = self.x_motor.rotate_to(x)
        t2 = self.y_motor.rotate_to(y)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

    # Draw a 2D sequence.
    def draw_sequences(self, sequences):
        for [(x, y), sequence] in sequences:
            self.pen_up()
            self.set_position(x, y)
            self.pen_down()
            for [dx, dy] in sequence:
                if dx == -1:
                    self.x_motor.step(False)
                elif dx == 1:
                    self.x_motor.step(True)
                if dy == -1:
                    self.y_motor.step(False)
                elif dy == 1:
                    self.y_motor.step(True)
                sleep(Stepper.SHORTEST_DELAY)



