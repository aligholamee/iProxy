import socket

UDP_IP = '127.0.0.1'
UDP_PORT = 50505
rcv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
rcv_sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = rcv_sock.recvfrom(2048)
    data = data.decode()
    site_address = data.split(":")[1].strip(' ').strip('\n');

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((site_address, 80))
    print(data)
    print(site_address)
    s.send(data.encode())
    data = s.recv(1)

    print("rcv google is ", data)

