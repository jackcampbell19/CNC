import json


# Creates mstp file data from list of points and metadata.
def create(points, name, path=None):
    out = ""
    mstp = json.dumps({'name': name, 'data': points})
    if path is not None:
        f = open(path + name + '.mstp', 'w')
        f.write(mstp)
        f.close()
    return mstp


# Loads a file and returns the mstp data.
def load(filename):
    with open(filename, 'r') as file:
        data = file.read()
        return json.loads(data)
