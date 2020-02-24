from svg.path import parse_path
from xml.dom import minidom
import numpy as np
import re
import math


# SVG class parses an .svg file into discrete line segments measured in motor steps.
class SVG:

    def __init__(self, StepsPerRotation):
        self.STEPS_PER_POINT = 1 / ((8 / StepsPerRotation) * (72 / 25.4))

    # Converts points to steps
    def points_to_steps(self, points):
        return int(self.STEPS_PER_POINT * float(points))

    def apply_transform(self, x, y, tx, ty, r):
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
            rotate = re.search(r'(?<=rotate\()[0-9\-. ]+', transform_string)
            if rotate:
                rotate = float(rotate.group(0))
            return [translate, rotate]
        return [None, None]

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

            [translate, rotate] = self.extract_transform(elem)

            if elem.getAttribute('transform'):
                x0, y0 = self.apply_transform(x0, y0, translate[0], translate[1], rotate)
                x1, y1 = self.apply_transform(x1, y1, translate[0], translate[1], rotate)
                x2, y2 = self.apply_transform(x2, y2, translate[0], translate[1], rotate)
                x3, y3 = self.apply_transform(x3, y3, translate[0], translate[1], rotate)

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
        for elem in doc.getElementsByTagName('circle'):
            circle = [self.points_to_steps(elem.getAttribute('cx')),
                         self.points_to_steps(elem.getAttribute('cy')),
                         self.points_to_steps(elem.getAttribute('r'))]
            l.append(circle)
        return l

    # Parse paths from a doc, returns list of tuples containing [x, y]
    # for each point on the path adjusted from points to steps.
    def parse_path(self, doc):
        l = []
        for elem in doc.getElementsByTagName('path'):
            pd = elem.getAttribute('d')
            path = parse_path(pd)
            element_path = []
            for e in path:
                if e.length() == 0:
                    continue
                samples = self.points_to_steps(e.length())
                sampled_path = [(self.points_to_steps(e.point(1 / samples * i).real),
                                 self.points_to_steps(e.point(1 / samples * i).imag),
                                 self.points_to_steps(e.point(1 / samples * (i + 1)).real),
                                 self.points_to_steps(e.point(1 / samples * (i + 1)).imag))
                                for i in range(samples)]
                element_path += sampled_path
            l.append(element_path)
        return l

    def parse_polyline(self, doc):
        l = []
        for elem in doc.getElementsByTagName('polyline'):
            pnts = elem.getAttribute('points').split(' ')
            points = []
            for xy in range(0, len(pnts) - 2, 2):
                points.append(
                    (
                        self.points_to_steps(float(pnts[xy % len(pnts)])),
                        self.points_to_steps(float(pnts[(xy + 1) % len(pnts)])),
                        self.points_to_steps(float(pnts[(xy + 2) % len(pnts)])),
                        self.points_to_steps(float(pnts[(xy + 3) % len(pnts)]))
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

    # Parse a file for all objects. Returns a list of line definitions.
    def parse(self, filename):
        doc = minidom.parse(filename)
        paths = []
        paths += self.parse_line(doc)
        paths += self.parse_polyline(doc)
        paths += self.parse_path(doc)
        paths += self.parse_rect(doc)
        doc.unlink()
        return paths
