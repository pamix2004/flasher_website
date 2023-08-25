from flask import Blueprint,render_template


views = Blueprint("views",__name__)

@views.route("/")
def route():
    return render_template("homepage.html")

