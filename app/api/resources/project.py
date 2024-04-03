# -*- coding: utf-8 -*-
# Coded By Kuduxaaa

from flask_restful import Resource
from app.models.projects import Projects
from flask import request, jsonify

# This is example API Resource
class Project(Resource):
    def get(self):
        """
        Route get method
        type something :)
        happy coding
        """
        projects = Projects.query.all()
        project_data = [{'no': project.id, 'project_name': project.name, 'open_project': project.open, 'status': project.status, 'notes': project.notes} for project in projects]

        return {'projects': project_data}

    

    def post(self):
        """
        Route post method
        type something :)
        happy coding
        """
        if request.is_json:
            data = request.get_json()
            if 'id' in data:
                project_id = data['id']
                project = Projects.query.get(project_id)

                if project:
                    # Perform further processing using the retrieved project
                    files_data = []
                    for file in project.files_pj:
                        file_data = {
                            'name': file.name,
                            'source': file.source,
                            'notes': file.notes,
                            'type': file.type,
                            'file_type': file.file_type,
                            'projects_id': file.projects_id
                            # Include other relevant fields of the file object
                        }
                        files_data.append(file_data)

                    return {
                        'message': 'Project found',
                        'project_id': project.id,
                        'project_files': files_data
                        # Add more fields as needed
                    }
                else:
                    return {'error': 'Project with id {} not found'.format(project_id)}, 404

            else:
                return {'error': 'ID not found in JSON data'}, 400
        else:
            return {'error': 'Request data is not in JSON format'}, 400


    def delete(self):
        """
        Route delete method
        type something :)
        happy coding
        """

        pass