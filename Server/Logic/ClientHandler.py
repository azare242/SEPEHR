import threading
import socket
from Server.Model.User import User
from Server.Logic.Parser import *
from Server.Logic.DatabaseConnection import *
from Server.Logic.Parser import *

class ClientHandler:
    def __init__(self, client_socket: socket.socket, clients: set, database_connection: DatabaseConnection):
        self.user = None
        self.client_socket = client_socket
        self.thread = threading.Thread(target=self.handling, args=())
        self.server_clients = clients
        self.parser = Parser(database_connection)
    def handling(self):
        while True:
            try:
                data_received = self.client_socket.recv(4096).decode('utf-8')
                self.parser.parse(data_received, self.server_clients)

            except socket.error as err:
                print("USER DISCONNECTED")
                self.client_socket.close()
                break
            finally:
                print("USER EXITED")
                self.client_socket.close()
                break

    def start(self):
        self.thread.start()
