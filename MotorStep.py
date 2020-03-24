import json
from CoordinateTrace import CoordinateTrace
import Line

# Motor Step file.

class MotorStep:

    def __init__(self, ct=None, motor_sequence=(), name=None, safe_height=None, origin=None):
        self.name = ct.name if ct is not None else name
        self.safe_height = ct.safe_height if ct is not None else safe_height
        self.motor_sequence = motor_sequence
        self.coordinates = ct.coordinates if ct is not None else []
        self.origin = ct.coordinates[0] if ct is not None else origin

    @staticmethod
    def character(v):
        out = 0b0
        for x in range(3):
            if v[x] == 1:
                out |= 0b1 << x
            elif v[x] == -1:
                out |= 0b1000 << x
        return chr(out)

    @staticmethod
    def array(c):
        c = ord(c)
        out = [0, 0, 0]
        for x in range(3):
            if c & (0b1 << x) != 0:
                out[x] = 1
            elif c & (0b1000 << x) != 0:
                out[x] = -1
        return out

    def generate_step_sequence(self):
        current_position = self.origin
        le = len(self.coordinates)
        out = ''
        for x in range(1, le):
            next_position = self.coordinates[x]
            sequence = Line.calculate_motor_sequence(current_position, next_position)
            out += ''.join([MotorStep.character(v) for v in sequence])
            current_position = next_position
        return out

    def extract_motor_sequence(self):
        sequences = []
        for x in self.motor_sequence:
            sequences.append(MotorStep.array(x))
        return sequences

    def export(self, path):
        f = open(path + self.name + '.mstp', 'w')
        f.write(json.dumps({'name': self.name, 'safe-height': self.safe_height,
                            'origin': self.origin, 'sequence': self.generate_step_sequence()}))
        f.close()

    @staticmethod
    def load(filename):
        with open(filename, 'r') as file:
            data = json.loads(file.read())
            return MotorStep(name=data['name'], origin=data['origin'], motor_sequence=data['sequence'], safe_height=data['safe-height'])
