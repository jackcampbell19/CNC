import json

# Instructs the server that an mstp is being sent.
LOAD_MSTP = 'load-mstp'

# Instructs the server to run the current mstp.
RUN_MSTP = 'run-mstp'

# Instructs the server to pause the current mstp.
PAUSE_MSTP = 'pause-mstp'

# Instruct the server to abort the current mstp.
ABORT_MSTP = 'abort-mstp'

# Sets the cnc to the given position.
SET_POSITION = 'set-position'

# Sets the cnc to be the origin.
SET_ORIGIN = 'set-origin'

# Shuts down the CNC.
SHUTDOWN = 'shutdown'

# Creates an encoded command.
def create_command(command, data=None):
    return json.dumps({'command': command, 'data': data}).encode('ascii')
