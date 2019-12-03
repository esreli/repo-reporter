from app import app, db, static, gh_client
from app.models import Repo
from datetime import datetime, date

def crawl():
    # Timestamp
    today = date.today()
    timestamp = datetime(year=today.year, month=today.month, day=today.day)

    print("[Crawler] starting crawl {0}".format(datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))

    # Grab static repos
    repos = Repo.from_yaml(static.repos())

    try:
        for repo in repos:
            # Get Github Repo
            gh_repo = gh_client.get_repo(repo.repo)

            # Views
            views = gh_repo.get_views_traffic()
            for view in views["views"]:
                k = { "timestamp": view.timestamp, "repo": repo.repo }
                v = { "timestamp": view.timestamp, "repo": repo.repo, "count": view.count, "uniques": view.uniques }
                v_id = db.view.update_one(k, {"$set": v}, upsert=True)

            # Clones
            clones = gh_repo.get_clones_traffic()
            for clone in clones["clones"]:
                k = { "timestamp": clone.timestamp, "repo": repo.repo }
                c = { "timestamp": clone.timestamp, "repo": repo.repo, "count": clone.count, "uniques": clone.uniques }
                c_id = db.clone.update_one(k, {"$set": c}, upsert=True)

            # Paths
            paths = gh_repo.get_top_paths()
            for path in paths:
                count = float(path.count) / 14.0
                uniques = float(path.uniques) / 14.0
                k = { "timestamp": timestamp, "repo": repo.repo, "path": path.path }
                p = { "timestamp": timestamp, "repo": repo.repo, "count": count, "uniques": uniques, "path": path.path, "title": path.title }
                p_id = db.path.update_one(k, {"$set": p}, upsert=True)

            # Referrer
            referrers = gh_repo.get_top_referrers()
            for referrer in referrers:
                count = float(referrer.count) / 14.0
                uniques = float(referrer.uniques) / 14.0
                k = { "timestamp": timestamp, "repo": repo.repo, "referrer": referrer.referrer }
                r = { "timestamp": timestamp, "repo": repo.repo, "count": count, "uniques": uniques, "referrer": referrer.referrer }
                r_id = db.referrer.update_one(k, {"$set": r}, upsert=True)

        print("[Crawler] finished crawl")

    except Exception as e:
        print(e)
        print("[Crawler] failed crawl")
        raise e
