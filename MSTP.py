import json


# Creates mstp data from sequences for motors and metadata.
def create(sequences, mode=None, safe_height=100, step_down=None):
    out = ""
    for [(x, y, z), sequence] in sequences:
        seq = ""
        for [dx, dy, dz] in sequence:
            l = lambda g: '2' if g == -1 else str(g)
            seq += l(dx) + l(dy) + l(dz)
        out += str(x) + ',' + str(y) + ',' + str(z) + ':' + seq + ';'
    return json.dumps({'mode': mode, 'safe-height': safe_height, 'step-down': step_down}) + '=' + out


# Exports the mstp to a file.
def export(filename, mstp):
    s = mstp
    f = open(filename, 'w')
    f.write(s)
    f.close()


# Parses a string of data into an mstp.
def parse(input_data):
    [meta, data] = input_data.split('=')
    meta = json.loads(meta)
    sequences = []
    for object_sequence_string in data.split(';'):
        initial_coordinate_motor_step_sequence = object_sequence_string.split(':')
        if len(initial_coordinate_motor_step_sequence) != 2:
            continue
        initial_coordinates = list(map(lambda x: int(x), initial_coordinate_motor_step_sequence[0].split(',')))
        step_sequence = []
        for x in range(0, len(initial_coordinate_motor_step_sequence[1]), 3):
            dx = initial_coordinate_motor_step_sequence[1][x]
            dy = initial_coordinate_motor_step_sequence[1][x + 1]
            dz = initial_coordinate_motor_step_sequence[1][x + 2]
            step_sequence.append([int(dx), int(dy), int(dz)])
        sequences.append([initial_coordinates, step_sequence])
    output = {'meta': meta, 'data': sequences}
    return output




# Loads a file and returns the mstp data.
def load(filename):
    with open(filename, 'r') as file:
        data = file.read()
        return parse(data)
