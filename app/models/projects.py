# -*- coding: utf-8 -*-
# Coded By Kuduxaaa

from app import db


"""
Example Project model
"""
class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    status = db.Column(db.String(80), nullable=True)
    notes = db.Column(db.String(120), nullable=True)
    open = db.Column(db.Boolean, unique=False, default=True)
    
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
