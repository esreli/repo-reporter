class Config(object):
    DEBUG = False
    TESTING = False

class ProductionConfig(Config):
    DATABASE_NAME = 'repo-reporter-prod'

class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_NAME = 'repo-reporter-dev'
