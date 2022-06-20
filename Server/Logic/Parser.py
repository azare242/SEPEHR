from Server.Logic.DatabaseConnection import *


class Parser:
    def __init__(self, database_connection: DatabaseConnection):
        self.dbc = database_connection

    def login(self, username, password):
        check1 = self.dbc.execute_query(f"""
        SELECT sepehr.users.ID
        FROM sepehr.users
        WHERE sepehr.users.ID == '{username}'
        """)
        check2 = self.dbc.execute_query(f"""
        SELECT COUNT(*)
        FROM sepehr.passwords
        WHERE USER_ID == '{username}' AND ENCRYPTED_PASSWORD == '{password}'
        """)
        if len(check1) == 1 and check2[0][0] == 1:
            return "DONE"
        else:
            return "ERROR"

    def parse(self, data_received: str, clients: set):
        info = data_received.split('//')
        if info[0] == 'login':
            result = [self.login(data_received[1], data_received[2]) , 'LOGIN']
            if result[0] != 'ERROR':
                clients.add(data_received[1])
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
        # TODO : LOGGING
