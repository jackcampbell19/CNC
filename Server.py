import socket
import hashlib

# Create socket.
TCP_IP = '127.0.0.1'
TCP_PORT = 5026
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

# Constantly listen for new connections.
while True:
    # Accept connection.
    conn, _ = s.accept()
    print("Connected.")
    # Collect data.
    data = ""
    while True:
        try:
            buff_data = conn.recv(5)
            if not buff_data:
                break
            data += buff_data.decode('ascii')
            conn.sendall("Server Says:hi".encode('ascii'))
        except socket.error:
            break
    # Return hash of data.
    hsh = hashlib.sha256(data.encode()).hexdigest()
    print(hsh)
    # conn.send(hsh.encode('ascii'))
    conn.sendall(hsh.encode('ascii'))
    # Close the connection.
    conn.close()
