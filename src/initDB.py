import pymysql


def initalization():
    # Open database connection
    db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    # Drop table if it already exist using execute() method.
    cursor.execute("DROP TABLE IF EXISTS submitted")
    # Create table as per requirement
    sql = """CREATE TABLE `dbmysql`.`submitted`(`WORKER_ID` VARCHAR(20) NOT NULL , `HIT_ID` VARCHAR(20) 
    NOT NULL, `QUALITY` INT, `AGE` VARCHAR(10), `SEX` VARCHAR(1), `RESOLUTION` VARCHAR(10))ENGINE = InnoDB;"""
    # Execute the SQL command
    cursor.execute(sql)
    # disconnect from server
    db.close()
    # Open database connection
    db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    # Drop table if it already exist using execute() method.
    cursor.execute("DROP TABLE IF EXISTS imagefile")
    # Create table as per requirement
    sql = """CREATE TABLE `dbmysql`.`imagefile`(`HIT_ID` VARCHAR(20) NOT NULL , `IMAGE_FILE` VARCHAR(100))ENGINE = InnoDB;"""
    # Execute the SQL command
    cursor.execute(sql)
    # disconnect from server
    db.close()
    # Open database connection
    db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    # Drop table if it already exist using execute() method.
    cursor.execute("DROP TABLE IF EXISTS videofile")
    # Create table as per requirement
    sql = """CREATE TABLE `dbmysql`.`videofile`(`HIT_ID` VARCHAR(20) NOT NULL , `VIDEO_FILE` VARCHAR (100) )ENGINE = InnoDB;"""
    # Execute the SQL command
    cursor.execute(sql)
    # disconnect from server
    db.close()
    # Open database connection
    db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    # Drop table if it already exist using execute() method.
    cursor.execute("DROP TABLE IF EXISTS meta")
    # Create table as per requirement
    sql = """CREATE TABLE `dbmysql`.`meta`(`FOLDER` INT NOT NULL, `DESCRIPTION` VARCHAR(280))ENGINE = InnoDB;"""
    # Execute the SQL command
    cursor.execute(sql)
    # disconnect from server
    db.close()


initalization()  # run this module the first time ever, you need to set up MYSQL dbms earlier (e.g. PhpMyAdmin in XAMPP).
# after the execution, recomment this line with
