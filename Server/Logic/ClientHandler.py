import threading
from threading import *
import socket
from Server.Logic.Server import Server
from Server.Model.User import User


def generate_user(info):
    return User(info[0], info[1], info[2], info[3], info[4])


class ClientHandler:
    def __init__(self, client_socket: socket.socket, server: Server):
        self.user = None
        self.client_socket = client_socket
        self.thread = threading.Thread(target=self.handling, args=(socket,))
        self.server = server

    def handling(self):
        try:
            self.client_socket.send('login'.encode('utf-8'))
            while True:
                user_information = self.client_socket.recv(4096).decode('utf-8')
                info = user_information.split('//')
                if self.server.client_handlers.search_by_username(info[0]) is None:
                    self.user = generate_user(info)
                    self.client_socket.send('done'.encode('utf-8'))
                    break
                else:
                    self.client_socket.send('try-again'.encode('utf-8'))

        except socket.error as err :
            self.client_socket.close()
            self.server.client_handlers.remove_client(self)
        finally:
            self.client_socket.close()
            self.server.client_handlers.remove_client(self)

    def start(self):
        self.thread.start()
