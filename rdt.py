from state import State
from config import *


def validate_msg_size(msg):

    msg_size = len(msg)

    msg_segments = []

    if(msg_size > MTU_SIZE):
        count = (msg_size - 1) // MTU_SIZE + 1

        for i in range(count):
            offset = i * MTU_SIZE
            msg_segments.append(msg[offset:offset + MTU_SIZE])

    else:
        msg_segments.append(msg)
    
    return msg_segments


print(validate_msg_size("Milad".encode()))