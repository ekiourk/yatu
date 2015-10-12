
class ShortUrl:

    visited_counter = 0

    def __init__(self, sid, url, visited_counter=0):
        self.sid = sid
        self.url = url
        self.visited_counter = visited_counter

    def increase_visits(self):
        self.visited_counter = ShortUrl.visited_counter + 1