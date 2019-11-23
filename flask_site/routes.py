from flask_site import app
from flask import render_template

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title="Generic", user="New User")

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
