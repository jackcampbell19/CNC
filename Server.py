import socket
import hashlib
import json
import Commands

# Create socket.
TCP_IP = '127.0.0.1'
TCP_PORT = 5000
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
            data = conn.recv(2000000).decode('ascii')
            if data is None:
                break
            print(data)
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
        except socket.error:
            break

    # Close the connection.
    conn.close()
