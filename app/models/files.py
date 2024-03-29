# -*- coding: utf-8 -*-
# Coded By Kuduxaaa

from app import db


"""
Example Project model
"""
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
