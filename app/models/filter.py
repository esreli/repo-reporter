
class Filter(object):

    @staticmethod
    def no_filter():
        return Filter(None, "All", "All repos")

    def __init__(self, attribute, display, title):
        self.attribute = attribute
        self.display = display
        self.title = title
