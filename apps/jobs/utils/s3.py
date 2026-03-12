import boto3
import uuid
from django.conf import settings


def upload_file_to_s3(file, folder="company-logos"):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION,
    )

    extension = file.name.split(".")[-1]
    filename = f"{folder}/{uuid.uuid4()}.{extension}"

    s3.upload_fileobj(
        file,
        settings.AWS_BUCKET_NAME,
        filename,
        ExtraArgs={"ContentType": file.content_type},
    )

    return f"https://{settings.AWS_BUCKET_NAME}.s3.{settings.AWS_REGION}.amazonaws.com/{filename}"