from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_pyfile('settings.cfg')

db = SQLAlchemy(app)

if not app.debug:
    import logging

    fmt = "%(levelname)s - %(asctime)s %(filename)s:%(lineno)d %(message)s"
    formatter = logging.Formatter(fmt=fmt)
    log_path = '/var/log/flask/{}.log'.format(__name__)
    file_handler = logging.FileHandler(log_path)
    file_handler.setFormatter(formatter)

    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
