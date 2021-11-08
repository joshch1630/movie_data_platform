# 🔷 Data Source

_This section is about the general idea how data move end to end in the Movie Data Platform._
_If you want to know the architecture design or technical stack, you could visit the “Behind The Scenes” section._

There are two data sources feeding the Movie Data Platform.

 1. [IMDb](https://www.imdb.com/interfaces/)
 2. [MovieLens](https://grouplens.org/datasets/movielens/) - [(GroupLens)](https://grouplens.org/) 

## 🔹 IMDb

IMDb Datasets are gzipped, **tab-separated-values (tsv)** formatted files in the UTF-8 character set. 

There are 7 datasets available as follows:

- **title.akas.tsv.gz** -> Contains alternate titles information
- **title.basics.tsv.gz** -> Contains basic titles information
- **title.crew.tsv.gz** -> Contains the director and writer information for all the titles in IMDb
- **title.episode.tsv.gz** -> Contains the tv episode information
- **title.principals.tsv.gz** -> Contains the principal cast/crew for titles
- **title.ratings.tsv.gz** -> Contains the IMDb rating and votes information for titles
- **name.basics.tsv.gz** -> Contains detail information for people

## 🔹 MovieLens

MovieLens Datasets are zipped, **comma-separated values (csv)** files with a single header row. These files are encoded as UTF-8.

There are 6 datasets available as follows:

- **ratings.csv** -> Contains rating information
- **tags.csv** -> Contains tags information of movies
- **movies.csv** -> Contains movie information (Movie titles are entered manually or imported from https://www.themoviedb.org/)
- **links.csv** -> Contains Identifiers information that can be used to link to other sources e.g. IMDb, TMDB
- **genome-scores.csv** -> Contains "Tag Genome" movie-tag relevance information
- **genome-tags.csv** -> Contains "Tag Genome" tag IDs information

# 🔷 Data Flow

Data Flow is a conversation term of data move from end to end. The jargon that we use is called **Data Pipeline/ETL Pipeline**.

*Data Pipeline* is more a general term which is a set of processes that move data from various sources to a destination. It may or may not involve data transformation.

*ETL Pipeline* is a type of Data Pipeline which is an acronym for "Extract, Transform, and Load".

- *Extract*: Extraction refers to pulling the source data from the data source.
- *Transform*: Transformation refers to the process of changing the structure of the information
- *Load*: Loading refers to the process of depositing the information into a data storage system.

And there are other Data Pipeline Patterns like **ELT** and **EtLT**. You can find more when you google them.

Derailing Enough! Let's go back to Movie Data Platform.

There are two main components in Data Flow:

1. Data Lake
2. Data Mart

Data Engineer (like me 🙂) helps to build the Data Lake and Data Mart infrastructure.

If you want to know more about how Data Engineering works, you can visit the YouTube video [How Data Engineering Works](https://youtu.be/qWru-b6m030) for more information.

## 🔹 Data Lake

Data Lake is a central storage that **holds a large amount of data in structured or unstructured format**. 

In Movie Data Platform, Data Lake contains two important processes:

1. Data Injection
2. Data Cleansing

#### Data Injection

The main task in data injection process is to inject the raw data into the Data Lake.
This task gets the IMDb and MovieLens files and save them into the Data Lake.

#### Data Cleansing

There are different tasks in Data Cleansing process.

Firstly, duplicated record will be removed or deleted.
Secondly, turn dirty or N/A record into null value.
Thirdly, convert the data/time string into timestamp data type.

Sometimes, it may change the null value into default value or validate the datasets. However, none of these are needed in Movie Data Platform.

## 🔹 Data Mart

Data Mart is a oriented dataset for a specific solution. In Movie Data Platform, cleansing data is transformed in Data Mart for Web Application visualization.

By joining different datasets, applying certain conditions and restructuring the datasets, the result is much smaller and can be directly fed to Web Application.

# 🔷 Data Visualization

There are many data visualization approaches like Tableau or MS Power BI. 

Those tools are intended for complicated data analysis. 

In Movie Data Platform, we only scratch the surface here and want to share the data which people can interact with. That's why I build the Web Application for data visualization.

##### If you want to know more about data and web implemntation, please visit "Behind The Scense" section.
