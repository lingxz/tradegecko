import os

# Logging configurations
LOG_FILE_MAX_SIZE = 256
APP_LOG_NAME = 'app.log'
WERKZEUG_LOG_NAME = 'werkzeug.log'

# DB configurations
MONGO_DBNAME = 'tradegecko'
MONGO_HOST = os.environ.get('MONGO_HOST') or 'localhost'
MONGO_PORT = 27017