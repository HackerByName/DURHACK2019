from flask import Flask

app = Flask(__name__)

from flask_site import routes
