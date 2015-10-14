
class ShortUrl:

    visited_counter = 0

    def __init__(self, sid, url, visited_counter=0):
        self.sid = sid
        self.url = url
        self.visited_counter = visited_counter

    def increase_visits(self):
        self.visited_counter = ShortUrl.visited_counter + 1


class User:

    def __init__(self, username):
        self.username = username


class AccessToken:

    def __init__(self, token):
        self.token = token
