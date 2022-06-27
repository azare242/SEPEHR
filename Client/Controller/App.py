from Client.View.Menu import Menu
from Client.Model.Connection import *
from Utils.Passwords import *
import re
from Client.Controller.UserApplication import UserApplication
from Client.Model.Disconnector import disconnect


def get_email():
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    while True:
        email_in = input('Enter Email: ')
        if re.search(regex, email_in):
            return email_in
        elif email_in == '<back>':
            return '<back>'
        else:
            print('Try Again')


class App:
    def __init__(self):
        self.connection = Connection()

    def check(self, choice: str, corrects: list):
        for c in corrects:
            if choice == c:
                return True
        return False

    def get_phone_number(self):
        while True:
            phone_number = input('enter phone number (11 digits): ')
            if len(phone_number) == 11:
                return phone_number
            elif phone_number == '<back>':
                return '<back>'
            else:
                print('Try again')

    def create_sq(self):
        q = input('Security Question: ')
        a = input('Answer: ')
        return q, a

    def signup_a(self):
        print('Notice: if you want to back enter "<back>"')
        while True:
            un = input('Username : ')
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
            e = get_email()
            if e == '<back>':
                return
            pw = encrypt(input('Password : '))
            if decrypt(pw) == '<back>':
                return
            self.connection.connect()
            data = f'signup//{un}//{pw}//{fname}//{lname}//{phone_number}//{e}'
            self.connection.send(data)
            response = self.connection.receive()
            if response == 'DONE':
                q, a = self.create_sq()
                data = f'create-security-question//{un}//{q}//{a}'
                self.connection.send(data)
                UserApplication(un, self.connection).main_loop()
                return
            else:
                disconnect(self.connection)
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
                    self.signup_a()
                    return

    def check_password(self, correct_password):
        flag = 0
        i = 3
        for _ in range(0, 3):
            pw = encrypt(input('Password: '))
            if pw == '<back>':
                return '<back>'

            if pw == correct_password:
                flag = 1
                return pw
            else:
                i -= 1
                print(f"PASSWORD INCORRECT you have {i} try")

        return "ERROR"

    def login_a(self):
        print('Notice: if you want to back enter "<back>"')

        while True:
            un = input('Username : ').lower()
            if un == '<back>':
                return
            # TODO : CHECK PENALTY
            data = f'get-password//{un}'

            self.connection.send(data)
            r = self.connection.receive()
            if r != "ERROR":
                pw = self.check_password(r)
                if pw == '<back>':
                    return
                if pw != 'ERROR':
                    data = f'login//{un}//{pw}'
                    self.connection.send(data)
                    response = self.connection.receive()
                    if response == "DONE":
                        UserApplication(un, self.connection).main_loop()
                        return
                    else:
                        print('user logged in before')
                        return
                else:
                    pass
                    # TODO : DO PENALTY
            else:
                print("username not found")

    def login_m(self):
        print(Menu['login-m'])
        while True:
            choice = input()
            if self.check(choice, ['1', '2', 'x', 'X']):
                if choice == '1':
                    self.login_a()
                    return
                elif choice == '2':
                    self.forgot_password()
                    return
                break
            else:
                print('invalid input try again', end=':')

    def security_question_check(self, username):
        data = f'security//{username}'
        self.connection.send(data)
        q, a = self.connection.receive().split('//')
        ain = input(q + ' |||<back> for back')
        if ain == '<back>':
            return '<back>'
        return ain == a

    def change_password(self, username):
        pw = encrypt(input('new password <back> for back: '))
        if decrypt(pw) == '<back>':
            return
        data = f'change-password//{username}//{pw}'
        self.connection.send(data)
        response = self.connection.receive()

    def forgot_password(self):
        uin = input('Enter Username<back> for back: ')
        if uin == '<back>':
            return
        c = self.security_question_check(uin)
        if c == '<back>':
            return
        if c:
            self.change_password(uin)

    def run(self):
        self.connection.connect()
        cmd_in = None
        while True:
            print(Menu['main'])
            cmd_in = input()
            if cmd_in == 'x':
                disconnect(self.connection)
                sys.exit()
            elif cmd_in == '1':
                self.login_m()
            elif cmd_in == '2':
                self.signup_m()
            else:
                print('invalid input try again: ', end='')
