import os

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'csv'])
DATA_FILE = os.path.join(UPLOAD_FOLDER, 'data.csv')
MONGO_HOST = os.environ.get('MONGO_HOST') or 'localhost'
MONGO_PORT = 27017
HEADERS = ['object_id', 'object_type', 'timestamp', 'object_changes']