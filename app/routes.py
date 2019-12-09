from flask import request, abort, request, redirect, url_for, render_template, flash, make_response
from app import app, crawler, static
from app.models import Repo, Report, Collection, Insight
from datetime import datetime, timedelta
from json import dumps

def __to_date(dateString):
    if dateString is None: return None
    d = datetime.strptime(dateString, "%Y-%m-%d").date()
    t = datetime.min.time()
    return datetime.combine(d, t)

def __to_string(date):
    if date is None: return None
    return "{0}-{1}-{2}".format(date.year, date.month, date.day)

def __strip_time(date):
    if date is None: return None
    return datetime(date.year, date.month, date.day)

def __build_dates_from_request(request):
    # Build default start, end dates
    if request.args.get('d', default=False, type=bool):
        default_end = __to_date(request.cookies.get('rr-end')) or datetime.now()
        default_start = __to_date(request.cookies.get('rr-start')) or default_end-timedelta(days=14)
    else:
        default_end = datetime.now()
        default_start = default_end-timedelta(days=14)
    # Gather start, end dates
    end = request.args.get('end', default=__strip_time(default_end), type=__to_date)
    start = request.args.get('start', default=__strip_time(default_start), type=__to_date)
    # Return dates
    return (start, end)

def __build_response_with_dates_cookies(rendered, code, start, end):
    # Build response with render
    resp = make_response(rendered, code)
    # Set start and end cookies
    resp.set_cookie('rr-end', __to_string(end), max_age=60*60*24*365*2)
    resp.set_cookie('rr-start', __to_string(start), max_age=60*60*24*365*2)
    return resp

@app.context_processor
def inject_collection():
    return dict(collection_name=Collection.name(), collection_accent=Collection.accent_color(), dumps=dumps)

@app.route('/')
@app.route('/index')
def index():
    # Build start and end dates
    (start, end) = __build_dates_from_request(request)
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
    # Render from template
    rendered = render_template("report.html", report=report, platforms=platforms, names=names)
    # Build response
    return __build_response_with_dates_cookies(rendered, 200, start, end)

@app.route('/<app_full_name>')
def repo_report(app_full_name):
    # Build start and end dates
    (start, end) = __build_dates_from_request(request)
    # Build Repo model
    repo = Repo.from_slug(app_full_name)
    # Check URL is valid
    if repo is None:
        flash('No project matches that URL.')
        return redirect(url_for('index'))
    # Build Insight model
    insight = Insight(repo, start, end)
    # Render page
    rendered = render_template("insight.html", insight=insight)
    # Build response
    return __build_response_with_dates_cookies(rendered, 200, start, end)

@app.route('/crawl')
def perform_crawl():
    # Crawl first
    try:
        crawler.crawl()
    except Exception as e:
        flash('Error crawling Github.\n{0}'.format(e))
    # Then redirect with latest data
    return redirect(url_for('index'))
