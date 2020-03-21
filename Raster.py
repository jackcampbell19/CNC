from PIL import Image
import numpy as np
from SVG import calculate_line_steps
import MSTP
import math


def extract_pixel_matrix(filename):
    im = Image.open(filename, 'r')
    m = np.array(im.getdata())
    m = m.reshape((800, 800, 3))
    return m


def proccess(pix_matrix):
    width = pix_matrix.shape[0]
    height = pix_matrix.shape[1]
    x = 0
    dir = 1
    lines = []
    dx = 3
    for y in range(0, height, 3):
        sx = None
        ex = None
        for _ in range(math.floor(width / dx) - 1):

            s = pix_matrix[y, x][0] + pix_matrix[y, x][1] + pix_matrix[y, x][2]
            prob = (765 - s) / 765
            # if pix_matrix[x, y][0] == 255 and pix_matrix[x, y][1] == 255 and pix_matrix[x, y][2] == 255:
            #     if sx is not None:
            #         ex = x
            #         lines.append((sx, y, ex, y))
            #         sx = None
            #         ex = None
            # else:
            #     if sx is None:
            #         sx = x
            if np.random.uniform() > prob:
                if sx is not None:
                    ex = x
                    lines.append((sx, y, ex, y))
                    sx = None
                    ex = None
            else:
                if sx is None:
                    sx = x
            x += dir * dx
        if sx is not None and ex is not None:
            lines.append((sx, y, ex, y))
        dir *= -1
    out = []
    for line in lines:
        out.append(((line[0], line[1], 0), calculate_line_steps(line[0], line[1], line[2], line[3])))
    return out


pix_matrix = extract_pixel_matrix('jpg/jack.jpg')
sequences = proccess(pix_matrix)
mstp = MSTP.create(sequences, safe_height=25, mode='draw-2d')
MSTP.export('mstp/jack.mstp', mstp)
# import Visualization
# Visualization.visualize_mstp(sequences)