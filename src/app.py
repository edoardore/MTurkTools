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


@app.route("/upload")
def up():
    return render_template("upload.html")


@app.route("/upload", methods=["POST"])
def upload():
    type = request.form['type']
    if type == 'Image':
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
    elif type == 'Video':
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
    return render_template("home.html", label=result, percent='')


@app.route("/homepost", methods=['POST'])
def homepost():
    refreshButtonNumber = request.form['button']
    db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
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
    refreshButtonNumber = int(refreshButtonNumber)
    if refreshButtonNumber < 100 and refreshButtonNumber >= 0:
        percent = str(resultsImm.execute(refreshButtonNumber)) + '% of the Task completed by Workers'
    elif refreshButtonNumber >= 100 and refreshButtonNumber < 200:
        percent = str(resultsVid.execute(refreshButtonNumber - 100)) + '% of the Task completed by Workers'
    return render_template("home.html", label=result, percent=percent)


@app.route("/dashboard", methods=["POST"])
def dashboard():
    session['dashboard'] = request.form['dashboard']
    return render_template("dashboard.html")


@app.route('/dashboardnp')
def dashboardnp():
    return render_template("dashboard.html")


@app.route("/chartFile")
def chartFile():
    numDashboard = session['dashboard']
    numDashboard = int(numDashboard)
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
    return render_template("chartFile.html", result=result, data1='0', data2='0')


@app.route('/chartFileP', methods=['POST'])
def chartFileP():
    numDashboard = session['dashboard']
    numDashboard = int(numDashboard)
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
    return render_template("chartFile.html", result=result, data1=quality, data2=worker, file=file)


@app.route('/chartWorker')
def chartWorker():
    numDashboard = session['dashboard']
    numDashboard = int(numDashboard)
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
    return render_template("chartWorker.html", result=result, data1='0', data2='0')


@app.route('/chartWorkerP', methods=['POST'])
def chartWorkerP():
    numDashboard = session['dashboard']
    numDashboard = int(numDashboard)
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
    return render_template("chartWorker.html", result=result, data1=quality, data2=file, worker=workerid)


@app.route('/radar')
def radar():
    numDashboard = session['dashboard']
    numDashboard = int(numDashboard)
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
    return render_template("radar.html", result=result, data1='0', data2='0')


@app.route('/radarP', methods=['POST'])
def radarP():
    numDashboard = session['dashboard']
    numDashboard = int(numDashboard)
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
                           workerid2=workerid2)


@app.route("/cake")
def cake():
    numDashboard = session['dashboard']
    numDashboard = int(numDashboard)
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
    return render_template("cake.html", result=result, data1='0', data2='0')


@app.route('/cakeP', methods=['POST'])
def cakeP():
    numDashboard = session['dashboard']
    numDashboard = int(numDashboard)
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
    return render_template("cake.html", result=result, data1=quality, file=file)


@app.route('/topUser')
def topUser():
    numDashboard = session['dashboard']
    numDashboard = int(numDashboard)
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
    return render_template("topUser.html", data1=workerid, data2=count, file=typefile)


@app.route('/scatter')
def scatter():
    numDashboard = session['dashboard']
    numDashboard = int(numDashboard)
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
    return render_template("scatter.html", data1=workerid, data2=count, data3=average, file=typefile)


@app.route('/randomChart')
def randomChart():
    numDashboard = session['dashboard']
    numDashboard = int(numDashboard)
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
    return render_template("randomChart.html", data1=workerid, data2=count, file=typefile)

@app.route('/sexChart')
def sexChart():
    return render_template("sexChart.html", data1='0', sex='')

@app.route('/sexChartP', methods=['POST'])
def sexChartP():
    return render_template("sexChart.html", data1='0', sex='')



if __name__ == "__main__":
    app.run(port=4555, debug=True)
