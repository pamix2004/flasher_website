from .extensions import db

class User(db.Model):
    email = db.Column(db.String,primary_key = True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    verified = db.Column(db.Boolean)
    decks = db.relationship("Deck",backref="user")

class Deck(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String)
    user_email = db.Column(db.String,db.ForeignKey("user.email"))
