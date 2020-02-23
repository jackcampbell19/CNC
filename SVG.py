from svg.path import parse_path
from svg.path.path import Line
from xml.dom import minidom


class SVG:

    def __init__(self, StepsPerRotation):
        self.STEPS_PER_POINT = 1 / ((8 / StepsPerRotation) * (72 / 25.4))

    def points_to_steps(self, points):
        return int(self.STEPS_PER_POINT * float(points))

    def parse(self, filename):
        parse = {}
        doc = minidom.parse(filename)
        # Rect parse
        parse['rect'] = []
        for elem in doc.getElementsByTagName('rect'):
            rectangle = [self.points_to_steps(elem.getAttribute('x')),
                         self.points_to_steps(elem.getAttribute('y')),
                         self.points_to_steps(elem.getAttribute('width')),
                         self.points_to_steps(elem.getAttribute('height'))]
            parse['rect'].append(rectangle)
        # Circle parse
        parse['circle'] = []
        for elem in doc.getElementsByTagName('circle'):
            rectangle = [self.points_to_steps(elem.getAttribute('cx')),
                         self.points_to_steps(elem.getAttribute('cy')),
                         self.points_to_steps(elem.getAttribute('r'))]
            parse['circle'].append(rectangle)
        # Path parse
        parse['path'] = []
        for elem in doc.getElementsByTagName('path'):
            pd = elem.getAttribute('d')
            path = parse_path(pd)
            element_path = []
            for e in path:
                if e.length() == 0:
                    continue
                samples = self.points_to_steps(e.length())
                sampled_path = [[self.points_to_steps(e.point(1 / samples * x).real),
                                 self.points_to_steps(e.point(1 / samples * x).imag)]
                                for x in range(samples + 1)]
                element_path += sampled_path
            parse['path'].append(element_path)

        doc.unlink()
        return parse





# doc = minidom.parse('test-files/path.svg')
# path_strings = [path.getAttribute('d') for path in doc.getElementsByTagName('path')]
# doc.unlink()
#
# import Sequence
#
# seq = []
# for path_string in path_strings:
#     path = parse_path(path_string)
#     for e in path:
#         print(int(e.length() * 1 / ((8 / 256) * (72 / 25.4)) / 4))
#         samples = int(e.length() * 1 / ((8 / 256) * (72 / 25.4)) / 4)
#         x = [[int(e.point(1/samples*x).real * 1 / ((8 / 256) * (72 / 25.4))),
#               int(e.point(1/samples*x).imag * 1 / ((8 / 256) * (72 / 25.4)))] for x in range(samples + 1)]
#         seq.append(x)
#
# Sequence.plot_proper(seq)



svgp = SVG(StepsPerRotation=256)
seq = svgp.parse('test-files/shapes.svg')
print(len(seq['path']))
import Sequence
Sequence.plot_proper(seq['path'])


