import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 5026

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))


def send(string):
    s.send(string.encode('ascii'))
    data = s.recv(5)
    print("Returned:", data)


while True:
    send(input("::"))


s.close()