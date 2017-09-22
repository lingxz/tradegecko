import os
from flask import Flask, flash, request, redirect, url_for, render_template, abort
import json
import utils
import constants

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in constants.ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload_file', methods=["POST"])
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
    utils.process_csv(infile=constants.DATA_FILE, outfile=constants.OUTPUT_FILE)
    return json.dumps({'success': True}), 200, {'ContentType':'application/json'}


# run development server locally, uses uswgi on deployment
if __name__ == '__main__':
    app.run(debug=True)