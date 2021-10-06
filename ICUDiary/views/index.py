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

@ICUDiary.app.route("/uploads/<file>")
def file_func(file):
    """Send file."""
    if logged() is False:
        abort(403)
    return flask.send_from_directory(ICUDiary.app.config["UPLOAD_FOLDER"],  file)


@ICUDiary.app.route("/")
def home():
    if logged() is False:
        abort(403)
    return flask.render_template("home.html")


def logged():
    """User logged in check."""
    return "user" in flask.session