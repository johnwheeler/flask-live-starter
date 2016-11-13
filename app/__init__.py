import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_pyfile('settings.cfg')

db = SQLAlchemy(app)
