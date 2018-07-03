import socket
from config import *
import sys


class Proxy():
    def __init__(self, protocol):
        self.protocol = protocol

    @staticmethod
    def listen_for_http():
        client_proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_proxy_socket.bind((PROXY_UDP_IP, PROXY_UDP_PORT))

        http_request, addr = client_proxy_socket.recvfrom(MAX_BUFFER_SIZE)
        http_request = http_request.decode()

        site_address = http_request.split(":")[1].strip(' ').strip('\r\n')

        proxy_destination_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        proxy_destination_socket.connect((site_address, 80))
        proxy_destination_socket.sendall(http_request.encode())
        http_response = proxy_destination_socket.recv(MAX_BUFFER_SIZE)
        proxy_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        proxy_client_socket.sendto(
            http_response, (CLIENT_UDP_IP, CLIENT_UDP_PORT))

    @staticmethod
    def listen_for_dns():
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((PROXY_TCP_IP, PROXY_TCP_PORT))
        server_socket.listen(20000)
        client_proxy_socket, addr = server_socket.accept()
        raw_message = client_proxy_socket.recv(MAX_BUFFER_SIZE).decode()
        print('x' + raw_message)
        dns_query = '\r\n'.join(raw_message.split('\r\n')[1:])
        dns_server = raw_message.split(':')[0]
        print(dns_query, dns_server)

    def listen(self):
        if self.protocol == 'dns':
            self.listen_for_dns()
        if self.protocol == 'http':
            self.listen_for_http()


if __name__ == '__main__':
    proxy = Proxy(sys.argv[1])
    proxy.listen()
