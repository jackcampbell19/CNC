import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))


def send(string):
    s.sendall(string.encode('ascii'))
    data = s.recv(2000000).decode('ascii')
    print("Received:", data)


while True:
    send(input("::"))


s.close()
