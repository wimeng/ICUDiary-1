"""
Account view.

URLs include:
/accounts/create/
/accounts/login/
/accounts/logout/
"""
import uuid
import hashlib
import os
import pathlib
import flask
from flask import request
from flask import abort
import ICUDiary
from ICUDiary import config


@ICUDiary.app.route('/accounts/create/', methods=['POST', 'GET'])
def create_user():
    """Create page."""
    # gets username, password, stores into session object,
    # and redirect to / page
    # check if username already exists
    # and password is not empty, otherwise abort(403)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        connect = ICUDiary.model.get_db()

        user = connect.execute(
            "SELECT * "
            "FROM users "
            "WHERE username = ?", (username,)
        )

        users = user.fetchall()

        # check if user already exists
        if len(users) > 0:
            abort(409)

        # check for empty password
        if len(password) == 0:
            abort(400)

        # hashing the password
        algorithm = 'sha512'
        salt = uuid.uuid4().hex
        hash_obj = hashlib.new(algorithm)
        salted = salt + password
        hash_obj.update(salted.encode('utf-8'))
        password_hash = hash_obj.hexdigest()
        password_db_string = "$".join([algorithm, salt, password_hash])

        # Unpack flask object
        fileobject = request.files["file"]
        filename = fileobject.filename

        # Compute base name (filename without directory).
        # We use a UUID to avoid
        # clashes with existing files,
        # and ensure that the name is compatible with the
        # filesystem.
        uuid_basename = "{stem}{suffix}".format(
            stem=uuid.uuid4().hex,
            suffix=pathlib.Path(filename).suffix
        )

        # Save to disk
        path = ICUDiary.app.config["UPLOAD_FOLDER"]/uuid_basename
        fileobject.save(path)

        # Query database
        insertion = connect.execute(
            "INSERT INTO users(username, firstname, lastname, email, filename, password, role) "
            "VALUES (?, ?, ?, ?, ?, ?, ?) ",
            (username, request.form["firstname"], request.form["lastname"], request.form["email"],
                uuid_basename, password_db_string, request.form["role"])
                # replace 'e' with uuid_basename later
        )

        flask.session["user"] = username
        if request.form["role"] == "Patient":
            # generate patient and superuser codes
            patient_hash = hashlib.new(algorithm)
            patient_hash.update(username.encode('utf-8'))
            patientcode = patient_hash.hexdigest()[0:12].upper()
            connect.execute(
            "INSERT INTO patient(username, patientcode) "
            "VALUES (?, ?) ",
            (username, patientcode)
            )

            superuser_hash = hashlib.new(algorithm)
            superuser_hash.update(('super' + username).encode('utf-8'))
            superusercode = superuser_hash.hexdigest()[0:12].upper()
            connect.execute(
            "INSERT INTO superuser(superusername, superusercode) "
            "VALUES (?, ?) ",
            (username, superusercode)
            )
            return flask.redirect("/showcodes/")
        elif request.form["role"] == "Superuser":
            return flask.redirect("/accounts/superuser/")
        else:
            return flask.redirect("/accounts/patientcode/")
            pass
            
        return flask.redirect("/")

    return flask.render_template("create.html")

@ICUDiary.app.route('/accounts/login/', methods=['POST', 'GET'])
def login():
    """Login page."""
    # gets username, password,
    # stores into session object, and redirect to / page
    # check that username exists and password matches, otherwise abort(403)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # Connect to database
        connect = ICUDiary.model.get_db()

        # Query database
        user = connect.execute(
            "SELECT * "
            "FROM users "
            "WHERE username = ?", (username,)
        )

        users = user.fetchall()

        if len(users) == 0:
            abort(403) # change to reload login page with error message

        pswd = connect.execute(
            "SELECT password "
            "FROM users "
            "WHERE username = ?",(username,)
        )

        correct_pass = pswd.fetchall()
        correct_pass = correct_pass[0]['password']
        algorithm, salt, password_db_hash = correct_pass.split("$")

        # hashing the password
        algorithm = 'sha512'
        # salt = uuid.uuid4().hex
        hash_obj = hashlib.new(algorithm)
        salted = salt + password
        hash_obj.update(salted.encode('utf-8'))
        password_user_hash = hash_obj.hexdigest()
        # password_db_string = "$".join([algorithm, salt, password_hash])
        if password_db_hash != password_user_hash:
            abort(403)

        # store user as current user
        flask.session["user"] = username
        return flask.redirect("/")
        
    else:
        return flask.render_template("login.html")

@ICUDiary.app.route('/accounts/password/', methods=['POST', 'GET'])
def edit_password():
    """Edit pass page."""
    if logged() is False:
        return flask.redirect("accounts/login/")

    connect = ICUDiary.model.get_db()
    # gets username, password, stores into
    # session object, and redirect to / page
    # check that username exists and password
    # matches, otherwise abort(403)
    if request.method == "POST":
        old_password = request.form["password"]
        new_password = request.form["new_password"]
        new_password2 = request.form["new_password_check"]

        if new_password != new_password2:
            abort(401)

        cur_pass = connect.execute(
            "SELECT password "
            "FROM users "
            "WHERE username = ? ", (flask.session["user"],)
        )

        correct_pass = cur_pass.fetchall()
        correct_pass = correct_pass[0]['password']

        algorithm, salt, password_db_hash = correct_pass.split("$")

        # hashing the password
        algorithm = 'sha512'
        hash_obj = hashlib.new(algorithm)
        password_salted = salt + old_password
        hash_obj.update(password_salted.encode('utf-8'))
        password_user_hash = hash_obj.hexdigest()

        if password_db_hash != password_user_hash:
            abort(403)

        # checking if old_password matches one in database
        algorithm = 'sha512'
        salt = uuid.uuid4().hex
        hash_obj = hashlib.new(algorithm)
        password_salted = salt + new_password
        hash_obj.update(password_salted.encode('utf-8'))
        password_hash = hash_obj.hexdigest()
        password_db_string = "$".join([algorithm, salt, password_hash])

        connect.execute(
            "UPDATE users "
            "SET password = ? "
            "WHERE username = ? ", (password_db_string, flask.session["user"],)
        )
        return flask.redirect("/accounts/edit/")

    context = {
        "logname": flask.session["user"]
    }
    return flask.render_template("password.html", **context)
@ICUDiary.app.route('/accounts/edit/', methods=['GET', 'POST'])

def edit():
    """Edit user page."""
    if logged() is False:
        return flask.redirect("/accounts/login/")
    # Connect to database
    connect = ICUDiary.model.get_db()
    if request.method == "POST":
        photoicon = request.files["file"]
        first_name = request.form["firstname"]
        last_name = request.form["lastname"]
        email = request.form["email"]

        if photoicon.filename:

            cur = connect.execute(
                "SELECT filename FROM users "
                "WHERE username = ? ", (flask.session["user"],)
            )

            to_delete = cur.fetchone()
            os.remove((config.UPLOAD_FOLDER) / to_delete['filename'])

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

            cur = connect.execute(
                "UPDATE users "
                "SET filename = ? "
                "WHERE username = ? ", (uuid_basename, flask.session["user"],)
            ) 
        if first_name:
            cur = connect.execute(
                "UPDATE users "
                "SET firstname = ? "
                "WHERE username = ? ", (first_name, flask.session["user"],)
            )
        if last_name:
            cur = connect.execute(
                "UPDATE users "
                "SET lastname = ? "
                "WHERE username = ? ", (last_name, flask.session["user"],)
            )
        if email:
            cur = connect.execute(
                "UPDATE users "
                "SET email = ? "
                "WHERE username = ? ", (email, flask.session["user"],)
            )

    cur = connect.execute(
        "SELECT firstname, lastname, email, filename FROM users "
        "WHERE username = ? ", (flask.session["user"],)
    )
    photo = cur.fetchall()
    # delete image in uploads folder and add new image
    context = {
        "filename": photo[0]["filename"],
        "firstname": photo[0]["firstname"],
        "lastname": photo[0]["lastname"],
        "email": photo[0]["email"],
        "logname": flask.session["user"]
    }

    return flask.render_template("edit.html", **context)

@ICUDiary.app.route('/accounts/logout/', methods=['POST', 'GET'])
def logout():
    """Logout page."""
    if logged() is False:
        return flask.redirect("/accounts/login/")
    if request.method == "POST":
        # check form
        flask.session.clear()

    return flask.redirect("/accounts/login/")

def logged():
    """User logged in check."""
    return "user" in flask.session

@ICUDiary.app.route('/showcodes/', methods=['GET'])
def showcodes():
    connect = ICUDiary.model.get_db()
    patientcodeinfo = connect.execute(
        "SELECT patientcode "
        "FROM patient "
        "WHERE username = ?",(flask.session['user'],)
    )
    patientcode = patientcodeinfo.fetchall()[0]['patientcode']
    
    superusercodeinfo = connect.execute(
        "SELECT superusercode "
        "FROM superuser "
        "WHERE superusername = ?",(flask.session['user'],)
    )
    superusercode = superusercodeinfo.fetchall()[0]['superusercode']

    pictureinfo = connect.execute(
        "SELECT filename "
        "FROM users "
        "WHERE username = ?",(flask.session['user'],)
    )
    picture = pictureinfo.fetchall()[0]['filename']
    
    context = {"patientcode": patientcode, "superusercode": superusercode, "filename": picture}

    return flask.render_template("showcodes.html", **context)

@ICUDiary.app.route('/accounts/superuser/', methods=['POST', 'GET'])
def superuser():
    """Superuser authentication."""
    if request.method == "POST":
        pcode = request.form["patientcode"]
        scode = request.form["superusercode"]

        connect = ICUDiary.model.get_db()

        patientcode = connect.execute(
            "SELECT patientcode "
            "FROM patient "
            "WHERE patientcode = ?",(pcode,)
        )

        matching_pcode = patientcode.fetchall()
        
        if len(matching_pcode) == 0:
            # no matching patient
            flask.session.clear()
            return flask.redirect("/accounts/login/")

        superusercode = connect.execute(
            "SELECT superusercode "
            "FROM superuser "
            "WHERE superusercode = ?",(scode,)
        )
        
        matching_scode = superusercode.fetchall()
        
        if len(matching_scode) == 0:
            # no matching superuser
            flask.session.clear()
            return flask.redirect("/accounts/login/")

        insertion = connect.execute(
            "INSERT INTO patient(username, patientcode) "
            "VALUES (?, ?) ",
            (flask.session["user"], pcode)
        )
        return flask.redirect("/")
    
    return flask.render_template("superuser.html")

@ICUDiary.app.route('/accounts/patientcode/', methods=['POST', 'GET'])
def patientcode():
    """Patient account association."""
    if request.method == "POST":
        pcode = request.form["patientcode"]

        connect = ICUDiary.model.get_db()

        patientcode = connect.execute(
            "SELECT patientcode "
            "FROM patient "
            "WHERE patientcode = ?",(pcode,)
        )

        matching_pcode = patientcode.fetchall()
        
        if len(matching_pcode) == 0:
            # no matching patient
            flask.session.clear()
            return flask.redirect("/accounts/login/")

        insertion = connect.execute(
            "INSERT INTO patient(username, patientcode) "
            "VALUES (?, ?) ",
            (flask.session["user"], pcode)
        )
        return flask.redirect("/")

    return flask.render_template("patientcode.html")


def logged():
    """User logged in check."""
    return "user" in flask.session