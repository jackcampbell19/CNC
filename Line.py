import numpy as np
import math


def calculate_line_steps(p0, p1):
    seq = []
    p0 = np.array(p0)
    p1 = np.array(p1)
    vector = np.subtract(p1, p0)
    length = int(round(np.linalg.norm(vector)))
    f = 1.0 / length
    last_position = (0, 0, 0)
    for x in range(length + 1):
        sample_percent = f * x
        vector_position = np.multiply(sample_percent, vector)
        delta_position = list(map(lambda t: int(math.floor(t)), vector_position))
        if not np.array_equal(last_position, delta_position):
            dp = np.subtract(delta_position, last_position)
            while abs(dp[0]) > 1 or abs(dp[1]) > 1 or abs(dp[2]) > 1:
                intermediate = np.array([0, 0, 0])
                for i in range(3):
                    if abs(dp[i]) > 1:
                        intermediate[i] = 1 * (dp[i] / abs(dp[i]))
                dp = np.subtract(dp, intermediate)
                seq.append(list(intermediate))
            seq.append(list(dp))
        last_position = delta_position
    return seq


# Calculates sequence of steps to take to draw a line with a given x, y, z coordinates from s to e.
def calculate_motor_sequence(s, e):
    sequence = []
    s = np.array(s)
    e = np.array(e)
    d = e - s
    m = round(np.linalg.norm(d))
    f = 1.0 / m
    last_position = (0, 0, 0)
    scalar = 0
    for _ in range(int(m) + 1):
        vector_position = (scalar * d).round()
        dv = vector_position - last_position
        if np.linalg.norm(dv) != 0:
            sequence.append([int(dv[0]), int(dv[1]), int(dv[2])])
        last_position = vector_position
        scalar += f
    return sequence


def calculate_even_steps(s, e):
    s = np.array(s)
    e = np.array(e)
    d = e - s
    a = np.absolute(d)
    dv = list(map(lambda x: (x[1] / a[x[0]]) if a[x[0]] != 0 else 0, enumerate(d)))
    sz = max(a)
    sequence = [[0, 0, 0] for _ in range(sz)]
    f = np.floor(np.array(list(map(lambda x: (sz / x) if x != 0 else 0, a))))
    m = [0, 0, 0]
    for i in range(1, sz + 1):
        for j in range(3):
            if dv[j] != 0 and i % f[j] == 0 and m[j] < a[j]:
                sequence[i - 1][j] = int(dv[j])
                m[j] += 1
    return sequence
