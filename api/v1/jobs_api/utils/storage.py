import boto3
import uuid
from django.conf import settings


def upload_logo_to_bucket(file):

    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION
    )

    file_name = f"{uuid.uuid4()}-{file.name}"

    s3.upload_fileobj(
        file,
        settings.AWS_S3_BUCKET_NAME,
        file_name,
        ExtraArgs={"ContentType": file.content_type}
    )

    file_url = f"{settings.AWS_S3_BASE_URL}{file_name}"

    return file_url