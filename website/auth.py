from flask import Blueprint,render_template,request,flash,current_app,url_for,redirect
from itsdangerous import URLSafeTimedSerializer
from .extensions import db,mail
from .models import User
import os
from flask_mail import Message
from werkzeug.security import generate_password_hash,check_password_hash

auth = Blueprint("auth",__name__)

@auth.route("/login")
def login():
    return render_template("login.html")


def encode_mail_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email,salt=os.environ.get("EMAIL_CONFIRM_SALT"))

def decode_mail_token(token):
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    try:
        email = serializer.loads(token,salt=os.environ.get("EMAIL_CONFIRM_SALT"),max_age=300 )
        user = User.query.filter_by(email=email).first()
        user.verified = True
        db.session.commit()

        

        return True
    

    except:
        return False



@auth.route("/mail_confirmation/<token>")
def mail_confirmation(token):
    valid_token = decode_mail_token(token)

    if valid_token:
        flash("Your account has been verivied, now you can log in")
    else:
        return "<h1>Some error has occured</h1>"

    
    

@auth.route("/sign_up",methods=["GET","POST"])
def sign_up():

    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        #handle invalid credentials/typos
        user_exists = User.query.filter_by(email=email).first()

        if user_exists and user_exists.verified:
            flash(message="Account with this email already exists",category="error")
            
        elif password1 != password2:
            flash(message="Passwords do not match",category="error")
        
        else:
            if user_exists:
                User.query.filter_by(email=email).delete()
                db.session.commit()
            msg = Message("Hey",sender=os.environ.get("MAIL_USERNAME"),recipients=[email])
            
            verification_link = url_for("auth.mail_confirmation",token=encode_mail_token(email),_external=True)
            msg.body = verification_link

            mail.send(msg)

            hashed_password = generate_password_hash(password1,"sha256")
            new_user = User(username=username,email=email,password=hashed_password,verified=False)
            db.session.add(new_user)
            db.session.commit()



            return "<h1>Now we need to verify your email, check your inbox!</h1>"
    
    
        
    
    return render_template("sign_up.html")