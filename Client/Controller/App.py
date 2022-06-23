from Client.View.Menu import Menu
from Client.Model.Connection import *
from Utils.Passwords import *
import re

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

    def get_phone_number(self):
        while True:
            phone_number = input('enter phone number (11 digits): ')
            if len(phone_number) == 11:
                return phone_number
            elif phone_number == '<back>':
                return '<back>'
            else:
                print('Try again')

    def get_email(self):
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        while True:
            email_in = input('Enter Email: ')
            if (re.search(regex,email_in)):
                return email_in
            elif email_in == '<back>':
                return '<back>'
            else:
                print('Try Again')

    def signup_a(self):
        print('Notice: if you want to back enter "<back>"')
        while True:
            un = input('Username : ').lower()
            if un == '<back>':
                return
            fname = input('First name: ')
            if fname == '<back>':
                return
            lname = input('Last Name: ')
            if lname == '<back>':
                return
            phone_number = self.get_phone_number()
            if phone_number == '<back>':
                return
            e = self.get_email()
            if e == '<back>':
                return
            pw = encrypt(input('Password : '))
            if decrypt(pw) == '<back>':
                return
            self.connection.connect()
            data = f'sign-up//{un}//{pw}//{fname}//{lname}//{phone_number}//{e}'
            self.connection.send(data)
            response = self.connection.receive()
            if response == 'DONE':
                print('done')
                self.exit_from_server()
                # TODO : USERMENU
            else:
                print("username exists or something went wrong try again")
                return

    def signup_m(self):
        print(Menu['signup-m'])
        while True:
            choice = input()
            if self.check(choice, ['1', 'x', 'X']):
                if choice == 'x' or choice == 'X':
                    return
                else:
                    self.login_a()
                    return


    def login_a(self):
        print('Notice: if you want to back enter "<back>"')
        while True:
            un = input('Username : ').lower()
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
                    return
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
