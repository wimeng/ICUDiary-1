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
import uuid
import pathlib

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
                "INSERT INTO text_entries(entryname, entrytext, writer, patient, transcription) "
                "VALUES (?, ?, ?, ?, ?) ", (entry_title, entry_text, flask.session['user'], selected_patient, "")
            )

            connect.execute(
                "UPDATE patient "
                "SET notifcount = notifcount + 1 "
                "WHERE username = ? ",(selected_patient,)
            )

            return flask.redirect("/archive/")
        
        if request.form['type'] == 'audio':

            fileobj = request.files["file"]
            filename = fileobj.filename
            # Compute base name (filename without directory).
            # We use a UUID to avoid
            # clashes with existing files, and ensure
            # that the name is compatible with the
            # filesystem.
            uuid_basename = "{stem}{suffix}".format(
                stem=uuid.uuid4().hex,
                suffix=pathlib.Path(filename).suffix
            )
            # Save to disk
            path = ICUDiary.app.config["UPLOAD_FOLDER"]/uuid_basename
            fileobj.save(path)

            entry_title = request.form['title']
            entry_audio = path
            selected_patient = request.form['patient']
            transcript = request.form['transcript']
            connect.execute(
                "INSERT INTO audio_entries(entryname, entryaudio, writer, patient, transcription) "
                "VALUES (?, ?, ?, ?, ?) ", (entry_title, uuid_basename, flask.session['user'], selected_patient, transcript)
            )

            connect.execute(
                "UPDATE patient "
                "SET notifcount = notifcount + 1 "
                "WHERE username = ? ",(selected_patient,)
            )

            return flask.redirect("/archive/")

        if request.form['type'] == 'photo':
            fileobj = request.files["file"]
            filename = fileobj.filename
            # Compute base name (filename without directory).
            # We use a UUID to avoid
            # clashes with existing files, and ensure
            # that the name is compatible with the
            # filesystem.
            uuid_basename = "{stem}{suffix}".format(
                stem=uuid.uuid4().hex,
                suffix=pathlib.Path(filename).suffix
            )
            # Save to disk
            path = ICUDiary.app.config["UPLOAD_FOLDER"]/uuid_basename
            fileobj.save(path)

            entry_title = request.form['entrytitle']
            entry_audio = path
            selected_patient = request.form['patient']
            transcript = request.form['entry']

            connect.execute(
                "INSERT INTO audio_entries(entryname, entryaudio, writer, patient, transcription) "
                "VALUES (?, ?, ?, ?, ?) ", (entry_title, uuid_basename, flask.session['user'], selected_patient, transcript)
            )

            connect.execute(
                "UPDATE patient "
                "SET notifcount = notifcount + 1 "
                "WHERE username = ? ",(selected_patient,)
            )

            return flask.redirect("/archive/")

        if request.form['type'] == 'video':
            fileobj = request.files["file"]
            filename = fileobj.filename
            # Compute base name (filename without directory).
            # We use a UUID to avoid
            # clashes with existing files, and ensure
            # that the name is compatible with the
            # filesystem.
            uuid_basename = "{stem}{suffix}".format(
                stem=uuid.uuid4().hex,
                suffix=pathlib.Path(filename).suffix
            )
            # Save to disk
            path = ICUDiary.app.config["UPLOAD_FOLDER"]/uuid_basename
            fileobj.save(path)

            entry_title = request.form['entrytitle']
            entry_audio = path
            selected_patient = request.form['patient']
            transcript = request.form['entry']

            connect.execute(
                "INSERT INTO audio_entries(entryname, entryaudio, writer, patient, transcription) "
                "VALUES (?, ?, ?, ?, ?) ", (entry_title, uuid_basename, flask.session['user'], selected_patient, transcript)
            )

            connect.execute(
                "UPDATE patient "
                "SET notifcount = notifcount + 1 "
                "WHERE username = ? ",(selected_patient,)
            )

            return flask.redirect("/archive/")
    print("what")
    return flask.render_template("recording.html", **context)

# THE REAL ENDPOINT FOR THIS IS /archive/, THIS IS TEMPORARILY SET FOR THE DEMO
@ICUDiary.app.route("/archive/", methods=['POST', 'GET'])
def archive():
    """Send file."""
    if request.method == "GET":
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
            message = connect.execute(
                "SELECT * "
                "FROM text_entries "
                "WHERE writer = ?"
                "UNION "
                "SELECT * "
                "FROM audio_entries "
                "WHERE writer = ? "
                "ORDER BY created DESC ", (flask.session["user"],flask.session["user"])
            ).fetchall()

            for entry in message:
                picture = connect.execute(
                    "SELECT filename, firstname, lastname "
                    "FROM users "
                    "WHERE username = ? ",
                    (entry["writer"],)
                ).fetchone()
                entry['photo'] = picture['filename']
                entry['firstname'] = picture['firstname']
                entry['lastname'] = picture['lastname']
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

            for entry in message:
                picture = connect.execute(
                    "SELECT filename, firstname, lastname "
                    "FROM users "
                    "WHERE username = ? ",
                    (entry["writer"],)
                ).fetchone()
                entry['photo'] = picture['filename']
                entry['firstname'] = picture['firstname']
                entry['lastname'] = picture['lastname']

        # # example test code delete later
        # audio_message = connect.execute(
        #     "SELECT * "
        #     "FROM audio_entries JOIN patient ON (audio_entries.patient = patient.username) "
        #     "WHERE patientcode = ? "
        #     "ORDER BY audio_entries.created DESC",
        #     (pcode,)
        # ).fetchall()

            connect.execute(
                "UPDATE patient "
                "SET notifcount = 0 "
                "WHERE username = ? ",(flask.session['user'],)
            )
            context["notifcount"] = 0

            context["entries"] = message
            # context["audio_entries"] = audio_message

        if curr_role == "Superuser":
            scode = connect.execute(
                "SELECT superusercode "
                "FROM superuser "
                "WHERE username = ?",(flask.session['user'],)
            ).fetchone()['superusercode']
        

            message = connect.execute(
                "SELECT * "
                "FROM text_entries JOIN superuser ON (text_entries.patient = superuser.username) "
                "WHERE superusercode = ? "
                "UNION "
                "SELECT * "
                "FROM audio_entries JOIN superuser ON (audio_entries.patient = superuser.username) "
                "WHERE superusercode = ? "
                "ORDER BY created DESC ",
                (scode,scode)
            ).fetchall()

            for entry in message:
                picture = connect.execute(
                    "SELECT filename, firstname, lastname "
                    "FROM users "
                    "WHERE username = ? ",
                    (entry["writer"],)
                ).fetchone()
                entry['photo'] = picture['filename']
                entry['firstname'] = picture['firstname']
                entry['lastname'] = picture['lastname']

            context["entries"] = message
    

        return flask.render_template("archive.html", **context)

    if request.method == "POST":
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

        if (request.form["sort"] == "newest"):

            if curr_role == "User":
                message = connect.execute(
                    "SELECT * "
                    "FROM text_entries "
                    "WHERE writer = ?"
                    "UNION "
                    "SELECT * "
                    "FROM audio_entries "
                    "WHERE writer = ? "
                    "ORDER BY created DESC ", (flask.session["user"],flask.session["user"])
                ).fetchall()

                for entry in message:
                    picture = connect.execute(
                        "SELECT filename, firstname, lastname "
                        "FROM users "
                        "WHERE username = ? ",
                        (entry["writer"],)
                    ).fetchone()
                    entry['photo'] = picture['filename']
                    entry['firstname'] = picture['firstname']
                    entry['lastname'] = picture['lastname']
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

                for entry in message:
                    picture = connect.execute(
                        "SELECT filename, firstname, lastname "
                        "FROM users "
                        "WHERE username = ? ",
                        (entry["writer"],)
                    ).fetchone()
                    entry['photo'] = picture['filename']
                    entry['firstname'] = picture['firstname']
                    entry['lastname'] = picture['lastname']

                connect.execute(
                    "UPDATE patient "
                    "SET notifcount = 0 "
                    "WHERE username = ? ",(flask.session['user'],)
                )
                context["notifcount"] = 0

                context["entries"] = message

            if curr_role == "Superuser":
                scode = connect.execute(
                    "SELECT superusercode "
                    "FROM superuser "
                    "WHERE username = ?",(flask.session['user'],)
                ).fetchone()['superusercode']
        

                message = connect.execute(
                    "SELECT * "
                    "FROM text_entries JOIN superuser ON (text_entries.patient = superuser.username) "
                    "WHERE superusercode = ? "
                    "UNION "
                    "SELECT * "
                    "FROM audio_entries JOIN superuser ON (audio_entries.patient = superuser.username) "
                    "WHERE superusercode = ? "
                    "ORDER BY created DESC ",
                    (scode,scode)
                ).fetchall()

                for entry in message:
                    picture = connect.execute(
                        "SELECT filename, firstname, lastname "
                        "FROM users "
                        "WHERE username = ? ",
                        (entry["writer"],)
                    ).fetchone()
                    entry['photo'] = picture['filename']
                    entry['firstname'] = picture['firstname']
                    entry['lastname'] = picture['lastname']

                context["entries"] = message

            return flask.render_template("archive.html", **context)

        elif(request.form["sort"] =="oldest"):
            if curr_role == "User":
                message = connect.execute(
                    "SELECT * "
                    "FROM text_entries "
                    "WHERE writer = ?"
                    "UNION "
                    "SELECT * "
                    "FROM audio_entries "
                    "WHERE writer = ? "
                    "ORDER BY created ASC ", (flask.session["user"],flask.session["user"])
                ).fetchall()

                for entry in message:
                    picture = connect.execute(
                        "SELECT filename, firstname, lastname "
                        "FROM users "
                        "WHERE username = ? ",
                        (entry["writer"],)
                    ).fetchone()
                    entry['photo'] = picture['filename']
                    entry['firstname'] = picture['firstname']
                    entry['lastname'] = picture['lastname']
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
                    "ORDER BY created ASC ",
                    (pcode, pcode)
                ).fetchall()

                for entry in message:
                    picture = connect.execute(
                        "SELECT filename, firstname, lastname "
                        "FROM users "
                        "WHERE username = ? ",
                        (entry["writer"],)
                    ).fetchone()
                    entry['photo'] = picture['filename']
                    entry['firstname'] = picture['firstname']
                    entry['lastname'] = picture['lastname']

                connect.execute(
                    "UPDATE patient "
                    "SET notifcount = 0 "
                    "WHERE username = ? ",(flask.session['user'],)
                )
                context["notifcount"] = 0

                context["entries"] = message

            if curr_role == "Superuser":
                scode = connect.execute(
                    "SELECT superusercode "
                    "FROM superuser "
                    "WHERE username = ?",(flask.session['user'],)
                ).fetchone()['superusercode']
        

                message = connect.execute(
                    "SELECT * "
                    "FROM text_entries JOIN superuser ON (text_entries.patient = superuser.username) "
                    "WHERE superusercode = ? "
                    "UNION "
                    "SELECT * "
                    "FROM audio_entries JOIN superuser ON (audio_entries.patient = superuser.username) "
                    "WHERE superusercode = ? "
                    "ORDER BY created ASC ",
                    (scode,scode)
                ).fetchall()

                for entry in message:
                    picture = connect.execute(
                        "SELECT filename, firstname, lastname "
                        "FROM users "
                        "WHERE username = ? ",
                        (entry["writer"],)
                    ).fetchone()
                    entry['photo'] = picture['filename']
                    entry['firstname'] = picture['firstname']
                    entry['lastname'] = picture['lastname']

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