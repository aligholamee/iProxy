# in the name of God

# python3 server.py
# python3 client.py HTTP www.google.com

from client import Client
import sys


print(sys.argv[1])
clnt = Client(sys.argv[1] , sys.argv[2])
clnt.send_http_message()


