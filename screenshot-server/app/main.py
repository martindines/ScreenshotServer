import os
import sys
import pathlib
from utilities import get_random_hash
from flask import Flask, flash, request, redirect, url_for, send_from_directory, jsonify, Response

UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') if os.environ.get('UPLOAD_FOLDER') else '/tmp'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
SECRET = os.environ.get('SECRET')


app = Flask(__name__)
app.config['SERVER_NAME'] = os.environ.get('SERVER_NAME')

def allowed_file(filename):
    return '.' in filename and \
           pathlib.Path(filename).suffix[1:] in ALLOWED_EXTENSIONS


def is_secret_valid(guess):
    try:
        if guess == SECRET:
            return True
        return False

    except KeyError:
        return False


def verify_auth_headers():
    if 'secret' in request.headers:
        guess = request.headers['secret']

        return is_secret_valid(guess)
    return False


def upload_file_and_return_external_path(file):
    extension = pathlib.Path(file.filename).suffix
    filename = get_random_hash() + extension
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    if os.path.exists(filepath):
        upload_file_and_return_external_path(file)
    else:
        file.save(filepath)
        return url_for('upload', filename=filename, _external=True)


@app.route('/')
def index():
    return '''
    <!doctype html>
    '''


@app.route('/<filename>', methods=['GET'])
def upload(filename):
    if allowed_file(filename):
        return send_from_directory(UPLOAD_FOLDER, filename)


@app.route('/api/auth', methods=['GET'])
def api_auth():
    if verify_auth_headers():
        return jsonify(
            success=True
        )
    return jsonify(
        success=False,
        message='Invalid secret'
    )


@app.route('/api/upload', methods=['POST'])
def api_upload():
    if verify_auth_headers():
        # check if the post request has the file part
        if 'file' not in request.files:
            return jsonify(
                success=False,
                message='No file present'
            )

        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return jsonify(
                success=False,
                message='Filename missing'
            )

        if file and allowed_file(file.filename):
            path = upload_file_and_return_external_path(file)
            return jsonify(
                success=True,
                path=path
            )
        else:
            return jsonify(
                success=False,
                message='File type not allowed'
            )

    return jsonify(
        success=False,
        message='Invalid secret'
    )

