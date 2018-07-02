# in the name of God
import socket

MAX_BUFFER_SIZE = 1024
PROXY_UDP_IP = "127.0.0.1"
PROXY_UDP_PORT = 50505
CLIENT_UDP_IP = '127.0.0.1'
CLIENT_UDP_PORT = 60606


class Client:
    msg = ""

    def __init__(self, protocol, dest_address):
        self.protocol = protocol
        self.dest_address = dest_address

    def set_http_header(self, header, value):
        self.msg += header + ': ' + value + '\n';

    def make_http_message(self):
        dest_host = self.dest_address.split('/')[0]
        dest_path = "/" + self.dest_address.split('/')[1]
        self.msg += "GET " + dest_path + " HTTP/1.1\n"
        self.set_http_header("Host", dest_host)

    def send_http_message(self):
        self.make_http_message()
        self.msg = str.replace(self.msg, '\n', '\r\n\r\n')
        client_proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_proxy_socket.sendto(self.msg.encode(), (PROXY_UDP_IP, PROXY_UDP_PORT))
        self.wait_for_response()

    def wait_for_response(self):
        proxy_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        proxy_client_socket.bind((CLIENT_UDP_IP, CLIENT_UDP_PORT))
        http_response, addr = proxy_client_socket.recvfrom(MAX_BUFFER_SIZE)
        print(http_response)
