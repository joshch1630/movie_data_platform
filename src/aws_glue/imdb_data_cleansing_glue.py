import sys
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions
from pyspark.sql.functions import when, col


DEFAULT_REGION = "us-east-1"
glue_context = GlueContext(SparkContext.getOrCreate())
logger = glue_context.get_logger()
spark = glue_context.spark_session

IMDB_PATH = "imdb/"
RAW_ZONE_PATH = "/raw_zone/"
CLEANSED_ZONE_PATH = "/cleansed_zone/"

IMDB_FILE_NAME_LIST = [
    "name.basics.tsv",
    "title.akas.tsv",
    "title.basics.tsv",
    "title.crew.tsv",
    "title.episode.tsv",
    "title.principals.tsv",
    "title.ratings.tsv"
]

ALL_DATA_TYPE_DICT = {
    "name.basics.tsv": {
        "nconst": "string",
        "primaryName": "string",
        "birthYear": "int",
        "deathYear": "int",
        "primaryProfession": "string",
        "knownForTitles": "string"
    },
    "title.akas.tsv": {
        "titleId": "string",
        "ordering": "int",
        "title": "string",
        "region": "string",
        "language": "string",
        "types": "string",
        "attributes": "string",
        "isOriginalTitle": "boolean",
    },
    "title.basics.tsv": {
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
    "title.crew.tsv": {
        "tconst": "string",
        "directors": "string",
        "writers": "string"
    },
    "title.episode.tsv": {
        "tconst": "string",
        "parentTconst": "string",
        "seasonNumber": "int",
        "episodeNumber": "int"
    },
    "title.principals.tsv": {
        "tconst": "string",
        "ordering": "int",
        "nconst": "string",
        "category": "string",
        "job": "string",
        "characters": "string"
    },
    "title.ratings.tsv": {
        "tconst": "string",
        "averageRating": "float",
        "numVotes": "int"
    }
}

ALL_PARTITION_DICT = {
    "name.basics.tsv": ["birthYear", "deathYear"],
    "title.akas.tsv": ["region", "language", "types"],
    "title.basics.tsv": ["titleType", "startYear", "endYear"],
    "title.principals.tsv": ["category"]
}


def main():
    logger.info("===== Start IMDB data cleansing =====")

    try:
        args = getResolvedOptions(sys.argv, [
            "job_name",
            "aws_region",
            "s3_bucket"
        ]
        )
        logger.info("job_name: {}".format(args['job_name']))
        logger.info("aws_region: {}".format(args['aws_region']))
        logger.info("s3_bucket: {}".format(args['s3_bucket']))

        df_dict = extract_data_from_s3_raw_zone(args['s3_bucket'], IMDB_FILE_NAME_LIST)

        data_cleansing(df_dict)

        load_data_into_s3_cleansed_zone(args['s3_bucket'], df_dict)

    except Exception as err:
        logger.info("Err")
        raise Exception(err)

    logger.info("===== End IMDB data cleansing =====")


def extract_data_from_s3_raw_zone(s3_bucket, file_list):
    logger.info("Start extract_raw_data_from_s3")
    df_dict = {}
    for file_name in file_list:
        file_path = "s3://" + s3_bucket + RAW_ZONE_PATH + IMDB_PATH + file_name
        logger.info("Extract {} from {} on S3".format(file_name, file_path))

        df = glue_context.create_dynamic_frame_from_options(connection_type="s3",
                                                            connection_options={"paths": [file_path]},
                                                            format_options={"withHeader": True, "separator": "\t"},
                                                            format="csv").toDF()

        logger.info("Before cleansing - {} - row count: {}".format(file_name, df.count()))
        logger.info("Before cleansing - {} - column list: {}".format(file_name, df.columns))

        df_dict[file_name] = df

    return df_dict


def data_cleansing(df_dict):
    logger.info("Start data_cleansing")
    remove_duplicated_data(df_dict)
    standardize_null_value(df_dict)
    assign_data_type(df_dict)


def remove_duplicated_data(df_dict):
    logger.info("Start remove_duplicated_data")

    for name, df in df_dict.items():
        logger.info("Remove {} duplicate data".format(name))
        df_dict[name] = df.drop_duplicates()

    return df_dict


def standardize_null_value(df_dict):
    logger.info("Start standardize_null_value")

    for name, df in df_dict.items():
        logger.info("Standardize {} null data".format(name))
        for column_name in df.columns:
            logger.info("Checking {} col null data".format(column_name))
            df = df.withColumn(column_name,
                               when(
                                   (col(column_name) == "N/A")
                                   | (col(column_name) == "None")
                                   | (col(column_name) == "Null")
                                   | (col(column_name) == "NA")
                                   | (col(column_name) == "na")
                                   | (col(column_name) == "NaN")
                                   | (col(column_name) == "")
                                   | (col(column_name) == " ")
                                   | (col(column_name) == "none")
                                   | (col(column_name) == "\\N"), "null").otherwise(col(column_name)))
        df_dict[name] = df

    return df_dict


def assign_data_type(df_dict):
    logger.info("Start assign_data_type")

    for name, df in df_dict.items():
        logger.info("assign {} data type".format(name))
        data_type_dict = ALL_DATA_TYPE_DICT[name]
        for column_name, data_type in data_type_dict.items():
            logger.info("Assign col {} to {})".format(column_name, data_type))
            df = df.withColumn(column_name, col(column_name).cast(data_type))
        df_dict[name] = df

    return df_dict


def load_data_into_s3_cleansed_zone(s3_bucket, df_dict):
    logger.info("Start load_cleansed_data_into_s3")

    for name, df in df_dict.items():
        file_name = "imdb_" + name.replace(".tsv", "")
        file_path = "s3://" + s3_bucket + CLEANSED_ZONE_PATH + IMDB_PATH + file_name
        logger.info("Save {} into S3 {}".format(file_name, file_path))
        logger.info("After cleansing - {} - row count: {}".format(file_name, df.count()))
        logger.info("After cleansing - {} - column list: {}".format(file_name, df.columns))

        if name in ALL_PARTITION_DICT:
            df.write.mode("overwrite").format("parquet").partitionBy(ALL_PARTITION_DICT[name]).save(file_path)
        else:
            df.write.mode("overwrite").format("parquet").save(file_path)


if __name__ == "__main__":
    main()
