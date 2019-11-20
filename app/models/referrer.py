
class Referrer(object):

    def __init__(self, referrer, count, uniques):
        self.referrer = referrer
        self.count = round(count+0.5)
        self.uniques = round(uniques+0.5)

    def __repr__(self):
        return "Referrer({0} - c: {1}, u: {2})".format(self.referrer, self.count, self.uniques)
