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
        WHERE sepehr.users.ID = '{username}'
        """)
        check2 = self.dbc.execute_query(f"""
        SELECT COUNT(*)
        FROM sepehr.passwords
        WHERE USER_ID = '{username}' AND ENCRYPTED_PASSWORD = '{password}'
        """)
        if len(check1) == 1 and check2[0][0] == 1:
            return "DONE"
        else:
            return "ERROR"

    def new_user_check(self, username, phone_number, email):
        check = self.dbc.execute_query(f"""
        SELECT count(*)
        FROM sepehr.users
        WHERE sepehr.users.ID = '{username}' OR sepehr.users.PHONE_NUMBER = '{phone_number}' OR sepehr.users.EMAIL = '{email}'
        """)
        return check[0][0] == 0

    def signup(self, data):
        if self.new_user_check(data[0], data[4], data[5]):
            self.dbc.execute_query(f"""
            INSERT INTO sepehr.users(ID, FNAME, LNAME, PHONE_NUMBER, EMAIL) VALUE 
            ('{data[0]}','{data[2]}','{data[3]}','{data[4]}','{data[5]}')
            """, mode=1)
            self.dbc.execute_query(f"""
            INSERT INTO sepehr.passwords(USER_ID, Encrypted_Password) VALUE 
            ('{data[0]}','{data[1]}')
            """)
            return 'DONE'
        else:
            return 'ERROR'

    def create_security_question(self, data):
        self.dbc.execute_query(f"""
        INSERT INTO sepehr.security_questions(USER_ID, Question, Answer) 
        VALUE ('{data[0]}', '{data[1]}', '{data[2]}')
        """, mode=1)

    def search(self, data):
        return self.dbc.execute_query(f"""
        SELECT sepehr.users.ID from sepehr.users
        WHERE sepehr.users.{data[0]} = '%{data[1]}%'
        """)

    def get_friends_list(self,username):
        return self.dbc.execute_query(f"""
        SELECT sepehr.friends.USER_ID1 FROM sepehr.friends
        WHERE sepehr.friends.USER_ID2 = '{username}'
        UNION 
        SELECT sepehr.friends.USER_ID2 FROM sepehr.friends
        WHERE sepehr.friends.USER_ID1 = '{username}'
        """)

    def parse(self, data_received: str, clients: set):

        info = data_received.split('//')
        if info[0] == 'login':
            result = self.login(info[1], info[2])
            if result != 'ERROR':
                if not clients.__contains__(info[1]):
                    clients.add(info[1])
                    return 'DONE'
                else:
                    return 'ERROR'
        elif info[0] == 'signup':
            result = self.signup(info[1:])
            clients.add(info[1])
            return result

        elif info[0] == 'create-security-question':
            self.create_security_question(info[1:])
            return 'DONE'
        elif info[0] == 'search':
            return self.search(info[1:])
        elif info[0] == 'friends':
            return self.get_friends_list(info[1])
        elif info[0] == 'send-message':
            pass
            # TODO : SEND-MESSAGE

        elif info[0] == 'friend-request':
            pass
            # TODO : FRIEND-REQUEST
        # TODO : OTHER COMMANDS
        # TODO : LOGGING
        return 'ERROR'
