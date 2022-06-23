from Client.Model.Connection import Connection
from Client.View.Menu import *


def get_friends_list(username, connection: Connection):
    l_res = []
    data = f'friends//{username}'
    connection.send(data)
    response = connection.receive()
    if len(response) == 0:
        return l_res

    l_res = response.split('//')
    return l_res


class UserApplication:
    def __init__(self, username, connection: Connection):
        self.username = username
        self.friends = get_friends_list(username, connection)
        self.connection = connection

    def print_friends_list(self):
        i = 1
        for x in self.friends:
            print(f'{i} - {x}')
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
                elif c == '1':
                    self.send_message()
                elif c == '3':
                    self.search()

    def check_message_friend(self, username: str):
        for x in self.friends:
            if username.__eq__(x):
                return True
        return False

    def check_message(self, data: str):
        data2 = data.split('->')
        return self.check_message_friend(data2[1])

    def send_message(self):
        if len(self.friends) == 0:
            print('Add some friends')
            return
        self.print_friends_list()
        m = input('Enter Like : message/friend username or <back> for back')
        if m =='<back>':
            return
        ms = m.split('->')
        print(ms)
        if not self.check_message(m):
            print('invlaid')
            return
        data = f'send-message//{ms[0]}//{self.username}//{ms[1]}'
        self.connection.send(data)





    def print_search_result(self, result: str):
        if result == 'NOTHING':
            print('Nothing...')
        print('search result')
        data = result.split('//')
        i = 1
        for x in data:
            print(f'{i} - {x}')

    def search(self):
        elements = ['ID', 'FNAME', 'LNAME', 'PHONE_NUMBER', 'EMAIL']
        while True:
            print(Menu['search'])
            e = input()
            if self.check(e, ['1', '2', '3', '4', '5', 'x', 'X']):
                if e == 'x' or e == 'X':
                    return
                s = input('Enter here for search(<back> for back):  ')
                if s == '<exit>':
                    return
                data = f'search//{elements[int(e) - 1]}//{s}'
                self.connection.send(data)
                response = self.connection.receive()
                self.print_search_result(response)
                return
