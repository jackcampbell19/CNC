import math


# Calculates sequence of steps to take to draw a circle with a given radius. Sequence returned
# is array of tuples where each value specifies if the associated motor should be stepped
# forward, backward, or stay still.
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


# Calculates sequence of steps to take to draw a rectangle with a given width and height.
# Sequence returned is array of tuples where each value specifies if the associated motor
# should be stepped forward, backward, or stay still.
def calculate_rectangle_steps(width, height):
    sequence = []
    for _ in range(height):
        sequence.append([0, -1])
    for _ in range(width):
        sequence.append([1, 0])
    for _ in range(height):
        sequence.append([0, 1])
    for _ in range(width):
        sequence.append([-1, 0])
    return sequence


# Calculates sequence of steps to take to draw a line with a given x,y coordinates.
# Sequence returned is array of tuples where each value specifies if the associated motor
# should be stepped forward, backward, or stay still.
def calculate_line_steps(x0, y0, x1, y1):
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





import matplotlib.pyplot as plt
import numpy as np

def plot(*seqs):
    for seq in seqs:
        xx = 0
        yy = 0
        c = 0
        for (x, y) in seq:
            _ = plt.plot(xx, yy, '.')
            xx += x
            yy += y
        _ = plt.plot(xx, yy, '.')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

def plot_proper(seqs):
    for seq in seqs:
        for (x, y) in seq:
            _ = plt.plot(x, y, '.')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

def plot_lines(lines):
    for seq in lines:
        for (x0, y0, x1, y1) in seq:
            _ = plt.plot((x0, x1), (-y0, -y1), '-')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()


def cnc_visualize(sequences):
    cx = 0
    cy = 0
    for [(x0, y0), sequence] in sequences:
        cx = x0
        cy = -y0
        for [dx, dy] in sequence:
            cx += dx
            cy += -dy
            _ = plt.plot(cx, cy, '.')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()
