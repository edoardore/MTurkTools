import boto3
from botocore.exceptions import NoCredentialsError
import os
import mimetypes
import Key
import pymysql


def getVid():
    aws_access_key_id = Key.getAws_access_key_id()
    aws_secret_access_key = Key.getAws_secret_access_key()

    def upload_to_aws(local_file, bucket, s3_file):
        s3 = boto3.client('s3',
                          aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key,
                          )

        try:
            s3.put_object(Bucket="videosformturk", Key=(directory + '/'))

            s3.upload_file(local_file, bucket, s3_file,
                           ExtraArgs={"ContentType": mimetypes.MimeTypes().guess_type(s3_file)[0]})

            print("Upload Successful of " + s3_file)
            return True

        except NoCredentialsError:
            print("Credentials not available")
            return False

    uploaded = []
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
    if i[0][0] == 0:
        directory = "video"
    else:
        s = i[0][0]
        directory = "video" + str(s)
    videos = os.listdir(directory)
    for vid in videos:
        if upload_to_aws(directory + "/" + vid, 'videosformturk', directory + "/" + vid):
            uploaded.append("https://videosformturk.s3.eu-central-1.amazonaws.com/" + directory + "/" + vid)
    tuple = []
    tuple.append(uploaded)
    tuple.append(directory)
    return tuple
