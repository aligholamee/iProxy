# in the name of God
import socket

class Client:
    msg = ""
    UDP_IP = "127.0.0.1"
    UDP_PORT = 50505
    ack = false

    def __init__(self, protocol, dest_address):
        self.protocol = protocol
        self.dest_address = dest_address

    def set_http_header(self, header, value):
        self.msg += header + ': ' + value + '\n';

    def make_http_message(self):
        dest_host = self.dest_address.split('/')[0]
        dest_path = "/" + self.dest_address.split('/')[1]
        print(dest_host, dest_path)
        self.msg += "GET " + dest_path + " HTTP/1.1\n"
        self.set_http_header("Host", dest_host)

    def send_http_message(self):
        self.make_http_message()
        self.msg = str.replace(self.msg, '\n', '\r\n\r\n')
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def getAck()
        return ack;