import os
import pymysql
import createImmHIT
import createVideoHIT
import resultsImm
import resultsVid
from flask import *

__author__ = 'Edoardo Re'

app = Flask(__name__)

app.secret_key = "super secret key"

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

global percentage
percentage = []
for i in range(0, 200):
    percentage.append('')


@app.route("/")
def start():
    db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    # Prepare SQL query to INSERT a record into the database.
    sqlSelect = "SELECT * FROM metaimage"
    sqlSelect2 = "SELECT * FROM metavideo"

    try:
        cursor.execute(sqlSelect)
        result = cursor.fetchall()
        cursor.execute(sqlSelect2)
        result2 = cursor.fetchall()
        # if the raw not in the table already
        if len(result) == 0 and len(result2) == 0:
            return render_template("index.html")
        else:
            return redirect(url_for('home'))
    except:
        # Rollback in case there is any error
        db.rollback()
    # disconnect from server
    db.close()


@app.route("/uploadImm")
def uploadImm():
    return render_template("uploadImm.html")


@app.route("/uploadVid")
def uploadVid():
    return render_template("uploadVid.html")


@app.route("/uploadImage", methods=["POST"])
def uploadImage():
    db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    # Prepare SQL query to INSERT a record into the database.
    sqlSelect = "SELECT MAX(FOLDER) FROM metaimage"
    try:
        cursor.execute(sqlSelect)
        i = cursor.fetchall()
    except:
        # Rollback in case there is any error
        db.rollback()
    # disconnect from server
    db.close()
    if i[0][0] == None:
        s = ''
        folder = 0
    else:
        s = i[0][0] + 1
        folder = s
    target = os.path.join(APP_ROOT, 'images' + str(s) + '/')
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))
    print(request.files.getlist("file"))
    for upload in request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        destination = "/".join([target, filename])
        print ("Accept incoming file:", filename)
        print ("Save it to:", destination)
        upload.save(destination)
    description = request.form['description']
    db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    # Prepare SQL query to INSERT a record into the database.
    sqlInsert = "INSERT INTO metaimage(FOLDER, DESCRIPTION)VALUES" \
                "('%s', '%s')" % (folder, description)
    try:
        # Execute the SQL command
        cursor.execute(sqlInsert)
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()
    # disconnect from server
    db.close()
    createImmHIT.execute()
    return redirect(url_for('home'))


@app.route("/uploadVideo", methods=["POST"])
def uploadVideo():
    db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    # Prepare SQL query to INSERT a record into the database.
    sqlSelect = "SELECT MAX(FOLDER) FROM metavideo"
    try:
        cursor.execute(sqlSelect)
        i = cursor.fetchall()
    except:
        # Rollback in case there is any error
        db.rollback()
    # disconnect from server
    db.close()
    if i[0][0] == None:
        s = ''
        folder = 0
    else:
        s = i[0][0] + 1
        folder = s
    target = os.path.join(APP_ROOT, 'video' + str(s) + '/')
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))
    print(request.files.getlist("file"))
    for upload in request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        destination = "/".join([target, filename])
        print ("Accept incoming file:", filename)
        print ("Save it to:", destination)
        upload.save(destination)
    description = request.form['description']
    db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    # Prepare SQL query to INSERT a record into the database.
    sqlInsert = "INSERT INTO metavideo(FOLDER, DESCRIPTION)VALUES" \
                "('%s', '%s')" % (folder, description)
    try:
        # Execute the SQL command
        cursor.execute(sqlInsert)
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()
    # disconnect from server
    db.close()
    createVideoHIT.execute()
    return redirect(url_for('home'))


@app.route("/home")
def home():
    db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    # Prepare SQL query to INSERT a record into the database.
    sqlSelect = "SELECT DESCRIPTION FROM metaimage"
    sqlSelect2 = "SELECT DESCRIPTION FROM metavideo"
    try:
        cursor.execute(sqlSelect)
        resultimage = cursor.fetchall()
        cursor.execute(sqlSelect2)
        resultvideo = cursor.fetchall()
    except:
        # Rollback in case there is any error
        db.rollback()
    # disconnect from server
    db.close()
    result = []
    for i in range(0, 200):
        result.append('')
    i = 0
    for description in resultimage:
        result[i] = description[0]
        i += 1
    i = 100
    for description in resultvideo:
        result[i] = description[0]
        i += 1
    return render_template("home.html", label=result, percentage=percentage)


buttonNumber = []


@app.route("/homepost", methods=['POST'])
def homepost():
    global buttonNumber
    buttonNumber.append(request.form['button_number'])
    return jsonify(None)


@app.route("/homejson")
def homejson():
    words = {}
    refreshButtonNumber = buttonNumber.pop()
    refreshButtonNumber = int(refreshButtonNumber)
    if refreshButtonNumber < 100 and refreshButtonNumber >= 0:
        words['percent'] = str(resultsImm.execute(refreshButtonNumber)) + '%'
    elif refreshButtonNumber >= 100 and refreshButtonNumber < 200:
        words['percent'] = str(resultsVid.execute(refreshButtonNumber - 100)) + '%'
    percentage[refreshButtonNumber] = words['percent']
    return jsonify(words)


@app.route('/refreshall', methods=['POST'])
def refreshall():
    db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    # Prepare SQL query to INSERT a record into the database.
    sqlSelect = "SELECT DESCRIPTION FROM metaimage"
    sqlSelect2 = "SELECT DESCRIPTION FROM metavideo"
    try:
        cursor.execute(sqlSelect)
        resultimage = cursor.fetchall()
        cursor.execute(sqlSelect2)
        resultvideo = cursor.fetchall()
    except:
        # Rollback in case there is any error
        db.rollback()
    # disconnect from server
    db.close()
    result = []
    for i in range(0, 200):
        result.append('')
    i = 0
    for description in resultimage:
        result[i] = description[0]
        percentage[i] = str(resultsImm.execute(i)) + '%'
        i += 1
    i = 100
    for description in resultvideo:
        result[i] = description[0]
        percentage[i] = str(resultsVid.execute(i - 100)) + '%'
        i += 1
    return redirect(url_for('home'))


@app.route("/dashboard", methods=["POST"])
def dashboard():
    session['dashboard'] = request.form['dashboard']
    return render_template("dashboard.html")


@app.route('/dashboardnp')
def dashboardnp():
    return render_template("dashboard.html")


@app.route("/chartFile")
def chartFile():
    oldnumDashboard = session['dashboard']
    numDashboard = int(oldnumDashboard)
    if numDashboard < 100 and numDashboard >= 0:
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect = "SELECT DISTINCT IMAGE_FILE FROM `imagefile` WHERE FOLDER='%s'" % numDashboard
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
    elif numDashboard >= 100 and numDashboard < 200:
        numDashboard = numDashboard - 100
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect = "SELECT DISTINCT VIDEO_FILE FROM `videofile` WHERE FOLDER='%s'" % numDashboard
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
    return render_template("chartFile.html", result=result, data1='0', data2='0',
                           taskname='Task: ' + getTaskName(int(oldnumDashboard)))


def getTaskName(numDashboard):
    if numDashboard < 100 and numDashboard >= 0:
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect = "SELECT DESCRIPTION FROM `metaimage` WHERE FOLDER='%s'" % numDashboard
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
    elif numDashboard >= 100 and numDashboard < 200:
        numDashboard = numDashboard - 100
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect = "SELECT DESCRIPTION FROM `metavideo` WHERE FOLDER='%s'" % numDashboard
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
    return str(result[0][0])


@app.route('/chartFileP', methods=['POST'])
def chartFileP():
    oldnumDashboard = session['dashboard']
    numDashboard = int(oldnumDashboard)
    if numDashboard < 100 and numDashboard >= 0:
        imm = request.form['file']
        imm = str(imm)
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect = "SELECT QUALITY, WORKER_ID FROM `submitted` AS s, `imagefile` AS i WHERE s.HIT_ID=i.HIT_ID AND FOLDER='%s' AND IMAGE_FILE='%s'" % (
            numDashboard, imm)
        sqlSelect2 = "SELECT DISTINCT IMAGE_FILE FROM `imagefile` WHERE FOLDER='%s'" % numDashboard
        try:
            cursor.execute(sqlSelect)
            result1 = cursor.fetchall()
            cursor.execute(sqlSelect2)
            result = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
        file = imm
    elif numDashboard >= 100 and numDashboard < 200:
        numDashboard = numDashboard - 100
        vid = request.form['file']
        vid = str(vid)
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect2 = "SELECT QUALITY, WORKER_ID FROM `submitted` AS s, `videofile` AS i WHERE s.HIT_ID=i.HIT_ID AND FOLDER='%s' AND VIDEO_FILE='%s'" % (
            numDashboard, vid)
        sqlSelect = "SELECT DISTINCT VIDEO_FILE FROM `videofile` WHERE FOLDER='%s'" % numDashboard
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
            cursor.execute(sqlSelect2)
            result1 = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
        file = vid
    quality = []
    worker = []
    for tuple in result1:
        quality.append(tuple[0])
        worker.append(str(tuple[1]))
    return render_template("chartFile.html", result=result, data1=quality, data2=worker, file=file,
                           taskname='Task: ' + getTaskName(int(oldnumDashboard)))


@app.route("/chartFileWidget")
def chartFileWidget():
    oldnumDashboard = session['dashboard']
    numDashboard = int(oldnumDashboard)
    if numDashboard < 100 and numDashboard >= 0:
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect = "SELECT DISTINCT IMAGE_FILE FROM `imagefile` WHERE FOLDER='%s'" % numDashboard
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
    elif numDashboard >= 100 and numDashboard < 200:
        numDashboard = numDashboard - 100
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect = "SELECT DISTINCT VIDEO_FILE FROM `videofile` WHERE FOLDER='%s'" % numDashboard
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
    return render_template("chartFileWidget.html", result=result, data1='0', data2='0',
                           taskname='Task: ' + getTaskName(int(oldnumDashboard)))


@app.route('/chartFilePWidget', methods=['POST'])
def chartFilePWidget():
    oldnumDashboard = session['dashboard']
    numDashboard = int(oldnumDashboard)
    if numDashboard < 100 and numDashboard >= 0:
        imm = request.form['file']
        imm = str(imm)
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect = "SELECT QUALITY, WORKER_ID FROM `submitted` AS s, `imagefile` AS i WHERE s.HIT_ID=i.HIT_ID AND FOLDER='%s' AND IMAGE_FILE='%s'" % (
            numDashboard, imm)
        sqlSelect2 = "SELECT DISTINCT IMAGE_FILE FROM `imagefile` WHERE FOLDER='%s'" % numDashboard
        try:
            cursor.execute(sqlSelect)
            result1 = cursor.fetchall()
            cursor.execute(sqlSelect2)
            result = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
        file = imm
    elif numDashboard >= 100 and numDashboard < 200:
        numDashboard = numDashboard - 100
        vid = request.form['file']
        vid = str(vid)
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect2 = "SELECT QUALITY, WORKER_ID FROM `submitted` AS s, `videofile` AS i WHERE s.HIT_ID=i.HIT_ID AND FOLDER='%s' AND VIDEO_FILE='%s'" % (
            numDashboard, vid)
        sqlSelect = "SELECT DISTINCT VIDEO_FILE FROM `videofile` WHERE FOLDER='%s'" % numDashboard
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
            cursor.execute(sqlSelect2)
            result1 = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
        file = vid
    quality = []
    worker = []
    for tuple in result1:
        quality.append(tuple[0])
        worker.append(str(tuple[1]))
    return render_template("chartFileWidget.html", result=result, data1=quality, data2=worker, file=file,
                           taskname='Task: ' + getTaskName(int(oldnumDashboard)))


@app.route('/chartWorker')
def chartWorker():
    oldnumDashboard = session['dashboard']
    numDashboard = int(oldnumDashboard)
    if numDashboard < 100 and numDashboard >= 0:
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect = "SELECT DISTINCT WORKER_ID FROM `submitted` AS s,`imagefile` AS i WHERE i.FOLDER='%s' AND s.HIT_ID=i.HIT_ID" % numDashboard
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
    elif numDashboard >= 100 and numDashboard < 200:
        numDashboard = numDashboard - 100
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect = "SELECT DISTINCT WORKER_ID FROM `submitted` AS s,`videofile` AS i WHERE i.FOLDER='%s' AND s.HIT_ID=i.HIT_ID" % numDashboard
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
    return render_template("chartWorker.html", result=result, data1='0', data2='0',
                           taskname='Task: ' + getTaskName(int(oldnumDashboard)))


@app.route('/chartWorkerP', methods=['POST'])
def chartWorkerP():
    oldnumDashboard = session['dashboard']
    numDashboard = int(oldnumDashboard)
    workerid = request.form['worker_id']
    workerid = str(workerid)
    if numDashboard < 100 and numDashboard >= 0:
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect2 = "SELECT QUALITY, IMAGE_FILE FROM `submitted` AS s, `imagefile` AS i WHERE s.HIT_ID=i.HIT_ID AND FOLDER='%s' AND WORKER_ID='%s'" % (
            numDashboard, workerid)
        sqlSelect = "SELECT DISTINCT WORKER_ID FROM `submitted` AS s,`imagefile` AS i WHERE i.FOLDER='%s' AND s.HIT_ID=i.HIT_ID" % numDashboard
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
            cursor.execute(sqlSelect2)
            result1 = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
    elif numDashboard >= 100 and numDashboard < 200:
        numDashboard = numDashboard - 100
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect2 = "SELECT QUALITY, VIDEO_FILE FROM `submitted` AS s, `videofile` AS i WHERE s.HIT_ID=i.HIT_ID AND FOLDER='%s' AND WORKER_ID='%s'" % (
            numDashboard, workerid)
        sqlSelect = "SELECT DISTINCT WORKER_ID FROM `submitted` AS s,`videofile` AS i WHERE i.FOLDER='%s' AND s.HIT_ID=i.HIT_ID" % numDashboard
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
            cursor.execute(sqlSelect2)
            result1 = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
    quality = []
    file = []
    for tuple in result1:
        quality.append(tuple[0])
        file.append(str(tuple[1])[53:])
    return render_template("chartWorker.html", result=result, data1=quality, data2=file, worker=workerid,
                           taskname='Task: ' + getTaskName(int(oldnumDashboard)))


@app.route('/chartWorkerWidget')
def chartWorkerWidget():
    oldnumDashboard = session['dashboard']
    numDashboard = int(oldnumDashboard)
    if numDashboard < 100 and numDashboard >= 0:
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect = "SELECT DISTINCT WORKER_ID FROM `submitted` AS s,`imagefile` AS i WHERE i.FOLDER='%s' AND s.HIT_ID=i.HIT_ID" % numDashboard
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
    elif numDashboard >= 100 and numDashboard < 200:
        numDashboard = numDashboard - 100
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect = "SELECT DISTINCT WORKER_ID FROM `submitted` AS s,`videofile` AS i WHERE i.FOLDER='%s' AND s.HIT_ID=i.HIT_ID" % numDashboard
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
    return render_template("chartWorkerWidget.html", result=result, data1='0', data2='0',
                           taskname='Task: ' + getTaskName(int(oldnumDashboard)))


@app.route('/chartWorkerPWidget', methods=['POST'])
def chartWorkerPWidget():
    oldnumDashboard = session['dashboard']
    numDashboard = int(oldnumDashboard)
    workerid = request.form['worker_id']
    workerid = str(workerid)
    if numDashboard < 100 and numDashboard >= 0:
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect2 = "SELECT QUALITY, IMAGE_FILE FROM `submitted` AS s, `imagefile` AS i WHERE s.HIT_ID=i.HIT_ID AND FOLDER='%s' AND WORKER_ID='%s'" % (
            numDashboard, workerid)
        sqlSelect = "SELECT DISTINCT WORKER_ID FROM `submitted` AS s,`imagefile` AS i WHERE i.FOLDER='%s' AND s.HIT_ID=i.HIT_ID" % numDashboard
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
            cursor.execute(sqlSelect2)
            result1 = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
    elif numDashboard >= 100 and numDashboard < 200:
        numDashboard = numDashboard - 100
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect2 = "SELECT QUALITY, VIDEO_FILE FROM `submitted` AS s, `videofile` AS i WHERE s.HIT_ID=i.HIT_ID AND FOLDER='%s' AND WORKER_ID='%s'" % (
            numDashboard, workerid)
        sqlSelect = "SELECT DISTINCT WORKER_ID FROM `submitted` AS s,`videofile` AS i WHERE i.FOLDER='%s' AND s.HIT_ID=i.HIT_ID" % numDashboard
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
            cursor.execute(sqlSelect2)
            result1 = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
    quality = []
    file = []
    for tuple in result1:
        quality.append(tuple[0])
        file.append(str(tuple[1])[53:])
    return render_template("chartWorkerWidget.html", result=result, data1=quality, data2=file, worker=workerid,
                           taskname='Task: ' + getTaskName(int(oldnumDashboard)))


@app.route('/radar')
def radar():
    oldnumDashboard = session['dashboard']
    numDashboard = int(oldnumDashboard)
    if numDashboard < 100 and numDashboard >= 0:
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect = "SELECT DISTINCT WORKER_ID FROM `submitted` AS s,`imagefile` AS i WHERE i.FOLDER='%s' AND s.HIT_ID=i.HIT_ID" % numDashboard
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
    elif numDashboard >= 100 and numDashboard < 200:
        numDashboard = numDashboard - 100
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect = "SELECT DISTINCT WORKER_ID FROM `submitted` AS s,`videofile` AS i WHERE i.FOLDER='%s' AND s.HIT_ID=i.HIT_ID" % numDashboard
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
    return render_template("radar.html", result=result, data1='0', data2='0',
                           taskname='Task: ' + getTaskName(int(oldnumDashboard)))


@app.route('/radarP', methods=['POST'])
def radarP():
    oldnumDashboard = session['dashboard']
    numDashboard = int(oldnumDashboard)
    workerid1 = request.form['worker_id1']
    workerid2 = request.form['worker_id2']
    workerid1 = str(workerid1)
    workerid2 = str(workerid2)
    if numDashboard < 100 and numDashboard >= 0:
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect2 = "SELECT QUALITY FROM `submitted` AS s, `imagefile` AS i WHERE s.HIT_ID=i.HIT_ID AND FOLDER='%s' AND WORKER_ID='%s'" % (
            numDashboard, workerid1)
        sqlSelect3 = "SELECT QUALITY FROM `submitted` AS s, `imagefile` AS i WHERE s.HIT_ID=i.HIT_ID AND FOLDER='%s' AND WORKER_ID='%s'" % (
            numDashboard, workerid2)
        sqlSelect = "SELECT DISTINCT WORKER_ID FROM `submitted` AS s,`imagefile` AS i WHERE i.FOLDER='%s' AND s.HIT_ID=i.HIT_ID" % numDashboard
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
            cursor.execute(sqlSelect2)
            result1 = cursor.fetchall()
            cursor.execute(sqlSelect3)
            result2 = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
    elif numDashboard >= 100 and numDashboard < 200:
        numDashboard = numDashboard - 100
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect2 = "SELECT QUALITY FROM `submitted` AS s, `videofile` AS i WHERE s.HIT_ID=i.HIT_ID AND FOLDER='%s' AND WORKER_ID='%s'" % (
            numDashboard, workerid1)
        sqlSelect3 = "SELECT QUALITY FROM `submitted` AS s, `videofile` AS i WHERE s.HIT_ID=i.HIT_ID AND FOLDER='%s' AND WORKER_ID='%s'" % (
            numDashboard, workerid2)
        sqlSelect = "SELECT DISTINCT WORKER_ID FROM `submitted` AS s,`videofile` AS i WHERE i.FOLDER='%s' AND s.HIT_ID=i.HIT_ID" % numDashboard
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
            cursor.execute(sqlSelect2)
            result1 = cursor.fetchall()
            cursor.execute(sqlSelect3)
            result2 = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
    quality1 = []
    for tuple in result1:
        quality1.append(tuple[0])
    quality2 = []
    for tuple in result2:
        quality2.append(tuple[0])
    return render_template("radar.html", result=result, data1=quality1, data2=quality2, workerid1=workerid1,
                           workerid2=workerid2, taskname='Task: ' + getTaskName(int(oldnumDashboard)))


@app.route('/radarWidget')
def radarWidget():
    oldnumDashboard = session['dashboard']
    numDashboard = int(oldnumDashboard)
    if numDashboard < 100 and numDashboard >= 0:
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect = "SELECT DISTINCT WORKER_ID FROM `submitted` AS s,`imagefile` AS i WHERE i.FOLDER='%s' AND s.HIT_ID=i.HIT_ID" % numDashboard
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
    elif numDashboard >= 100 and numDashboard < 200:
        numDashboard = numDashboard - 100
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect = "SELECT DISTINCT WORKER_ID FROM `submitted` AS s,`videofile` AS i WHERE i.FOLDER='%s' AND s.HIT_ID=i.HIT_ID" % numDashboard
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
    return render_template("radarWidget.html", result=result, data1='0', data2='0',
                           taskname='Task: ' + getTaskName(int(oldnumDashboard)))


@app.route('/radarPWidget', methods=['POST'])
def radarPWidget():
    oldnumDashboard = session['dashboard']
    numDashboard = int(oldnumDashboard)
    workerid1 = request.form['worker_id1']
    workerid2 = request.form['worker_id2']
    workerid1 = str(workerid1)
    workerid2 = str(workerid2)
    if numDashboard < 100 and numDashboard >= 0:
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect2 = "SELECT QUALITY FROM `submitted` AS s, `imagefile` AS i WHERE s.HIT_ID=i.HIT_ID AND FOLDER='%s' AND WORKER_ID='%s'" % (
            numDashboard, workerid1)
        sqlSelect3 = "SELECT QUALITY FROM `submitted` AS s, `imagefile` AS i WHERE s.HIT_ID=i.HIT_ID AND FOLDER='%s' AND WORKER_ID='%s'" % (
            numDashboard, workerid2)
        sqlSelect = "SELECT DISTINCT WORKER_ID FROM `submitted` AS s,`imagefile` AS i WHERE i.FOLDER='%s' AND s.HIT_ID=i.HIT_ID" % numDashboard
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
            cursor.execute(sqlSelect2)
            result1 = cursor.fetchall()
            cursor.execute(sqlSelect3)
            result2 = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
    elif numDashboard >= 100 and numDashboard < 200:
        numDashboard = numDashboard - 100
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect2 = "SELECT QUALITY FROM `submitted` AS s, `videofile` AS i WHERE s.HIT_ID=i.HIT_ID AND FOLDER='%s' AND WORKER_ID='%s'" % (
            numDashboard, workerid1)
        sqlSelect3 = "SELECT QUALITY FROM `submitted` AS s, `videofile` AS i WHERE s.HIT_ID=i.HIT_ID AND FOLDER='%s' AND WORKER_ID='%s'" % (
            numDashboard, workerid2)
        sqlSelect = "SELECT DISTINCT WORKER_ID FROM `submitted` AS s,`videofile` AS i WHERE i.FOLDER='%s' AND s.HIT_ID=i.HIT_ID" % numDashboard
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
            cursor.execute(sqlSelect2)
            result1 = cursor.fetchall()
            cursor.execute(sqlSelect3)
            result2 = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
    quality1 = []
    for tuple in result1:
        quality1.append(tuple[0])
    quality2 = []
    for tuple in result2:
        quality2.append(tuple[0])
    return render_template("radarWidget.html", result=result, data1=quality1, data2=quality2, workerid1=workerid1,
                           workerid2=workerid2, taskname='Task: ' + getTaskName(int(oldnumDashboard)))


@app.route("/cake")
def cake():
    oldnumDashboard = session['dashboard']
    numDashboard = int(oldnumDashboard)
    if numDashboard < 100 and numDashboard >= 0:
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect = "SELECT DISTINCT IMAGE_FILE FROM `imagefile` WHERE FOLDER='%s'" % numDashboard
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
    elif numDashboard >= 100 and numDashboard < 200:
        numDashboard = numDashboard - 100
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect = "SELECT DISTINCT VIDEO_FILE FROM `videofile` WHERE FOLDER='%s'" % numDashboard
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
    return render_template("cake.html", result=result, data1='0', data2='0',
                           taskname='Task: ' + getTaskName(int(oldnumDashboard)))


@app.route('/cakeP', methods=['POST'])
def cakeP():
    oldnumDashboard = session['dashboard']
    numDashboard = int(oldnumDashboard)
    if numDashboard < 100 and numDashboard >= 0:
        imm = request.form['file']
        imm = str(imm)
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect = "SELECT QUALITY FROM `submitted` AS s, `imagefile` AS i WHERE s.HIT_ID=i.HIT_ID AND FOLDER='%s' AND IMAGE_FILE='%s'" % (
            numDashboard, imm)
        sqlSelect2 = "SELECT DISTINCT IMAGE_FILE FROM `imagefile` WHERE FOLDER='%s'" % numDashboard
        try:
            cursor.execute(sqlSelect)
            result1 = cursor.fetchall()
            cursor.execute(sqlSelect2)
            result = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
        file = imm
    elif numDashboard >= 100 and numDashboard < 200:
        numDashboard = numDashboard - 100
        vid = request.form['file']
        vid = str(vid)
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect2 = "SELECT QUALITY FROM `submitted` AS s, `videofile` AS i WHERE s.HIT_ID=i.HIT_ID AND FOLDER='%s' AND VIDEO_FILE='%s'" % (
            numDashboard, vid)
        sqlSelect = "SELECT DISTINCT VIDEO_FILE FROM `videofile` WHERE FOLDER='%s'" % numDashboard
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
            cursor.execute(sqlSelect2)
            result1 = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
        file = vid
    quality = []
    for tuple in result1:
        quality.append(tuple[0])
    return render_template("cake.html", result=result, data1=quality, file=file,
                           taskname='Task: ' + getTaskName(int(oldnumDashboard)))


@app.route("/cakeWidget")
def cakeWidget():
    oldnumDashboard = session['dashboard']
    numDashboard = int(oldnumDashboard)
    if numDashboard < 100 and numDashboard >= 0:
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect = "SELECT DISTINCT IMAGE_FILE FROM `imagefile` WHERE FOLDER='%s'" % numDashboard
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
    elif numDashboard >= 100 and numDashboard < 200:
        numDashboard = numDashboard - 100
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect = "SELECT DISTINCT VIDEO_FILE FROM `videofile` WHERE FOLDER='%s'" % numDashboard
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
    return render_template("cakeWidget.html", result=result, data1='0', data2='0',
                           taskname='Task: ' + getTaskName(int(oldnumDashboard)))


@app.route('/cakePWidget', methods=['POST'])
def cakePWidget():
    oldnumDashboard = session['dashboard']
    numDashboard = int(oldnumDashboard)
    if numDashboard < 100 and numDashboard >= 0:
        imm = request.form['file']
        imm = str(imm)
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect = "SELECT QUALITY FROM `submitted` AS s, `imagefile` AS i WHERE s.HIT_ID=i.HIT_ID AND FOLDER='%s' AND IMAGE_FILE='%s'" % (
            numDashboard, imm)
        sqlSelect2 = "SELECT DISTINCT IMAGE_FILE FROM `imagefile` WHERE FOLDER='%s'" % numDashboard
        try:
            cursor.execute(sqlSelect)
            result1 = cursor.fetchall()
            cursor.execute(sqlSelect2)
            result = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
        file = imm
    elif numDashboard >= 100 and numDashboard < 200:
        numDashboard = numDashboard - 100
        vid = request.form['file']
        vid = str(vid)
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect2 = "SELECT QUALITY FROM `submitted` AS s, `videofile` AS i WHERE s.HIT_ID=i.HIT_ID AND FOLDER='%s' AND VIDEO_FILE='%s'" % (
            numDashboard, vid)
        sqlSelect = "SELECT DISTINCT VIDEO_FILE FROM `videofile` WHERE FOLDER='%s'" % numDashboard
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
            cursor.execute(sqlSelect2)
            result1 = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
        file = vid
    quality = []
    for tuple in result1:
        quality.append(tuple[0])
    return render_template("cakeWidget.html", result=result, data1=quality, file=file,
                           taskname='Task: ' + getTaskName(int(oldnumDashboard)))


@app.route('/topUser')
def topUser():
    oldnumDashboard = session['dashboard']
    numDashboard = int(oldnumDashboard)
    if numDashboard < 100 and numDashboard >= 0:
        typefile = 'Image' + str(numDashboard)
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect = "SELECT DISTINCT WORKER_ID, COUNT(s.HIT_ID) AS NUM FROM `submitted` AS s, `imagefile` " \
                    "AS i WHERE FOLDER='%s' AND i.HIT_ID=s.HIT_ID GROUP BY WORKER_ID ORDER BY NUM DESC" % numDashboard
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
    elif numDashboard >= 100 and numDashboard < 200:
        numDashboard = numDashboard - 100
        typefile = 'Video' + str(numDashboard)
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect = "SELECT DISTINCT WORKER_ID, COUNT(s.HIT_ID) AS NUM FROM `submitted` AS s, `videofile` " \
                    "AS i WHERE FOLDER='%s' AND i.HIT_ID=s.HIT_ID GROUP BY WORKER_ID ORDER BY NUM DESC" % numDashboard
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
    workerid = []
    count = []
    for tuple in result:
        workerid.append(str(tuple[0]))
        count.append(tuple[1])
    return render_template("topUser.html", data1=workerid, data2=count, file=typefile,
                           taskname='Task: ' + getTaskName(int(oldnumDashboard)))


@app.route('/topUserWidget')
def topUserWidget():
    oldnumDashboard = session['dashboard']
    numDashboard = int(oldnumDashboard)
    if numDashboard < 100 and numDashboard >= 0:
        typefile = 'Image' + str(numDashboard)
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect = "SELECT DISTINCT WORKER_ID, COUNT(s.HIT_ID) AS NUM FROM `submitted` AS s, `imagefile` " \
                    "AS i WHERE FOLDER='%s' AND i.HIT_ID=s.HIT_ID GROUP BY WORKER_ID ORDER BY NUM DESC" % numDashboard
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
    elif numDashboard >= 100 and numDashboard < 200:
        numDashboard = numDashboard - 100
        typefile = 'Video' + str(numDashboard)
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect = "SELECT DISTINCT WORKER_ID, COUNT(s.HIT_ID) AS NUM FROM `submitted` AS s, `videofile` " \
                    "AS i WHERE FOLDER='%s' AND i.HIT_ID=s.HIT_ID GROUP BY WORKER_ID ORDER BY NUM DESC" % numDashboard
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
    workerid = []
    count = []
    for tuple in result:
        workerid.append(str(tuple[0]))
        count.append(tuple[1])
    return render_template("topUserWidget.html", data1=workerid, data2=count, file=typefile,
                           taskname='Task: ' + getTaskName(int(oldnumDashboard)))


@app.route('/scatter')
def scatter():
    oldnumDashboard = session['dashboard']
    numDashboard = int(oldnumDashboard)
    if numDashboard < 100 and numDashboard >= 0:
        typefile = 'Image' + str(numDashboard)
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect = "SELECT DISTINCT WORKER_ID, COUNT(s.HIT_ID) AS NUM, AVG(QUALITY) AS AVERAGE FROM `submitted` AS s, `imagefile` " \
                    "AS i WHERE FOLDER='%s' AND i.HIT_ID=s.HIT_ID GROUP BY WORKER_ID ORDER BY NUM DESC" % numDashboard
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
    elif numDashboard >= 100 and numDashboard < 200:
        numDashboard = numDashboard - 100
        typefile = 'Video' + str(numDashboard)
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect = "SELECT DISTINCT WORKER_ID, COUNT(s.HIT_ID) AS NUM, AVG(QUALITY) AS AVERAGE FROM `submitted` AS s, `videofile` " \
                    "AS i WHERE FOLDER='%s' AND i.HIT_ID=s.HIT_ID GROUP BY WORKER_ID ORDER BY NUM DESC" % numDashboard
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
    workerid = []
    count = []
    average = []
    for triple in result:
        workerid.append(str(triple[0]))
        count.append(triple[1])
        average.append(triple[2])
    return render_template("scatter.html", data1=workerid, data2=count, data3=average, file=typefile,
                           taskname='Task: ' + getTaskName(int(oldnumDashboard)))


@app.route('/scatterWidget')
def scatterWidget():
    oldnumDashboard = session['dashboard']
    numDashboard = int(oldnumDashboard)
    if numDashboard < 100 and numDashboard >= 0:
        typefile = 'Image' + str(numDashboard)
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect = "SELECT DISTINCT WORKER_ID, COUNT(s.HIT_ID) AS NUM, AVG(QUALITY) AS AVERAGE FROM `submitted` AS s, `imagefile` " \
                    "AS i WHERE FOLDER='%s' AND i.HIT_ID=s.HIT_ID GROUP BY WORKER_ID ORDER BY NUM DESC" % numDashboard
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
    elif numDashboard >= 100 and numDashboard < 200:
        numDashboard = numDashboard - 100
        typefile = 'Video' + str(numDashboard)
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect = "SELECT DISTINCT WORKER_ID, COUNT(s.HIT_ID) AS NUM, AVG(QUALITY) AS AVERAGE FROM `submitted` AS s, `videofile` " \
                    "AS i WHERE FOLDER='%s' AND i.HIT_ID=s.HIT_ID GROUP BY WORKER_ID ORDER BY NUM DESC" % numDashboard
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
    workerid = []
    count = []
    average = []
    for triple in result:
        workerid.append(str(triple[0]))
        count.append(triple[1])
        average.append(triple[2])
    return render_template("scatterWidget.html", data1=workerid, data2=count, data3=average, file=typefile,
                           taskname='Task: ' + getTaskName(int(oldnumDashboard)))


@app.route('/randomChart')
def randomChart():
    oldnumDashboard = session['dashboard']
    numDashboard = int(oldnumDashboard)
    if numDashboard < 100 and numDashboard >= 0:
        typefile = 'Image' + str(numDashboard)
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect = "SELECT DISTINCT WORKER_ID, COUNT(DISTINCT SEX) AS COUNTSEX, COUNT(DISTINCT AGE) AS COUNTAGE" \
                    " FROM `submitted` AS s, `imagefile` AS i WHERE FOLDER='%s' AND s.HIT_ID=i.HIT_ID GROUP BY WORKER_ID ORDER BY COUNTAGE DESC, COUNTSEX" % numDashboard
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
    elif numDashboard >= 100 and numDashboard < 200:
        numDashboard = numDashboard - 100
        typefile = 'Video' + str(numDashboard)
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect = "SELECT DISTINCT WORKER_ID, COUNT(DISTINCT SEX) AS COUNTSEX, COUNT(DISTINCT AGE) AS COUNTAGE" \
                    " FROM `submitted` AS s, `videofile` AS i WHERE FOLDER='%s' AND s.HIT_ID=i.HIT_ID GROUP BY WORKER_ID ORDER BY COUNTAGE DESC, COUNTSEX" % numDashboard
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
    workerid = []
    count = []
    for triple in result:
        if (triple[1] > 1 or triple[2] > 1):
            workerid.append(str(triple[0]))
            if triple[1] == 1:
                count.append(triple[2])
            elif triple[2] == 1:
                count.append(triple[1])
            else:
                count.append(triple[1] + triple[2])
    return render_template("randomChart.html", data1=workerid, data2=count, file=typefile,
                           taskname='Task: ' + getTaskName(int(oldnumDashboard)))


@app.route('/randomChartWidget')
def randomChartWidget():
    oldnumDashboard = session['dashboard']
    numDashboard = int(oldnumDashboard)
    if numDashboard < 100 and numDashboard >= 0:
        typefile = 'Image' + str(numDashboard)
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect = "SELECT DISTINCT WORKER_ID, COUNT(DISTINCT SEX) AS COUNTSEX, COUNT(DISTINCT AGE) AS COUNTAGE" \
                    " FROM `submitted` AS s, `imagefile` AS i WHERE FOLDER='%s' AND s.HIT_ID=i.HIT_ID GROUP BY WORKER_ID ORDER BY COUNTAGE DESC, COUNTSEX" % numDashboard
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
    elif numDashboard >= 100 and numDashboard < 200:
        numDashboard = numDashboard - 100
        typefile = 'Video' + str(numDashboard)
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect = "SELECT DISTINCT WORKER_ID, COUNT(DISTINCT SEX) AS COUNTSEX, COUNT(DISTINCT AGE) AS COUNTAGE" \
                    " FROM `submitted` AS s, `videofile` AS i WHERE FOLDER='%s' AND s.HIT_ID=i.HIT_ID GROUP BY WORKER_ID ORDER BY COUNTAGE DESC, COUNTSEX" % numDashboard
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
    workerid = []
    count = []
    for triple in result:
        if (triple[1] > 1 or triple[2] > 1):
            workerid.append(str(triple[0]))
            if triple[1] == 1:
                count.append(triple[2])
            elif triple[2] == 1:
                count.append(triple[1])
            else:
                count.append(triple[1] + triple[2])
    return render_template("randomChartWidget.html", data1=workerid, data2=count, file=typefile,
                           taskname='Task: ' + getTaskName(int(oldnumDashboard)))


@app.route('/sexChart')
def sexChart():
    numDashboard = session['dashboard']
    numDashboard = int(numDashboard)
    return render_template("sexChart.html", data1='0', sex='', taskname='Task: ' + getTaskName(numDashboard))


@app.route('/sexChartP', methods=['POST'])
def sexChartP():
    oldnumDashboard = session['dashboard']
    numDashboard = int(oldnumDashboard)
    sex = request.form['sex']
    sex = str(sex)
    if numDashboard < 100 and numDashboard >= 0:
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect = "SELECT QUALITY FROM `submitted` AS s, `imagefile` AS i WHERE s.HIT_ID=i.HIT_ID AND FOLDER='%s' AND SEX='%s'" % (
            numDashboard, sex)
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
    elif numDashboard >= 100 and numDashboard < 200:
        numDashboard = numDashboard - 100
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect = "SELECT QUALITY FROM `submitted` AS s, `videofile` AS i WHERE s.HIT_ID=i.HIT_ID AND FOLDER='%s' AND SEX='%s'" % (
            numDashboard, sex)
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
    quality = []
    for tuple in result:
        quality.append(tuple[0])
    return render_template("sexChart.html", data1=quality, sex=sex,
                           taskname='Task: ' + getTaskName(int(oldnumDashboard)))


@app.route('/sexChartWidget')
def sexChartWidget():
    numDashboard = session['dashboard']
    numDashboard = int(numDashboard)
    return render_template("sexChartWidget.html", data1='0', sex='', taskname='Task: ' + getTaskName(numDashboard))


@app.route('/sexChartPWidget', methods=['POST'])
def sexChartPWidget():
    oldnumDashboard = session['dashboard']
    numDashboard = int(oldnumDashboard)
    sex = request.form['sex']
    sex = str(sex)
    if numDashboard < 100 and numDashboard >= 0:
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect = "SELECT QUALITY FROM `submitted` AS s, `imagefile` AS i WHERE s.HIT_ID=i.HIT_ID AND FOLDER='%s' AND SEX='%s'" % (
            numDashboard, sex)
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
    elif numDashboard >= 100 and numDashboard < 200:
        numDashboard = numDashboard - 100
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect = "SELECT QUALITY FROM `submitted` AS s, `videofile` AS i WHERE s.HIT_ID=i.HIT_ID AND FOLDER='%s' AND SEX='%s'" % (
            numDashboard, sex)
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
    quality = []
    for tuple in result:
        quality.append(tuple[0])
    return render_template("sexChartWidget.html", data1=quality, sex=sex,
                           taskname='Task: ' + getTaskName(int(oldnumDashboard)))


@app.route('/resolution')
def resolution():
    oldnumDashboard = session['dashboard']
    numDashboard = int(oldnumDashboard)
    if numDashboard < 100 and numDashboard >= 0:
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect = "SELECT RESOLUTION FROM `submitted` AS s, `imagefile` AS i WHERE s.HIT_ID=i.HIT_ID AND FOLDER='%s' GROUP BY WORKER_ID" % (
            numDashboard)
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
        file = 'Image' + str(numDashboard)
    elif numDashboard >= 100 and numDashboard < 200:
        numDashboard = numDashboard - 100
        file = 'Video' + str(numDashboard)
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect = "SELECT RESOLUTION FROM `submitted` AS s, `videofile` AS i WHERE s.HIT_ID=i.HIT_ID AND FOLDER='%s' GROUP BY WORKER_ID" % (
            numDashboard)
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
    resolution = []
    for tuple in result:
        resolution.append(tuple[0])
    return render_template("resolution.html", data1=resolution, file=file,
                           taskname='Task: ' + getTaskName(int(oldnumDashboard)))


@app.route('/resolutionWidget')
def resolutionWidget():
    oldnumDashboard = session['dashboard']
    numDashboard = int(oldnumDashboard)
    if numDashboard < 100 and numDashboard >= 0:
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect = "SELECT RESOLUTION FROM `submitted` AS s, `imagefile` AS i WHERE s.HIT_ID=i.HIT_ID AND FOLDER='%s' GROUP BY WORKER_ID" % (
            numDashboard)
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
        file = 'Image' + str(numDashboard)
    elif numDashboard >= 100 and numDashboard < 200:
        numDashboard = numDashboard - 100
        file = 'Video' + str(numDashboard)
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect = "SELECT RESOLUTION FROM `submitted` AS s, `videofile` AS i WHERE s.HIT_ID=i.HIT_ID AND FOLDER='%s' GROUP BY WORKER_ID" % (
            numDashboard)
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
    resolution = []
    for tuple in result:
        resolution.append(tuple[0])
    return render_template("resolutionWidget.html", data1=resolution, file=file,
                           taskname='Task: ' + getTaskName(int(oldnumDashboard)))


@app.route('/age')
def age():
    oldnumDashboard = session['dashboard']
    numDashboard = int(oldnumDashboard)
    if numDashboard < 100 and numDashboard >= 0:
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect = "SELECT AGE FROM `submitted` AS s, `imagefile` AS i WHERE s.HIT_ID=i.HIT_ID AND FOLDER='%s' GROUP BY WORKER_ID" % (
            numDashboard)
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
        file = 'Image' + str(numDashboard)
    elif numDashboard >= 100 and numDashboard < 200:
        numDashboard = numDashboard - 100
        file = 'Video' + str(numDashboard)
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect = "SELECT AGE FROM `submitted` AS s, `videofile` AS i WHERE s.HIT_ID=i.HIT_ID AND FOLDER='%s' GROUP BY WORKER_ID" % (
            numDashboard)
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
    age = []
    for tuple in result:
        age.append(tuple[0])
    return render_template("age.html", data1=age, file=file, taskname='Task: ' + getTaskName(int(oldnumDashboard)))


@app.route('/ageWidget')
def ageWidget():
    oldnumDashboard = session['dashboard']
    numDashboard = int(oldnumDashboard)
    if numDashboard < 100 and numDashboard >= 0:
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect = "SELECT AGE FROM `submitted` AS s, `imagefile` AS i WHERE s.HIT_ID=i.HIT_ID AND FOLDER='%s' GROUP BY WORKER_ID" % (
            numDashboard)
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
        file = 'Image' + str(numDashboard)
    elif numDashboard >= 100 and numDashboard < 200:
        numDashboard = numDashboard - 100
        file = 'Video' + str(numDashboard)
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect = "SELECT AGE FROM `submitted` AS s, `videofile` AS i WHERE s.HIT_ID=i.HIT_ID AND FOLDER='%s' GROUP BY WORKER_ID" % (
            numDashboard)
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
    age = []
    for tuple in result:
        age.append(tuple[0])
    return render_template("ageWidget.html", data1=age, file=file,
                           taskname='Task: ' + getTaskName(int(oldnumDashboard)))


@app.route('/personal')
def personal():
    session['sel1'] = 1
    session['sel2'] = 2
    session['sel3'] = 3
    pages = ['/chartFileWidget', '/chartWorkerWidget', '/radarWidget', '/cakeWidget',
             '/topUserWidget', '/scatterWidget', '/randomChartWidget', '/sexChartWidget',
             '/resolutionWidget', '/ageWidget', '/comparedWidget']
    return render_template('personal.html', page1=pages[session['sel1']], page2=pages[session['sel2']],
                           page3=pages[session['sel3']])


@app.route('/personalp', methods=['POST'])
def personalp():
    button = int(request.form['button'])
    if button == 1:
        session['sel1'] = (session['sel1'] + 1) % 11
    if button == 2:
        session['sel2'] = (session['sel2'] + 1) % 11
    if button == 3:
        session['sel3'] = (session['sel3'] + 1) % 11
    pages = ['/chartFileWidget', '/chartWorkerWidget', '/radarWidget', '/cakeWidget',
             '/topUserWidget', '/scatterWidget', '/randomChartWidget', '/sexChartWidget',
             '/resolutionWidget', '/ageWidget', '/comparedWidget']
    return render_template('personal.html', page1=pages[session['sel1']], page2=pages[session['sel2']],
                           page3=pages[session['sel3']])


@app.route('/compared')
def compared():
    oldnumDashboard = session['dashboard']
    numDashboard = int(oldnumDashboard)
    if numDashboard < 100 and numDashboard >= 0:
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect = "SELECT AVG(s.QUALITY), i.IMAGE_FILE, STD(s.quality) FROM `imagefile` AS i, `submitted` as s WHERE s.HIT_ID=i.HIT_ID AND i.FOLDER='%s' GROUP BY IMAGE_FILE" % (
            numDashboard)
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
    elif numDashboard >= 100 and numDashboard < 200:
        numDashboard = numDashboard - 100
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect = "SELECT AVG(s.QUALITY), i.VIDEO_FILE, STD(s.quality) FROM `videofile` AS i, `submitted` as s WHERE s.HIT_ID=i.HIT_ID AND i.FOLDER='%s' GROUP BY VIDEO_FILE" % (
            numDashboard)
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
    quality = []
    file = []
    stddev = []
    for triple in result:
        quality.append(triple[0])
        file.append(triple[1][53:])
        stddev.append(triple[2])
    return render_template('compared.html', data1=quality, data2=file, data3=stddev,
                           taskname='Task: ' + getTaskName(int(oldnumDashboard)))


@app.route('/comparedWidget')
def comparedWidget():
    oldnumDashboard = session['dashboard']
    numDashboard = int(oldnumDashboard)
    if numDashboard < 100 and numDashboard >= 0:
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect = "SELECT AVG(s.QUALITY), i.IMAGE_FILE, STD(s.quality) FROM `imagefile` AS i, `submitted` as s WHERE s.HIT_ID=i.HIT_ID AND i.FOLDER='%s' GROUP BY IMAGE_FILE" % (
            numDashboard)
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
    elif numDashboard >= 100 and numDashboard < 200:
        numDashboard = numDashboard - 100
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlSelect = "SELECT AVG(s.QUALITY), i.VIDEO_FILE, STD(s.quality) FROM `videofile` AS i, `submitted` as s WHERE s.HIT_ID=i.HIT_ID AND i.FOLDER='%s' GROUP BY VIDEO_FILE" % (
            numDashboard)
        try:
            cursor.execute(sqlSelect)
            result = cursor.fetchall()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
    quality = []
    file = []
    stddev = []
    for triple in result:
        quality.append(triple[0])
        file.append(triple[1][53:])
        stddev.append(triple[2])
    return render_template('comparedWidget.html', data1=quality, data2=file, data3=stddev,
                           taskname='Task: ' + getTaskName(int(oldnumDashboard)))


if __name__ == "__main__":
    app.run(port=4555, debug=True)
