import mysql.connector
from Utils import Properties, Passwords


class DatabaseConnection:
    def __init__(self):
        self.HOST = Properties.get('Server', 'HOST')
        self.DATABASE = Properties.get('Server', 'DATABASE')
        self.USER = Properties.get('Server', 'USER')
        self.PASSWORD = Passwords.decrypt(Properties.get('Server', 'RANDOM'))
        self.connection = mysql.connector.connect(host=self.HOST,
                                                  database=self.DATABASE,
                                                  user=self.USER,
                                                  password=self.PASSWORD)
        print("CONNECTED TO DATABASE")

    def execute_query(self, query: str, mode=0):
        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            response = None
            if mode == 0:
                response = cursor.fetchall()
            else:
                response = 'Done'
                cursor.commit()
        except mysql.connector.Error as err:
            print(err)
            response = 'ERROR'
            self.connection.rollback()
        finally:
            if cursor is not None:
                cursor.close()
        return response

    def close_connection(self):
        self.connection.close()

    def is_connected(self):
        return self.connection.is_connected()
