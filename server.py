"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Rating, Movie


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")


@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route("/register", methods=["GET"])
def register_form():
    """Render register form"""
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def register_process():
    """Add user email and password to database."""

    email = request.form["email"]
    password = request.form["password"]

    new_user = User(email=email, password=password)

    db.session.add(new_user)
    db.session.commit()
    flash("Registered!")
    return redirect("/")

@app.route("/login", methods = ["GET"])
def login_form():
	"""Render login form"""

	return render_template("login_form.html")

@app.route("/login-check", methods = ["GET"])
def login_check():
	"""Check user's input. If email matches password in database, store user in session."""

	email = request.args.get("email")
	password = request.args.get("password")
	user = User.query.filter(User.email == email).first()

	if user.email == email and user.password == password:
		session["user_id"]= user.user_id
		flash("Logged in!")
		return redirect ("/")
	else:
		flash("Please try again.")

		return redirect("/login")

@app.route("/user/:user_id")
def go_to_userpage(user_id):
    """Render user page when link is clicked in user_list route"""
    user - User.query.filter(User.user_id == user_id).one()
    age = user.age
    zicode = user.zipcode
    
    return render_template("user_page.html", user_id = user_id)

@app.route("/logout")
def logout():
	"""Logout user by clearing session """
	if session:
		session.clear()
		return redirect("/")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
