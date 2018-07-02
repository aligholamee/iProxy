import time

class Util:

    def __init__(self):
        pass

    @staticmethod
    def udp_reliable_send(cls, sock, data , ip , port , master):
        while True:        
            sock.sendto(data, (ip, port))
            time.sleep(5)
            if master.getAck() == True:
                break;


