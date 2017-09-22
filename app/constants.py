import os

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'csv'])
DATA_FILE = os.path.join(UPLOAD_FOLDER, 'data.csv')
OUTPUT_FILE = 'out.json'