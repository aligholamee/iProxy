# in the name of God

# python3 main.py http http://www.google.com/
# python3 main.py dns A 8.8.8.8 aut.ac.ir
# python3 proxy.py http

from client import Client
import sys

clnt = Client()
if sys.argv[1] == 'http':
    clnt.send_http_message(sys.argv[2])

if sys.argv[1] == 'dns':
    clnt.send_dns_query(sys.argv[2], sys.argv[3] , sys.argv[4])
