# in the name of God
import socket
from config import *
from rdt import *


class Client:
    msg = ""

    def __init__(self):
        pass

    def set_header(self, header, value):
        self.msg += header + ': ' + value + '\n'

    def send_http_message(self, dest_address):
        client_proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        rdt_send(client_proxy_socket, dest_address.encode(), PROXY_UDP_IP, PROXY_UDP_PORT)
        
        # client_proxy_socket.sendto(
        #     dest_address.encode(), (PROXY_UDP_IP, PROXY_UDP_PORT))
        self.wait_for_http_response()

    def wait_for_http_response(self):
        proxy_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        proxy_client_socket.bind((CLIENT_UDP_IP, CLIENT_UDP_PORT))
        http_response, addr = proxy_client_socket.recvfrom(MAX_BUFFER_SIZE)
        print(http_response)

    def make_dns_query(self, type, dns_server, dest_address):
        dest_host = dest_address.split('/')[0]
        self.msg += dns_server + '\n' + type + '\n' + dest_host + '\n'

    def send_dns_query(self, type, dns_server, dest_address):
        self.make_dns_query(type, dns_server, dest_address)
        self.msg = str.replace(self.msg, '\n', '\r\n')
        client_proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_proxy_socket.connect((PROXY_TCP_IP, PROXY_TCP_PORT))
        print('self dns query' , self.msg)
        client_proxy_socket.send(self.msg.encode())
        self.wait_for_dns_response()

    def wait_for_dns_response(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((CLIENT_TCP_IP, CLIENT_TCP_PORT))
        server_socket.listen(20000)
        proxy_client_socket, addr = server_socket.accept()
        dns_response = proxy_client_socket.recv(MAX_BUFFER_SIZE)
        print(dns_response.decode())