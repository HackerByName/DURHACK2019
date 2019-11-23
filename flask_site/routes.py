from flask_site import *
from flask import render_template, flash, redirect
from flask_site.forms import LoginForm, RegisterForm
from .mongo import MongoDatabase
from .helper import Verifications, User

@app.route("/")
@app.route("/index")
def index():
    return render_template("base.html", title="Homepage", user=(session["user"] if "user" in session else None))

@app.route("/register", methods=["GET"])
def register():
    register_form = RegisterForm()
    return render_template("register.html", form=register_form, title="Register", user=(session["user"] if "user" in session else None))

@app.route("/register", methods=["POST"])
def process_register():
    form = RegisterForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        hashed = bcrypt.generate_password_hash(password).decode("utf-8")
        MongoDatabase.insert_new_user(student_records, first_name, last_name, email, hashed)
        ##flash("{}, {}, {}, {}".format(email, password, first_name, last_name))
        return redirect("/login")

    return render_template("register.html", title="Register", form=form, user=(session["user"] if "user" in session else None))

@app.route("/login", methods=["GET"])
def login():
    if Verifications.is_logged_in():
        #flash("Already logged in")
        return redirect("/index")

    login_form = LoginForm()
    return render_template("login.html", form=login_form, title="Login", user=(session["user"] if "user" in session else None))

@app.route("/login", methods=["POST"])
def process_login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user_record = MongoDatabase.find_record(student_records, {"email": email})

        if user_record == None:
            #flash("Wrong username")
            return redirect("/index")

        if not bcrypt.check_password_hash(user_record['password'], password):
            #wrong password
            #flash("Wrong password")
            return redirect("/index")

        session["user"] = User.from_record(user_record)

        #flash("Logged in, {}".format(email))
        return redirect("/index")

    return render_template("login.html", title="Login", form=form, user=(session["user"] if "user" in session else None))

@app.route("/logout")
def logout():
    if Verifications.is_logged_in():
        #flash("Logged out")
        Verifications.logout()

    return redirect("/index")
