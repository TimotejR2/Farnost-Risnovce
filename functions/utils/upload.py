from werkzeug.utils import secure_filename
import os
from ..database.database import Database
db = Database()

from io import BytesIO
from PIL import Image
import os
import boto3

def upload_image_with_thumbnail(file, filename, path):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("CF_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("CF_SECRET_KEY"),
        endpoint_url=os.getenv("CF_ACCOUNT_ENDPOINT"),
        region_name="auto"
    )

    bucket_name = 'uploads'
    # 🔴 načítaj celý súbor do pamäte
    file_bytes = file.read()

    # --- originál ---
    original_key = f"{path}/{filename}"

    s3.upload_fileobj(
        Fileobj=BytesIO(file_bytes),
        Bucket=bucket_name,
        Key=original_key,
        ExtraArgs={"ContentType": file.content_type}
    )

    # --- resize ---
    img = Image.open(BytesIO(file_bytes))

    max_width = 300
    if img.width > max_width:
        ratio = max_width / img.width
        new_height = int(img.height * ratio)
        img = img.resize((max_width, new_height), Image.LANCZOS)

    # názov _low
    if "." in filename:
        name, ext = filename.rsplit(".", 1)
    else:
        name, ext = filename, "jpg"

    low_key = f"{path}/{name}_low.{ext}"

    buffer = BytesIO()
    img.save(buffer, format="JPEG", quality=85)
    buffer.seek(0)

    s3.upload_fileobj(
        Fileobj=buffer,
        Bucket=bucket_name,
        Key=low_key,
        ExtraArgs={"ContentType": "image/jpeg"}
    )

    return original_key


def insert_post_to_db(form, filename):
    db.execute_file(
        'sql_scripts/user_insert/insert_posts.sql',
        (form['nazov'], filename, form['alt'], form['date'], form['text'], form['oblast'])
    )
