from flask_site import *
from flask import render_template, flash, redirect
from flask_site.forms import LoginForm, RegisterForm
from . import mongo

@app.route("/")
@app.route("/index")
def index():
    return render_template("base.html")

@app.route("/register", methods=["GET"])
def register():
    register_form = RegisterForm()
    return render_template("register.html", form=register_form)

@app.route("/register", methods=["POST"])
def process_register():
    form = RegisterForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        hashed = bcrypt.generate_password_hash(password).decode("utf-8")
        mongo.Mongo.insertNewUser(student_records, first_name, last_name, email, hashed)
        flash("{}, {}, {}, {}".format(email, password, first_name, last_name))
        return redirect("/login")

    return render_template("register.html", title="Register", form=form)

@app.route("/login", methods=["GET"])
def login():
    flash("Already logged in")

    if "email" in session:
        return redirect("/index")

    login_form = LoginForm()
    return render_template("login.html", form=login_form)

@app.route("/login", methods=["POST"])
def process_login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user_record = mongo.Mongo.find_record(student_records, {"email": email})

        if user_record == None:
            flash("Wrong username")
            return redirect("/index")

        if not bcrypt.check_password_hash(user_record['password'], password):
            #wrong password
            flash("Wrong password")
            return redirect("/index")

        session["email"] = email

        flash("Logged in, {}".format(email))
        return redirect("/index")

    return render_template("login.html", title="Login", form=form)

@app.route("/logout")
def logout():
    if "email" in session:
        flash("Logged out")
        session.pop("email", None)
    else:
        flash("You weren't logged in anyway")

    return redirect("/index")
