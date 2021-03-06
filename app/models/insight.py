from datetime import datetime, timedelta
from app import db
from .referrer import Referrer
from .path import Path
from json import dumps


class Insight(object):

    def __init__(self, repo, start, end):
        self.repo = repo
        self.start = start
        self.end = end

        match = {'$match': {'repo': self.repo.repo, 'timestamp': {'$gte': start, '$lte': end}}}

        # Views & Clones
        agr = [match, {'$group': {'_id': 1, 'count': {'$sum': '$count'}, 'uniques': {'$sum': '$uniques'}}}]

        # Views
        view = list(db.view.aggregate(agr))
        self.view_count = Insight.__get_value(view, 'count') or 0
        self.view_uniques = Insight.__get_value(view, 'uniques') or 0

        # Clones
        clone = list(db.clone.aggregate(agr))
        self.clone_count = Insight.__get_value(clone, 'count') or 0
        self.clone_uniques = Insight.__get_value(clone, 'uniques') or 0

        # Referrers
        agr = [match, {'$group': {'_id': '$referrer', 'count': {'$sum': '$count'}, 'uniques': {'$sum': '$uniques'}}}, {'$sort': {'count': -1}}, {'$limit': 10}]
        referrers = list(db.referrer.aggregate(agr))
        self.referrers = [ Referrer(ref["_id"], ref["count"], ref["uniques"]) for ref in referrers ]

        # Paths
        agr = [match, {'$group': {'_id': '$path', 'title': {'$first': '$title'}, 'count': {'$sum': '$count'}, 'uniques': {'$sum': '$uniques'}}}, {'$sort': {'count': -1}}, {'$limit': 10}]
        paths = list(db.path.aggregate(agr))
        self.paths = [ Path(path["_id"], path["title"], path["count"], path["uniques"]) for path in paths]

        # Date Range
        dates = [ start + timedelta(days=d) for d in range((end - start).days + 1)]

        # Views and uniques
        self.views = []
        self.uniques = []

        for date in dates:
            fDate = "{0}-{1}-{2}".format(date.month, date.day, date.year)
            record = db.view.find_one({'repo': self.repo.repo, 'timestamp': {'$gte': date, '$lte': date}})
            if record is None:
                self.views.append((fDate, 0))
                self.uniques.append((fDate, 0))
            else:
                self.views.append((fDate, record["count"]))
                self.uniques.append((fDate, record["uniques"]))


    def __repr__(self):
        return 'Insight({0})'.format(self.repo.repo)

    @staticmethod
    def __get_value(values, key):
        try: return values[0][key]
        except (IndexError, KeyError) as e: return None

    @staticmethod
    def __to_string(date):
        return "{0}-{1}-{2}".format(format(date.year, "04"), format(date.month, "02"), format(date.day, "02"))

    def date_range(self):
        formatted = lambda date: "{0}/{1}/{2}".format(date.month, date.day, date.year)
        return "{0} - {1}".format(formatted(self.start), formatted(self.end))

    def start_formatted(self):
        return Insight.__to_string(self.start)

    def end_formatted(self):
        return Insight.__to_string(self.end)
