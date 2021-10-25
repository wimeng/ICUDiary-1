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

def common_context():
    connect = ICUDiary.model.get_db()
    context = {'patient': ''}
    if 'patient' in flask.session:
        context['patient'] = flask.session['patient']
    if 'user' in flask.session:
        context['user'] = flask.session['user']
        cur = connect.execute(
            "SELECT filename, role FROM users "
            "WHERE username = ? ", (flask.session["user"],)
        )
        photo = cur.fetchall()
        context['filename'] = photo[0]['filename']
        context['role'] = photo[0]['role']
    return context

@ICUDiary.app.route("/newentry/", methods=['POST', 'GET'])
def newentry():
    """Send file."""
    if logged() is False:
        return flask.redirect("/accounts/login/")
    context = common_context()
    
    if request.method == "POST":
        entry_title = request.form['entrytitle']
        entry_text = request.form['entry']
        connect = ICUDiary.model.get_db()
        insert = connect.execute(
            "INSERT INTO text_entries(entryname, entrytext, writer) "
            "VALUES (?, ?, ?) ", (entry_title, entry_text, flask.session['user'])
        )
        return flask.redirect("/archive/")

    return flask.render_template("recording.html", **context)

# THE REAL ENDPOINT FOR THIS IS /archive/, THIS IS TEMPORARILY SET FOR THE DEMO
@ICUDiary.app.route("/archive/")
def archive():
    """Send file."""

    if logged() is False:
        return flask.redirect("/accounts/login/")
    context = common_context()

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
        message = connect.execute(
            "SELECT * "
            "FROM text_entries "
            "WHERE writer = ?", (flask.session["user"],)
        ).fetchall()
        context["entries"] = message

    if curr_role == "Patient":
        pcode = connect.execute(
            "SELECT patientcode "
            "FROM patient "
            "WHERE username = ?",(flask.session['user'],)
        ).fetchone()['patientcode']
        
        """ messages = []

        users = connect.excecute(
            "SELECT username "
            "FROM patient "
            "WHERE patientcode = ? ", (pcode,)
        ).fetchall()

        for user in users:
            message = connect.execute(
                "SELECT * "
                "FROM text_entries "
                "WHERE writer = ? ", (user,)
            ).fetchall()
            messages.append(message)
         """
        message = connect.execute(
            "SELECT * "
            "FROM text_entries JOIN patient ON (text_entries.writer = patient.username) "
            "WHERE patientcode = ? ",
            (pcode,)
        ).fetchall()
        context["entries"] = message
    

    return flask.render_template("archive.html", **context)

@ICUDiary.app.route("/archive/1/")
def archive1():
    """Send file."""

    if logged() is False:
        return flask.redirect("/accounts/login/")
    context = common_context()

    # authenticate that only patient and superuser can view archive
    connect = ICUDiary.model.get_db()

    role = connect.execute(
        "SELECT role "
        "FROM users "
        "WHERE username = ?", (flask.session["user"],)
    )
    
    curr_role = role.fetchall()[0]['role']

    if curr_role == "User":
        abort(403)

    return flask.render_template("archive-hardcoded1.html", **context)