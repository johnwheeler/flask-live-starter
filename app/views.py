from flask import render_template

from . import app, db


@app.route('/')
def index():
    app.logger.info('test logging message')
    app.logger.info('this is a test')
    app.logger.error('this is a severe test')
    result = None
    try:
        result = db.engine.execute('select 1')
    except Exception as ex:
        pass

    return render_template('index.html', result=result)
