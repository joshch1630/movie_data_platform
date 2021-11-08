# Data Pipeline

![Data Piepline](https://moviedataplatform.com/img/aws_data_pipeline.png)

*This is a technical section for software engineers to comprehend what is going on under the hood.
If you are not a software engineer, you can leave this page now (or stay because you are eager to learn more).*

>📍 *"Data pipelines are sets of processes that move and transform data from various sources to a destination where new value can be derived. They are the foundation of analytics, reporting , and machine learning capabilities."* 

The above AWS architecture diagram represents the cloud infrastructure on AWS platform. We can divide the diagram into five categories:

1. Data Source
2. Data Lake
3. Data Mart
4. CI/CD
5. Web

The source code can be found in GitHub [here](https://github.com/joshch1630/movie_data_platform "here").

## 🔷 Data Source

There are two data sources feeding the Movie Data Platform.

 1. [IMDb](https://www.imdb.com/interfaces/)
 2. [MovieLens](https://grouplens.org/datasets/movielens/) - [(GroupLens)](https://grouplens.org/) 

### 🔹 IMDb

IMDb Datasets are gzipped, **tab-separated-values (tsv)** formatted files in the UTF-8 character set. 

There are 7 datasets available as follows:

- **title.akas.tsv.gz** -> Contains alternate titles information
- **title.basics.tsv.gz** -> Contains basic titles information
- **title.crew.tsv.gz** -> Contains the director and writer information for all the titles in IMDb
- **title.episode.tsv.gz** -> Contains the tv episode information
- **title.principals.tsv.gz** -> Contains the principal cast/crew for titles
- **title.ratings.tsv.gz** -> Contains the IMDb rating and votes information for titles
- **name.basics.tsv.gz** -> Contains detail information for people

### 🔹 MovieLens

MovieLens Datasets are zipped, **comma-separated values (csv)** files with a single header row. These files are encoded as UTF-8.

There are 6 datasets available as follows:

- **ratings.csv** -> Contains rating information
- **tags.csv** -> Contains tags information of movies
- **movies.csv** -> Contains movie information (Movie titles are entered manually or imported from https://www.themoviedb.org/)
- **links.csv** -> Contains Identifiers information that can be used to link to other sources e.g. IMDb, TMDB
- **genome-scores.csv** -> Contains "Tag Genome" movie-tag relevance information
- **genome-tags.csv** -> Contains "Tag Genome" tag IDs information

## 🔷 Data Lake

> 📍 *"A data lake is where data is stored, but without the structure or query optimization of a data warehouse. It will likely contain a high volume of data as well as a variety of data types."* 

Data Lake contains two important processes:

1. Data Injection
2. Data Cleansing

### 🔹 Data Injection

In AWS, I use Amazon EventBridge with the event schedule rule (act like cron) to trigger the injection service yearly.

```shell
cron(0 1 1 4 ? *)
```

The EventBridge will trigger the AWS Lambda and the Lambda function will use wget to retrieve IMDb and MovieLens dataset. This Lambda function also unzip the dataset and save the raw files into S3 bucket as a Raw Zone.

```python
# Get the files with wget
wget.download(remote_url, zip_file_path)

# Save the raw files into S3 by using boto3
s3 = boto3.resource("s3")
s3.Bucket(S3_BUCKET_NAME).put_object(Key=s3_raw_path, Body=file_content)
```

After the injection AWS Lambda function finish, it will trigger the AWS Glue job. This AWS Glue job will retrieve the raw files in S3 Raw Zone and carry out the Data Cleansing task.

#### 🔹 Unit Test

For the unit test, moto is applied to mock the boto3 AWS service with Given-When-Then unit test pattern in AWS Lambda.

```python
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
```

### 🔹 Data Cleansing

The Data Cleansing process helps to increase the data accuracy and consistency. AWS cloud platform provides the AWS Glue which is based on Apache Spark to preform data processing.

> 📍 *"Apache Spark is an open-source tool and a unified analytics engine for large-scale data processing. This framework can run in a standalone mode or on a cloud. It is designed for fast performance and uses RAM for caching and processing data."* 

In AWS Glue, pySpark is used to process the data. I highly recommend to use [Spark by {Examples}](https://sparkbyexamples.com/pyspark-tutorial/) for the pySpark guide.

The data cleansing job helps to remove the duplicated record, standardise the "Not Applicable" into `null` value and assign the data type.

You can find the code snippet below:

```python
# Extract data from s3 raw zone
df = glue_context.create_dynamic_frame_from_options(connection_type="s3",
                                                            connection_options={"paths": [file_path]},
                                                            format_options={"withHeader": True, "separator": "\t"},
                                                            format="csv").toDF()
# Remove duplicated data
df.drop_duplicates()

# Standardize the null value
df.withColumn(column_name,
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

# Assign data type
df.withColumn(column_name, col(column_name).cast(data_type))
```

After the cleansing, the data will be saved into S3 Cleansed Zone with parquet format with partition.

> 📍 *"Parquet is an efficient columnar data storage format that supports complex nested data structures in a flat columnar format. Parquet is perfect for services like AWS Athena andAmazon Redshift Spectrum which are serverless, interactive technologies."* 

```python
# Load data into S3 with partition
df.write.mode("overwrite").format("parquet").partitionBy(ALL_PARTITION_DICT[name]).save(file_path)
```

When the AWS Glue job end, the Glue crawler will be triggered to crawl the meta data and save them into Glue Data Catalog.

> 📍 *"The AWS Glue Data Catalog is a managed service that lets you store, annotate, and share metadata in the AWS Cloud in the same way you would in an Apache Hive metastore."* 

Data Analyst or Data Scientist can access the data by using SQL query in AWS Athena.

> 📍 *"Amazon Athena is an interactive query service that makes it easy to analyze data in Amazon S3 using standard SQL."* 

#### 🔹 Unit Test

For the unit test, same as data injection, moto is applied to mock the boto3 AWS service with Given-When-Then unit test pattern in AWS Glue.

```python
# Setup Spark in unit test
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
```

## 🔷 Data Mart

> 📍 *"A data mart is a subset of a data lake or data warehouse oriented to a specific business line. Data marts contain repositories of summarized data collected for analysis on a specific section or unit within an organization."* 

In Movie Data Platform, there is only a single Data Mart built. The prepose of this Data Mart is to provide analysed data to Data Visualization which is a Web Application.

The main task in Data Mart is to carry out the Data Transformation. We can find more detail in the below section.

### 🔹 Data Transformation

> 📍 *"A Data Transformation can be something as simple as converting a timestamp stored in a table from one time zone to another. It can also be a more complex operation that creates a new metric from multiple source columns that are aggregated and filtered through some business logic."* 

There are two jobs in Data Transformation:
1. AWS Glue -  Transform the cleansed data into meaningful dataset by using pySpark to split columns and join tables.

```python
# Split the genres column
imdb_title_basics_df = (imdb_title_basics_df.withColumn("genres_1", split(imdb_title_basics_df['genres'], ",").getItem(0))
                            .withColumn("genres_2", split(imdb_title_basics_df['genres'], ",").getItem(1))
                            .withColumn("genres_3", split(imdb_title_basics_df['genres'], ",").getItem(2)))

# Join tables
imdb_title_basics_ratings_df = imdb_title_basics_df.join(imdb_title_ratings_df,
                                                             imdb_title_basics_df['tconst'] == imdb_title_ratings_df['tconst'],
                                                             how='left').drop(imdb_title_ratings_df['tconst'])
```
2. AWS Lambda - Run analytic SQL to generate result dataset and save into Amazon DynamoDB for the request from Web Application.

```python
# Use AWS Athena to run SQL statemnet in Data Lake
athena = boto3.client("athena", region_name=DEFAULT_REGION)
response = athena.start_query_execution(
            QueryString=query_dict['query'],
            QueryExecutionContext={
                'Database': DATABASE
            },
            ResultConfiguration={
                'OutputLocation': ATHENA_RESULT_BUCKET,
            }

# Save the query result into AWS Dynamodb
dynamodb = boto3.client("dynamodb", region_name=DEFAULT_REGION)
item = { "data_title": {"S": query_dict['data_title']},
            "data_type": {"S": query_dict['data_type']},
            "query_execution_id": {"S": query_dict['query_execution_id']},
            "data_content": {"S": str(query_dict['result_data'])}}
dynamodb.put_item(TableName=DYNAMODB_TABLE_NAME, Item=item)
```

## 🔷 CI/CD

CI/CD stand for **Continuous Integration** and **Continuous Delivery**.

> 📍 *"Continuous Integration describes the process of the changes flows to the repository. Continuous Delivery describes the process of the new product version automatic deployment."* 

The important thing in CI/CD is automation.

For the Continuous Integration part, **Github** is used to maintain the repository and handle the git operation.

For the Continuous Delivery part, **Terraform** (Infrastructure as Code) is used to deploy the AWS Cloud service automatically.

Here is the sample of AWS Lambda creation:

```terraform
resource "aws_lambda_function" "imdb_data_injection_lambda" {
  function_name    = "imdb_data_injection_lambda"
  filename         = "./src/aws_lambda/imdb_data_injection_lambda.zip"
  source_code_hash = data.archive_file.imdb_data_injection_lambda_file.output_base64sha256
  handler          = "imdb_data_injection_lambda.lambda_handler"
  runtime          = "python3.8"
  timeout          = 300
  memory_size      = 4096
  role             = aws_iam_role.mdp_lambda_role.arn
  tags             = var.tags
}
```

**circleci** is used to run the Unit Test Case and then run the Terraform code to deployment the infrastructure into AWS.

Here is the sample of running Terraform planning

```yaml
  plan-apply:
    docker:
      - image: docker.mirror.hashicorp.services/hashicorp/terraform:light
    steps:
      - attach_workspace:
          at: /tmp/project
      - run:
          name: terraform init & plan
          command: |
            cd /tmp/project
            terraform init -input=false
            terraform plan -out tfapply -var-file _variables.tfvars
      - persist_to_workspace:
          root: /tmp/project
          paths:
            - .
```

#  Web

*If you are a data engineer and not interested in Web Appliaction development, you can leave this section now (or stay because you are eager to learn more).*

![Data Piepline](https://moviedataplatform.com/img/aws_web.png)

## 🔷 Frontend

The Frontend of the Movie Data Platform is developed based on [React](https://reactjs.org/ "React") javascript library (Not framework!). In React 16.8, Hooks was introduced as a gaming changing feature so that we can write the code cleaner. `useState` and `useeffect` are heavily used to handle the state and lifecycle. 
Also, functional component is implemented with Hooks to write the code shorter and simpler rather than implementing class component.

Along with React, there are many libraries used. Let's talk more about them in Library section.

### 🔹 Library

Here is the list of main libraries (beside React) in Movie Data Platform:

1. [MUI](https://mui.com/ "MUI") - Material UI is a CSS/UI framework helping to build beautiful and responsive layouts and elements
2. [React Router](https://v5.reactrouter.com/web/guides/quick-start "React Router") - React Router enables the navigation among views of various components in a React Application, allows changing the browser URL, and keeps the UI in sync with the URL
3. [react-chartjs-2](https://github.com/reactchartjs/react-chartjs-2 "react-chartjs-2") - React wrapper for Chart.js which is a simple yet flexible JavaScript library for creating charts
4. [Axios](https://axios-http.com/ "Axios") - Axios is a simple promise based HTTP client for creating RESTful api requst.

### 🔹 Testing

[React Testing Library](https://testing-library.com/docs/react-testing-library/intro/ "React Testing Library") is used for the rendering testing on the screen.

```javascript
describe('Rendering - Top menu bar and side menu', () => {
........................
  test('renders side menu', () => {
    render(<App />);
    let expectedElement = '';
    // Home link
    const link = screen.getByRole('link', {
      name: /home/i
    });
    expectedElement = within(link).getByText(/home/i);
    expect(expectedElement).toBeInTheDocument();
........................
```

### 🔹 Web Hosting

The low cost and easy way to host the React application is to put it into S3 and enable the **"Static website hosting"**. After enable it, the "Bucket website endpoint" will be created for the internet access.

## 🔷 Backend

The Backend of the Movie Data Platform is supported by AWS Cloud.

1. **Amazon API Gateway** provides the API access from the frontend to the backend services. 
2. **AWS Lambda** provides the logic of the API call. Mostly query the data in the AWS Dynamodb.
3. **AWS Dynamodb** provides the NoSQL database for the analysized data storage.

## 🔷 DNS

The webside domain was registered in **Amazon Route 53**. **Cloudflare** is used as an internet access for the domain. Cloudflare provides many free services including DDoS attacks protection, distributed Remote edge caching and web traffic statistics.

## 🔷 CI/CD

Same as the Data Pipeline, **Github** and **circle ci** are used for CI/CD with **Terraform** as Infrastructure as Code deployment.