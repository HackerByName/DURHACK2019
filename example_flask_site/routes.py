from flask_site import app
from flask import render_template, flash, redirect
from flask_site.forms import LoginForm

@app.route("/")
@app.route("/index")
def index():
    return render_template("base.html")

@app.route("/test")
def another():
    return "Another"

@app.route("/user_test")
def user_test():
    user = {"username": "Finlay"}
    return render_template("index.html", title="User", user=user)

@app.route("/config")
def config_display():
    return render_template("display.html", skey=app.config["SECRET_KEY"]);

@app.route("/login", methods=["GET", "POST"])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        flash("Login requested for {}, remember = {}".format(form.username.data, form.remember_me.data))
        return redirect("/index")
    return render_template("login.html", title="Sign In", form=form)
