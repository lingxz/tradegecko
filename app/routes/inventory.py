import os
import json
from app import utils
from flask import Blueprint, render_template, request
from app import constants

inventory = Blueprint('inventory', __name__)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in constants.ALLOWED_EXTENSIONS

@inventory.route('/')
def home():
    return render_template('index.html')

@inventory.route('/upload_file', methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        message = 'No file part'
        abort(400)
    file = request.files['file']
    if file.filename == '':
        message = 'No selected file'
        abort(400)
    if file and allowed_file(file.filename):
        file.save(constants.DATA_FILE)
    utils.process_csv(infile=constants.DATA_FILE)
    return json.dumps({'success': True}), 200, {'ContentType':'application/json'}

@inventory.route('/item')
def get_prev_state():
    object_type = request.args.get('object_type', type=str)
    object_id = request.args.get('object_id', type=int)
    timestamp = request.args.get('timestamp', type=int)
    current_state = utils.get_past_state(object_type, object_id, timestamp)
    return json.dumps(current_state)