from PIL import Image
import numpy as np
from CoordinateTrace import CoordinateTrace
import math
from MotorStep import MotorStep


class Rasterizer:

    def __init__(self):
        self.pixle_matrix = None
        self.coordinates = None
        self.ct = None

    def extract_pixel_matrix(self, filename):
        im = Image.open(filename, 'r')
        m = np.array(im.getdata())
        # height, width
        m = m.reshape((im.size[1], im.size[0], 3))
        self.pixle_matrix = m

    def proccess(self):
        if self.pixle_matrix is None:
            return None
        width = self.pixle_matrix.shape[1]
        height = self.pixle_matrix.shape[0]
        x = 0
        dir = 1
        points = []
        dx = 4
        dy = 4
        is_down = False
        safe_height = 30
        for y in range(0, height, dy):
            for p in range(math.floor(width / dx) - 1):
                s = self.pixle_matrix[y, x][0] + self.pixle_matrix[y, x][1] + self.pixle_matrix[y, x][2]
                prob = (1 / 765 ** 2) * (s - 765) ** 2
                if np.random.uniform() > prob:
                    if is_down:
                        points.append((x, y, 0))
                        points.append((x, y, safe_height))
                        is_down = False
                else:
                    if not is_down:
                        points.append((x, y, safe_height))
                        points.append((x, y, 0))
                        is_down = True
                x += dir * dx
            dir *= -1
        return points

    def load(self, filename):
        self.extract_pixel_matrix(filename)
        self.coordinates = self.proccess()

    def export_ct(self, name, path):
        ct = CoordinateTrace(name, self.coordinates, safe_height=30)
        ct.export(path)
        self.ct = ct

    def export_mstp(self, name, path):
        if self.ct is None:
            self.ct = CoordinateTrace(name, self.coordinates, safe_height=30)
        mstp = MotorStep(ct=self.ct)
        mstp.export(path)
