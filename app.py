import threading
import database
import json
import os
import time

import flask
import flask_login
import pandas as pd
from ast import literal_eval
from flask_cors import CORS
from werkzeug.utils import secure_filename
from k3y5 import ADMIN_USERNAME, ADMIN_PASSWORD, ADMIN_KEY

app = flask.Flask(__name__)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
CORS(app, support_credentials=True)
app.config['FILE_UPLOADS'] = 'resume_uploads'

# ---- flask login setup ----------------------------------
app.secret_key = ADMIN_KEY
users = {ADMIN_USERNAME: {'password': ADMIN_PASSWORD}}

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return
    user = User()
    user.id = email
    return user

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return
    user = User()
    user.id = email
    user.is_authenticated = request.form['password'] == users[email]['password']
    return user
# -----------------------------------------------------

# ---- public services --------------------------------
@app.route('/', methods=['GET'])
def homepage():
    return flask.render_template('homepage.html')

@app.route('/darwin/<jobid>', methods=['GET'])
def darwin(jobid):
    return flask.render_template('chatbot.html', jobid = jobid)

@app.route('/data/getAllJobs', methods=['GET'])
def getAllJobs():
    allJobs = database.getAllJobs()
    return flask.jsonify(allJobs)

@app.route('/data/getResume/<id>', methods=['GET'])
def getResume(id):
    database.resume_vault.download_item(id, os.path.join(os.path.join(app.root_path, app.config['FILE_UPLOADS']), id+str('.pdf')))
    del_thread = threading.Thread(target=delay_delete, args=(5, os.path.join(os.path.join(os.path.join(app.root_path, app.config['FILE_UPLOADS']), id+str('.pdf')))))
    del_thread.start()
    return  flask.send_from_directory(directory=os.path.join(app.root_path, app.config['FILE_UPLOADS']), filename=id+str('.pdf'))

def delay_delete (t, path):
    print ("started")
    time.sleep(t)
    print ("trying to delete")
    os.remove(path)
    print ("done")
    return

@app.route('/data/newCandidate', methods=['POST'])
def newCandidate():
    resumeFile = flask.request.files['resumeFile']
    candyInfo = json.loads(flask.request.form['jsonInput'])
    path = os.path.join(app.config["FILE_UPLOADS"], resumeFile.filename)
    resumeFile.save(path)
    print (":adding new candidate")
    print (candyInfo)
    database.add_candidate({
        "jobId": str(candyInfo['jobid']),
        "cname": candyInfo['cname'],
        "email": candyInfo['email'],
        "gitId": candyInfo['gitId'],
        "tweetId": candyInfo['tweetId'],
        "yoe": int(candyInfo['yoe']),
        "jobskills": candyInfo['jobskills'],
        "self_desc": candyInfo['self_desc'],
        "job_want_why": candyInfo['job_want_why'],
        "job_req_what": candyInfo['job_req_what'],
        "passion": candyInfo['passion'],
        "date_join": candyInfo['date_join'],
        "apt": candyInfo['apt']
    }, path)
    print (":new candidate added")
    os.remove(path)
    return flask.redirect(flask.url_for('homepage'))

@app.route('/data/getQuestions', methods=['GET'])
def getQues():
    _qt = pd.read_csv('data_src/g4g/quants.csv', converters={"OPT": literal_eval}, dtype=str)
    _lg = pd.read_csv('data_src/g4g/logix.csv', converters={"OPT": literal_eval}, dtype=str)
    _vr = pd.read_csv('data_src/g4g/verbs.csv', converters={"OPT": literal_eval}, dtype=str)

    qt = _qt.sample(n=5)
    lg = _lg.sample(n=5)
    vr = _vr.sample(n=5)

    response = {
        "que": list(qt['QUE'].values) + list(lg['QUE'].values) + list(vr['QUE'].values),
        "opt": list(qt['OPT'].values) + list(lg['OPT'].values) + list(vr['OPT'].values),
        "ans": list(qt['ANS'].values) + list(lg['ANS'].values) + list(vr['ANS'].values)
    }
    print (response)
    return flask.jsonify(response)
# -----------------------------------------------------

# ---- admin services ---------------------------------
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if flask.request.method == 'GET':
        return flask.render_template('admin_login.html')

    email = flask.request.form['email']
    if email in list(users.keys()):
        if flask.request.form['password'] == users[email]['password']:
            user = User()
            user.id = email
            flask_login.login_user(user)
            return flask.redirect(flask.url_for('billboard'))
    return flask.redirect(flask.url_for('admin'))

@app.route('/billboard')
@flask_login.login_required
def billboard():
    return flask.render_template('job_billboard.html')

@app.route('/applicants/<jobid>')
@flask_login.login_required
def applicants(jobid):
    return flask.render_template('job_applicants.html', jobid=jobid)

@app.route('/admin/jobdetails/add', methods=['GET', 'POST'])
@flask_login.login_required
def jobdetails_add():
    if flask.request.method == 'POST':
        jobData = flask.request.json
        database.add_job(jobData)
        return flask.redirect(flask.url_for('billboard'))
    return flask.render_template('job_manage.html')

@app.route('/data/admin/getCandidates/<jobid>')
@flask_login.login_required
def getCandidates(jobid):
    allCandidates = database.getAllCandidates(jobid)
    return flask.jsonify(allCandidates) 

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for('admin'))

@login_manager.unauthorized_handler
def unauthorized_handler():
    return flask.redirect(flask.url_for('admin'))
# -------------------------------------------------------

if __name__ == "__main__":
    # for hot reload and tracking static files and templates
    from os import path, walk

    extra_dirs = ['templates/', 'static/']
    extra_files = extra_dirs[:]
    for extra_dir in extra_dirs:
        for dirname, dirs, files in walk(extra_dir):
            for filename in files:
                filename = path.join(dirname, filename)
                if path.isfile(filename):
                    extra_files.append(filename)

    # flask app run
    app.run(debug=True, extra_files=extra_files)