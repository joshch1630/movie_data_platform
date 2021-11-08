import logging
import boto3
import time
from data_analysis_imdb_query import IMDB_QUERY_DICT_LIST
from data_analysis_movie_lens_query import MOVIE_LENS_QUERY_DICT_LIST

DEFAULT_REGION = "us-east-1"
logger = logging.getLogger()
logger.setLevel(logging.INFO)

DATABASE = "movie_database_platform"
ATHENA_RESULT_BUCKET = "s3://movie-data-platform.mpd/athena/query_result/"
EACH_QUERY_WAIT_TIME_SECOND = 3
ALL_QUERY_WAIT_TIME_SECOND = 10
MAX_NUM_RETRY = 6
DYNAMODB_TABLE_NAME = "mdp_data_analysis"

def lambda_handler(event, context):

    logger.info("===== Start data analysis =====")

    athena = boto3.client("athena", region_name=DEFAULT_REGION)
    dynamodb = boto3.client("dynamodb", region_name=DEFAULT_REGION)

    query_dict_list = IMDB_QUERY_DICT_LIST + MOVIE_LENS_QUERY_DICT_LIST

    run_all_query(athena, query_dict_list)

    get_all_query_result(athena, query_dict_list)

    save_result_into_dynamodb(dynamodb, query_dict_list)

    logger.info("===== End data analysis =====")

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        }
    }


def run_all_query(athena, query_dict_list):
    logger.info("Start run_all_query")

    for query_dict in query_dict_list:
        response = athena.start_query_execution(
            QueryString=query_dict['query'],
            QueryExecutionContext={
                'Database': DATABASE
            },
            ResultConfiguration={
                'OutputLocation': ATHENA_RESULT_BUCKET,
            }
        )
        query_dict['query_execution_id'] = response['QueryExecutionId']

        logger.info("data_title: {}".format(str(query_dict['data_title'])))
        logger.info("query_execution_id: {}".format(str(query_dict['query_execution_id'])))
        time.sleep(EACH_QUERY_WAIT_TIME_SECOND)


def get_all_query_result(athena, query_dict_list):
    logger.info("Start get_all_query_result")

    num_retry = 0
    while is_all_query_not_completed(query_dict_list) and num_retry < MAX_NUM_RETRY:
        time.sleep(ALL_QUERY_WAIT_TIME_SECOND)

        for query_dict in query_dict_list:
            query_execution = athena.get_query_execution(QueryExecutionId=query_dict['query_execution_id'])
            query_execution_status = query_execution['QueryExecution']['Status']['State']

            if query_execution_status == "FAILED":
                raise Exception("Query error for {} with query name {}".format(query_execution, query_dict['data_title']))

            if query_execution_status == 'SUCCEEDED' and not query_dict['is_completed']:
                result = athena.get_query_results(QueryExecutionId=query_dict['query_execution_id'])
                result_data_list = process_row(result)
                query_dict['result_data'] = result_data_list
                query_dict['is_completed'] = True

        num_retry += 1


def is_all_query_not_completed(query_dict_list):
    for query_dict in query_dict_list:
        if not query_dict['is_completed']:
            return True
    return False


def process_row(response):
    logger.info("Start process_row")

    column_name_list = []
    result_data_list = []

    column_name_data_row = response['ResultSet']['Rows'].pop(0)
    for column_name_data in column_name_data_row['Data']:
        if "VarCharValue" in column_name_data:
            column_name_list.append(column_name_data['VarCharValue'])

    logger.info("column_name_list: {}".format(str(column_name_list)))

    for row in response['ResultSet']['Rows']:
        result_row = {}
        for i, column_name in enumerate(column_name_list):
            column_data = row['Data'][i]
            if "VarCharValue" in column_data:
                result_row[column_name] = column_data['VarCharValue']
            else:
                result_row[column_name] = "NA"

        result_data_list.append(result_row)

    return result_data_list


def save_result_into_dynamodb(dynamodb, query_dict_list):
    logger.info("Start save_data_into_dynamodb")

    for query_dict in query_dict_list:
        logger.info("save data_title: {}".format(query_dict['data_title']))
        item = {
            "data_title": {"S": query_dict['data_title']},
            "data_type": {"S": query_dict['data_type']},
            "query_execution_id": {"S": query_dict['query_execution_id']},
            "data_content": {"S": str(query_dict['result_data'])}
        }
        dynamodb.put_item(TableName=DYNAMODB_TABLE_NAME, Item=item)
