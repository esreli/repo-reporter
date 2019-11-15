from flask import request, abort, redirect, url_for, render_template
from app import app, crawler, generate
from datetime import datetime, timedelta
from pytablewriter import MarkdownTableWriter, HtmlTableWriter

def __to_date(dateString):
    d = datetime.strptime(dateString, "%Y-%m-%d").date()
    t = datetime.min.time()
    return datetime.combine(d, t)

def __to_string(date):
    return "{0}-{1}-{2}".format(date.year, date.month, date.day)

@app.route('/')
@app.route('/index')
def index():
    days = request.args.get('days', default=14, type=int)
    _start = datetime.now() - timedelta(days=days)
    default_start = datetime(year=_start.year, month=_start.month, day=_start.day)
    start = request.args.get('start', default=default_start, type=__to_date)
    report = generate.generate(start, start + timedelta(days=days))

    f = request.args.get('f', default = 'html', type = str)
    if f == "html":
        writer = HtmlTableWriter()
    elif f == "md":
        writer = MarkdownTableWriter()
    else:
        abort(400)

    writer.headers = report[0]
    writer.value_matrix = report[1]

    if f == "html":
        return render_template("report.html", writer=writer, start=__to_string(start), days=days)
    else:
        return writer.dumps()

@app.route('/crawl')
def perform_crawl():
    print("will perform crawl")
    crawler.crawl()
    return redirect(url_for('index'))
