from Client.Model.Connection import Connection
from Client.Model.Disconnector import disconnect
from Client.View.Menu import *
from Client.Model.Message import *

def get_friends_list(username, connection: Connection):
    l_res = []
    data = f'friends//{username}'
    connection.send(data)
    response = connection.receive()
    if response == 'EMPTY':
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
            i +=1

    def check(self, choice: str, corrects: list):
        for c in corrects:
            if choice == c:
                return True
        return False

    def check_c(self, c):
        l = [str(x) for x in range(0, len(self.friends))]
        for x in l:
            if c == x:
                return True
        return False


    def print_messages(self, data: str):
        l = []
        data2 = data.split('***')
        i = 1
        for d in data2:
            d2 = d.split('//')
            m = Message(d2)
            l.append(m)
            print(f'{i} - {m}')
            i += 1
        return l

    def read_messages(self):
        if len(self.friends) == 0:
            print('Add some friends')
            return
        self.print_friends_list()
        c = input('choose <back> for back')
        if not self.check_c(c):
            print('invalid')
            return
        data = f'get-messages//{self.username}//{self.friends[int(c) - 1]}'
        self.connection.send(data)
        response = self.connection.receive()
        l = self.print_messages(response)
        like = input('if you want like enter index of message or <back> for back: ')
        if like == '<back>':
            return
        like = int(like) - 1
        data = f'like//{self.username}//{l[like].id}'
        self.connection.send(data)
        self.connection.receive()


    def add_friend(self):
        u = input('enter your new friend username or <back> for back: ')
        if u == '<back>':
            return

        data = f'add-friend//{self.username}//{u}'
        self.connection.send(data)
        response = self.connection.receive()
        if response == 'DONE':
            print('your request in pending')
        elif response == 'ERROR':
            print('invalid')
        return

    def print_friend_requests(self):
        data = f'friend-requests//{self.username}'
        self.connection.send(data)
        response = self.connection.receive()
        i = 1
        for x in response.split('//'):
            print(f'{i} - {x}')
            i += 1
        return response.split('//')

    def friend_requests(self):
        p = self.print_friend_requests()
        c = input('Enter like username-><i> (i = 0 accept i = 1 reject) and <back> for back:')
        if c == '<back>':
            return

        cs = c.split('->')
        print(cs)
        if not self.check(cs[0], p):
            print('invalid')
            return
        mode = None
        if cs[1] == '0':
            mode = 'accept'
        else:
            mode = 'reject'
        print(f'{cs[0]} {mode}')
        data = f'{mode}//{self.username}//{cs[0]}'
        self.connection.send(data)
        self.connection.receive()

    def remove_friend(self):
        self.print_friends_list()
        c = input('enter username to delete or <back> for back:')
        if c == '<back>':
            return
        if not self.check(c, self.friends):
            print('invalid')
            return
        data = f'remove-friend//{self.username}//{c}'
        self.connection.send(data)
        self.connection.receive()
        self.friends = get_friends_list(self.username, self.connection)

    def print_blocks(self, blocks: str):
        if blocks == 'EMPTY':
            print('nothing...')
            return
        blocks2 = blocks.split('//')
        i = 1
        for x in blocks2:
            print(f'{i} - {x}')
            i += 1

    def block(self):
        data = f'block-list//{self.username}'
        self.connection.send(data)
        response = self.connection.receive()
        self.print_blocks(response)
        c = input('enter like username->block/unblock <back> to back: ')
        if c == '<back>':
            return
        cs = c.split('->')
        data = f'{cs[1]}//{self.username}//{cs[0]}'
        self.connection.send(data)
        self.connection.receive()
        if cs[1] == 'block':
            self.friends = get_friends_list(self.username, self.connection)

    def main_loop(self):
        while True:
            print(get_user_menu())
            c = input()
            if self.check(c, [str(x) for x in range(0, 8)]):
                if c == '0':
                    disconnect(self.connection)
                    return
                elif c == '1':
                    self.send_message()
                elif c == '2':
                    self.read_messages()
                elif c == '3':
                    self.search()
                elif c == '4':
                    self.add_friend()
                elif c == '5':
                    pass
                elif c == '6':
                    self.friend_requests()
                elif c == '7':
                    self.block()
                elif c == 8:
                    t = self.delete_account()
                    if t:
                        print('Good bye')
                        return


    def delete_account(self):
        if input('do you sure? 1 for yes anything for no :,( :') == '1':
            data = f'delete-account//{self.username}'
            self.connection.send(data)
            self.connection.receive()
            disconnect(self.connection)
            return True
        else:
            return False

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
        m = input('Enter Like : message->friend username or <back> for back')
        if m == '<back>':
            return
        ms = m.split('->')
        print(ms)
        if not self.check_message(m):
            print('invalid')
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
            i += 1

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
