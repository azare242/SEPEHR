import threading
import socket
from Server.Model.User import User
from Server.Logic.Parser import *


class ClientHandler:
    def __init__(self, client_socket: socket.socket):
        self.user = None
        self.client_socket = client_socket
        self.thread = threading.Thread(target=self.handling, args=())

    def handling(self):
        while True:
            try:
                data_received = self.client_socket.recv(4096).decode('utf-8')
                parse(data_received)

            except socket.error as err:
                print("USER EXITED")
                self.client_socket.close()
                break
            finally:
                print("USER EXITED")
                self.client_socket.close()
                break

    def start(self):
        self.thread.start()
