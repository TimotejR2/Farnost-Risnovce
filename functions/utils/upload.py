from werkzeug.utils import secure_filename
import os
from ..database.database import Database
db = Database()

import boto3
from io import BytesIO
from PIL import Image

def upload_image_with_thumbnail(file, filename, path):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("CF_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("CF_SECRET_KEY"),
        endpoint_url=os.getenv("CF_ACCOUNT_ENDPOINT"),
        region_name="auto"
    )

    bucket_name = 'uploads'
    filename = secure_filename(filename)

    # rozdelenie mena a prípony
    if "." in filename:
        name, ext = filename.rsplit(".", 1)
        ext = ext.lower()
    else:
        name, ext = filename, "jpg"

    original_key = f"{path}/{name}.{ext}"
    low_key = f"{path}/{name}_low.{ext}"

    # --- 1. upload originálu ---
    file.stream.seek(0)
    s3.upload_fileobj(
        Fileobj=file.stream,
        Bucket=bucket_name,
        Key=original_key,
        ExtraArgs={"ContentType": file.content_type}
    )

    # --- 2. vytvorenie zmenšeného obrázka ---
    file.stream.seek(0)
    img = Image.open(file.stream)

    # zachovanie pomeru strán, max šírka 300
    max_width = 300
    if img.width > max_width:
        ratio = max_width / float(img.width)
        new_height = int(img.height * ratio)
        img = img.resize((max_width, new_height), Image.LANCZOS)

    # uloženie do pamäte
    buffer = BytesIO()

    format_map = {
        "jpg": "JPEG",
        "jpeg": "JPEG",
        "png": "PNG",
        "webp": "WEBP"
    }
    img_format = format_map.get(ext, "JPEG")

    img.save(buffer, format=img_format)
    buffer.seek(0)

    # --- 3. upload zmenšeného ---
    s3.upload_fileobj(
        Fileobj=buffer,
        Bucket=bucket_name,
        Key=low_key,
        ExtraArgs={"ContentType": file.content_type}
    )

    return original_key


def insert_post_to_db(form, filename):
    db.execute_file(
        'sql_scripts/user_insert/insert_posts.sql',
        (form['nazov'], filename, form['alt'], form['date'], form['text'], form['oblast'])
    )
