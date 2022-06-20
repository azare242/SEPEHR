import socket

from Utils.Properties import *

from Server.Logic.ClientHandler import ClientHandler
from Server.Logic.DatabaseConnection import *


class Server:
    def __init__(self):
        self.HOST = get('Server', "HOST")
        self.PORT = int(get('Server', "PORT"))
        self.database_connection = DatabaseConnection()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.HOST, self.PORT))
        self.socket.listen(5)
        self.clients = set()

    def server_loop(self):
        while True:
            client, address = self.socket.accept()
            print(f'Connected with {str(address)}')
            client_handler = ClientHandler(client, self.clients, self.database_connection)
            client_handler.start()
