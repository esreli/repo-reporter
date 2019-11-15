# Flask
from flask import Flask
app = Flask(__name__)

# Config
import os
app.config['GITHUB_PERSONAL_ACCESS_TOKEN'] = os.getenv('GITHUB_PERSONAL_ACCESS_TOKEN')

from app.config import ProductionConfig, DevelopmentConfig

# Specify the proper configuration
if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object(ProductionConfig())
else:
    app.config.from_object(DevelopmentConfig())

# MongoDB
from pymongo import MongoClient
m = MongoClient()
db_name = app.config['DATABASE_NAME']
db = m[db_name]
print(" * Using database: {0}".format(db_name))

# Routes
from app import routes

# Report Generate
from app import generate

# Scheduler
import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from app import crawler

scheduler = BackgroundScheduler()
scheduler.add_job(func=crawler.crawl, trigger="interval", hours=1)

# Start App
if __name__ == "__main__":
    # TODO: enforce required config keys (github personal access token)

    # Start crawler scheduler
    scheduler.start()

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())

    # Finally, run app
    app.run(use_reloader=False)
