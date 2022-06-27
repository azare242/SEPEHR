from Client.Model.Connection import *


def disconnect(connection: Connection):
    connection.send('exit')
    connection.close()