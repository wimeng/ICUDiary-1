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

@ICUDiary.app.route("/newentry/", methods=['POST', 'GET'])
def newentry():
    """Send file."""
    if logged() is False:
        return flask.redirect("/accounts/login/")
    context = common_context()
    
    connect = ICUDiary.model.get_db()
    
    if request.method == "POST":
        if request.form['type'] == 'text':
            entry_title = request.form['entrytitle']
            entry_text = request.form['entry']
            selected_patient = request.form['patient']
            connect.execute(
                "INSERT INTO text_entries(entryname, entrytext, writer, patient) "
                "VALUES (?, ?, ?, ?) ", (entry_title, entry_text, flask.session['user'], selected_patient, )
            )
            return flask.redirect("/archive/")
        
        if request.form['type'] == 'audio':
            entry_title = request.form['entrytitle']
            entry_audio = request.form['entry']
            selected_patient = request.form['patient']
            connect.execute(
                "INSERT INTO audio_entries(entryname, entryaudio, writer, patient) "
                "VALUES (?, ?, ?, ?) ", (entry_title, entry_audio, flask.session['user'], selected_patient, )
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
        
        message = connect.execute(
            "SELECT * "
            "FROM text_entries JOIN patient ON (text_entries.patient = patient.username) "
            "WHERE patientcode = ? "
            "UNION "
            "SELECT * "
            "FROM audio_entries JOIN patient ON (audio_entries.patient = patient.username) "
            "WHERE patientcode = ? "
            "ORDER BY created DESC ",
            (pcode, pcode)
        ).fetchall()

        # example test code delete later
        audio_message = connect.execute(
            "SELECT * "
            "FROM audio_entries JOIN patient ON (audio_entries.patient = patient.username) "
            "WHERE patientcode = ? "
            "ORDER BY audio_entries.created DESC",
            (pcode,)
        ).fetchall()


        context["entries"] = message
        context["audio_entries"] = audio_message

    if curr_role == "Superuser":
        scode = connect.execute(
            "SELECT superusercode "
            "FROM superuser "
            "WHERE username = ?",(flask.session['user'],)
        ).fetchone()['superusercode']
        

        message = connect.execute(
            "SELECT * "
            "FROM text_entries JOIN superuser ON (text_entries.patient = superuser.username) "
            "WHERE superusercode = ? ",
            (scode,)
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