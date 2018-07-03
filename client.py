# in the name of God
import socket
from config import *


class Client:
    http_msg = ""
    dns_query = ""


    def __init__(self):
        pass

    def set_http_header(self, header, value):
        self.http_msg += header + ': ' + value + '\n'


    def make_http_message(self, dest_address):
        dest_host = dest_address.split('/')[0]
        dest_path = "/" + dest_address.split('/')[1]
        self.http_msg += "GET " + dest_path + " HTTP/1.1\n"
        self.set_http_header("Host", dest_host)


    def send_http_message(self , dest_address):
        self.make_http_message(dest_address)
        self.http_msg = str.replace(self.http_msg, '\n', '\r\n\r\n')
        client_proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_proxy_socket.sendto(self.http_msg.encode(), (PROXY_UDP_IP, PROXY_UDP_PORT))
        self.wait_for_response()


    def wait_for_response(self):
        proxy_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        proxy_client_socket.bind((CLIENT_UDP_IP, CLIENT_UDP_PORT))
        http_response, addr = proxy_client_socket.recvfrom(MAX_BUFFER_SIZE)
        print(http_response)


    def set_dns_header(self, header, value):
        self.dns_query += header + ': ' + value + '\n'
    

    def make_dns_query(self , type,dest_address):
        dest_host = dest_address.split('/')[0]
        self.set_dns_header("Name", dest_host)
        self.set_dns_header("Type", type)
        self.set_dns_header("Class", 'IN')

    def send_dns_query(self, type,dest_address):
        self.make_dns_query(type , dest_address)
        self.dns_query = str.replace(self.dns_query, '\n', '\r\n\r\n')
        client_proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_proxy_socket.connect(PROXY_TCP_IP, PROXY_TCP_PORT)
        client_proxy_socket.sendall(self.dns_query.encode())

        