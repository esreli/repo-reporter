from flask import request, abort, redirect, url_for, render_template
from app import app, crawler, static
from app.models import Repo, Report
from datetime import datetime, timedelta

def __to_date(dateString):
    d = datetime.strptime(dateString, "%Y-%m-%d").date()
    t = datetime.min.time()
    return datetime.combine(d, t)

@app.route('/')
@app.route('/index')
def index():
    # Gather start, end dates
    end = request.args.get('end', default=datetime.now(), type=__to_date)
    start = request.args.get('start', default=end-timedelta(days=14), type=__to_date)
    # Gather filters
    platform = request.args.get('platform', default="all")
    name = request.args.get('name', default="all")
    # Build Repo Models
    repos = Repo.from_yaml(static.repos())
    # Filter Repos by platform
    if platform is not "all":
        repos = [repo for repo in repos if repo.platform == platform]
    # Filter Repos by name
    if name is not "all":
        repos = [repo for repo in repos if repo.family_name == name]
    # Generate Report
    report = Report(repos, start, end)

    return render_template("report.html", report=report)

@app.route('/crawl')
def perform_crawl():
    # Crawl first
    crawler.crawl()
    # Then redirect with latest data
    return redirect(url_for('index'))
