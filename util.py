import time
import socket
import struct

DNS_QUERY_MESSAGE_HEADER = struct.Struct("!6H")
DNS_QUERY_SECTION_FORMAT = struct.Struct("!2H")

class Util:

    def __init__(self):
        pass

    @staticmethod
    def udp_reliable_send(cls, sock, data, ip, port, master):
        while True:
            sock.sendto(data, (ip, port))
            time.sleep(5)
            if master.getAck() == True:
                break

    @staticmethod
    def decode_labels(cls, message, offset):
        labels = []
        while True:
            length, = struct.unpack_from("!B", message, offset)

            if (length & 0xC0) == 0xC0:
                pointer, = struct.unpack_from("!H", message, offset)
                offset += 2

                return labels + cls.decode_labels(message, pointer & 0x3FFF), offset

            if (length & 0xC0) != 0x00:
                raise Exception("unknown label encoding")

            offset += 1

            if length == 0:
                return labels, offset

            labels.append(*struct.unpack_from("!%ds" % length, message, offset))
            offset += length


    @staticmethod
    def decode_question_section(cls, message, offset, qdcount):
        questions = []

        for _ in range(qdcount):
            qname, offset = cls.decode_labels(message, offset)

            qtype, qclass = DNS_QUERY_SECTION_FORMAT.unpack_from(message, offset)
            offset += DNS_QUERY_SECTION_FORMAT.size

            question = {"domain_name": qname,
                        "query_type": qtype,
                        "query_class": qclass}

            questions.append(question)

        return questions, offset

    @staticmethod
    def decode_dns_message(cls, message):

        id, misc, qdcount, ancount, nscount, arcount = DNS_QUERY_MESSAGE_HEADER.unpack_from(message)

        qr = (misc & 0x8000) != 0
        opcode = (misc & 0x7800) >> 11
        aa = (misc & 0x0400) != 0
        tc = (misc & 0x200) != 0
        rd = (misc & 0x100) != 0
        ra = (misc & 0x80) != 0
        z = (misc & 0x70) >> 4
        rcode = misc & 0xF

        offset = DNS_QUERY_MESSAGE_HEADER.size
        questions, offset = cls.decode_question_section(message, offset, qdcount)

        result = {"id": id,
                "is_response": qr,
                "opcode": opcode,
                "is_authoritative": aa,
                "is_truncated": tc,
                "recursion_desired": rd,
                "recursion_available": ra,
                "reserved": z,
                "response_code": rcode,
                "question_count": qdcount,
                "answer_count": ancount,
                "authority_count": nscount,
                "additional_count": arcount,
                "questions": questions}

        return result