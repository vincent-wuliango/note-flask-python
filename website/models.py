from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Data = db.Column(db.String(10000))
    Date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(100), unique=True)
    Password = db.Column(db.String(100))
    FirstName = db.Column(db.String(100))
    LastName = db.Column(db.String(100))
    Notes = db.relationship('Note')