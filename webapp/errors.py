from flask import render_template

from webapp import app


@app.errorhandler(404)
def not_found():
    return render_template('error.html', errMsg='page not foun!')


@app.errorhandler(500)
def server_error():
    return render_template('error.html', errMsg='server error!')
