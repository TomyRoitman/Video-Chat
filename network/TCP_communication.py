import socket
import struct
import threading
import time

import numpy as np

FPS = 100
UDP_IP = '127.0.0.1'
UDP_PORT = 10000
MSG_CODE_SIZE = 4
MSG_SIZE_HEADER_SIZE = 8
MSG_CHUNK_SIZE = 1024
MAX_SIZE_UDP_MSG = 65507


# SERVER_IP = '127.0.0.1'
# SERVER_PORT = 11233

class TCPStream:

    def __init__(self, client_socket):
        self.client_socket = client_socket

    def recv_by_size(self):
        msg_code = ""
        while len(msg_code) < MSG_CODE_SIZE:
            msg_code += self.client_socket.recv(MSG_CODE_SIZE - len(msg_code)).decode()

        size_header = ""
        while len(size_header) < MSG_SIZE_HEADER_SIZE:
            size_header += self.client_socket.recv(MSG_SIZE_HEADER_SIZE - len(size_header)).decode()

        content_length = int(size_header)
        content = ""
        while len(content) < content_length:
            content += self.client_socket.recv(content_length - len(content)).decode()

        return msg_code, content_length, content

    def recv_by_size_with_timeout(self, interval):
        self.client_socket.settimeout(interval)
        msg_code = ""
        while len(msg_code) < MSG_CODE_SIZE:
            try:
                msg_code += self.client_socket.recv(MSG_CODE_SIZE - len(msg_code)).decode()
            except socket.timeout:
                return "Not received yet"
        size_header = ""
        while len(size_header) < MSG_SIZE_HEADER_SIZE:
            try:
                size_header += self.client_socket.recv(MSG_SIZE_HEADER_SIZE - len(size_header)).decode()
            except socket.timeout:
                return "Not received yet"
        content_length = int(size_header)
        content = ""
        while len(content) < content_length:
            try:
                content += self.client_socket.recv(content_length - len(content)).decode()
            except socket.timeout:
                return "Not received yet"

        return msg_code, content_length, content

    def __split_by_len(self, seq, length):
        return [seq[x: x + length] for x in range(0, len(seq), length)]

    def send_by_size(self, msg_code, content):
        header_to_send = msg_code + str(len(content)).zfill(MSG_SIZE_HEADER_SIZE)
        header_to_send = header_to_send.encode()
        self.client_socket.send(header_to_send)
        chunks = self.__split_by_len(content, MSG_CHUNK_SIZE)
        for chunk in chunks:
            self.client_socket.send(chunk.encode())
