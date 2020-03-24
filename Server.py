import socket
import hashlib
import json
import Commands
from CNC import CNC
import signal
import time

# Create socket.
TCP_IP = '10.0.0.47'#'raspberrypi.local'
TCP_PORT = 5000


def handler(l, f):
    print("Program interrupted. Cleaning up.")
    cnc.shutdown()
    s.shutdown(1)
    exit(0)


def error(e):
    print(e)


if __name__ == '__main__':

    signal.signal(signal.SIGINT, handler)

    # Define cnc
    cnc = CNC(200, error_handler=error)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)

    # Constantly listen for new connections.
    while True:
        # Accept connection.
        conn, _ = s.accept()
        print("Connected.")

        while True:
            try:
                data = conn.recv(1048576).decode('ascii')
                if data is None:
                    break
                print('recieved: ', data)
                hsh = hashlib.sha256(data.encode()).hexdigest()[:8]
                conn.sendall(hsh.encode('ascii'))
                try:
                    j = json.loads(data)
                except json.decoder.JSONDecodeError:
                    continue
                if j['command'] == Commands.SHUTDOWN:
                    conn.close()
                    break
                elif j['command'] == Commands.SET_POSITION:
                    [x, y, z] = j['data']
                    cnc.set_position(x, y, z)
                elif j['command'] == Commands.SET_ORIGIN:
                    pass
                elif j['command'] == Commands.LOAD_MSTP:
                    mstp = j['data']
                    cnc.ct = mstp
                    print("setting mstp data to ", cnc.ct)
                elif j['command'] == Commands.RUN_MSTP:
                    cnc.run()
            except socket.error:
                break

        # Close the connection.
        conn.close()
