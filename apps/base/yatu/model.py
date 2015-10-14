
class ShortUrl:

    visited_counter = 0

    def __init__(self, sid, url, user=None, visited_counter=0):
        self.sid = sid
        self.url = url
        self.visited_counter = visited_counter
        self.user = user

    def increase_visits(self):
        self.visited_counter = ShortUrl.visited_counter + 1


class User:

    def __init__(self, username):
        self.username = username

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.username == other.username
        )


class AccessToken:

    def __init__(self, token):
        self.token = token
