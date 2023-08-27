from flask import Blueprint,render_template,session,flash,g,redirect,url_for


views = Blueprint("views",__name__)

@views.route("/")
def index():
    return render_template("homepage.html")

@views.route("/learning")
def learning():
    if g.email and g.username:
        return render_template("learning.html")
    else:
        flash("You have to log in in order to use learning")
        return redirect(url_for("auth.login"))
    

