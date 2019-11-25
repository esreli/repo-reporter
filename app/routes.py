from flask import request, abort, redirect, url_for, render_template
from app import app, crawler, static
from app.models import Repo, Report
from datetime import datetime, timedelta

def __to_date(dateString):
    d = datetime.strptime(dateString, "%Y-%m-%d").date()
    t = datetime.min.time()
    return datetime.combine(d, t)

def __strip_time(date):
    return datetime(date.year, date.month, date.day)

@app.route('/')
@app.route('/index')
def index():
    # Gather start, end dates
    end = request.args.get('end', default=__strip_time(datetime.now()), type=__to_date)
    start = request.args.get('start', default=__strip_time(end-timedelta(days=14)), type=__to_date)
    # Gather filters
    platform = request.args.get('platform', default="All")
    name = request.args.get('name', default="All")
    # Build Repo models
    repos = Repo.from_yaml(static.repos())
    # Build filters for UI
    platforms = ["All"] + list(set([repo.platform for repo in repos]))
    names = ["All"] + list(set([repo.family_name for repo in repos]))
    # Filter Repos by platform
    if platform != "All":
        repos = [repo for repo in repos if repo.platform == platform]
    # Filter Repos by name
    if name != "All":
        repos = [repo for repo in repos if repo.family_name == name]
    # Generate report
    report = Report(repos, start, end, platform, name)
    # Render page
    return render_template("report.html", report=report, platforms=platforms, names=names)

@app.route('/crawl')
def perform_crawl():
    # Crawl first
    crawler.crawl()
    # Then redirect with latest data
    return redirect(url_for('index'))
