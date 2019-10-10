import os
import pymysql
import createImmHIT
import createVideoHIT
import resultsImm
import resultsVid
from flask import *

__author__ = 'Edoardo Re'

app = Flask(__name__)

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


@app.route("/home", methods=['POST'])
def homepost():
    refreshButtonNumber = request.form['button']
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
    for i in range(0, 12):
        result.append('')
    i = 0
    for description in resultimage:
        result[i] = description[0]
        i += 1
    i = 6
    for description in resultvideo:
        result[i] = description[0]
        i += 1
    if refreshButtonNumber < 6 and refreshButtonNumber >= 0:
        resultsImm.execute(refreshButtonNumber)
    elif refreshButtonNumber >= 6 and refreshButtonNumber < 12:
        resultsVid.execute(refreshButtonNumber)

    return render_template("home.html", label0=result[0], label1=result[1], label2=result[2],
                           label3=result[3], label4=result[4], label5=result[5], label6=result[6], label7=result[7],
                           label8=result[8], label9=result[9], label10=result[10], label11=result[11])

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
    for i in range(0, 12):
        result.append('')
    i = 0
    for description in resultimage:
        result[i] = description[0]
        i += 1
    i = 6
    for description in resultvideo:
        result[i] = description[0]
        i += 1
    return render_template("home.html", label0=result[0], label1=result[1], label2=result[2],
                           label3=result[3], label4=result[4], label5=result[5], label6=result[6], label7=result[7],
                           label8=result[8], label9=result[9], label10=result[10], label11=result[11])





@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/chartFile")
def chartFile():
    return render_template("chartFile.html")


@app.route("/chartFile", methods=["POST"])
def chartFileM():
    return render_template("chartFile.html")


if __name__ == "__main__":
    app.run(port=4555, debug=True)
