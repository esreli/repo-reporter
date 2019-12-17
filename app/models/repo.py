from app import static
from slugify import slugify
from .insight import Insight

class Repo(object):

    __all = None

    @staticmethod
    def filterable_attributes():
        return [Filter("family_name", "Family"), Filter("platform", "Platform")]

    @staticmethod
    def all(sorted=True):
        if Repo.__all is None:
            repos = [Repo(**repo) for repo in static.collection()["collection-repos"]]
            if sorted: repos.sort(key=lambda repo: repo.full_name())
            Repo.__all = repos
        return Repo.__all

    @staticmethod
    def all_crawler():
        return [repo for repo in Repo.all() if repo.crawl == True]

    @staticmethod
    def all_display():
        return [repo for repo in Repo.all() if repo.display == True]

    @staticmethod
    def from_slug(app_full_name):
        try: return next(repo for repo in Repo.all() if app_full_name == repo.slugged_full_name())
        except: return None

    def __init__(self, family_name, platform, repo, crawl, display, **kwargs):
        self.family_name = family_name
        self.platform = platform
        self.repo = repo
        self.crawl = crawl
        self.display = display

    def __repr__(self):
        return "Repo({0})".format(self.repo)

    def full_name(self):
        return "{0} {1}".format(self.family_name, self.platform)

    def url(self, base="https://github.com/"):
        return "{0}{1}".format(base, self.repo)

    def slugged_full_name(self):
        return slugify(self.full_name())

class Filter(object):

    def __init__(self, attribute, display):
        self.attribute = attribute
        self.display = display

class Group(object):

    @staticmethod
    def group_repos(repos, filter, start, end):
        # 0. Check if grouping is needed
        if filter.attribute is None: return [Group(repos, filter.display, start, end)]
        # 1. Divide by attribte
        grouped = {}
        for repo in repos:
            print(type(repo), type(filter))
            value = getattr(repo, filter.attribute)
            if value in grouped:
                grouped[value] += [repo]
            else:
                grouped[value] = [repo]
        # 2. Build groups
        return [Group(v, filter.display, start, end) for (k, v) in grouped.items()]

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
