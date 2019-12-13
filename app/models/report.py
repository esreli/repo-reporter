from .insight import Insight

class Report(object):

    def __init__(self, groups, start, end, title):
        self.groups = groups
        self.start = start
        self.end = end
        self.title = platform
        self.view_count_sum = sum(group.view_count for group in self.groups)
        self.view_uniques_sum = sum(group.view_uniques for group in self.groups)
        self.clone_count_sum = sum(group.clone_count for group in self.groups)
        self.clone_uniques_sum = sum(group.clone_uniques for group in self.groups)
        # TODO: Consider Build Referrers for full report
        # https://docs.mongodb.com/manual/reference/operator/query/or/

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

    def get_report_title(self):
        return self.title
