import socket

MAX_BUFFER_SIZE = 1024
PROXY_UDP_IP = '127.0.0.1'
PROXY_UDP_PORT = 50505
CLIENT_UDP_IP = '127.0.0.1'
CLIENT_UDP_PORT = 60606

client_proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_proxy_socket.bind((PROXY_UDP_IP, PROXY_UDP_PORT))

http_request, addr = client_proxy_socket.recvfrom(MAX_BUFFER_SIZE)
http_request = http_request.decode()

site_address = http_request.split(":")[1].strip(' ').strip('\r\n');

proxy_destination_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
proxy_destination_socket.connect((site_address, 80))
proxy_destination_socket.sendall(http_request.encode())
print(site_address)
http_response = proxy_destination_socket.recv(MAX_BUFFER_SIZE)
print(http_response)
proxy_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
proxy_client_socket.sendto(http_response, (CLIENT_UDP_IP, CLIENT_UDP_PORT))