import binascii
from state import State
from config import *

def radix2(num):
    ret = ""
    
    for i in range(4):
        if (num % 2 == 1):
            ret += '1'
        else:
            ret += '0'
        num //= 2
    
    return ret[::-1]

def calculate_checksum(msg):
    checksum = 0

    for ch in msg:
        checksum += ch  # ord('\x03`) -> 3

    checksum %= 16 # Returns 8 LSBs
    
    return radix2(checksum).encode()
    
"""
 make_packet("milad".encode())
[b'0110->checksum 0->continue 0->sequence mi', b'111001la', b'010110d']
"""
def make_packet(msg):

    msg_size = len(msg)

    msg_segments = []

    if(msg_size > MTU_SIZE):
        count = (msg_size - 1) // MTU_SIZE + 1

        for i in range(count):

            seq_flag = b'0' if (i % 2 == 0) else b'1'
            # if 0 seq num = 0 

            cont_flag = b'1' if (i == (count - 1)) else b'0'
            # if 1 the byte stream finish
            offset = i * MTU_SIZE
            msg_segments.append(calculate_checksum(cont_flag + seq_flag + msg[offset:offset + MTU_SIZE]) + cont_flag + seq_flag + msg[offset:offset + MTU_SIZE])
    else:
        msg_segments.append(calculate_checksum(b'1' + b'0' + msg) + b'1' + b'0' + msg)
    
    return msg_segments

# def rdt_send(sock, msg, dest_ip, dest_port):


#     # byte + byte + last_byte_indicator + msg

#     segments = make_packet(msg)
#     pnt = 0

#     # Initial point
#     state = State.WAIT_FOR_CALL_0

#     while(True):


#         if(state == State.WAIT_FOR_ACK_0):

#             sock.sendto(msg.encode(), (dest_ip, dest_port))

#         elif(state == State.WAIT_FOR_ACK_1):

#         elif(state == State.WAIT_FOR_CALL_0):
        
#         elif(state == State.WAIT_FOR_CALL_1):
        
#         else:
#             raise("Inavlid rdt_send state")

# print(make_packet("Milads".e1ncode()))
