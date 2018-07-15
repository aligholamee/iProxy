import time
import socket
import struct


class Util:

    def __init__(self):
        pass

    @staticmethod
    def write_into_file(filename, text):
        my_file = open(filename, "w")
        my_file.write(text)
        my_file.close()
