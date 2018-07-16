import time
import socket
import struct
import config

class Util:

    def __init__(self):
        pass

    @staticmethod
    def write_into_file(filename, text):
        my_file = open(filename, "w")
        my_file.write(text)
        my_file.close()

    @staticmethod
    def lookup_in_dict(searchFor, document):
        for k, v in document.items():
            if searchFor == k:
                return config.CACHE_HIT
        return config.CACHE_MISS