from Client.Model.Connection import Connection
from Client.View.Menu import *


def get_friends_list(username, connection: Connection):
    l_res = []
    data = f'friends//{username}'
    connection.send(data)
    response = connection.receive()
    if len(response) == 0:
        return l_res



    return l_res


class UserApplication:
    def __init__(self, username, connection: Connection):
        self.username = username
        self.friends = get_friends_list(username, connection)
        self.connection = connection

    def check(self, choice: str, corrects: list):
        for c in corrects:
            if choice == c:
                return True
        return False

    def main_loop(self):
        while True:
            print(get_user_menu(m_count=0, p_count=0))
            c = input()
            if self.check(c, [str(x) for x in range(0, 8)]):
                if c == '0':
                    self.connection.send(f'logout//{self.username}')
                    response = self.connection.receive()
                    self.connection.close()
                    return

    def search(self):
        elements = ['ID', 'FNAME', 'LNAME', 'PHONE_NUMBER', 'EMAIL']
        while True:
            print(Menu['search'])
            e = input()
            if self.check(e, ['1', '2', '3', '4', '5', 'x', 'X']):
                s = input('Enter here for search(<back> for back):  ')
                if s == '<exit>':
                    return
                data = f'search//{elements[int(e) - 1]}//{s}'
                self.connection.send(data)
                response = self.connection.receive()
                return
