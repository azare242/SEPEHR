from Client.View.Menu import Menu
from Client.Model.Connection import *


class App:
    def __init__(self):
        self.connection = Connection()

    def run(self):
        cmd_in = str()
        self.connection.send('HI')
        while True:
            print(Menu['main'])
            cmd_in = input()
            if cmd_in == 'x':
                self.connection.close()
            elif cmd_in == '1':
                print(Menu['login'])
                # TODO : LOGIN
            elif cmd_in == '2':
                print(Menu['signup'])
                # TODO : SIGNUP