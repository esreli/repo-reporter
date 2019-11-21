from app import db
from .referrer import Referrer

class Insight(object):

    def __init__(self, repo, start, end):
        self.repo = repo
        self.paths = []

        # DB Aggregate
        agr = [{'$match': {'repo': self.repo.repo, 'timestamp': {'$gte': start, '$lte': end}}}, {'$group': {'_id': 1, 'count': {'$sum': '$count'}, 'uniques': {'$sum': '$uniques'}}}]

        # Views
        view = list(db.view.aggregate(agr))
        self.view_count = Insight.__get_value(view, 'count') or 0
        self.view_uniques = Insight.__get_value(view, 'uniques') or 0

        # Clones
        clone = list(db.clone.aggregate(agr))
        self.clone_count = Insight.__get_value(clone, 'count') or 0
        self.clone_uniques = Insight.__get_value(clone, 'uniques') or 0

        # Paths
        # TODO

        # Referrers
        agr = [{'$match': {'repo': self.repo.repo, 'timestamp': {'$gte': start, '$lte': end}}}, {'$group': {'_id': '$referrer', 'count': {'$sum': '$count'}, 'uniques': {'$sum': '$uniques'}}}, {'$sort': {'count': -1}}]
        referrers = list(db.referrer.aggregate(agr))
        self.referrers = [ Referrer(ref["_id"], ref["count"], ref["uniques"]) for ref in referrers ]

    def __repr__(self):
        return 'Insight({0}- v: {1}, vu: {2}, c: {3}, cu: {4})'.format(self.repo.repo, self.view_count, self.view_uniques, self.clone_count, self.clone_uniques)

    @staticmethod
    def __get_value(values, key):
        try: return values[0][key]
        except (IndexError, KeyError) as e: return None
