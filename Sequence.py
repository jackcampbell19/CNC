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
