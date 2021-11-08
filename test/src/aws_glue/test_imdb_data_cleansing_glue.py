import pytest
import gzip
import os
import sys
import boto3
from unittest import mock
from moto import mock_s3
from pyspark.sql import SparkSession
from chispa.dataframe_comparer import *
from pyspark.sql.functions import col

IMDB_PATH = "imdb/"
RAW_ZONE_PATH = "raw_zone/"
CLEANSED_ZONE_PATH = "cleansed_zone/"

sys.modules['awsglue.context'] = mock.MagicMock()
sys.modules['awsglue.utils'] = mock.MagicMock()


@pytest.fixture(scope='session')
def spark():
    return SparkSession.builder \
        .master("local") \
        .appName("imdb_unit_test") \
        .getOrCreate()


def test_GIVEN_duplicated_imdb_df_WHEN_remove_duplicated_data_THEN_return_cleansed_data(spark):

    from src.aws_glue.imdb_data_cleansing_glue import remove_duplicated_data

    # GIVEN
    duplicated_file_list = [
        "duplicated_name.basics.tsv",
        "duplicated_title.akas.tsv",
        "duplicated_title.basics.tsv",
    ]
    duplicated_df_dict = {}
    for file_name in duplicated_file_list:
        df = spark.read.csv("test/src/aws_glue/testing_files/imdb/duplicated/" + file_name, sep="\t", header="true")
        duplicated_df_dict[file_name] = df

    # WHEN
    cleansed_df_dict = remove_duplicated_data(duplicated_df_dict)

    # THEN
    non_duplicated_file_list = [
        "non_duplicated_name.basics.tsv",
        "non_duplicated_title.akas.tsv",
        "non_duplicated_title.basics.tsv",
    ]
    non_duplicated_df_dict = {}
    for file_name in non_duplicated_file_list:
        df = spark.read.csv("test/src/aws_glue/testing_files/imdb/duplicated/" + file_name, sep="\t", header="true")
        non_duplicated_df_dict[file_name] = df

    for i in range(0, len(duplicated_file_list)):
        actual_df = cleansed_df_dict[duplicated_file_list[i]]
        actual_df = actual_df.orderBy([actual_df.columns[0], actual_df.columns[1], actual_df.columns[2], actual_df.columns[3]])
        expected_df = non_duplicated_df_dict[non_duplicated_file_list[i]]
        expected_df = expected_df.orderBy([expected_df.columns[0], expected_df.columns[1], expected_df.columns[2], expected_df.columns[3]])
        assert_df_equality(actual_df, expected_df)


def test_GIVEN_diff_null_imdb_df_WHEN_standardize_null_value_THEN_return_cleansed_data(spark):

    from src.aws_glue.imdb_data_cleansing_glue import standardize_null_value

    # GIVEN
    diff_null_file_list = [
        "non_standardized_name.basics.tsv",
        "non_standardized_title.episode.tsv"
    ]
    diff_null_df_dict = {}
    for file_name in diff_null_file_list:
        df = spark.read.csv("test/src/aws_glue/testing_files/imdb/standardize_null/" + file_name, sep="\t", header="true")
        diff_null_df_dict[file_name] = df

    # WHEN
    cleansed_df_dict = standardize_null_value(diff_null_df_dict)

    # THEN
    same_null_file_list = [
        "standardized_name.basics.tsv",
        "standardized_title.episode.tsv"
    ]
    same_null_df_dict = {}
    for file_name in same_null_file_list:
        df = spark.read.csv("test/src/aws_glue/testing_files/imdb/standardize_null/" + file_name, sep="\t", header="true")
        same_null_df_dict[file_name] = df

    for i in range(0, len(diff_null_file_list)):
        actual_df = cleansed_df_dict[diff_null_file_list[i]]
        actual_df = actual_df.orderBy([actual_df.columns[0]])
        expected_df = same_null_df_dict[same_null_file_list[i]]
        expected_df = expected_df.orderBy([expected_df.columns[0]])
        assert_df_equality(actual_df, expected_df)


def test_GIVEN_unassigned_imdb_df_WHEN_assign_data_type_THEN_return_cleansed_data(spark):

    from src.aws_glue.imdb_data_cleansing_glue import assign_data_type

    # GIVEN
    unassigned_file_list = [
        "name.basics.tsv",
        "title.akas.tsv",
        "title.basics.tsv",
        "title.crew.tsv",
        "title.episode.tsv",
        "title.principals.tsv",
        "title.ratings.tsv"
    ]
    unassigned_df_dict = {}
    for file_name in unassigned_file_list:
        df = spark.read.csv("test/src/aws_glue/testing_files/imdb/assign_data_type/" + file_name, sep="\t", header="true")
        unassigned_df_dict[file_name] = df

    # WHEN
    cleansed_df_dict = assign_data_type(unassigned_df_dict)

    # THEN
    assigned_file_list = [
        "assigned_name.basics.tsv",
        "assigned_title.akas.tsv",
        "assigned_title.basics.tsv",
        "assigned_title.crew.tsv",
        "assigned_title.episode.tsv",
        "assigned_title.principals.tsv",
        "assigned_title.ratings.tsv"
    ]
    assigned_df_dict = {}
    ALL_DATA_TYPE_DICT = {
        "assigned_name.basics.tsv": {
            "nconst": "string",
            "primaryName": "string",
            "birthYear": "int",
            "deathYear": "int",
            "primaryProfession": "string",
            "knownForTitles": "string"
        },
        "assigned_title.akas.tsv": {
            "titleId": "string",
            "ordering": "int",
            "title": "string",
            "region": "string",
            "language": "string",
            "types": "string",
            "attributes": "string",
            "isOriginalTitle": "boolean",
        },
        "assigned_title.basics.tsv": {
            "tconst": "string",
            "titleType": "string",
            "primaryTitle": "string",
            "originalTitle": "string",
            "isAdult": "boolean",
            "startYear": "int",
            "endYear": "int",
            "runtimeMinutes": "int",
            "genres": "string"
        },
        "assigned_title.crew.tsv": {
            "tconst": "string",
            "directors": "string",
            "writers": "string"
        },
        "assigned_title.episode.tsv": {
            "tconst": "string",
            "parentTconst": "string",
            "seasonNumber": "int",
            "episodeNumber": "int"
        },
        "assigned_title.principals.tsv": {
            "tconst": "string",
            "ordering": "int",
            "nconst": "string",
            "category": "string",
            "job": "string",
            "characters": "string"
        },
        "assigned_title.ratings.tsv": {
            "tconst": "string",
            "averageRating": "float",
            "numVotes": "int"
        }
    }

    for file_name in assigned_file_list:
        df = spark.read.csv("test/src/aws_glue/testing_files/imdb/assign_data_type/" + file_name, sep="\t", header="true")
        data_type_dict = ALL_DATA_TYPE_DICT[file_name]
        for column_name, data_type in data_type_dict.items():
            df = df.withColumn(column_name, col(column_name).cast(data_type))
        assigned_df_dict[file_name] = df

    for i in range(0, len(unassigned_file_list)):
        actual_df = cleansed_df_dict[unassigned_file_list[i]]
        actual_df = actual_df.orderBy([actual_df.columns[0], actual_df.columns[1], actual_df.columns[2]])
        expected_df = assigned_df_dict[assigned_file_list[i]]
        expected_df = expected_df.orderBy([expected_df.columns[0], expected_df.columns[1], expected_df.columns[2]])
        assert_df_equality(actual_df, expected_df)
