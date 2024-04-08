from flask import (
    Blueprint, render_template, request
)
import os
import pandas as pd
from app import app
import json
from app.models.files import Files
bp = Blueprint('file_api', __name__)

@bp.route('/file-processing', methods=['GET', 'POST'])
def index():
    data = request.get_json()
    selected_files_ids = data['selected_files']
    form_data = []
    for seleted_file_id in selected_files_ids:
        selected_file = Files.query.get(seleted_file_id)
        filepath = selected_file.source
        data = pd.read_excel(filepath)
        # Get columns
        columns = data.columns.tolist()
        first_row_data = data.iloc[0].astype(str).tolist()
        # pair each column with its corresponding data
        column_data = dict(zip(columns,first_row_data)) 
        form_data.append(
            {
                'id': seleted_file_id,
                'name': selected_file.name,
                'columns': columns,
                'row_data': column_data
            }
        )
    return {
        "data": form_data
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

    return {
        'message': 'Project found',
    }
    
@bp.route('/file-generate', methods=['GET','POST'])
def generate():
    
    try:
        input_settings_json = request.form.get('inputSettings')
        input_settings = json.loads(input_settings_json)
    except json.JSONDecodeError:
        print("Decoding JSON has failed")
        input_settings = None
    try:
        prompt_settings_json = request.form.get('PromptSettings')
        prompt_settings = json.loads(prompt_settings_json)
    except json.JSONDecodeError:
        print("Decoding JSON has failed")
        prompt_settings = None
    all_data = pd.DataFrame()
    max_rows = 0

    # For each input setting
    for setting in input_settings:
    # Fetch the file entry from database
        file_entry = Files.query.get(setting['id'])
        if file_entry is None:
            # Skip if there is no file for the given id
            print(f"No file found for id {setting['id']}")
            continue

        # Read the Excel file into a pandas DataFrame
        df = pd.read_excel(file_entry.source)

        # Update max_rows with length of the currently loaded dataframe
        max_rows = max(max_rows, len(df))
        
        # List all available fields
        fields = ['sku', 'brand', 'spec']

        # For each available field
        for field in fields:

            # Get the corresponding field specified in this setting's selectedItem (e.g., 'brand', 'sku')
            selected_field = setting['selectedItem'][field]

            # If the selected field exists in the dataframe's columns
            if selected_field in df.columns:

                # If the all_data dataframe already has data
                if not all_data.empty and field in all_data.columns:
        
                    # Merge cell data by concatenating the data in at the same index from all_data and df
                    all_data.loc[:, field] = all_data.loc[:, field].astype(str) + ' ' + df.loc[:, selected_field].astype(str)
    
                # If all_data dataframe is empty, or has no column named field
                else:
                    # Assign the values of the selected field from the original dataframe to all_data
                    all_data[field] = df[selected_field]

    # Resize all_data to the size of the largest original dataframe
    all_data = all_data.iloc[:max_rows]
                
                
        # # Combine all data
        # all_data = pd.concat([all_data, new_df], ignore_index=True)

    file_save_path = os.path.join(app.config['UPLOAD_FOLDER'], "transform.xlsx")
    file_public_path = os.path.join(app.config['UPLOAD_PUBLIC_FOLDER'], "transform.xlsx")
    # Write the all_data DataFrame to a new Excel file
    with pd.ExcelWriter(file_save_path) as writer:
        all_data.to_excel(writer)

    return {'data': 'Processing completed', 'file_public_url': file_public_path}