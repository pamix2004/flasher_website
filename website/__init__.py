from flask import Flask
from .extensions import db,mail
import os

def create_app():

    app = Flask(__name__)
    app.config["SECRET_KEY"]=os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    
    
    mail_username = os.environ.get("MAIL_USERNAME")
    mail_password = os.environ.get("MAIL_PASSWORD")



    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = os.environ.get("EMAIL_USERNAME")
    app.config['MAIL_PASSWORD'] = os.environ.get("EMAIL_PASSWORD")
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True

    







    from . import views
    from . import auth
    app.register_blueprint(views.views)
    app.register_blueprint(auth.auth)

    from .models import User
    with app.app_context():
        db.init_app(app)
        db.create_all()
        mail.init_app(app)





    return app