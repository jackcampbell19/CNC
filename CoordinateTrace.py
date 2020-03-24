import json

# Coordinate Trace file.

class CoordinateTrace:

    def __init__(self, name='coordinate-trace', coordinates=(), safe_height=100):
        self.name = name
        self.coordinates = coordinates
        self.safe_height = safe_height

    def export(self, path):
        f = open(path + self.name + '.ct', 'w')
        f.write(json.dumps({'name': self.name, 'coordinates': self.coordinates, 'safe-height': self.safe_height}))
        f.close()

    @staticmethod
    def load(filename):
        with open(filename, 'r') as file:
            data = json.loads(file.read())
            return CoordinateTrace(name=data['name'], coordinates=data['coordinates'], safe_height=data['safe-height'])
