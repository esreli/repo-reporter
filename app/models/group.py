from .insight import Insight

class Group(object):

    @staticmethod
    def group_repos(repos, filter, start, end):
        # 0. Check if grouping is needed
        if filter.attribute is None: return [Group(repos, filter.display, start, end)]
        # 1. Divide by attribte
        grouped = {}
        for repo in repos:
            value = getattr(repo, filter.attribute)
            if value in grouped:
                grouped[value] += [repo]
            else:
                grouped[value] = [repo]
        # 2. Build groups
        return [Group(v, k, start, end) for (k, v) in grouped.items()]

    def __init__(self, repos, title, start, end):
        self.insights = []
        self.start = start
        self.end = end
        self.title = title
        self.insights  = [Insight(repo, self.start, self.end) for repo in repos]
        self.view_count_sum = sum(insight.view_count for insight in self.insights)
        self.view_uniques_sum = sum(insight.view_uniques for insight in self.insights)
        self.clone_count_sum = sum(insight.clone_count for insight in self.insights)
        self.clone_uniques_sum = sum(insight.clone_uniques for insight in self.insights)

    def __repr__(self):
        return "Group({0} - ({1}) repos)".format(self.title, len(self.insights))
