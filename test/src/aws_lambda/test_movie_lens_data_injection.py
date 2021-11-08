import pytest
import os
import boto3
import zipfile
import csv
from unittest import mock
from moto import mock_s3


@mock.patch("wget.download", return_value="dummy")
@mock.patch("os.stat")
def test_GIVEN_movie_lens_file_name_WHEN_get_file_from_movie_lens_THEN_return_zip_file_path(mock_wget_download, mock_os_stat):

    from src.aws_lambda.movie_lens_data_injection_lambda import get_file_from_movie_lens

    # GIVEN
    TEMP_PATH = "/tmp/"
    MOVIE_LENS_URL_PREFIX = "test.com"
    MOVIE_LENS_FILE_NAME = "test.zip"

    # WHEN
    zip_file_path = get_file_from_movie_lens(MOVIE_LENS_URL_PREFIX + MOVIE_LENS_FILE_NAME, MOVIE_LENS_FILE_NAME)

    # THEN
    assert (zip_file_path == TEMP_PATH + MOVIE_LENS_FILE_NAME)

@mock_s3
def test_GIVEN_zip_file_WHEN_unzip_file_and_save_into_s3_THEN_unzip_and_saved():

    from src.aws_lambda.movie_lens_data_injection_lambda import unzip_file_and_save_into_s3

    # GIVEN
    MOVIE_LENS_PATH = "movie_lens/"
    RAW_ZONE_PATH = "raw_zone/"
    S3_BUCKET_NAME = "movie-data-platform.mpd"
    
    s3 = boto3.resource("s3")
    s3.create_bucket(Bucket=S3_BUCKET_NAME)

    file_name_1 = "test1.csv"
    file_name_2 = "test2.csv"
    file_name_3 = "test3.csv"
    csv_header = ["col1", "col2", "col3"]

    file_1_content_1 = ["1", "row_1_col_2", "row_1_col_3"]
    file_1_content_2 = ["1", "row_2_col_2", "row_2_col_3"]
    file_1_content_3 = ["1", "row_3_col_2", "row_3_col_3"]
    with open(file_name_1, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(csv_header)
        writer.writerow(file_1_content_1)
        writer.writerow(file_1_content_2)
        writer.writerow(file_1_content_3)

    file_2_content_1 = ["2", "row_1_col_2", "row_1_col_3"]
    file_2_content_2 = ["2", "row_2_col_2", "row_2_col_3"]
    file_2_content_3 = ["2", "row_3_col_2", "row_3_col_3"]
    with open(file_name_2, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(csv_header)
        writer.writerow(file_2_content_1)
        writer.writerow(file_2_content_2)
        writer.writerow(file_2_content_3)

    
    file_3_content_1 = ["3", "row_1_col_2", "row_1_col_3"]
    file_3_content_2 = ["3", "row_2_col_2", "row_2_col_3"]
    file_3_content_3 = ["3", "row_3_col_2", "row_3_col_3"]
    with open(file_name_3, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(csv_header)
        writer.writerow(file_3_content_1)
        writer.writerow(file_3_content_2)
        writer.writerow(file_3_content_3)

    zip_file_path = "/tmp/test.zip"
    lista_files = ["test1.csv","test2.csv","test3.csv"]
    with zipfile.ZipFile(zip_file_path, 'w') as zipMe:        
        for file in lista_files:
            zipMe.write(file, compress_type=zipfile.ZIP_DEFLATED)

    # WHEN
    unzip_file_and_save_into_s3(zip_file_path)

    # THEN
    s3_raw_path = RAW_ZONE_PATH + MOVIE_LENS_PATH + file_name_1
    s3_response_object = s3.Object(S3_BUCKET_NAME, s3_raw_path)
    result_content = s3_response_object.get()['Body'].read().decode('ascii')
    for content in file_1_content_1:
        assert (content in result_content)
    for content in file_1_content_2:
        assert (content in result_content)
    for content in file_1_content_3:
        assert (content in result_content)

    s3_raw_path = RAW_ZONE_PATH + MOVIE_LENS_PATH + file_name_2
    s3_response_object = s3.Object(S3_BUCKET_NAME, s3_raw_path)
    result_content = s3_response_object.get()['Body'].read().decode('ascii')
    for content in file_2_content_1:
        assert (content in result_content)
    for content in file_2_content_2:
        assert (content in result_content)
    for content in file_2_content_3:
        assert (content in result_content)

    s3_raw_path = RAW_ZONE_PATH + MOVIE_LENS_PATH + file_name_3
    s3_response_object = s3.Object(S3_BUCKET_NAME, s3_raw_path)
    result_content = s3_response_object.get()['Body'].read().decode('ascii')
    for content in file_3_content_1:
        assert (content in result_content)
    for content in file_3_content_2:
        assert (content in result_content)
    for content in file_3_content_3:
        assert (content in result_content)
    
    os.remove('test1.csv')
    os.remove('test2.csv')
    os.remove('test3.csv')

