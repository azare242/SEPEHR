from Server.Logic.DatabaseConnection import *
import datetime


class Parser:
    def __init__(self, database_connection: DatabaseConnection):
        self.dbc = database_connection

    def log(self, info):
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_type = info[1]
        status = info[0]

        if type == 'LOGIN' and status == 'DONE':
            text = f'{info[2]} logged in successfully'
            self.dbc.execute_query(f"""
            INSERT INTO sepehr.logs (TYPE, TEXT, TIME)
            VALUE ({log_type}, {text}, {time})
        """)

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
            result = [self.login(info[1], info[2]), 'LOGIN', info[1]]
            if result[0] != 'ERROR':
                clients.add(info[1])
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
