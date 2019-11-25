class Repo(object):

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
