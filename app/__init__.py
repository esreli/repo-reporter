# Flask
from flask import Flask, session
app = Flask(__name__)

# Config
import os
from app.config import ProductionConfig, DevelopmentConfig
## Secret Key
app.secret_key = os.getenv('RR_SECRET_KEY')
## Github Auth
app.config['GITHUB_PERSONAL_ACCESS_TOKEN'] = os.getenv('GITHUB_PERSONAL_ACCESS_TOKEN')
## Env Config
if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object(ProductionConfig())
else:
    app.config.from_object(DevelopmentConfig())

## Mongo Environment
## assume it is localhost if not explicitely set
## same goes for the port, assume 27017
m_host = os.getenv('MONGO_HOST') 
if m_host is None:
    m_host = 'localhost'

m_port = os.getenv('MONGO_PORT')
if m_port is None:
    m_port = 27017
else:
    m_port = int(m_port)

# Get Github Access Token from Environment
pat = app.config['GITHUB_PERSONAL_ACCESS_TOKEN']
assert(pat is not None), "[Crawler: Error] missing environment GITHUB_PERSONAL_ACCESS_TOKEN. Ending crawl."

# Github
from github import Github
gh_client = Github(pat)

# MongoDB
from pymongo import MongoClient
m = MongoClient(host=m_host, port=m_port)
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
