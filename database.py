# imports
import ibm_db
import ibm_db_dbi
import datetime
from k3y5 import DB2_DB, DB2_HOSTNAME, DB2_PWD, DB2_UID
import score
import resume_vault

# database connection string
dsn = "DATABASE=" + DB2_DB + ";HOSTNAME=" + DB2_HOSTNAME + ";PORT=50000;PROTOCOL=TCPIP;" + "UID=" + DB2_UID  + ";PWD=" + DB2_PWD + ";"

# add single candidate and calculate score
def add_candidate(newCandy, resumeFilePath):
    try:
        ideal_data = getJobReq(newCandy['jobId'])
    except:
        print('error fetching ideal data from JOBS_RAW')
        return False

    try:
        print('scoring candidate..')
        candyScore = score.score_candidate(newCandy, ideal_data)
        print('candidate scored!')
    except:
        print('Error scoring candidate')
        return False

    try:
        ibm_db_conn = ibm_db.connect(dsn, '', '')
        conn = ibm_db_dbi.Connection(ibm_db_conn)
        cursor = conn.cursor()
        print ("Connected to {0}".format(DB2_DB))
    except:
        print ("Couldn't Connect to Database")
        return False    

    try:
        cursor.execute("SELECT count(*) FROM JOB_" + str(newCandy['jobId']) + ";")
        candyCount = int(cursor.fetchall()[0][0])
        print("No. of current Applicants: ", candyCount)

        q1 = "INSERT INTO JOB_" + str(newCandy['jobId']) + " (CANDY_ID, CNAME, EMAIL, GITID, TWEETID, YOE, SKILLS, SELF_DESC, JOB_WANT_WHY, JOB_REQ_WHAT, PASSION, DATE_JOIN, OVERALL_SCORE)"
        q1 = q1 + " VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', {5}, '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}');".format(
            candyCount+1,
            newCandy['cname'],
            newCandy['email'],
            newCandy['gitId'],
            newCandy['tweetId'],
            newCandy['yoe'],
            newCandy['jobskills'],
            newCandy['self_desc'],
            newCandy['job_want_why'],
            newCandy['job_req_what'],
            newCandy['passion'],
            datetime.datetime.strptime(newCandy['date_join'], '%m-%d-%y'),
            candyScore
        )
        cursor.execute(q1)
        cursor.execute("SELECT * FROM JOB_" + str(newCandy['jobId']) + ";")
        for r in cursor.fetchall():
            print(r)
    except:
        print ("Candy Query Error!")
        ibm_db.close(ibm_db_conn)
        print ("connection closed")
        return False

    try:
        print ("uploading resume for " + str(newCandy['jobId']) + "_" + str(candyCount+1))
        resume_vault.upload_item(str(newCandy['jobId']) + "_" + str(candyCount+1), resumeFilePath)
    except:
        print ("resume upload error")
        ibm_db.close(ibm_db_conn)
        print ("connection closed")
        return False

    print ("candidate added succesfully")
    ibm_db.close(ibm_db_conn)
    print ("connection closed")
    return True


# add single job to jobs_raw and create job_<id> table
def add_job(jobData):
    try:
        ibm_db_conn = ibm_db.connect(dsn, '', '')
        conn = ibm_db_dbi.Connection(ibm_db_conn)
        cursor = conn.cursor()
        print ("Connected to {0}".format(DB2_DB))
    except:
        print ("Couldn't Connect to Database")
        return False

    try:
        cursor.execute("SELECT count(*) FROM JOBS_RAW;")
        jobCount = int(cursor.fetchall()[0][0])
        print("No. of current Job Postings: ", jobCount)

        q1 = "INSERT INTO JOBS_RAW (JOBID, JOBROLE, JOBLOC, JOBDESC, JOBYOE, JOBYOE_MUL, JOBSKILLS, JOBSKILLS_MUL, GITID, GIT_MUL, TWEETID, BIG5_MUL, VALUES_MUL, SELF_DESC, SELF_DESC_MUL, JOB_WANT_WHY, JOB_WANT_WHY_MUL, JOB_REQ_WHAT, JOB_REQ_WHAT_MUL, PASSION, PASSION_MUL, DATE_JOIN, DATE_JOIN_MUL)"
        q1 = q1 + " VALUES ({0}, '{1}', '{2}', '{3}', {4}, {5}, '{6}', {7}, '{8}', {9}, '{10}', {11}, {12}, '{13}', {14}, '{15}', {16}, '{17}', {18}, '{19}', {20}, '{21}', {22});".format(
            jobCount+1,
            jobData['jobrole'],
            jobData['location'],
            jobData['description'],
            jobData['yoe'],
            jobData['yoe_mul'],            
            jobData['jobskills'],
            jobData['jobskills_mul'],
            jobData['gitId'],
            jobData['gitId_mul'],
            jobData['tweetId'],
            jobData['big5_mul'],
            jobData['values_mul'],
            jobData['self_desc'],
            jobData['self_desc_mul'],
            jobData['job_want_why'],
            jobData['job_want_why_mul'],
            jobData['job_req_what'],
            jobData['job_req_what_mul'],
            jobData['passion'],
            jobData['passion_mul'],
            datetime.datetime.strptime(jobData['date_join'], '%m-%d-%y'),
            jobData['date_join_mul']
        )
        # print (q1)
        cursor.execute(q1)
        cursor.execute("SELECT * FROM JOBS_RAW;")
        for r in cursor.fetchall():
            print(r)
    except:
        print ("JOBS_RAW Query Error!")
        ibm_db.close(ibm_db_conn)
        print ("connection closed")
        return False

    try:
        q1 = "CREATE TABLE JOB_" + str(jobCount+1)
        q1 = q1 + " (CANDY_ID INT, CNAME VARCHAR(50), EMAIL VARCHAR(30), GITID VARCHAR(30), TWEETID VARCHAR(30), YOE INT, SKILLS VARCHAR(128), SELF_DESC VARCHAR(256), JOB_WANT_WHY VARCHAR(256), JOB_REQ_WHAT VARCHAR(256), PASSION VARCHAR(256), DATE_JOIN DATE, OVERALL_SCORE FLOAT);"
        cursor.execute(q1)
        cursor.execute("SELECT * FROM JOB_" + str(jobCount+1) + ";")
        for r in cursor.fetchall():
            print(r)
    except:
        print ("JOB_" + str(jobCount+1) + " Query Error!")
        ibm_db.close(ibm_db_conn)
        print ("connection closed")
        return False
    ibm_db.close(ibm_db_conn)
    print ('job added succesfully!')
    print ("connection closed")
    return jobCount+1

# return job data from db for given ID
def getJobReq(id):
    try:
        ibm_db_conn = ibm_db.connect(dsn, '', '')
        conn = ibm_db_dbi.Connection(ibm_db_conn)
        cursor = conn.cursor()
        print ("Connected to {0}".format(DB2_DB))
    except:
        print ("Couldn't Connect to Database")
        return False
    
    try:
        q1 = "SELECT GITID, GIT_MUL, BIG5_MUL, VALUES_MUL, SELF_DESC, SELF_DESC_MUL, JOB_WANT_WHY, JOB_WANT_WHY_MUL, JOB_REQ_WHAT, JOB_REQ_WHAT_MUL, PASSION, PASSION_MUL, JOBSKILLS, JOBSKILLS_MUL, JOBYOE, JOBYOE_MUL, DATE_JOIN, DATE_JOIN_MUL"
        q1 = q1 + " FROM JOBS_RAW WHERE JOBID = " + str(id) + ";"
        cursor.execute(q1)
        jobReq = cursor.fetchall()[0]
    except:
        print ('Error Querying JOB Requirement')
        ibm_db.close(ibm_db_conn)
        print ("connection closed")
        return False
    
    print('fetched job requirement')
    ibm_db.close(ibm_db_conn)
    print ("connection closed")
    return {
        'gitId': jobReq[0],
        'gitId_mul': jobReq[1],
        'big5_mul': jobReq[2],
        'values_mul': jobReq[3],
        'self_desc': jobReq[4],
        'self_desc_mul': jobReq[5],
        'job_want_why': jobReq[6],
        'job_want_why_mul': jobReq[7],
        'job_req_what': jobReq[8],
        'job_req_what_mul': jobReq[9],
        'passion': jobReq[10],
        'passion_mul': jobReq[11],
        'jobskills': jobReq[12],
        'jobskills_mul': jobReq[13],
        'yoe': jobReq[14],
        'yoe_mul': jobReq[15],
        'date_join': jobReq[16],
        'date_join_mul': jobReq[17]
    }

# return all job data from DB
def getAllJobs():
    try:
        ibm_db_conn = ibm_db.connect(dsn, '', '')
        conn = ibm_db_dbi.Connection(ibm_db_conn)
        cursor = conn.cursor()
        print ("Connected to {0}".format(DB2_DB))
    except:
        print ("Couldn't Connect to Database")
        return False
    
    try:
        q1 = "SELECT JOBID, JOBROLE, JOBLOC, JOBDESC, JOBSKILLS, JOBYOE"
        q1 = q1 + " FROM JOBS_RAW;"
        cursor.execute(q1)
        jobReq = cursor.fetchall()
        allJobs = []
        for j in jobReq:
            thisJob = {
                'id': j[0],
                'role': j[1],
                'loc': j[2],
                'des': j[3],
                'skill': j[4],
                'yoe': j[5]
            }
            allJobs.append(thisJob)
    except:
        print ('Error Querying JOB Requirements')
        ibm_db.close(ibm_db_conn)
        print ("connection closed")
        return False
    
    print('fetched job requirements')
    ibm_db.close(ibm_db_conn)
    print ("connection closed")
    return allJobs

# return all candidates for a given jobId
def getAllCandidates(id):
    try:
        ibm_db_conn = ibm_db.connect(dsn, '', '')
        conn = ibm_db_dbi.Connection(ibm_db_conn)
        cursor = conn.cursor()
        print ("Connected to {0}".format(DB2_DB))
    except:
        print ("Couldn't Connect to Database")
        return False

    try:
        q1 = "SELECT * FROM JOB_" + str(id)
        q1 = q1 + " ORDER BY OVERALL_SCORE DESC;"
        cursor.execute(q1)
        candyData = cursor.fetchall()
        allCandy = []
        for candy in candyData:
            thisCandy = {
                "id": candy[0],
                "name": candy[1],
                "email": candy[2],
                "score": candy[-1]
            }
            allCandy.append(thisCandy)
    except:
        print ('Error Querying Candidates')
        ibm_db.close(ibm_db_conn)
        print ("connection closed")
        return False
    
    print('fetched candidates')
    ibm_db.close(ibm_db_conn)
    print ("connection closed")
    return allCandy

# ---- mock functions -----------------------------------------------------------
# add_job({
#     'jobrole': "BACKEND DEVELOPER",
#     'location': "Delhi, India",
#     'description': "The job will have the require the recruit to work his/her way through complex infrastructure problems and build scalable and robust web applications.",
#     'yoe': 2,
#     'jobskills': "AI, Data Science, NoSQL",
#     'gitId': "mihirs16",
#     'tweetId': "@cached_cadet",
#     'self_desc': "Highly interested in unlocking answers through Data and Stats for questions in fields like Electronics, Robotics Healthcare, Media and Sports. I am currently learning and working in the field of Natural Language Processing and Deep Learning.",
#     'job_want_why': "Well, I believe Blueprint can help me develop my skills and offer me a fair paygrade for all my work",
#     'job_req_what': "I think I will be assigned to a team that develops software and I will handle the frontend.",
#     'passion': "I am passionate about my technology and the web.",
#     'date_join': "6-19-20",
#     'yoe_mul': 0.5,
#     'jobskills_mul': 0.5,
#     'gitId_mul': 0.5,
#     'big5_mul': 0.5,
#     'values_mul': 0.5,
#     'self_desc_mul': 0.5,
#     'job_want_why_mul': 0.5,
#     'job_req_what_mul': 0.5,
#     'passion_mul': 0.5,
#     'date_join_mul': 0.5
# })
# add_candidate({
#     "jobId": "2",
#     "cname": "Mihir Singh",
#     "email": "mihirs16@gmail.com",
#     "gitId": "mihirs16",
#     "tweetId": "@cached_cadet",
#     "yoe": 2,
#     "jobskills": "AI, Data Science, Frontend",
#     "self_desc": "Highly interested in unlocking answers through Data and Stats for questions in fields like Electronics, Robotics Healthcare, Media and Sports. I am currently learning and working in the field of Natural Language Processing and Deep Learning.",
#     "job_want_why": "Well, I believe Blueprint can help me develop my skills and offer me a fair paygrade for all my work",
#     "job_req_what": "I think I will be assigned to a team that develops software and I will handle the frontend.",
#     "passion": "I am passionate about my technology and the web.",
#     "date_join": "6-20-20"
# }, "data_src\\resume\\mihir_resume.pdf")
# print(getAllJobs())
# print(getAllCandidates(1))
# -------------------------------------------------------------------------------------------