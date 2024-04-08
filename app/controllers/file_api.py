from flask import (
    Blueprint, render_template, request
)
import os
from app import app
from app.models.files import Files
bp = Blueprint('file_api', __name__)

@bp.route('/file-processing', methods=['GET', 'POST'])
def index():
    data = request.get_json()

    return {
        "data": data
    }
    
@bp.route('/file-upload', methods=['GET','POST'])
def upload():
    if 'file' not in request.files:
        return "No file part in the request", 400
    
    file = request.files['file']
    file_save_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_save_path)
    project_id = request.form.get('projectId')
    ext = os.path.splitext(file.filename)[1]
    new_file = Files(name = file.filename, source = file_save_path, notes = 'test_file', type = 'in', file_type = ext, projects_id = project_id)
    existing_file = Files.query.filter_by(name=file.filename).first()

    if existing_file:
        Files.delete(existing_file)
    Files.save(new_file)
    if file.filename == '':
        return "No file selected for uploading", 400
    # files_data = []
    # files = Files.query.filter(Files.projects_id == project_id).all()
    # for file in files:
    #     file_data = {
            
    #         'name': file.name,
    #         'source': file.source,
    #         'notes': file.notes,
    #         'type': file.type,
    #         'file_type': file.file_type,
    #         'projects_id': file.projects_id
    #         # Include other relevant fields of the file object
    #     }
    #     files_data.append(file_data)

    return {
        'message': 'Project found',
    }