import os
import gzip
import logging
import boto3
import wget

logger = logging.getLogger()
logger.setLevel(logging.INFO)

S3_BUCKET_NAME = "movie-data-platform.mpd"
TEMP_PATH = "/tmp/"
IMDB_PATH = "imdb/"
RAW_ZONE_PATH = "raw_zone/"
IMDB_URL_PREFIX = "https://datasets.imdbws.com/"
IMDB_FILE_NAME_LIST = [
    "name.basics.tsv.gz",
    "title.akas.tsv.gz",
    "title.basics.tsv.gz",
    "title.crew.tsv.gz",
    "title.episode.tsv.gz",
    "title.principals.tsv.gz",
    "title.ratings.tsv.gz"
]


def lambda_handler(event, context):

    logger.info("===== Start IMDB data injection =====")

    for imdb_file_name in IMDB_FILE_NAME_LIST:

        zip_file_path = get_file_from_imdb(imdb_file_name)

        file_content = unzip_file(zip_file_path)

        save_file_into_s3(file_content, imdb_file_name)

        os.remove(zip_file_path)
        file_content = None

    start_glue_workflow()

    logger.info("===== End IMDB data injection =====")

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        }
    }


def get_file_from_imdb(imdb_file_name):
    logger.info("Start get_file_from_imdb")

    remote_url = IMDB_URL_PREFIX + imdb_file_name
    zip_file_path = TEMP_PATH + imdb_file_name

    logger.info('zip_file: {}'.format(zip_file_path))

    wget.download(remote_url, zip_file_path)

    logger.info('File info: {}'.format(os.stat(zip_file_path)))

    return zip_file_path


def unzip_file(zip_file_path):
    logger.info("Start unzip_file")

    with gzip.open(zip_file_path, 'r') as f:
        file_content = f.read()

    return file_content


def save_file_into_s3(file_content, file_name):
    logger.info("Start save_file_into_s3")

    unzip_file_name = file_name.replace(".gz", "")
    logger.info('unzip_file: {}'.format(unzip_file_name))

    s3_raw_path = RAW_ZONE_PATH + IMDB_PATH + unzip_file_name

    s3 = boto3.resource("s3")
    s3.Bucket(S3_BUCKET_NAME).put_object(Key=s3_raw_path, Body=file_content)


def start_glue_workflow():
    logger.info("Start start_glue_workflow")

    glue = boto3.client("glue")
    glue.start_workflow_run(
        Name = "imdb_data_cleansing_glue_workflow"
    )
