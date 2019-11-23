from flask_site import *
from flask import render_template, flash, redirect
from flask_site.forms import LoginForm, RegisterForm
from .mongo import MongoDatabase
from .helper import Verifications, User

@app.route("/settings")
def settings():
    #logic here

    return render_template("settings.html", title="Settings", user=(session["user"] if "user" in session else None))

@app.route("/user")
def user():
    form = UserForm()

    return render_template("user.html", title="User Settings", user=(session["user"] if "user" in session else None))
