def encrypt(password):
    result = ''
    s = len(password) % 100
    for i in range(len(password)):
        result += chr(ord(password[i]) + s)

    return result


def decrypt(encrypted):
    result = ''
    s = len(encrypted) % 100
    for i in range(len(encrypted)):
        result += chr(ord(encrypted[i]) - s)

    return result
