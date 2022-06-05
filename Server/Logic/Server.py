import socket
import _thread

from Server.Model.User import User
from Utils import Properties
from Server.Model import Sets
from Server.Logic.ClientHandler import ClientHandler



class Server:
    def __init__(self):
        self.client_handlers = Sets.ClientHandlersSet()
        self.HOST = Properties.get('Server', "HOST")
        self.PORT = Properties.get('Server', "HOST")

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.HOST, self.PORT))
        self.socket.listen()


    def generate_user(self, info):
        return User(info[0], info[1], info[2], info[3], info[4])

    def login(self, client: socket.socket):
        client.send('login'.encode('utf-8'))
        while True:
            user_information = client.recv(4096).decode('utf-8')
            info = user_information.split('//')
            if self.client_handlers.search_by_username(info[0]) is not None:
                user = self.generate_user(info)
                client.send('done'.encode('utf-8'))
            else:
                client.send('try-again'.encode('utf-8'))

    def server_loop(self):
        while True:
            client, address = self.socket.accept()
            print(f'Connected with {str(address)}')
            client_handler = ClientHandler(client, self)
            client_handler.start()
