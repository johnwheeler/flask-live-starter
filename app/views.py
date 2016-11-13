from flask import render_template

from . import app, db


@app.route('/')
def index():
    result = None
    try:
        result = db.engine.execute('select 1')
    except Exception as ex:
        pass

    return render_template('index.html', result=result)
