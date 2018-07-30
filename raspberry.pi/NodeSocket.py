import socket
import struct

class NodeSocket:

    def __init__(self, sock = None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else :
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host,port))

    def send(self, msg):
        totalsent = 0
        while totalsent < struct.calcsize(msg):
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broke")
            totalsent = totalsent + sent

    # the first int should be the size of the data
    # the second int should be the message type
    def receieve(self):
        chunks = []
        bytes_recd = 0
        MSGLEN = 65535
        while bytes_recd < MSGLEN:
            chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            MSGLEN = chunks[0:4]
            megtype = chunks[5:8]
            #todo: write the command type parser here
            bytes_recd = bytes_recd + len(chunk)
        return b''.join(chunks)