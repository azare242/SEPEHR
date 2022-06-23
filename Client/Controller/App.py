from Client.View.Menu import Menu
from Client.Model.Connection import *
from Utils.Passwords import *
class App:
    def __init__(self):
        self.connection = Connection()

    def check(self, choice: str, corrects: list):
        for c in corrects:
            if choice == c:
                return True
        return False

    def exit_from_server(self):
        self.connection.send('exit')
        self.connection.close()

    def login_a(self):
        print('Notice: if you want to back enter "<back>"')
        while True:
            un = input('Username : ')
            if un == '<back>':
                return
            pw = input('Password : ')
            if pw == '<back>':
                return
            print(encrypt(pw))
            self.connection.connect()
            data = f'login//{un}//{encrypt(pw)}'
            self.connection.send_login_data(data)
            response = self.connection.receive()
            if response == "DONE":
                print('done')
                self.exit_from_server()
                sys.exit()
                break
            else:

                print('username or password is wrong try again')

    def login_m(self):
        print(Menu['login-m'])
        while True:
            choice = input()
            if self.check(choice, ['1', '2', 'x', 'X']):
                if choice == '1':
                    self.login_a()
                elif choice == '2':
                    pass
                    # TODO : FORGOT PASSWORD
                break
            else:
                print('invalid input try again', end=':')

    def run(self):
        cmd_in = None
        print(Menu['main'])
        # self.connection.send('HI')
        while True:
            cmd_in = input()
            if cmd_in == 'x':
                sys.exit()
            elif cmd_in == '1':
                self.login_m()
                # TODO : LOGIN
            elif cmd_in == '2':
                print(Menu['signup-m'])
                # TODO : SIGNUP
            else:
                print('invalid input try again: ', end='')
