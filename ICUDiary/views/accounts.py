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
    # check that username exists
    # and password matches, otherwise abort(403)
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
        if leb(users) > 0:
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
        path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
        fileobject.save(path)

        # Query database
        insertion = connection.execute(
            "INSERT INTO users(username, firstname, lastname, email, filename, password)"
            "VALUES (?, ?, ?, ?, ?, ?)",
            (username, request.form["firstname"], request.form["lastname"], request.form["email"],
                uuid_basename, password_db_string)
        )

        flask.session["user"] = username
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
            abort(403)

        pswd = connection.execute(
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

""" @ICUDiary.app.route('/accounts/password/', methods=['POST', 'GET'])
def edit_password():
    Edit pass page.
    if not_logged is False:
        return flask.redirect("accounts/login/")

    connection = ICUDiary.model.get_db()
    # gets username, password, stores into
    # session object, and redirect to / page
    # check that username exists and password
    # matches, otherwise abort(403)
    if request.method == "POST":
        old_password = request.form["password"]
        new_password = request.form["new_password"]
        new_password2 = request.form["new_password_check"]

        if new_password != new_password_check:
            abort(401)

        cur_pass = connection.execute(
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

        connection.execute(
            "UPDATE users "
            "SET password = ? "
            "WHERE username = ? ", (password_db_string, flask.session["user"],)
        )
        return flask.redirect("/accounts/edit/")

    context = {
        "logname": flask.session["user"]
    }
    return flask.render_template("password.html", **context)


 """

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