def parse(data_received: str):
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