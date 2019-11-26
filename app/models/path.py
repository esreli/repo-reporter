
class Path(object):

    def __init__(self, path, title, count, uniques):
        self.path = path
        self.title = title
        self.count = round(count+0.5)
        self.uniques = round(uniques+0.5)

    def __repr__(self):
        return "Path({0} - c: {1}, u: {2})".format(self.path, self.count, self.uniques)

    def url(self, base="https://github.com"):
        return "{0}{1}".format(base, self.path)

    def path_truncated(self, limit=62):
        return ('...' + self.path[-limit:]) if len(self.path) > limit else self.path
