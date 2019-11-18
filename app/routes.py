from flask import request, abort, redirect, url_for, render_template
from app import app, crawler, static
from app.models import Repo, Report

from datetime import datetime, timedelta
from pytablewriter import MarkdownTableWriter, HtmlTableWriter

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
    # Generate Repo Models
    repos = Repo.from_yaml(static.repos())
    report = Report(repos, start, end)

    return render_template("report.html", report=report)

@app.route('/crawl')
def perform_crawl():
    print("will perform crawl")
    crawler.crawl()
    return redirect(url_for('index'))
