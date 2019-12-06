from flask import request, abort, redirect, url_for, render_template, flash
from app import app, crawler, static
from app.models import Repo, Report, Collection, Insight
from datetime import datetime, timedelta
from json import dumps

def __to_date(dateString):
    d = datetime.strptime(dateString, "%Y-%m-%d").date()
    t = datetime.min.time()
    return datetime.combine(d, t)

def __strip_time(date):
    return datetime(date.year, date.month, date.day)

@app.context_processor
def inject_collection():
    return dict(collection_name=Collection.name(), collection_accent=Collection.accent_color(), dumps=dumps)

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
    repos = Repo.all_display()
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

@app.route('/<app_full_name>')
def repo_report(app_full_name):
    # Gather start, end dates
    end = request.args.get('end', default=__strip_time(datetime.now()), type=__to_date)
    start = request.args.get('start', default=__strip_time(end-timedelta(days=14)), type=__to_date)
    # Build Repo model
    repo = Repo.from_slug(app_full_name)
    # Build Insight model
    insight = Insight(repo, start, end)
    # Render page
    return render_template("insight.html", insight=insight)

@app.route('/crawl')
def perform_crawl():
    # Crawl first
    try:
        crawler.crawl()
    except Exception as e:
        flash('Error crawling Github.\n{0}'.format(e))
    # Then redirect with latest data
    return redirect(url_for('index'))
