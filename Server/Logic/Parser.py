from Server.Logic.DatabaseConnection import *
import datetime
from Utils.datetimes import *

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
        WHERE sepehr.users.ID = '{username}' and deleted = 0
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
        if len(data) == 0:
            return "EMPTY"
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
            return "EMPTY"
        return self.create_string(friends)

    def send_message(self, data):
        _time_ = _time_ = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message_id = f'{data[1]}X{data[2]}X{_time_}'
        print(message_id)
        q1 = f"""
        INSERT INTO sepehr.messages(ID, TEXT, sentTIME) VALUE 
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
        self.log('INFO', logtxt)

    def create_messages_string(self, tuples):
        if len(tuples) == 0:
            return "EMPTY"
        res = ''
        i = 1
        for x in tuples:
            txt = x[0]
            s = x[1]
            id = x[2]
            res = res + f'{id}//{txt}//{s}***'
        print(res)
        return res

    def get_messages(self, data):
        q1 = f"""
        SELECT TEXT,USER_ID_SENDER,MESSAGE_ID
        FROM sepehr.messages AS M , sepehr.sender_reciver_messages AS SRM
        WHERE M.ID = SRM.MESSAGE_ID 
        AND USER_ID_SENDER = '{data[0]}' AND USER_ID_RECIVER = '{data[1]}'
        ORDER BY ASC sentTIME
        UNION 
        SELECT TEXT,USER_ID_SENDER,MESSAGE_ID
        FROM sepehr.messages AS M , sepehr.sender_reciver_messages AS SRM
        WHERE M.ID = SRM.MESSAGE_ID 
        AND USER_ID_SENDER = '{data[1]}' AND USER_ID_RECIVER = '{data[0]}'
        ORDER BY ASC sentTIME
        """
        messages = self.dbc.execute_query(q1)
        return self.create_messages_string(messages)

    def check_username(self, username):
        q = f"""
        SELECT ID FROM sepehr.users WHERE ID = '{username}'
        """
        return len(self.dbc.execute_query(q)) != 0

    def is_blocked(self, user_source, user_target):
        q = f"""
        SELECT count(*) FROM
        sepehr.blocks WHERE USER_ID_BLOCKER = '{user_target}' AND USER_ID_BLOCKED = '{user_source}'
        """
        r = self.dbc.execute_query(q)
        return r[0][0] != 0

    def add_friend(self, data):
        if self.check_username(data[1]):
            if self.is_blocked(data[0], data[1]):
                return "ERROR"
            elif self.is_blocked(data[1], data[0]):
                self.unblock([data[1], data[0]])
            q1 = f"""
            INSERT INTO sepehr.pending_friend_requests(USER_ID_SENDER, USER_ID_RECIVER) VALUE ('{data[0]}','{data[1]}')
            """
            self.dbc.execute_query(q1, mode=1)
            return "DONE"
        else:
            return "ERROR"

    def friend_requests(self, data):
        q = f"""
        SELECT USER_ID_SENDER FROM sepehr.pending_friend_requests
        WHERE USER_ID_RECIVER = '{data}' AND IS_ACCEPTED = 0
        """
        requests = self.dbc.execute_query(q)
        res = self.create_string(requests)
        return res

    def accept_request(self, data):
        print(data)
        q1 = f"""
        UPDATE sepehr.pending_friend_requests
        SET IS_ACCEPTED = 1
        WHERE USER_ID_RECIVER = '{data[0]}' AND USER_ID_SENDER = '{data[1]}' AND IS_ACCEPTED = 0
        """
        print(self.dbc.execute_query(q1, mode=1))
        q2 = f"""
        INSERT INTO sepehr.friends(USER_ID1, USER_ID2) VALUE 
        ('{data[1]}','{data[0]}')
        """
        print(self.dbc.execute_query(q2, mode=1))
        return "OK"

    def reject_request(self, data):
        q1 = f"""
                UPDATE sepehr.pending_friend_requests
                SET IS_ACCEPTED = -1
                WHERE USER_ID_RECIVER = '{data[0]}' AND USER_ID_SENDER = '{data[1]}'
                """
        print(self.dbc.execute_query(q1, mode=1))
        return "OK"

    def remove_friend(self, data):
        q = f"""
        DELETE FROM sepehr.friends
        WHERE (USER_ID1 = '{data[0]}' and USER_ID2 = '{data[1]}') OR (USER_ID1 = '{data[1]}' and USER_ID2 = '{data[0]}')
        """
        self.dbc.execute_query(q, mode=1)
        return "OK"

    def block(self, data):
        q = f"""
        INSERT INTO sepehr.blocks(USER_ID_BLOCKER, USER_ID_BLOCKED) VALUE 
        ('{data[0]}','{data[1]}')
        """
        self.dbc.execute_query(q, mode=1)
        friends = self.dbc.execute_query(f"""
                SELECT sepehr.friends.USER_ID1 FROM sepehr.friends
                WHERE sepehr.friends.USER_ID2 = '{data[0]}'
                UNION 
                SELECT sepehr.friends.USER_ID2 FROM sepehr.friends
                WHERE sepehr.friends.USER_ID1 = '{data[0]}'
                """)
        ff = self.create_string(friends).split('//')
        if ff.__contains__(data[1]):
            self.remove_friend(data)
        logtxt = f"""USER {data[0]} BLOCKED {data[1]}"""
        self.log('INFO', logtxt)
        return "OK"

    def security_q_a(self, username):
        q = f"""
        SELECT Question, Answer
        FROM sepehr.security_questions
        WHERE USER_ID = '{username}'
        """
        r = self.dbc.execute_query(q)
        if len(q) == 0:
            return "ERROR"
        return self.create_string(r)

    def change_password(self, data):
        q = f"""
        UPDATE sepehr.passwords
        SET Encrypted_Password = '{data[1]}'
        WHERE USER_ID = '{data[0]}'
        """
        self.dbc.execute_query(q, mode=1)
        logtxt = f"""USER {data[0]} CHANGED PASSWORD"""
        self.log('INFO', logtxt)
        return 'OK'

    def like(self, data):
        q = f"""
        INSERT INTO sepehr.likes(MESSAGE_ID, USER_ID_LIKER)  VALUE 
        ('{data[1]}','{data[0]}')
        """
        self.dbc.execute_query(q, mode=1)
        return 'OK'

    def delete_account(self, username):
        q = f"""
        UPDATE sepehr.users 
        SET deleted = 1
        WHERE ID = '{username}'
        """
        self.dbc.execute_query(q, mode=1)
        logtxt = f""" USER {username} DELETED"""
        self.log('INFO', logtxt)
        return 'OK'

    def unblock(self, data):
        q = f"""
        DELETE FROM sepehr.blocks
        WHERE USER_ID_BLOCKER = '{data[0]}' AND USER_ID_BLOCKED = '{data[1]}'
        """
        self.dbc.execute_query(q, mode=1)
        return 'OK'

    def get_password(self, username):
        q = f"""
        SELECT ENCRYPTED_PASSWORD FROM sepehr.passwords
        WHERE USER_ID = '{username}' 
        """
        r = self.dbc.execute_query(q)
        if len(r) == 0:
            return "ERROR"
        return r[0][0]

    def check_penalty_pw(self, username):
        q = f"""
        SELECT ENDTIME FROM sepehr.penalties
        WHERE USER_ID = '{username}' AND ATTEMPED_FOR = 1
        """
        r = self.dbc.execute_query(q)
        if len(r) == 0:
            return 'OK'
        else:
            if create_date(r[0][0]) < datetime.datetime.now():
                return 'OK'
            else:
                return "ERROR"

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
            return self.get_messages(info[1:])
        elif info[0] == 'add-friend':
            return self.add_friend(info[1:])
        elif info[0] == 'friend-requests':
            return self.friend_requests(info[1])
        elif info[0] == 'accept':
            return self.accept_request(info[1:])
        elif info[0] == 'reject':
            return self.reject_request(info[1:])
        elif info[0] == 'remove-friend':
            return self.remove_friend(info[1:])
        elif info[0] == 'block':
            return self.block(info[1:])
        elif info[0] == 'security':
            return self.security_q_a(info[1])
        elif info[0] == 'change-password':
            return self.change_password(info[1:])
        elif info[0] == 'like':
            return self.like(info[1:])
        elif info[0] == 'delete-account':
            return self.delete_account(info[1])
        elif info[0] == 'unblock':
            return self.unblock(info[1:])
        elif info[0] == 'get-password':
            return self.get_password(info[1])
        elif info[0] == 'check-penalty-pw':
            return self.check_penalty_pw(info[1])
        return 'ERROR'
