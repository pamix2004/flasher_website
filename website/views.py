from flask import Blueprint,render_template,session,flash,g,redirect,url_for,request
from .models import User,Deck
from .extensions import db

views = Blueprint("views",__name__)

@views.route("/")
def index():
    return render_template("homepage.html")

@views.route("/learning")
def learning():
    #for logged in users
    if g.email and g.username:
        current_user = User.query.filter_by(email=g.email).first()


        return render_template("learning.html",user_decks = current_user.decks)

    #if you are not logged in you cannot learn
    else:
        flash("You have to log in in order to use learning")
        return redirect(url_for("auth.login"))

@views.route("/learning/create_deck",methods = ["POST"])
def create_deck():
    deck_name = request.form.get("deck_name").strip()
    if deck_name == "":
        flash("Deck name cannot be empty")
    else:
        new_deck = Deck(name = deck_name,user_email = g.email)
        db.session.add(new_deck)
        db.session.commit()

    return redirect(url_for("views.learning"))

@views.route("/learning/delete_deck",methods=["POST"])
def delete_deck():
    
    deck_id = request.form.get("deck_id")
    #check if the deck that you want to delete is for sure yours, (it prevents bad user A from deleting deck of user B because he wants to be a bad person)

    deck_to_be_deleted = Deck.query.filter_by(id=deck_id).first()

    if deck_to_be_deleted.user_email == g.email:
        db.session.delete(deck_to_be_deleted)
        db.session.commit()
    else:
        return "Hey, you are trying to do something weird, don't inspect element! "

    
    return redirect(url_for("views.learning"))

@views.route("/learning/edit_deck_number/<deck_id>",methods = ["GET","POST"])
def edit_deck_number(deck_id):

    #check if the deck that you want to delete is for sure yours, (it prevents bad user A from deleting deck of user B because he wants to be a bad person)

    deck_to_be_edited = Deck.query.filter_by(id=deck_id).first()

    if deck_to_be_edited.user_email == g.email:

        if request.method=="POST":
            new_deck_name = request.form.get("deck_name")
            deck_to_be_edited.name=new_deck_name
            db.session.commit()
            return redirect(url_for("views.edit_deck_number",deck_id=deck_id))
        else:
            return render_template("edit_deck.html",deck_to_be_edited=deck_to_be_edited)



    else:
        return "Naughty, naughty, you wanted to delete someone else's deck, go and think about your behavior"


    

