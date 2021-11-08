import os
import zipfile
import logging
import boto3
import wget

logger = logging.getLogger()
logger.setLevel(logging.INFO)

S3_BUCKET_NAME = "movie-data-platform.mpd"
TEMP_PATH = "/tmp/"
MOVIE_LENS_PATH = "movie_lens/"
RAW_ZONE_PATH = "raw_zone/"
MOVIE_LENS_URL_PREFIX = "https://files.grouplens.org/datasets/movielens/"
MOVIE_LENS_FILE_NAME = "ml-25m.zip"
MOVIE_LENS_DIR_NAME = "ml-25m/"


def lambda_handler(event, context):

    logger.info("===== Start MovieLens data injection =====")

    zip_file_path = get_file_from_movie_lens(MOVIE_LENS_URL_PREFIX + MOVIE_LENS_FILE_NAME, MOVIE_LENS_FILE_NAME)
        
    unzip_file_and_save_into_s3(zip_file_path)

    start_glue_workflow()

    logger.info("===== End MovieLens data injection =====")

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        }
    }

def get_file_from_movie_lens(remote_url, file_name):
    logger.info("Start get_file_from_movie_lens")

    zip_file_path = TEMP_PATH + file_name

    logger.info('zip_file_path: {}'.format(zip_file_path))

    unzip_file_name = file_name.replace(".zip", "")

    logger.info('unzip_file: {}'.format(unzip_file_name))

    wget.download(remote_url, zip_file_path)

    logger.info('File info: {}'.format(os.stat(zip_file_path)))

    return zip_file_path

def unzip_file_and_save_into_s3(zip_file_path):
    logger.info("Start unzip_file_and_save_into_s3")

    s3 = boto3.resource("s3")
    z = zipfile.ZipFile(zip_file_path)

    logger.info('file name list: {}'.format(", ".join(str(file_name) for file_name in z.namelist())))

    for file_name in z.namelist():
        s3_raw_path = RAW_ZONE_PATH + MOVIE_LENS_PATH + file_name.replace(MOVIE_LENS_DIR_NAME, "")
        logger.info('s3_raw_path: {}'.format(s3_raw_path))
        s3.Bucket(S3_BUCKET_NAME).put_object(Key=s3_raw_path, Body=z.open(file_name))

def start_glue_workflow():
    logger.info("Start start_glue_workflow")

    glue = boto3.client("glue")
    glue.start_workflow_run(
        Name = "movie_lens_data_cleansing_glue_workflow"
    )