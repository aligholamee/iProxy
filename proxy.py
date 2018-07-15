import socket
from config import *
from util import Util
import requests
import dns.resolver
import dns.message
import dns.rdataclass
import dns.rdatatype
import dns.query
import sys
from rdt import *


class Proxy():

    def __init__(self, protocol):
        self.protocol = protocol

    def listen_for_http(self):

        site_address = rdt_receive(PROXY_UDP_IP, PROXY_UDP_PORT, CLIENT_UDP_IP, CLIENT_UDP_PORT)
        print(site_address)

        http_response = requests.get(site_address, timeout=30)
        print(http_response)
        print(http_response.text)
        rdt_send(http_response.text.encode(), PROXY_UDP_IP, PROXY_UDP_PORT, CLIENT_UDP_IP, CLIENT_UDP_PORT)

    def send_dns_query(self, dns_server, domain_name, query_type):
        dns_response = ""
        myResolver = dns.resolver.Resolver()
        myResolver.nameservers = [dns_server]
        myAnswers = myResolver.query(domain_name, query_type)
        for rdata in myAnswers:
            dns_response += str(rdata) + '\n'
        return dns_response

    def listen_for_dns(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((PROXY_TCP_IP, PROXY_TCP_PORT))
        server_socket.listen(20000)
        client_proxy_socket, addr = server_socket.accept()
        raw_message = client_proxy_socket.recv(MAX_BUFFER_SIZE).decode()

        dns_query = raw_message.split('\n')
        print(dns_query)
        dns_server = dns_query[0].strip('\r\n')
        query_type = dns_query[1].strip('\r\n')
        domain_name = dns_query[2].strip('\r\n')

        dns_response = ''
        if query_type == 'A' or query_type == 'CNAME':
            dns_response = self.send_dns_query(dns_server, domain_name, query_type)
        else:
            raise ('Query Type not supported')

        proxy_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        proxy_client_socket.connect((CLIENT_TCP_IP, CLIENT_TCP_PORT))
        proxy_client_socket.send(dns_response.encode())

    def listen(self):
        if self.protocol == 'dns':
            self.listen_for_dns()
        if self.protocol == 'http':
            self.listen_for_http()


if __name__ == '__main__':
    proxy = Proxy(sys.argv[1])
    proxy.listen()
