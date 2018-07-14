# in the name of God
import socket
from config import *


class Client:
    msg = ""

    def __init__(self):
        pass

    def set_header(self, header, value):
        self.msg += header + ': ' + value + '\n'

    def make_http_message(self, dest_address):
        dest_host = dest_address.split('/')[0]
        dest_path = "/" + dest_address.split('/')[1]
        self.msg += "GET " + dest_path + " HTTP/1.1\n\n"
        self.set_header("Host", dest_host)

    def send_http_message(self, dest_address):
        self.make_http_message(dest_address)
        self.msg = str.replace(self.msg, '\n', '\r\n\r\n')
        client_proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_proxy_socket.sendto(
            self.msg.encode(), (PROXY_UDP_IP, PROXY_UDP_PORT))
        self.wait_for_response()

    def wait_for_http_response(self):
        proxy_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        proxy_client_socket.bind((CLIENT_UDP_IP, CLIENT_UDP_PORT))
        http_response, addr = proxy_client_socket.recvfrom(MAX_BUFFER_SIZE)
        print(http_response)

    def make_dns_query(self, type, dns_server, dest_address):
        dest_host = dest_address.split('/')[0]
        self.set_header(dns_server, dns_server)
        self.set_header("Name", dest_host)
        self.set_header("Type", type)
        self.set_header("Class", 'IN')

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