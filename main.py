# in the name of God

# python3 server.py
# python3 client.py HTTP www.google.com

from client import Client
import sys

clnt = Client()
if sys.argv[1] == 'http':
    clnt.send_http_message(sys.argv[2])

if sys.argv[1] == 'dns':
    clnt.send_dns_query(sys.argv[2], sys.argv[3])
