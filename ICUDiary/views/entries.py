"""
Entry view.

URLs include:
/entries/newentry/
/entries/archive/

"""
import flask
from flask import request
from flask import abort
import ICUDiary
from ICUDiary import config

@ICUDiary.app.route("/newentry/")
def newentry():
    """Send file."""
    return flask.render_template("recording.html")

@ICUDiary.app.route("/archive/")
def archive():
    """Send file."""

    # authenticate that only patient and superuser can view archive
    curr_user = flask.session["user"]
    connect = ICUDiary.model.get_db()

    patient = connect.execute(
        "SELECT patient "
        "FROM users "
        "WHERE username = ?", (curr_user,)
    )
    
    curr_patient = patient.fetchall()


    if curr_patient != curr_user:
        abort(403)

    return flask.render_template("archive.html")
