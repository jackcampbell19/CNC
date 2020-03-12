from PIL import Image
import numpy as np


def extract_pixel_matrix(filename):
    im = Image.open(filename, 'r')
    m = np.array(im.getdata())
    m = m.reshape((1000, 1000, 3))
    return m


def proccess(pix_matrix):
    width = pix_matrix.shape[0]
    height = pix_matrix.shape[1]
    x = 0
    dir = 1
    for y in range(height):
        for _ in range(width - 1):
            print(x)
            x += dir
        dir *= -1


pix_matrix = extract_pixel_matrix('jpg/basic.jpg')
proccess(pix_matrix)