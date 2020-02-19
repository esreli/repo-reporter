from app import db
from .insight import Insight
from datetime import datetime, timedelta
from json import dumps
from slugify import slugify

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

        dates = [ start + timedelta(days=d) for d in range((end - start).days + 1)]
        # Views and uniques
        self.views = []
        self.uniques = []
        # Iterate
        for date in dates:
            fDate = "{0}-{1}-{2}".format(date.month, date.day, date.year)
            match = {'$match': {'$or':  [{'repo': repo.repo, 'timestamp': {'$gte': date, '$lte': date}} for repo in repos]}}
            agr = [match, {'$group': {'_id': 1, 'count': {'$sum': '$count'}, 'uniques': {'$sum': '$uniques'}}}]
            record = list(db.view.aggregate(agr))
            self.views.append((fDate, Group.__get_value(record, 'count')))
            self.uniques.append((fDate, Group.__get_value(record, 'uniques')))

    def id(self):
        return slugify(self.title).replace("-", "_")

    def dump_dates(self, attribute):
        return dumps([value[0] for value in getattr(self, attribute)])

    def dump_values(self, attribute):
        return dumps([value[1] for value in getattr(self, attribute)])

    def __repr__(self):
        return "Group({0} - ({1}) repos)".format(self.title, len(self.insights))

    @staticmethod
    def __get_value(values, key):
        try: return values[0][key]
        except (IndexError, KeyError) as e: return 0
