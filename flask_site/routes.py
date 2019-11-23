from flask_site import app
from flask import render_template

@app.route("/")
@app.route("/index")
def index():
    return "Hello, World!"

@app.route("/test")
def another():
    return "Another"

@app.route("/user_test")
def user_test():
    user = {"username": "Finlay"}
    return render_template("index.html", title="User", user=user)
