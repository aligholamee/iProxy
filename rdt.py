import binascii
import socket

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

    checksum %= 16  # Returns 8 LSBs

    return radix2(checksum).encode()


"""
 make_packet("milad".encode())
[b'0110->checksum 0->continue 0->sequence mi', b'111001la', b'010110d']
"""


def make_packet(msg):
    msg_size = len(msg)

    msg_segments = []

    if msg_size > MTU_SIZE:
        count = (msg_size - 1) // MTU_SIZE + 1

        for i in range(count):
            seq_flag = b'0' if (i % 2 == 0) else b'1'
            # if 0 seq num = 0 

            cont_flag = b'1' if (i == (count - 1)) else b'0'
            # if 1 the byte stream finish
            offset = i * MTU_SIZE
            msg_segments.append(
                calculate_checksum(cont_flag + seq_flag + msg[offset:offset + MTU_SIZE]) + cont_flag + seq_flag + msg[
                                                                                                                  offset:offset + MTU_SIZE])
    else:
        msg_segments.append(calculate_checksum(b'1' + b'0' + msg) + b'1' + b'0' + msg)

    return msg_segments


def rdt_send(msg, src_ip, src_port, dest_ip, dest_port):
    send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    segment = make_packet(msg)
    pnt = 0
    state = State.SEND_0

    while pnt < len(segment):

        if state == State.WAIT_FOR_ACK_0:
            rcv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            rcv_sock.bind((src_ip, src_port))
            rcv_sock.settimeout(5)

            try:
                rcv_msg, addr = rcv_sock.recvfrom(MAX_BUFFER_SIZE)
                rcv_msg = rcv_msg.decode()
                if rcv_msg == 'ACK0':
                    pnt += 1
                    state = State.SEND_1
                else:
                    state = State.SEND_0

            except socket.timeout:
                state = State.SEND_0
            finally:
                rcv_sock.close()

        elif state == State.WAIT_FOR_ACK_1:
            rcv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            rcv_sock.bind((src_ip, src_port))
            rcv_sock.settimeout(5)

            try:
                rcv_msg, addr = rcv_sock.recvfrom(MAX_BUFFER_SIZE)
                rcv_msg = rcv_msg.decode()
                if rcv_msg == 'ACK1':
                    pnt += 1
                    state = State.SEND_0
                else:
                    state = State.SEND_1

            except socket.timeout:
                state = State.SEND_1
            finally:
                rcv_sock.close()

        elif state == State.SEND_0:
            send_sock.sendto(segment[pnt], (dest_ip, dest_port))
            state = State.WAIT_FOR_ACK_0

        elif state == State.SEND_1:
            send_sock.sendto(segment[pnt], (dest_ip, dest_port))
            state = State.WAIT_FOR_ACK_1


def rdt_receive(src_ip, src_port, dest_ip, dest_port):
    message_received = ""

    state = State.RCV_0

    while True:

        if state == State.RCV_0:
            rcv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            rcv_sock.bind((src_ip, src_port))
            rcv_msg, (address, port) = rcv_sock.recvfrom(MAX_BUFFER_SIZE)
            rcv_sock.close()

            checksum = rcv_msg[0:4]
            has_cont = rcv_msg[4:5]
            seq_num = rcv_msg[5:6]
            data = rcv_msg[6:]

            send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            if checksum == calculate_checksum(has_cont + seq_num + data) or seq_num != b'0':
                send_sock.sendto(b'ACK0', (dest_ip, dest_port))
                state = State.RCV_1
                message_received += data.decode()
                print(data.decode())
                if has_cont == b'1':
                    break
            else:
                send_sock.sendto(b'ACK1', (dest_ip, dest_port))
        else:
            rcv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            rcv_sock.bind((src_ip, src_port))
            rcv_msg, (address, port) = rcv_sock.recvfrom(MAX_BUFFER_SIZE)
            rcv_sock.close()

            checksum = rcv_msg[0:4]
            has_cont = rcv_msg[4:5]
            seq_num = rcv_msg[5:6]
            data = rcv_msg[6:]

            send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            if checksum == calculate_checksum(has_cont + seq_num + data) or seq_num != b'0':
                send_sock.sendto(b'ACK1', (dest_ip, dest_port))
                state = State.RCV_0
                message_received += data.decode()
                print(data.decode())
                if has_cont == b'1':
                    break
            else:
                send_sock.sendto(b'ACK0', (dest_ip, dest_port))

    return message_received
