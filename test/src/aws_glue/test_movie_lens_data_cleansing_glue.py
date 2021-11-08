import pytest
import sys
from unittest import mock
from moto import mock_s3
from pyspark.sql import SparkSession
from chispa.dataframe_comparer import *
from pyspark.sql.functions import col, from_unixtime, to_timestamp

MOVIE_LENS_PATH = "movie_lens/"
RAW_ZONE_PATH = "/raw_zone/"
CLEANSED_ZONE_PATH = "/cleansed_zone/"

sys.modules['awsglue.context'] = mock.MagicMock()
sys.modules['awsglue.utils'] = mock.MagicMock()


@pytest.fixture(scope='session')
def spark():
    return SparkSession.builder \
        .master("local") \
        .appName("movie_lens_unit_test") \
        .getOrCreate()


def test_GIVEN_duplicated_movie_lens_df_WHEN_remove_duplicated_data_THEN_return_cleansed_data(spark):

    from src.aws_glue.movie_lens_data_cleansing_glue import remove_duplicated_data

    # GIVEN
    duplicated_file_list = [
        "duplicated_links.csv",
        "duplicated_movies.csv",
        "duplicated_ratings.csv",
    ]
    duplicated_df_dict = {}
    for file_name in duplicated_file_list:
        df = spark.read.csv("test/src/aws_glue/testing_files/movie_lens/duplicated/" + file_name, header="true")
        duplicated_df_dict[file_name] = df

    # WHEN
    cleansed_df_dict = remove_duplicated_data(duplicated_df_dict)

    # THEN
    non_duplicated_file_list = [
        "non_duplicated_links.csv",
        "non_duplicated_movies.csv",
        "non_duplicated_ratings.csv",
    ]
    non_duplicated_df_dict = {}
    for file_name in non_duplicated_file_list:
        df = spark.read.csv("test/src/aws_glue/testing_files/movie_lens/duplicated/" + file_name, header="true")
        non_duplicated_df_dict[file_name] = df

    for i in range(0, len(duplicated_file_list)):
        actual_df = cleansed_df_dict[duplicated_file_list[i]]
        actual_df = actual_df.orderBy([actual_df.columns[0], actual_df.columns[1], actual_df.columns[2]])
        expected_df = non_duplicated_df_dict[non_duplicated_file_list[i]]
        expected_df = expected_df.orderBy([expected_df.columns[0], expected_df.columns[1], expected_df.columns[2]])
        assert_df_equality(actual_df, expected_df)


def test_GIVEN_diff_null_movie_lens_df_WHEN_standardize_null_value_THEN_return_cleansed_data(spark):

    from src.aws_glue.movie_lens_data_cleansing_glue import standardize_null_value

    # GIVEN
    diff_null_file_list = [
        "non_standardized_movies.csv",
        "non_standardized_ratings.csv"
    ]
    diff_null_df_dict = {}
    for file_name in diff_null_file_list:
        df = spark.read.csv("test/src/aws_glue/testing_files/movie_lens/standardize_null/" + file_name, header="true")
        diff_null_df_dict[file_name] = df

    # WHEN
    cleansed_df_dict = standardize_null_value(diff_null_df_dict)

    # THEN
    same_null_file_list = [
        "standardized_movies.csv",
        "standardized_ratings.csv"
    ]
    same_null_df_dict = {}
    for file_name in same_null_file_list:
        df = spark.read.csv("test/src/aws_glue/testing_files/movie_lens/standardize_null/" + file_name, header="true")
        same_null_df_dict[file_name] = df

    for i in range(0, len(diff_null_file_list)):
        actual_df = cleansed_df_dict[diff_null_file_list[i]]
        actual_df = actual_df.orderBy([actual_df.columns[0]])
        expected_df = same_null_df_dict[same_null_file_list[i]]
        expected_df = expected_df.orderBy([expected_df.columns[0]])
        assert_df_equality(actual_df, expected_df)


def test_GIVEN_unassigned_movie_lens_df_WHEN_assign_data_type_THEN_return_cleansed_data(spark):

    from src.aws_glue.movie_lens_data_cleansing_glue import assign_data_type

    # GIVEN
    unassigned_file_list = [
        "genome-scores.csv",
        "genome-tags.csv",
        "links.csv",
        "movies.csv",
        "ratings.csv",
        "tags.csv",
    ]
    unassigned_df_dict = {}
    for file_name in unassigned_file_list:
        df = spark.read.csv("test/src/aws_glue/testing_files/movie_lens/assign_data_type/" + file_name, header="true")
        unassigned_df_dict[file_name] = df

    # WHEN
    cleansed_df_dict = assign_data_type(unassigned_df_dict)

    # THEN
    assigned_file_list = [
        "assigned_genome-scores.csv",
        "assigned_genome-tags.csv",
        "assigned_links.csv",
        "assigned_movies.csv",
        "assigned_ratings.csv",
        "assigned_tags.csv",
    ]
    assigned_df_dict = {}
    ALL_DATA_TYPE_DICT = {
        "assigned_genome-scores.csv": {
            "movieId": "string",
            "tagId": "string",
            "relevance": "string"
        },
        "assigned_genome-tags.csv": {
            "tagId": "string",
            "tag": "string"
        },
        "assigned_links.csv": {
            "movieId": "string",
            "imdbId": "string",
            "tmdbId": "string"
        },
        "assigned_movies.csv": {
            "movieId": "string",
            "title": "string",
            "genres": "string"
        },
        "assigned_ratings.csv": {
            "userId": "string",
            "movieId": "string",
            "rating": "float",
            "timestamp": "timestamp",
        },
        "assigned_tags.csv": {
            "userId": "string",
            "movieId": "string",
            "tag": "string",
            "timestamp": "timestamp",
        },
    }

    for file_name in assigned_file_list:
        df = spark.read.csv("test/src/aws_glue/testing_files/movie_lens/assign_data_type/" + file_name, header="true")
        data_type_dict = ALL_DATA_TYPE_DICT[file_name]
        for column_name, data_type in data_type_dict.items():
            if data_type == "timestamp":
                df = df.withColumn(column_name, to_timestamp(from_unixtime(col(column_name)), "yyyy-MM-dd HH:mm:ss"))
            else: 
                df = df.withColumn(column_name, col(column_name).cast(data_type))
        assigned_df_dict[file_name] = df

    for i in range(0, len(unassigned_file_list)):
        actual_df = cleansed_df_dict[unassigned_file_list[i]]
        actual_df = actual_df.orderBy([actual_df.columns[0], actual_df.columns[1]])
        expected_df = assigned_df_dict[assigned_file_list[i]]
        expected_df = expected_df.orderBy([expected_df.columns[0], expected_df.columns[1]])
        assert_df_equality(actual_df, expected_df)
