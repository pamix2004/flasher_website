from .extensions import db

class User(db.Model):
    email = db.Column(db.String,primary_key = True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    verified = db.Column(db.Boolean)