# -*- coding: utf-8 -*-
# Coded By Kuduxaaa

import os
import config

from flask import (
    Flask, 
    request,
    render_template,
    send_from_directory,
    abort
)

from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_migrate import Migrate
from flask_cors import CORS
# Application initialization
app = Flask(__name__, 
            template_folder='views',
            static_folder='public')

app.config.from_object(config.DevelopmentConfig)

api_router = Api(app, prefix='/api/v1')  # API Initialization
db = SQLAlchemy(app)                     # Database Initialization
migrate = Migrate(app, db)
class Projects(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    status = db.Column(db.String(80), nullable=True)
    notes = db.Column(db.String(120), nullable=True)
    open = db.Column(db.Boolean, unique=False, default=True)
    files = db.relationship('Files', backref='projects')
    def __init__(self, name, status):
        self.name = name
        self.status = status
        

    def save(self):
        """
        save in the database
        """

        db.session.add(self)
        db.session.commit()
        return True


    def delete(self):
        """
        delete from database
        """

        db.session.delete(self)
        db.session.commit()
        return True

    def __repr__(self):
        return '<Project %r>' % self.name
    
class Files(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    source = db.Column(db.String(80), nullable=True)
    notes = db.Column(db.String(120), nullable=True)
    type = db.Column(db.String(20), nullable=True)
    file_type = db.Column(db.String(20), nullable=True)
    projects_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    def __init__(self, name, source):
        self.name = name
        self.source = source
        

    def save(self):
        """
        save in the database
        """

        db.session.add(self)
        db.session.commit()
        return True


    def delete(self):
        """
        delete from database
        """

        db.session.delete(self)
        db.session.commit()
        return True

    def __repr__(self):
        return '<File %r>' % self.name
CORS(app)
"""
404 Page not found error default handler
"""
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html', error=e), 404



"""
Controllers and API Resources import
and register blueprints and resources 
"""

from app.controllers import main    # Controllers
from app.api.resources import test, project   # API Resources

api_router.add_resource(test.Example, '/')
api_router.add_resource(project.Project, '/project/')

# Register Blueprints
app.register_blueprint(main.bp)
