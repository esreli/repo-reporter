from app import app, db, static
from github import Github
from datetime import datetime, date

def crawl():
    # Timestamp
    today = date.today()
    timestamp = datetime(year=today.year, month=today.month, day=today.day)

    print("[Crawler] starting crawl {0}".format(datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))
    # Get Github Access Token from Environment
    pat = app.config['GITHUB_PERSONAL_ACCESS_TOKEN']
    assert(pat is not None), "[Crawler: Error] missing environment GITHUB_PERSONAL_ACCESS_TOKEN. Ending crawl."

    # Build Github Client
    g = Github(pat)

    # Grab static repos
    families = static.repos()["families"]

    # Iterate through app families
    for family in families:
        family_name = family["name"]
        platforms = family["platforms"]
        for platform in platforms:
            # Name
            platform_name = platform["platform"]
            name = "{0} {1}".format(family_name, platform_name)

            # Repo
            platform_repo = platform["repo"]
            repo = g.get_repo(platform_repo)

            # Views
            views = repo.get_views_traffic()
            for view in views["views"]:
                k = { "timestamp": view.timestamp, "repo": platform_repo }
                v = { "timestamp": view.timestamp, "repo": platform_repo, "count": view.count, "uniques": view.uniques }
                v_id = db.view.update_one(k, {"$set": v}, upsert=True)

            # Clones
            clones = repo.get_clones_traffic()
            for clone in clones["clones"]:
                k = { "timestamp": clone.timestamp, "repo": platform_repo }
                c = { "timestamp": clone.timestamp, "repo": platform_repo, "count": clone.count, "uniques": clone.uniques }
                c_id = db.clone.update_one(k, {"$set": c}, upsert=True)

            # Paths
            paths = repo.get_top_paths()
            for path in paths:
                count = float(path.count) / 14.0
                uniques = float(path.uniques) / 14.0
                k = { "timestamp": timestamp, "repo": platform_repo, "path": path.path }
                p = { "timestamp": timestamp, "repo": platform_repo, "count": count, "uniques": uniques, "path": path.path, "title": path.title }
                p_id = db.path.update_one(k, {"$set": p}, upsert=True)

            # Referrer
            referrers = repo.get_top_referrers()
            for referrer in referrers:
                count = float(referrer.count) / 14.0
                uniques = float(referrer.uniques) / 14.0
                k = { "timestamp": timestamp, "repo": platform_repo, "referrer": referrer.referrer }
                r = { "timestamp": timestamp, "repo": platform_repo, "count": count, "uniques": uniques, "referrer": referrer.referrer }
                r_id = db.referrer.update_one(k, {"$set": r}, upsert=True)

    print("[Crawler] finished crawl")
