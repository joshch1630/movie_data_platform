import sys
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions
from pyspark.sql.functions import when, col, from_unixtime, to_timestamp

DEFAULT_REGION = "us-east-1"
glue_context = GlueContext(SparkContext.getOrCreate())
logger = glue_context.get_logger()

MOVIE_LENS_PATH = "movie_lens/"
RAW_ZONE_PATH = "/raw_zone/"
CLEANSED_ZONE_PATH = "/cleansed_zone/"

MOVIE_LENS_FILE_NAME_LIST = [
    "genome-scores.csv",
    "genome-tags.csv",
    "links.csv",
    "movies.csv",
    "ratings.csv",
    "tags.csv"
]

ALL_DATA_TYPE_DICT = {
    "genome-scores.csv": {
        "movieId": "string",
        "tagId": "string",
        "relevance": "string"
    },
    "genome-tags.csv": {
        "tagId": "string",
        "tag": "string"
    },
    "links.csv": {
        "movieId": "string",
        "imdbId": "string",
        "tmdbId": "string"
    },
    "movies.csv": {
        "movieId": "string",
        "title": "string",
        "genres": "string"
    },
    "ratings.csv": {
        "userId": "string",
        "movieId": "string",
        "rating": "float",
        "timestamp": "timestamp",
    },
    "tags.csv": {
        "userId": "string",
        "movieId": "string",
        "tag": "string",
        "timestamp": "timestamp",
    },
}


def main():
    logger.info("===== Start MovieLens data cleansing =====")

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

        df_dict = extract_data_from_s3_raw_zone(args['s3_bucket'], MOVIE_LENS_FILE_NAME_LIST)

        data_cleansing(df_dict)

        load_data_into_s3_cleansed_zone(args['s3_bucket'], df_dict)

    except Exception as err:
        logger.info("Err")
        raise Exception(err)

    logger.info("===== End MovieLens data cleansing =====")


def extract_data_from_s3_raw_zone(s3_bucket, file_list):
    logger.info("Start extract_raw_data_from_s3")
    df_dict = {}
    for file_name in file_list:
        file_path = "s3://" + s3_bucket + RAW_ZONE_PATH + MOVIE_LENS_PATH + file_name
        logger.info("Extract {} from {} on S3".format(file_name, file_path))

        df = glue_context.create_dynamic_frame_from_options(connection_type="s3",
                                                            connection_options={"paths": [file_path]},
                                                            format_options={"withHeader": True},
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
            if data_type == "timestamp":
                df = df.withColumn(column_name, to_timestamp(from_unixtime(col(column_name)), "yyyy-MM-dd HH:mm:ss"))
            else: 
                df = df.withColumn(column_name, col(column_name).cast(data_type))
        df_dict[name] = df

    return df_dict


def load_data_into_s3_cleansed_zone(s3_bucket, df_dict):
    logger.info("Start load_cleansed_data_into_s3")

    for name, df in df_dict.items():
        file_name = "movie_lens_" + name.replace(".csv", "")
        file_path = "s3://" + s3_bucket + CLEANSED_ZONE_PATH + MOVIE_LENS_PATH + file_name
        logger.info("Save {} into S3 {}".format(file_name, file_path))
        logger.info("After cleansing - {} - row count: {}".format(file_name, df.count()))
        logger.info("After cleansing - {} - column list: {}".format(file_name, df.columns))

        df.write.mode("overwrite").format("parquet").save(file_path)



if __name__ == "__main__":
    main()
