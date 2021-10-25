"""REST API."""
import flask
import ICUDiary

@ICUDiary.app.route('/api/patientdropdown/', methods=["GET"])
def get_patients(): 

    connect= ICUDiary.model.get_db()
    patientlist = []
            
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

    context = {"patients" : patientlist}
    return flask.jsonify(**context)