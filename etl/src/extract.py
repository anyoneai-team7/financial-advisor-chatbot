import boto3
import os
import multiprocessing
import logging
from collections import Counter
from multiprocessing.connection import Connection

s3 = boto3.resource(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
)


def _get_top_company_list(objects, top: int = 100):
    """Returns the top companies by file count

    Args:
        objects (List[S3Object]): S3 object list
        top (int, optional): number of companies to retrieve. Defaults to 100.

    Returns:
        List[str]: Top company names
    """
    companies = [
        obj.key.split("/")[1] for obj in objects if len(obj.key.split("/")) > 2
    ]
    company_file_counter = Counter(companies)
    top_companies = company_file_counter.most_common(top)
    return [company[0] for company in top_companies]


def extract_docs(bucket_name: str, s3_folder: str, local_dir: str):
    """
    Download the contents of a folder directory
    Args:
        bucket_name: the name of the s3 bucket
        s3_folder: the folder path in the s3 bucket
        local_dir: a relative or absolute directory path in the local file system
    """
    bucket = s3.Bucket(bucket_name)
    objects = bucket.objects.filter(Prefix=s3_folder)
    companies = _get_top_company_list(objects)

    for company in companies:
        company_objects = objects.filter(Prefix=f"{s3_folder}/{company}")
        for obj in company_objects:
            target = (
                obj.key
                if local_dir is None
                else os.path.join(local_dir, os.path.relpath(obj.key, s3_folder))
            )
            if not os.path.exists(os.path.dirname(target)):
                os.makedirs(os.path.dirname(target))
            if obj.key[-1] == "/":
                continue

            # Check if file already exists to download it
            if not os.path.exists(target):
                logging.info(f"Downloading {obj.key} to {target}")
                bucket.download_file(obj.key, target)
            filesplit = obj.key.split("/")
            yield {
                "path": target,
                "company": filesplit[1],
                "year": filesplit[2].split("_")[2][:4],
                "filename": filesplit[2],
            }


class Extractor(multiprocessing.Process):
    def __init__(
        self,
        connection: Connection,
        bucket_name: str,
        s3_folder: str,
        local_dir: str = None,
    ):
        self.connection = connection
        self.bucket_name = bucket_name
        self.s3_folder = s3_folder
        self.local_dir = local_dir
        multiprocessing.Process.__init__(self)

    def run(self):
        for doc in extract_docs(
            self.bucket_name,
            self.s3_folder,
            self.local_dir,
        ):
            self.connection.send(doc)
            logging.info(f'Extracted doc with path: {doc["path"]}')
        self.connection.send(None)
        self.connection.close()
        logging.info("Closing connection. Extracted all requested documents")
