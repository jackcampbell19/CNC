from svg.path import parse_path
from xml.dom import minidom
import numpy as np
import re
import math
import json


# SVG class parses an .svg file into discrete line segments measured in motor steps.
class SVG:

    def __init__(self, StepsPerRotation):
        self.STEPS_PER_POINT = 1 / ((8 / StepsPerRotation) * (72 / 25.4))

    # Converts points to steps
    def points_to_steps(self, points):
        return int(self.STEPS_PER_POINT * float(points))

    def apply_transform(self, x, y, transform):
        if not transform:
            return x, y
        [[tx, ty], r] = transform
        xy = np.array([x, y, 1])
        if r:
            m2 = np.array([[math.cos(r * math.pi / 180), -math.sin(r * math.pi / 180), 0],
                           [math.sin(r * math.pi / 180), math.cos(r * math.pi / 180), 0],
                           [0, 0, 1]])
            xy = m2.dot(xy)
        if tx and ty:
            m1 = np.array([[1, 0, tx],
                           [0, 1, ty],
                           [0, 0, 1]])
            xy = m1.dot(xy)
        return xy[0], xy[1]

    def extract_transform(self, elem):
        transform_string = elem.getAttribute('transform')
        if transform_string:
            translate = re.search(r'(?<=translate\()[0-9\-. ]+', transform_string)
            if translate:
                translate = [float(x) for x in translate.group(0).split(' ')]
            else:
                translate = [0, 0]
            rotate = re.search(r'(?<=rotate\()[0-9\-. ]+', transform_string)
            if rotate:
                rotate = float(rotate.group(0))
            else:
                rotate = 0
            return [translate, rotate]
        return None

    # Parse rects from a doc, returns list of tuples containing [x, y, width, height]
    # for each rect adjusted from points to steps.
    def parse_rect(self, doc):
        l = []
        for elem in doc.getElementsByTagName('rect'):
            x = float(elem.getAttribute('x'))
            y = float(elem.getAttribute('y'))
            width = float(elem.getAttribute('width'))
            height = float(elem.getAttribute('height'))

            x0, y0 = x, y
            x1, y1 = x + width, y
            x2, y2 = x + width, y + height
            x3, y3 = x, y + height

            transform = self.extract_transform(elem)

            if transform:
                x0, y0 = self.apply_transform(x0, y0, transform)
                x1, y1 = self.apply_transform(x1, y1, transform)
                x2, y2 = self.apply_transform(x2, y2, transform)
                x3, y3 = self.apply_transform(x3, y3, transform)

            x0, y0 = self.points_to_steps(x0), self.points_to_steps(y0)
            x1, y1 = self.points_to_steps(x1), self.points_to_steps(y1)
            x2, y2 = self.points_to_steps(x2), self.points_to_steps(y2)
            x3, y3 = self.points_to_steps(x3), self.points_to_steps(y3)

            l.append([(x0, y0, x1, y1), (x1, y1, x2, y2), (x2, y2, x3, y3), (x3, y3, x0, y0)])
        return l

    # Parse circles from a doc, returns list of tuples containing [x, y, radius]
    # for each circle adjusted from points to steps.
    def parse_circle(self, doc):
        l = []
        # for elem in doc.getElementsByTagName('circle'):
        #     circle = [self.points_to_steps(elem.getAttribute('cx')),
        #                  self.points_to_steps(elem.getAttribute('cy')),
        #                  self.points_to_steps(elem.getAttribute('r'))]
        #     l.append(circle)
        return l

    # Parse paths from a doc, returns list of tuples containing [x, y]
    # for each point on the path adjusted from points to steps.
    def parse_path(self, doc):
        l = []
        for elem in doc.getElementsByTagName('path'):
            pd = elem.getAttribute('d')
            transform = self.extract_transform(elem)
            path = parse_path(pd)
            element_path = []
            for e in path:
                if e.length() == 0:
                    continue
                samples = self.points_to_steps(e.length())
                sampled_path = []
                for i in range(samples):
                    x0, y0 = e.point(1 / samples * i).real, e.point(1 / samples * i).imag
                    x1, y1 = e.point(1 / samples * (i + 1)).real, e.point(1 / samples * (i + 1)).imag
                    x0, y0 = self.apply_transform(x0, y0, transform)
                    x1, y1 = self.apply_transform(x1, y1, transform)
                    x0, y0 = self.points_to_steps(x0), self.points_to_steps(y0)
                    x1, y1 = self.points_to_steps(x1), self.points_to_steps(y1)
                    sampled_path.append((x0, y0, x1, y1))
                element_path += sampled_path
            if len(element_path) > 0:
                l.append(element_path)
        return l

    def parse_polyline(self, doc):
        l = []
        for elem in doc.getElementsByTagName('polyline') + doc.getElementsByTagName('polygon'):
            pnts = elem.getAttribute('points').split(' ')
            transform = self.extract_transform(elem)
            pnts = [float(x) for x in pnts]
            points = []
            for xy in range(0, len(pnts) - 2, 2):
                x0, y0 = pnts[xy % len(pnts)], pnts[(xy + 1) % len(pnts)]
                x1, y1 = pnts[(xy + 2) % len(pnts)], pnts[(xy + 3) % len(pnts)]
                x0, y0 = self.apply_transform(x0, y0, transform)
                x1, y1 = self.apply_transform(x1, y1, transform)
                points.append(
                    (
                        self.points_to_steps(x0),
                        self.points_to_steps(y0),
                        self.points_to_steps(x1),
                        self.points_to_steps(y1)
                    )
                )
            l.append(points)
        return l

    def parse_line(self, doc):
        l = []
        for elem in doc.getElementsByTagName('line'):
            points = [(self.points_to_steps(elem.getAttribute('x1')), self.points_to_steps(elem.getAttribute('y1')),
                       self.points_to_steps(elem.getAttribute('x2')), self.points_to_steps(elem.getAttribute('y2')))]
            l.append(points)
        return l

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
            subsequence = [dx, 0, 0]
            while current_y != expected_y:
                if current_y < expected_y:
                    current_y += 1
                    subsequence[1] = 1
                elif current_y > expected_y:
                    current_y -= 1
                    subsequence[1] = -1
                sequence.append(subsequence)
                subsequence = [0, 0, 0]
            if dx == 0:
                dx = direction
            if subsequence[0] != 0:
                sequence.append(subsequence)
        return sequence

    # Parse a file for all objects. Returns an mstp.
    def parse(self, filename):
        doc = minidom.parse(filename)
        paths = []
        paths += self.parse_line(doc)
        paths += self.parse_polyline(doc)
        paths += self.parse_path(doc)
        paths += self.parse_rect(doc)
        doc.unlink()
        sequences = []
        for path in paths:
            sequence = []
            for [x0, y0, x1, y1] in path:
                if len(sequence) == 0:
                    sequence = [(x0, y0, 0), []]
                sequence[1] += self.calculate_line_steps(x0, y0, x1, y1)
            sequences.append(sequence)
        sequences.sort(key=lambda x: math.sqrt(x[0][0] ** 2 + x[0][1] ** 2))
        return {'meta': {'mode': 'draw-2d', 'safe-height': 10, 'step-down': None}, 'data': sequences}

    def export(self, sequences, filename):
        s = json.dumps(sequences)
        f = open('mstp/' + filename, 'w')
        f.write(s)
        f.close()


def calculate_circle_steps(radius, angle_delta=math.pi/180):
    x = radius
    y = 0
    sequence = []
    angle = 0
    while angle < 2.0 * math.pi:
        xx = int(radius * math.cos(angle))
        yy = int(radius * math.sin(angle))
        while xx != x or yy != y:
            subsequence = [0,0]
            if xx > x:
                subsequence[0] = 1
                x += 1
            elif xx < x:
                subsequence[0] = -1
                x -= 1
            if yy > y:
                subsequence[1] = 1
                y += 1
            elif yy < y:
                subsequence[1] = -1
                y -= 1
            sequence.append(subsequence)
        angle += angle_delta
    return sequence