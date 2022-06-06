import socket
import _thread


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



    def server_loop(self):
        while True:
            client, address = self.socket.accept()
            print(f'Connected with {str(address)}')
            client_handler = ClientHandler(client, self)
            client_handler.start()
