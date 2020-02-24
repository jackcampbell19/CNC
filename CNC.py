from SVG import *

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
    # Returns list of sequences: [(x, y), [(1/0, 1/0), ...]]
    def load_svg(self, filename):
        paths = self.svg_parser.parse(filename)
        print(paths)
        print()
        sequences = []
        for path in paths:
            sequence = []
            for [x0, y0, x1, y1] in path:
                if len(sequence) == 0:
                    sequence = [(x0, y0), []]
                sequence[1] += self.calculate_line_steps(x0, y0, x1, y1)
            sequences.append(sequence)
        return sequences


cnc = CNC(200)
s = cnc.load_svg('test-files/alex.svg')

print(s)

import Visualization
Visualization.visualize_sequences(s)
