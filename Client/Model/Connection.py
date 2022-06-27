import socket
import sys

from Utils.Properties import *


class Connection:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.HOST = get('Client', 'HOST')
        self.PORT = int(get('Client', 'PORT'))

    def send(self, data: str):
        try:
            self.socket.send(data.encode('utf-8'))
        except socket.error as err:
            print(err)
            self.socket.close()

    def receive(self):
        try:
            return self.socket.recv(4096).decode('utf-8')
        except socket.error as err:
            print(err)
            self.close()

    def connect(self):
        self.socket.connect((self.HOST, self.PORT))

    def close(self, mode=0):
        self.socket.close()
        if mode == 1:
            sys.exit()
