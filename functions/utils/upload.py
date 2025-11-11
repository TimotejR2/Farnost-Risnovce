from werkzeug.utils import secure_filename
import os
from ..database.database import Database
db = Database()

def save_uploaded_file(file):
    UPLOAD_FOLDER = 'static/uploads/'
    if not file:
        return '-'
    filename = secure_filename(file.filename)
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    return filename

def upload_folder_to_s3(folder, bucket_name):
    import boto3
    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("CF_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("CF_SECRET_KEY"),
        endpoint_url=os.getenv("CF_ACCOUNT_ENDPOINT"),
        region_name="auto"
    )
    for f in os.listdir(folder):
        if f.lower().endswith('.jpg'):
            with open(os.path.join(folder, f), "rb") as file_obj:
                s3.upload_fileobj(file_obj, bucket_name, f)
            os.remove(os.path.join(folder, f))

def insert_post_to_db(form, filename):
    db.execute_file(
        'sql_scripts/user_insert/insert_posts.sql',
        (form['nazov'], filename, form['alt'], form['date'], form['text'], form['oblast'])
    )
