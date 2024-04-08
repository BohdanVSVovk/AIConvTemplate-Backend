from flask import (
    Blueprint, render_template, request
)
import os
from app import app
bp = Blueprint('file_api', __name__)

@bp.route('/file-processing', methods=['GET', 'POST'])
def index():
    data = request.get_json()

    return {
        data['id']
    }
    
@bp.route('/file-upload', methods=['GET','POST'])
def upload():
    if 'file' not in request.files:
        return "No file part in the request", 400
    
    file = request.files['file']
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

    if file.filename == '':
        return "No file selected for uploading", 400
    return "File uploaded successfully", 200