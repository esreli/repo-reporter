from .insight import Insight

class Report(object):

    def __init__(self, repos, start, end, platform, name):
        self.insights = []
        self.start = start
        self.end = end
        self.platform = platform
        self.name = name
        self.insights  = [Insight(repo, self.start, self.end) for repo in repos]
        self.view_count_sum = sum(insight.view_count for insight in self.insights)
        self.view_uniques_sum = sum(insight.view_uniques for insight in self.insights)
        self.clone_count_sum = sum(insight.clone_count for insight in self.insights)
        self.clone_uniques_sum = sum(insight.clone_uniques for insight in self.insights)
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
        name = self.name if self.name != "All" else "All repos"
        platform = self.platform if self.platform != "All" else "all platforms"
        return "{0} {1}".format(name, platform)
