from flask import Flask


def create_app():

    app = Flask(__name__)
    app.config["SECRET_KEY"]='pamix_developer'

    from . import views
    from . import auth
    app.register_blueprint(views.views)
    app.register_blueprint(auth.auth)

    return app