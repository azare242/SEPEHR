from Server.Logic.DatabaseConnection import *
import datetime


class Parser:
    def __init__(self, database_connection: DatabaseConnection):
        self.dbc = database_connection

    def log(self, type, text):
        _time_ = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.dbc.execute_query(f"""
        INSERT INTO sepehr.logs(TYPE, TEXT, TIME) VALUE 
        ('{type}', '{text}', '{_time_}')
        """, mode=1)

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
            logtxt = f"""Login field by USER {username}"""
            self.log('ERR', logtxt)
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
            logtxt = f"""USERNAME = {data[0]}
            FNAME = {data[2]}
            LNAME = {data[3]}
            PHONE NUMBER = {data[4]}
            EMAIL = {data[5]}
            Signed Up Successfully"""
            self.log('INFO', logtxt)
            return 'DONE'
        else:
            logtxt = 'Sign Up Field'
            self.log('ERR', logtxt)
            return 'ERROR'

    def create_security_question(self, data):
        self.dbc.execute_query(f"""
        INSERT INTO sepehr.security_questions(USER_ID, Question, Answer) 
        VALUE ('{data[0]}', '{data[1]}', '{data[2]}')
        """, mode=1)

    def create_string(self, data):
        temp = []
        for x in data:
            temp.append(x[0])
        return '//'.join(temp)

    def search(self, data):
        s_res = self.dbc.execute_query(f"""
        SELECT sepehr.users.ID from sepehr.users
        WHERE sepehr.users.{data[0]} LIKE '%{data[1]}%'
        """)
        print('1')
        if len(s_res) == 0:
            return 'NOTHING'
        return self.create_string(s_res)

    def get_friends_list(self, username):
        friends = self.dbc.execute_query(f"""
        SELECT sepehr.friends.USER_ID1 FROM sepehr.friends
        WHERE sepehr.friends.USER_ID2 = '{username}'
        UNION 
        SELECT sepehr.friends.USER_ID2 FROM sepehr.friends
        WHERE sepehr.friends.USER_ID1 = '{username}'
        """)
        if len(friends) == 0:
            return ""
        return self.create_string(friends)

    def send_message(self, data):
        _time_ = _time_ = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message_id = f'{data[1]}X{data[2]}X{_time_}'
        print(message_id)
        q1 = f"""
        INSERT INTO sepehr.messages(ID, TEXT, TIME) VALUE 
        ('{message_id}', '{data[0]}','{_time_}')
        """
        q2 = f"""
        INSERT INTO sepehr.sender_reciver_messages(MESSAGE_ID, USER_ID_RECIVER, USER_ID_SENDER) VALUE 
        ('{message_id}', '{data[1]}', '{data[2]}')
        """
        self.dbc.execute_query(q1, mode=1)
        self.dbc.execute_query(q2, mode=1)
        logtxt = f"""
        send message from {data[1]} ro {data[2]} successfully
        """

    def get_messages(self, data):
        q1 = f"""
        SELECT TEXT,USER_ID_SENDER,USER_ID_RECIVER
        FROM sepehr.messages AS M , sepehr.sender_reciver_messages AS SRM
        WHERE M.ID = SRM.MESSAGE_ID 
        AND USER_ID_SENDER = '{data[0]}' AND USER_ID_RECIVER = '{data[1]}'
        UNION 
        SELECT TEXT,USER_ID_SENDER,USER_ID_RECIVER
        FROM sepehr.messages AS M , sepehr.sender_reciver_messages AS SRM
        WHERE M.ID = SRM.MESSAGE_ID 
        AND USER_ID_SENDER = '{data[1]}' AND USER_ID_RECIVER = '{data[0]}'
        """
        messages = self.dbc.execute_query(q1)
        # TODO : CREATE MESSAGES STRING


    def parse(self, data_received: str, clients: set):

        info = data_received.split('//')
        if info[0] == 'login':
            result = self.login(info[1], info[2])
            if result != 'ERROR':
                if not clients.__contains__(info[1]):
                    clients.add(info[1])
                    logtxt = f"""USER {info[1]} logged in succsessfully"""
                    self.log('INFO', logtxt)
                    return 'DONE'
                else:
                    logtxt = f"""USER {info[1]} want logged in twice at same time"""
                    self.log('ERR', logtxt)
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
        elif info[0] == 'logout':
            clients.remove(info[1])
            return "DONE"
        elif info[0] == 'send-message':
            self.send_message(info[1:])
        elif info[0] == 'get-messages':
            pass
            # TODO : GET MESSAGES
        elif info[0] == 'friend-request':
            pass
            # TODO : FRIEND-REQUEST
        # TODO : OTHER COMMANDS
        # TODO : LOGGING
        return 'ERROR'
