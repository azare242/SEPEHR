from Server.Logic.DatabaseConnection import *


class Parser:
    def __init__(self, database_connection: DatabaseConnection):
        self.dbc = database_connection

    def login(self, username, password):
        check = self.dbc.execute_query(f"""
        SELECT sepehr.users.ID
        FROM sepehr.users
        WHERE sepehr.users.ID == '{username}'
        """)

    def parse(self, data_received: str, clients: set):
        info = data_received.split('//')
        if info[0] == 'login':
            pass
            # TODO : LOGIN
        elif info[0] == 'signup':
            pass
            # TODO : SIGNUP
        elif info[0] == 'send-message':
            pass
            # TODO : SEND-MESSAGE
        elif info[0] == 'friend-request':
            pass
            # TODO : FRIEND-REQUEST
        # TODO : OTHER COMMANDS
