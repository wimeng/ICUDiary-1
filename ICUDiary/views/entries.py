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
from ICUDiary.views.accounts import logged

@ICUDiary.app.route("/newentry/")
def newentry():
    """Send file."""
    if logged() is False:
        return flask.redirect("/accounts/login/")
    return flask.render_template("recording.html")

@ICUDiary.app.route("/archive/")
def archive():
    """Send file."""

    if logged() is False:
        return flask.redirect("/accounts/login/")

    # authenticate that only patient and superuser can view archive
    connect = ICUDiary.model.get_db()

    role = connect.execute(
        "SELECT role "
        "FROM users "
        "WHERE username = ?", (flask.session["user"],)
    )
    
    curr_role = role.fetchall()[0]['role']
    print(curr_role)

    if curr_role == "User":
        abort(403)

    return flask.render_template("archive.html")


# def logged():
#     """User logged in check."""
#     return "user" in flask.session