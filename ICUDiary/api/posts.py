"""REST API."""
import flask
import ICUDiary

@ICUDiary.app.route('/api/patientdropdown/', methods=["GET"])
def get_patients(): 

    connect= ICUDiary.model.get_db()
    patientlist = []
    
    role = connect.execute(
        "SELECT role FROM users "
        "WHERE username = ? ",
        (flask.session["user"],)
    ).fetchone()['role']

    if role == 'Patient':
        patientinfo = connect.execute(
            "SELECT * FROM users "
            "WHERE username = ? ",
            (flask.session["user"],)
        ).fetchone()

        patientlist = [{"username": flask.session["user"], "firstname": patientinfo['firstname'], "lastname": patientinfo['lastname']}]
    elif role == 'User':
        patientcodelist = connect.execute(
            "SELECT patientcode FROM patient "
            "WHERE username = ? ",
            (flask.session["user"],)
        ).fetchall()

        for patient in patientcodelist:
            patientcode = patient['patientcode']   

            patientname = connect.execute(
                "SELECT users.username, firstname, lastname FROM users "
                "JOIN patient ON (patient.username = users.username) "
                "WHERE patientcode = ? AND role = 'Patient'",
                (patientcode,)
            ).fetchall()

            patientlist.append({"username": patientname[0]['username'], "firstname": patientname[0]['firstname'], "lastname": patientname[0]['lastname']})
    else:
        superusercode = connect.execute(
            "SELECT superusercode FROM superuser "
            "WHERE username = ? ",
            (flask.session["user"],)
        ).fetchone()

        patientinfo = connect.execute(
            "SELECT users.username, firstname, lastname FROM users "
            "JOIN superuser ON (superuser.username = users.username) "
            "WHERE superusercode = ? AND role = 'Patient'",
            (superusercode['superusercode'],)
        ).fetchone()
        
        patientlist = [{"username": flask.session["user"], "firstname": patientinfo['firstname'], "lastname": patientinfo['lastname']}]

    context = {"patients" : patientlist}
    return flask.jsonify(**context)
