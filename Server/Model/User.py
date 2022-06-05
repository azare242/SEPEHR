from Sets import *

class User:
    def __init__(self, username, fname, lname, phone, email):
        self.username = username
        self.fname = fname
        self.lname = lname
        self.phone = phone
        self.email = email
        self.friends = FriendsSet() # TODO : INITIAL FRIENDS WITH DATABASE

