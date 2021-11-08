import pytest
import gzip
import os
import boto3
from unittest import mock
from moto import mock_s3


# import the module name with special character
# module_name = "xx-xxx-xx"
# module = importlib.import_module(module_name)
# function_name = "xxx"
# xxx = getattr(module, function_name)

@mock.patch("wget.download", return_value="dummy")
@mock.patch("os.stat")
def test_GIVEN_imdb_file_name_WHEN_get_file_from_imdb_THEN_return_zip_file_path(mock_wget_download, mock_os_stat):

    from src.aws_lambda.imdb_data_injection_lambda import get_file_from_imdb

    # GIVEN
    imdb_file_name = "test.file"
    temp_path = "/tmp/"

    # WHEN
    zip_file_path = get_file_from_imdb(imdb_file_name)

    # THEN
    assert (zip_file_path == temp_path + imdb_file_name)

def test_GIVEN_zip_file_and_path_WHEN_unzip_file_THEN_return_file_content():

    from src.aws_lambda.imdb_data_injection_lambda import unzip_file

    # GIVEN
    file_content = b"testing content"
    file_path = "testing/"
    file_name = "file.txt.gz"

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with gzip.open(file_path + file_name, 'wb') as f:
        f.write(file_content)

    # WHEN
    result = unzip_file(file_path + file_name)

    # THEN
    assert (result == file_content)
    os.remove(file_path + file_name)
    os.rmdir(file_path)

@mock_s3
def test_GIVEN_file_contend_WHEN_save_file_into_s3_THEN_saved():

    from src.aws_lambda.imdb_data_injection_lambda import save_file_into_s3

    # GIVEN
    file_content = b"testing content"
    file_name = "file.txt"
    s3 = boto3.resource("s3")
    S3_BUCKET_NAME = "movie-data-platform.mpd"
    s3.create_bucket(Bucket=S3_BUCKET_NAME)

    # WHEN
    save_file_into_s3(file_content, file_name)

    # THEN
    IMDB_PATH = "imdb/"
    RAW_ZONE_PATH = "raw_zone/"
    unzip_file_name = file_name.replace(".gz", "")
    s3_raw_path = RAW_ZONE_PATH + IMDB_PATH + unzip_file_name
    s3_response_object = s3.Object(S3_BUCKET_NAME, s3_raw_path)
    result_content = s3_response_object.get()['Body'].read()
    assert (result_content == file_content)