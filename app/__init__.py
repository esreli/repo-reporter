# Flask
from flask import Flask
app = Flask(__name__)

# Config
import os
from app.config import ProductionConfig, DevelopmentConfig
## Github Auth
app.config['GITHUB_PERSONAL_ACCESS_TOKEN'] = os.getenv('GITHUB_PERSONAL_ACCESS_TOKEN')
## Env Config
if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object(ProductionConfig())
else:
    app.config.from_object(DevelopmentConfig())

# Get Github Access Token from Environment
pat = app.config['GITHUB_PERSONAL_ACCESS_TOKEN']
assert(pat is not None), "[Crawler: Error] missing environment GITHUB_PERSONAL_ACCESS_TOKEN. Ending crawl."

# Github
from github import Github
gh_client = Github(pat)

# MongoDB
from pymongo import MongoClient
m = MongoClient()
db_name = app.config['DATABASE_NAME']
db = m[db_name]
print(" * Using database: {0}".format(db_name))

# Routes
from app import routes

# Scheduler
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from app import crawler

scheduler = BackgroundScheduler()
scheduler.add_job(func=crawler.crawl, trigger="interval", hours=1)

# Start crawler scheduler
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

# Start App
if __name__ == "__main__":
    # TODO: enforce required config keys (github personal access token)
    # Finally, run app
    app.run(use_reloader=False, debug=False)
