

class Friend:
    def __init__(self,username, fname, lname):
        self.username = username
        self.fname = fname
        self.lname = lname


class FriendsSet:

    def __init__(self):
        self.S = set()

    def add_friend(self, user: Friend):
        if not isinstance(user, Friend):
            return
        self.S.add(user)

    def remove_friend(self, user: Friend):
        if not isinstance(user, Friend):
            return
        self.S.remove(user)

    def search_by_username(self, username):
        f = None
        for friend in self.S:
            if friend.username == username:
                f = friend
        return f