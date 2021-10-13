"""
Entry view.

URLs include:
/
"""
import flask
from flask import request
from flask import abort
import ICUDiary
from ICUDiary import config

def common_context():
    context = {'patient': ''}
    if 'patient' in flask.session:
        context['patient'] = flask.session['patient']
    return context

@ICUDiary.app.route("/uploads/<file>")
def file_func(file):
    """Send file."""
    if logged() is False:
        abort(403)
    return flask.send_from_directory(ICUDiary.app.config["UPLOAD_FOLDER"],  file)

@ICUDiary.app.route("/image/<file>")
def static_func(file):
    """Send file."""
    return flask.send_from_directory(ICUDiary.app.config["STATIC_FOLDER"],  file)


@ICUDiary.app.route("/")
def home():
    if logged() is False:
        return flask.redirect("accounts/login/")
    context = common_context()
    connect = ICUDiary.model.get_db()
    role = connect.execute(
        "SELECT role FROM users WHERE username = ?",(flask.session['user'],) 
    ).fetchone()['role']
    context['role'] = role
    return flask.render_template("home.html", **context)


def logged():
    """User logged in check."""
    return "user" in flask.session