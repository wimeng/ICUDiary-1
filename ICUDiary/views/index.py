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
    connect = ICUDiary.model.get_db()
    context = {'patient': ''}
    if 'user' in flask.session:
        context['user'] = flask.session['user']
        cur = connect.execute(
            "SELECT filename, role FROM users "
            "WHERE username = ? ", (flask.session["user"],)
        )
        photo = cur.fetchall()
        context['filename'] = photo[0]['filename']
        context['role'] = photo[0]['role']

        patientname = ''
        if context['role'] == 'Patient':
            cur = connect.execute(
                "SELECT * FROM users "
                "WHERE username = ? ", (flask.session["user"],)
            ).fetchone()
            patientname = cur['firstname'] + " " + cur['lastname'] 

            notif = connect.execute(
                "SELECT notifcount FROM patient WHERE username = ? ", (flask.session["user"],)
            ).fetchone()
            context['notifcount'] = notif['notifcount']

        elif context['role'] == 'Superuser':
            scode = connect.execute(
                "SELECT superusercode FROM superuser "
                "WHERE username = ? ", (flask.session["user"],)
            ).fetchone()['superusercode']
            cur = connect.execute(
                "SELECT firstname, lastname FROM users JOIN superuser ON (users.username = superuser.username) "
                "WHERE superusercode = ? AND role = 'Patient'", (scode,)
            ).fetchone()
            patientname = cur['firstname'] + " " + cur['lastname']
            
        context['patient'] = patientname
        
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

    context['usesPatient'] = False
    if role == 'Superuser':
        superuser = connect.execute(
            "SELECT * FROM superuser WHERE username = ?",(flask.session['user'],) 
        ).fetchone()
        if superuser:
            context['usesPatient'] = True

    return flask.render_template("home.html", **context)

@ICUDiary.app.route("/help/")
def help():
    context = common_context()
    return flask.render_template("info.html", **context)


@ICUDiary.app.route("/changemode/", methods=['POST'])
def changemode():
    print(request.form)
    flask.session["mode"] = request.form["mode"]
    print(flask.session["mode"])
    return "", 200

def logged():
    """User logged in check."""
    return "user" in flask.session