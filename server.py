import socket

UDP_IP = '127.0.0.1'
UDP_PORT = 50505
rcv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
rcv_sock.bind((UDP_IP, UDP_PORT))

print("Serving...")
data, addr = rcv_sock.recvfrom(2048)
data = data.decode()
site_address = data.split(":")[1].strip(' ').strip('\r\n');

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((site_address, 80))
print(data)
print(site_address)

custom_package = "GET / HTTP/1.1\r\n\r\n"

while True:
    s.sendall(custom_package.encode())
    f = s.makefile('rb')
    data = f.read(1024)           # or any other file method call you need

    



