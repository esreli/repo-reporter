class Repo(object):

    @staticmethod
    def from_yaml(yaml_stream):
        repos = []
        for family in yaml_stream["families"]:
            family_name = family["name"]
            platforms = family["platforms"]
            for platform in platforms:
                platform_name = platform["platform"]
                platform_repo = platform["repo"]
                repo = Repo(family_name, platform_name, platform_repo)
                repos.append(repo)
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
