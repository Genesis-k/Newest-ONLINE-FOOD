from google.cloud import storage
import os

os.environ ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your-service-account.json"

BUCKET_NAME = "image_storageonlinefood"

def upload_image_to_gcs (file, filename):
    """Uploads an image to Google Cloud Storage and returns the public URL"""
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(filename)

    blob.upload_from_file(file, content_type=file.content_type)
    blob.make_public()

    return blob.public_url