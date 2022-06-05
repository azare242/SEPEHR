from User import User
from Server.Logic.ClientHandler import ClientHandler


class FriendsSet:

    def __init__(self):
        self.S = set()

    def add_friend(self, user: User):
        if not isinstance(user, User):
            return
        self.S.add(user)

    def remove_friend(self, user: User):
        if not isinstance(user, User):
            return
        self.S.remove(user)

    def search_by_username(self, username):
        u = None
        for user in self.S:
            if user.username == username:
                u = user
        return u

    def search_by_name(self, fname, lname):
        u = None
        for user in self.S:
            if user.fname == fname or user.lname == lname:
                u = user
        return u


class ClientHandlersSet:
    def __init__(self):
        self.S = set()

    def add_client(self, client: ClientHandler):
        if not isinstance(client, ClientHandler):
            return
        self.S.add(client)

    def remove_client(self, client: ClientHandler):
        if not isinstance(client, ClientHandler):
            return
        self.S.remove(client)

    def search_by_username(self, username: str):
        u = None
        for client in self.S:
            if client.user.username == username:
                u = client
        return u