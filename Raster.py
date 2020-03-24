from PIL import Image
import numpy as np
from CoordinateTrace import CoordinateTrace
import math


def extract_pixel_matrix(filename):
    im = Image.open(filename, 'r')
    m = np.array(im.getdata())
    # weight, width
    m = m.reshape((700, 700, 3))
    return m


def proccess(pix_matrix):
    width = pix_matrix.shape[1]
    height = pix_matrix.shape[0]
    x = 0
    dir = 1
    points = []
    dx = 5
    dy = 5
    is_down = False
    safe_height = 30
    for y in range(0, height, dy):
        for p in range(math.floor(width / dx) - 1):
            s = pix_matrix[y, x][0] + pix_matrix[y, x][1] + pix_matrix[y, x][2]
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


pix_matrix = extract_pixel_matrix('jpg/sq.jpg')
points = proccess(pix_matrix)
ct = CoordinateTrace('sq', points, safe_height=30)
ct.export('ct/')
import Visualization
Visualization.visualize_coordinates(points)