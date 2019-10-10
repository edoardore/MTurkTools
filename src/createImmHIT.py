import boto3
from src import imageManager, Key
import time
import pymysql


def execute():
    # Use the Amazon Mechanical Turk Sandbox to publish test Human Intelligence Tasks (HITs) without paying any money.
    host = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
    # Uncomment line below to connect to the live marketplace instead of the sandbox
    # host = 'https://mturk-requester.us-east-1.amazonaws.com'

    region_name = 'us-east-1'
    aws_access_key_id = Key.getAws_access_key_id()
    aws_secret_access_key = Key.getAws_secret_access_key()
    client = boto3.client('mturk',
                          endpoint_url=host,
                          region_name=region_name,
                          aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key,
                          )
    # Se si creano Hit aggiuntive mettere a True questa variabile
    tuple = imageManager.getImg()
    images = tuple[0]
    directory = tuple[1]
    if directory == 'images':
        directory = 0
    else:
        directory = directory[6:len(directory)]
    i = 0
    for img in images:
        i += 1
        if (i % 500) == 0:
            print 'Sleep for one minute'
            time.sleep(60)
        response = client.create_hit_with_hit_type(
            HITLayoutId=Key.getHITLayoutIdIMG(),
            HITTypeId=Key.getHITTypeIdIMG(),
            HITLayoutParameters=[
                {
                    'Name': 'img',
                    'Value': img
                }, ],
            # Quanto resta disponibile una HIT a tutti i Workers, non il timer dopo aver accettato.
            LifetimeInSeconds=60,
            MaxAssignments=5,
        )
        print str(i) + ')  ' + 'Created HIT for ' + img
        # The response included several fields that will be helpful later
        hit_type_id = response['HIT']['HITTypeId']
        hit_id = response['HIT']['HITId']
        db = pymysql.connect("localhost", "utente", "pass123", "dbmysql")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sqlInsert = "INSERT INTO `imagefile`(HIT_ID, IMAGE_FILE, FOLDER)VALUES" \
                    "('%s', '%s', '%s')" \
                    % (hit_id, img, directory)
        try:
            cursor.execute(sqlInsert)
            # Commit your changes in the database
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
    print("Your HITs has been created at link:")
    print("https://workersandbox.mturk.com/mturk/preview?groupId=" + hit_type_id)
