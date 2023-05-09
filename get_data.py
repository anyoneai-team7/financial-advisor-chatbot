import boto3
import os

s3 = boto3.resource(
    "s3",
    aws_access_key_id="AKIA2JHUK4EGBAMYAYFY",
    aws_secret_access_key="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",
)  # assumes credentials & configuration are handled outside python in .aws directory or environment variables


def download_s3_folder(
    bucket_name, s3_folder, local_dir=None, batch_size=100, random_sampling=False
):
    """
    Download the contents of a folder directory
    Args:
        bucket_name: the name of the s3 bucket
        s3_folder: the folder path in the s3 bucket
        local_dir: a relative or absolute directory path in the local file system
    """
    bucket = s3.Bucket(bucket_name)
    size_byte = 0
    count = 0
    for obj in bucket.objects.filter(Prefix=s3_folder):
        count += 1
        size_byte = size_byte + obj.size
        target = (
            obj.key
            if local_dir is None
            else os.path.join(local_dir, os.path.relpath(obj.key, s3_folder))
        )
        if not os.path.exists(os.path.dirname(target)):
            os.makedirs(os.path.dirname(target))
        if obj.key[-1] == "/":
            continue
        bucket.download_file(obj.key, target)
