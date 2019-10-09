import os, pymysql
import createImmHIT
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
    sqlSelect = "SELECT * FROM meta"
    try:
        cursor.execute(sqlSelect)
        result = cursor.fetchall()
        # if the raw not in the table already
        if len(result) == 0:
            return render_template("index.html")
        else:
            return render_template("home.html")
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
    db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    # Prepare SQL query to INSERT a record into the database.
    sqlSelect = "SELECT MAX(FOLDER) FROM meta"
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
    sqlInsert = "INSERT INTO meta(FOLDER, DESCRIPTION)VALUES" \
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


@app.route("/home")
def home():
    db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    # Prepare SQL query to INSERT a record into the database.
    sqlSelect = "SELECT DESCRIPTION FROM meta"
    try:
        cursor.execute(sqlSelect)
        result = cursor.fetchall()
    except:
        # Rollback in case there is any error
        db.rollback()
    # disconnect from server
    db.close()
    return render_template("home.html", label1=result)


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
