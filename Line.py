import numpy as np
import math


# Calculates sequence of steps to take to draw a line with a given x,y coordinates.
# Sequence returned is array of tuples where each value specifies if the associated motor
# should be stepped forward, backward, or stay still.
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
