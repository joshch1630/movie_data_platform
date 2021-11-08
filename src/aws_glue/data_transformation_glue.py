import sys
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions
from datetime import date
from pyspark.sql.functions import avg, count, col, split, lit, when


DEFAULT_REGION = "us-east-1"
glue_context = GlueContext(SparkContext.getOrCreate())
logger = glue_context.get_logger()
spark = glue_context.spark_session

DATABASE_NAME = "movie_database_platform"
IMDB_TITLE_BASICS = "imdb_title_basics"
IMDB_TITLE_RATINGS = "imdb_title_ratings"
MOVIE_LENS_MOVIES = "movie_lens_movies"
MOVIE_LENS_RATINGS = "movie_lens_ratings"
REFINED_ZONE_PATH = "/refined_zone/"
IMDB_PATH = "imdb/"
MOVIE_LENS_PATH = "movie_lens/"
FILTER_START_YEAR = 1950

def main():
    logger.info("===== Start data transformation =====")

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

        # imdb
        imdb_title_basics_df = extract_imdb_title_basics_with_movie_type_from_cleansed_zone()
        imdb_title_ratings_df = extract_imdb_title_ratings_from_cleansed_zone()

        imdb_title_basics_ratings_df = imdb_data_transformation(imdb_title_basics_df, imdb_title_ratings_df)

        load_imdb_data_into_s3_refined_zone(args['s3_bucket'], imdb_title_basics_ratings_df)

        # movieLens
        movie_lens_movies_df = extract_movie_lens_movies_from_cleansed_zone()
        movie_lens_ratings_df = extract_movie_lens_ratings_from_cleansed_zone()

        movie_lens_movies_ratings_df = movie_lens_data_transformation(movie_lens_movies_df, movie_lens_ratings_df)

        load_movie_lens_data_into_s3_refined_zone(args['s3_bucket'], movie_lens_movies_ratings_df)

    except Exception as err:
        logger.info("Err")
        raise Exception(err)

    logger.info("===== End data transformation =====")


def extract_imdb_title_basics_with_movie_type_from_cleansed_zone():
    logger.info("Start extract_imdb_title_basics_from_cleansed_zone")

    current_year = date.today().year
    ONLY_MOIVE_TYPE_AND_LIMITED_YEAR_CONDITION = "(titleType == 'movie' and startyear >= {} and startyear < {})".format(FILTER_START_YEAR, current_year)

    logger.info("ONLY_MOIVE_TYPE_CONDITION: {}".format(ONLY_MOIVE_TYPE_AND_LIMITED_YEAR_CONDITION))

    df = glue_context.create_dynamic_frame.from_catalog(database=DATABASE_NAME,
                                                        table_name=IMDB_TITLE_BASICS,
                                                        push_down_predicate=ONLY_MOIVE_TYPE_AND_LIMITED_YEAR_CONDITION).toDF()

    logger.info("Before transformation - imdb_title_basics - row count: {}".format(df.count()))
    logger.info("Before transformation - imdb_title_basics - column list: {}".format(df.columns))

    return df


def extract_imdb_title_ratings_from_cleansed_zone():
    logger.info("Start extract_imdb_title_ratings_from_cleansed_zone")

    df = glue_context.create_dynamic_frame.from_catalog(database=DATABASE_NAME,
                                                        table_name=IMDB_TITLE_RATINGS).toDF()

    logger.info("Before transformation - imdb_title_ratings - row count: {}".format(df.count()))
    logger.info("Before transformation - imdb_title_ratings - column list: {}".format(df.columns))

    return df


def imdb_data_transformation(imdb_title_basics_df, imdb_title_ratings_df):
    logger.info("Start imdb_data_transformation")

    imdb_title_basics_df = split_imdb_genres_colunm(imdb_title_basics_df)

    imdb_title_basics_ratings_df = join_imdb_title_basics_with_imdb_title_ratings(imdb_title_basics_df, imdb_title_ratings_df)

    return imdb_title_basics_ratings_df


def split_imdb_genres_colunm(imdb_title_basics_df):
    logger.info("Start split_imdb_genres_colunm")

    logger.info("Before split_imdb_genres_colunm - imdb_title_basics_df - row count: {}".format(imdb_title_basics_df.count()))
    logger.info("Before split_imdb_genres_colunm - imdb_title_basics_df - column list: {}".format(imdb_title_basics_df.columns))

    imdb_title_basics_df = (imdb_title_basics_df.withColumn("genres_1", split(imdb_title_basics_df['genres'], ",").getItem(0))
                            .withColumn("genres_2", split(imdb_title_basics_df['genres'], ",").getItem(1))
                            .withColumn("genres_3", split(imdb_title_basics_df['genres'], ",").getItem(2)))

    imdb_title_basics_df = imdb_title_basics_df.drop("genres")

    logger.info("After split_imdb_genres_colunm - imdb_title_basics_df - row count: {}".format(imdb_title_basics_df.count()))
    logger.info("After split_imdb_genres_colunm - imdb_title_basics_df - column list: {}".format(imdb_title_basics_df.columns))

    return imdb_title_basics_df


def join_imdb_title_basics_with_imdb_title_ratings(imdb_title_basics_df, imdb_title_ratings_df):
    logger.info("Start join_imdb_title_basics_with_imdb_title_ratings")

    logger.info("Before join_imdb_title_basics_with_imdb_title_ratings - imdb_title_basics_df - row count: {}".format(imdb_title_basics_df.count()))
    logger.info("Before join_imdb_title_basics_with_imdb_title_ratings - imdb_title_basics_df - column list: {}".format(imdb_title_basics_df.columns))
    logger.info("Before join_imdb_title_basics_with_imdb_title_ratings - imdb_title_ratings_df - row count: {}".format(imdb_title_ratings_df.count()))
    logger.info("Before join_imdb_title_basics_with_imdb_title_ratings - imdb_title_ratings_df - column list: {}".format(imdb_title_ratings_df.columns))

    imdb_title_basics_ratings_df = imdb_title_basics_df.join(imdb_title_ratings_df,
                                                             imdb_title_basics_df['tconst'] == imdb_title_ratings_df['tconst'],
                                                             how='left').drop(imdb_title_ratings_df['tconst'])

    logger.info("After join_imdb_title_basics_with_imdb_title_ratings - imdb_title_basics_ratings_df - row count: {}".format(imdb_title_basics_ratings_df.count()))
    logger.info("After join_imdb_title_basics_with_imdb_title_ratings - imdb_title_basics_ratings_df - column list: {}".format(imdb_title_basics_ratings_df.columns))

    return imdb_title_basics_ratings_df


def extract_movie_lens_movies_from_cleansed_zone():
    logger.info("Start extract_movie_lens_movies_from_cleansed_zone")

    df = glue_context.create_dynamic_frame.from_catalog(database=DATABASE_NAME,
                                                        table_name=MOVIE_LENS_MOVIES).toDF()

    logger.info("Before transformation - movie_lens_movies - row count: {}".format(df.count()))
    logger.info("Before transformation - movie_lens_movies - column list: {}".format(df.columns))

    return df


def extract_movie_lens_ratings_from_cleansed_zone():
    logger.info("Start extract_movie_lens_ratings_from_cleansed_zone")

    df = glue_context.create_dynamic_frame.from_catalog(database=DATABASE_NAME,
                                                        table_name=MOVIE_LENS_RATINGS).toDF()

    logger.info("Before transformation - movie_lens_ratings - row count: {}".format(df.count()))
    logger.info("Before transformation - movie_lens_ratings - column list: {}".format(df.columns))

    return df


def movie_lens_data_transformation(movie_lens_movies_df, movie_lens_ratings_df):
    logger.info("Start movie_lens_data_transformation")

    movie_lens_movies_df = get_year_from_title(movie_lens_movies_df)
    movie_lens_movies_df = split_movie_lens_genres_colunm(movie_lens_movies_df)
    movie_lens_movies_df = filter_year_range(movie_lens_movies_df)

    movie_lens_ratings_group_df = group_ratings_by_movie_id(movie_lens_ratings_df)

    movie_lens_movies_ratings_df = join_movie_lens_movies_with_movie_lens_ratings_group(movie_lens_movies_df, movie_lens_ratings_group_df)

    return movie_lens_movies_ratings_df


def get_year_from_title(movie_lens_movies_df):
    logger.info("Start get_year_from_title")

    logger.info("Before get_year_from_title - movie_lens_movies_df - row count: {}".format(movie_lens_movies_df.count()))
    logger.info("Before get_year_from_title - movie_lens_movies_df - column list: {}".format(movie_lens_movies_df.columns))

    movie_lens_movies_df = movie_lens_movies_df.withColumn("year", movie_lens_movies_df['title'].substr(-5, 4))

    movie_lens_movies_df = movie_lens_movies_df.withColumn("year", when(col("year").rlike("^[0-9]*$"), col("year")).otherwise("null"))

    logger.info("After get_year_from_title - movie_lens_movies_df - row count: {}".format(movie_lens_movies_df.count()))
    logger.info("After get_year_from_title - movie_lens_movies_df - column list: {}".format(movie_lens_movies_df.columns))

    return movie_lens_movies_df


def split_movie_lens_genres_colunm(movie_lens_movies_df):
    logger.info("Start split_movie_lens_genres_colunm")

    logger.info("Before split_movie_lens_genres_colunm - movie_lens_movies_df - row count: {}".format(movie_lens_movies_df.count()))
    logger.info("Before split_movie_lens_genres_colunm - movie_lens_movies_df - column list: {}".format(movie_lens_movies_df.columns))

    movie_lens_movies_df = (movie_lens_movies_df.withColumn("genres_1", split(movie_lens_movies_df['genres'], """\|""").getItem(0))
                            .withColumn("genres_2", split(movie_lens_movies_df['genres'], """\|""").getItem(1))
                            .withColumn("genres_3", split(movie_lens_movies_df['genres'], """\|""").getItem(2))
                            .withColumn("genres_4", split(movie_lens_movies_df['genres'], """\|""").getItem(3))
                            .withColumn("genres_5", split(movie_lens_movies_df['genres'], """\|""").getItem(4))
                            .withColumn("genres_6", split(movie_lens_movies_df['genres'], """\|""").getItem(5)))

    movie_lens_movies_df = movie_lens_movies_df.drop("genres")

    logger.info("After split_movie_lens_genres_colunm - movie_lens_movies_df - row count: {}".format(movie_lens_movies_df.count()))
    logger.info("After split_movie_lens_genres_colunm - movie_lens_movies_df - column list: {}".format(movie_lens_movies_df.columns))

    return movie_lens_movies_df


def filter_year_range(movie_lens_movies_df):
    logger.info("Start filter_year_range")

    logger.info("Before filter_year_range - movie_lens_movies_df - row count: {}".format(movie_lens_movies_df.count()))
    logger.info("Before filter_year_range - movie_lens_movies_df - column list: {}".format(movie_lens_movies_df.columns))

    current_year = date.today().year
    movie_lens_movies_df = movie_lens_movies_df.where("year >= {} and year < {}".format(FILTER_START_YEAR, current_year))

    logger.info("After filter_year_range - movie_lens_movies_df - row count: {}".format(movie_lens_movies_df.count()))
    logger.info("After filter_year_range - movie_lens_movies_df - column list: {}".format(movie_lens_movies_df.columns))

    return movie_lens_movies_df


def group_ratings_by_movie_id(movie_lens_ratings_df):
    logger.info("Start group_ratings_by_movie_id")

    logger.info("Before group_ratings_by_movie_id - movie_lens_ratings_df - row count: {}".format(movie_lens_ratings_df.count()))
    logger.info("Before group_ratings_by_movie_id - movie_lens_ratings_df - column list: {}".format(movie_lens_ratings_df.columns))

    movie_lens_ratings_group_df = movie_lens_ratings_df.groupBy("movieId").agg(
        avg("rating").alias("avg_rating"),
        count(lit(1)).alias("vote_count")
    ).select(col("movieid").alias("movieId"), "avg_rating", "vote_count")

    logger.info("After group_ratings_by_movie_id - movie_lens_ratings_group_df - row count: {}".format(movie_lens_ratings_group_df.count()))
    logger.info("After group_ratings_by_movie_id - movie_lens_ratings_group_df - column list: {}".format(movie_lens_ratings_group_df.columns))

    return movie_lens_ratings_group_df


def join_movie_lens_movies_with_movie_lens_ratings_group(movie_lens_movies_df, movie_lens_ratings_group_df):
    logger.info("Start join_movie_lens_movies_with_movie_lens_ratings_group")

    logger.info("Before join_movie_lens_movies_with_movie_lens_ratings_group - movie_lens_movies_df - row count: {}".format(movie_lens_movies_df.count()))
    logger.info("Before join_movie_lens_movies_with_movie_lens_ratings_group - movie_lens_movies_df - column list: {}".format(movie_lens_movies_df.columns))
    logger.info("Before join_movie_lens_movies_with_movie_lens_ratings_group - movie_lens_ratings_group_df - row count: {}".format(movie_lens_ratings_group_df.count()))
    logger.info("Before join_movie_lens_movies_with_movie_lens_ratings_group - movie_lens_ratings_group_df - column list: {}".format(movie_lens_ratings_group_df.columns))

    movie_lens_movies_ratings_df = movie_lens_movies_df.join(movie_lens_ratings_group_df,
                                                             movie_lens_movies_df['movieId'] == movie_lens_ratings_group_df['movieId'],
                                                             how='left').drop(movie_lens_ratings_group_df['movieId'])

    logger.info("After join_movie_lens_movies_with_movie_lens_ratings_group - movie_lens_movies_ratings_df - row count: {}".format(movie_lens_movies_ratings_df.count()))
    logger.info("After join_movie_lens_movies_with_movie_lens_ratings_group - movie_lens_movies_ratings_df - column list: {}".format(movie_lens_movies_ratings_df.columns))

    return movie_lens_movies_ratings_df


def load_imdb_data_into_s3_refined_zone(s3_bucket, df):
    logger.info("Start load_data_into_s3_refined_zone")

    file_name = "imdb_title_basics_ratings"
    file_path = "s3://" + s3_bucket + REFINED_ZONE_PATH + IMDB_PATH + file_name
    logger.info("Save {} into S3 {}".format(file_name, file_path))
    logger.info("After transformation - imdb_title_basics_ratings_df - row count: {}".format(df.count()))
    logger.info("After transformation - imdb_title_basics_ratings_df - column list: {}".format(df.columns))

    df.write.mode("overwrite").format("parquet").partitionBy(["startyear", "genres_1", "genres_2", "genres_3"]).save(file_path)


def load_movie_lens_data_into_s3_refined_zone(s3_bucket, df):
    logger.info("Start load_movie_lens_data_into_s3_refined_zone")

    file_name = "movie_lens_movies_ratings"
    file_path = "s3://" + s3_bucket + REFINED_ZONE_PATH + MOVIE_LENS_PATH + file_name
    logger.info("Save {} into S3 {}".format(file_name, file_path))
    logger.info("After transformation - movie_lens_movies_ratings_df - row count: {}".format(df.count()))
    logger.info("After transformation - movie_lens_movies_ratings_df - column list: {}".format(df.columns))

    df.write.mode("overwrite").format("parquet").partitionBy(["year", "genres_1", "genres_2", "genres_3", "genres_4", "genres_5", "genres_6"]).save(file_path)


if __name__ == "__main__":
    main()
