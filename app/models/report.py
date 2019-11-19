from .insight import Insight

class Report(object):

    def __init__(self, repos, start, end):
        self.insights = []
        self.start = start
        self.end = end
        self.insights  = [Insight(repo, self.start, self.end) for repo in repos]

    def __repr__(self):
        return "Report({0} Insight)".format(len(self.insights))

    def date_range(self):
        formatted = lambda date: "{0}/{1}/{2}".format(date.month, date.day, date.year)
        return "{0} - {1}".format(formatted(self.start), formatted(self.end))

    @staticmethod
    def __to_string(date):
        return "{0}-{1}-{2}".format(format(date.year, "04"), format(date.month, "02"), format(date.day, "02"))

    def start_formatted(self):
        return Report.__to_string(self.start)

    def end_formatted(self):
        return Report.__to_string(self.end)
