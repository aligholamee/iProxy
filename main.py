# in the name of God

# python3 client.py http www.google.com
# python3 main.py dns A 1.1.1.1 aut.ac.ir

from client import Client
import sys

clnt = Client()
if sys.argv[1] == 'http':
    clnt.send_http_message(sys.argv[2])

if sys.argv[1] == 'dns':
    clnt.send_dns_query(sys.argv[2], sys.argv[3] , sys.argv[4])
