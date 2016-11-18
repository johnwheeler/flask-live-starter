from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_pyfile('settings.cfg')

db = SQLAlchemy(app)

if not app.debug:
    import logging
    log_path = '/var/log/flask/{}.log'.format(__name__)
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(file_handler)
