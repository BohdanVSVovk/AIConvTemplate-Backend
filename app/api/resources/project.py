# -*- coding: utf-8 -*-
# Coded By Kuduxaaa

from flask_restful import Resource
from app.models.projects import Projects

# This is example API Resource
class Project(Resource):
    def get(self):
        """
        Route get method
        type something :)
        happy coding
        """
        projects = Projects.query.all()
        project_data = [{'id': project.id, 'project_name': project.name, 'open_project': project.open, 'status': project.status, 'notes': project.notes} for project in projects]

        return {'projects': project_data}


    def post(self):
        """
        Route post method
        type something :)
        happy coding
        """

        pass


    def delete(self):
        """
        Route delete method
        type something :)
        happy coding
        """

        pass