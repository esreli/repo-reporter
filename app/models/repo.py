from app import static
from slugify import slugify

class Repo(object):

    @staticmethod
    def all():
        return Repo.from_yaml(static.repos())

    @staticmethod
    def from_slug(app_full_name):
        for repo in Repo.all():
            if app_full_name == repo.slugged_full_name():
                return repo
        return None

    @staticmethod
    def from_yaml(yaml_stream, sorted=True):
        repos = [Repo(repo["name"], repo["platform"], repo["repo"]) for repo in yaml_stream["repos"]]
        if sorted:
            repos.sort(key=lambda repo: repo.full_name())
        return repos

    def __init__(self, family_name, platform, repo):
        self.family_name = family_name
        self.platform = platform
        self.repo = repo

    def __repr__(self):
        return "Repo({0}, {1})".format(self.repo, self.full_name())

    def full_name(self):
        return "{0} {1}".format(self.family_name, self.platform)

    def url(self, base="https://github.com/"):
        return "{0}{1}".format(base, self.repo)

    def slugged_full_name(self):
        return slugify(self.full_name())
