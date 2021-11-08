IMDB_DATA_TYPE = "imdb_type"
IMDB_QUERY_DICT_LIST = []

###########################
########### Year ##########
###########################

# by year
GET_BY_YEAR_IMDB_QUERY = """
SELECT startyear AS year, COUNT(1) AS movie_count, ROUND(AVG(averagerating), 2) AS avg_rating, SUM(numvotes) AS vote_count
FROM "movie_database_platform"."imdb_title_basics_ratings" 
GROUP BY startyear
ORDER BY startyear;
"""
BY_YEAR_IMDB_DICT = {
    "data_title": "imdb_by_year",
    "data_type": IMDB_DATA_TYPE,
    "query": GET_BY_YEAR_IMDB_QUERY,
    "query_execution_id": "",
    "is_completed": False,
    "result_data": {}
}
IMDB_QUERY_DICT_LIST.append(BY_YEAR_IMDB_DICT)


# is adult by year
GET_IS_ADULT_BY_YEAR_IMDB_QUERY = """
SELECT startyear AS year, COUNT(1) AS movie_count, ROUND(AVG(averagerating), 2) AS avg_rating, SUM(numvotes) AS vote_count
FROM "movie_database_platform"."imdb_title_basics_ratings" 
WHERE isadult = true
GROUP BY startyear
ORDER BY startyear;
"""
IS_ADULT_BY_YEAR_IMDB_DICT = {
    "data_title": "imdb_is_adult_by_year",
    "data_type": IMDB_DATA_TYPE,
    "query": GET_IS_ADULT_BY_YEAR_IMDB_QUERY,
    "query_execution_id": "",
    "is_completed": False,
    "result_data": {}
}
IMDB_QUERY_DICT_LIST.append(IS_ADULT_BY_YEAR_IMDB_DICT)

# rating by year
for i in range(0, 10):
    GET_RATING_BY_YEAR_IMDB_QUERY = """
    SELECT startyear AS year, COUNT(1) AS movie_count, ROUND(AVG(averagerating), 2) AS avg_rating, SUM(numvotes) AS vote_count
    FROM "movie_database_platform"."imdb_title_basics_ratings"
    WHERE averagerating >= {} AND averagerating < {}
    GROUP BY startyear
    ORDER BY startyear;
    """
    RATING_BY_YEAR_IMDB_DICT = {
        "data_title": "imdb_rating_{}_to_{}_by_year".format(i, i+1),
        "data_type": IMDB_DATA_TYPE,
        "query": GET_RATING_BY_YEAR_IMDB_QUERY.format(i, i+1),
        "query_execution_id": "",
        "is_completed": False,
        "result_data": {}
    }
    IMDB_QUERY_DICT_LIST.append(RATING_BY_YEAR_IMDB_DICT)

# genres by year
GENRES_LIST = ["Action", "Adventure", "Animation", "Biography", "Comedy", "Crime", "Documentary", "Drama", "Family", "Fantasy",
               "Film-Noir", "History", "Horror", "Music", "Musical", "Mystery", "Romance", "Sci-Fi", "Sport", "Thriller", "War", "Western"]
for genres in GENRES_LIST:
    GET_GENRES_BY_YEAR_IMDB_QUERY = """
    SELECT startyear AS year, COUNT(1) AS movie_count, ROUND(AVG(averagerating), 2) AS avg_rating, SUM(numvotes) AS vote_count
    FROM "movie_database_platform"."imdb_title_basics_ratings"
    WHERE genres_1 = '{}' OR genres_2 = '{}' OR genres_3 = '{}'
    GROUP BY startyear
    ORDER BY startyear;
    """
    GENRES_BY_YEAR_IMDB_DICT = {
        "data_title": "imdb_genres_{}_by_year".format(genres),
        "data_type": IMDB_DATA_TYPE,
        "query": GET_GENRES_BY_YEAR_IMDB_QUERY.format(genres, genres, genres),
        "query_execution_id": "",
        "is_completed": False,
        "result_data": {}
    }
    IMDB_QUERY_DICT_LIST.append(GENRES_BY_YEAR_IMDB_DICT)

###########################
########## Rating #########
###########################

# by rating
GET_BY_RATING_IMDB_QUERY = """
SELECT 
  CASE 
    WHEN averagerating >= 9 AND averagerating <= 10 THEN '9-10'
    WHEN averagerating >= 8 AND averagerating < 9 THEN '8-9'
    WHEN averagerating >= 7 AND averagerating < 8 THEN '7-8'
    WHEN averagerating >= 6 AND averagerating < 7 THEN '6-7'
    WHEN averagerating >= 5 AND averagerating < 6 THEN '5-6'
    WHEN averagerating >= 4 AND averagerating < 5 THEN '4-5'
    WHEN averagerating >= 3 AND averagerating < 4 THEN '3-4'
    WHEN averagerating >= 2 AND averagerating < 3 THEN '2-3'
    WHEN averagerating >= 1 AND averagerating < 2 THEN '1-2'
    WHEN averagerating >= 0 AND averagerating < 1 THEN '0-1'
    ELSE 'NA'
  END AS rating,
  COUNT(1) AS movie_count,
  SUM(numvotes) AS vote_count
FROM "movie_database_platform"."imdb_title_basics_ratings"
GROUP BY 1
ORDER BY 1;
"""
BY_RATING_IMDB_DICT = {
    "data_title": "imdb_by_rating",
    "data_type": IMDB_DATA_TYPE,
    "query": GET_BY_RATING_IMDB_QUERY,
    "query_execution_id": "",
    "is_completed": False,
    "result_data": {}
}
IMDB_QUERY_DICT_LIST.append(BY_RATING_IMDB_DICT)

# is adult by rating
GET_IS_ADULT_BY_RATING_IMDB_QUERY = """
SELECT 
  CASE 
    WHEN averagerating >= 9 AND averagerating <= 10 THEN '9-10'
    WHEN averagerating >= 8 AND averagerating < 9 THEN '8-9'
    WHEN averagerating >= 7 AND averagerating < 8 THEN '7-8'
    WHEN averagerating >= 6 AND averagerating < 7 THEN '6-7'
    WHEN averagerating >= 5 AND averagerating < 6 THEN '5-6'
    WHEN averagerating >= 4 AND averagerating < 5 THEN '4-5'
    WHEN averagerating >= 3 AND averagerating < 4 THEN '3-4'
    WHEN averagerating >= 2 AND averagerating < 3 THEN '2-3'
    WHEN averagerating >= 1 AND averagerating < 2 THEN '1-2'
    WHEN averagerating >= 0 AND averagerating < 1 THEN '0-1'
    ELSE 'NA'
  END AS rating,
  COUNT(1) AS movie_count,
  SUM(numvotes) AS vote_count
FROM "movie_database_platform"."imdb_title_basics_ratings"
WHERE isadult = true
GROUP BY 1
ORDER BY 1;
"""
IS_ADULT_BY_RATING_IMDB_DICT = {
    "data_title": "imdb_is_adult_by_rating",
    "data_type": IMDB_DATA_TYPE,
    "query": GET_IS_ADULT_BY_RATING_IMDB_QUERY,
    "query_execution_id": "",
    "is_completed": False,
    "result_data": {}
}
IMDB_QUERY_DICT_LIST.append(IS_ADULT_BY_RATING_IMDB_DICT)

# genres by rating
GENRES_LIST = ["Action", "Adventure", "Animation", "Biography", "Comedy", "Crime", "Documentary", "Drama", "Family", "Fantasy",
               "Film-Noir", "History", "Horror", "Music", "Musical", "Mystery", "Romance", "Sci-Fi", "Sport", "Thriller", "War", "Western"]
for genres in GENRES_LIST:
    GET_GENRES_BY_RATING_IMDB_QUERY = """
    SELECT 
        CASE 
            WHEN averagerating >= 9 AND averagerating <= 10 THEN '9-10'
            WHEN averagerating >= 8 AND averagerating < 9 THEN '8-9'
            WHEN averagerating >= 7 AND averagerating < 8 THEN '7-8'
            WHEN averagerating >= 6 AND averagerating < 7 THEN '6-7'
            WHEN averagerating >= 5 AND averagerating < 6 THEN '5-6'
            WHEN averagerating >= 4 AND averagerating < 5 THEN '4-5'
            WHEN averagerating >= 3 AND averagerating < 4 THEN '3-4'
            WHEN averagerating >= 2 AND averagerating < 3 THEN '2-3'
            WHEN averagerating >= 1 AND averagerating < 2 THEN '1-2'
            WHEN averagerating >= 0 AND averagerating < 1 THEN '0-1'
            ELSE 'NA'
        END AS rating,
        COUNT(1) AS movie_count,
    SUM(numvotes) AS vote_count
    FROM "movie_database_platform"."imdb_title_basics_ratings"
    WHERE genres_1 = '{}' OR genres_2 = '{}' OR genres_3 = '{}'
    GROUP BY 1
    ORDER BY 1;
    """
    GENRES_BY_RATING_IMDB_DICT = {
        "data_title": "imdb_genres_{}_by_rating".format(genres),
        "data_type": IMDB_DATA_TYPE,
        "query": GET_GENRES_BY_RATING_IMDB_QUERY.format(genres, genres, genres),
        "query_execution_id": "",
        "is_completed": False,
        "result_data": {}
    }
    IMDB_QUERY_DICT_LIST.append(GENRES_BY_RATING_IMDB_DICT)

###########################
########## Genres #########
###########################

# by genres
GET_BY_GENRES_IMDB_QUERY = """
SELECT 
  CASE 
    WHEN genres_1 = 'Action' OR genres_2 = 'Action' OR genres_3 = 'Action' THEN 'Action'
    WHEN genres_1 = 'Adventure' OR genres_2 = 'Adventure' OR genres_3 = 'Adventure' THEN 'Adventure'
    WHEN genres_1 = 'Animation' OR genres_2 = 'Animation' OR genres_3 = 'Animation' THEN 'Animation'
    WHEN genres_1 = 'Biography' OR genres_2 = 'Biography' OR genres_3 = 'Biography' THEN 'Biography'
    WHEN genres_1 = 'Comedy' OR genres_2 = 'Comedy' OR genres_3 = 'Comedy' THEN 'Comedy'
    WHEN genres_1 = 'Crime' OR genres_2 = 'Crime' OR genres_3 = 'Crime' THEN 'Crime'
    WHEN genres_1 = 'Documentary' OR genres_2 = 'Documentary' OR genres_3 = 'Documentary' THEN 'Documentary'
    WHEN genres_1 = 'Drama' OR genres_2 = 'Drama' OR genres_3 = 'Drama' THEN 'Drama'
    WHEN genres_1 = 'Family' OR genres_2 = 'Family' OR genres_3 = 'Family' THEN 'Family'
    WHEN genres_1 = 'Fantasy' OR genres_2 = 'Fantasy' OR genres_3 = 'Fantasy' THEN 'Fantasy'
    WHEN genres_1 = 'Film-Noir' OR genres_2 = 'Film-Noir' OR genres_3 = 'Film-Noir' THEN 'Film-Noir'
    WHEN genres_1 = 'History' OR genres_2 = 'History' OR genres_3 = 'History' THEN 'History'
    WHEN genres_1 = 'Horror' OR genres_2 = 'Horror' OR genres_3 = 'Horror' THEN 'Horror'
    WHEN genres_1 = 'Music' OR genres_2 = 'Music' OR genres_3 = 'Music' THEN 'Music'
    WHEN genres_1 = 'Musical' OR genres_2 = 'Musical' OR genres_3 = 'Musical' THEN 'Musical'
    WHEN genres_1 = 'Mystery' OR genres_2 = 'Mystery' OR genres_3 = 'Mystery' THEN 'Mystery'
    WHEN genres_1 = 'Romance' OR genres_2 = 'Romance' OR genres_3 = 'Romance' THEN 'Romance'
    WHEN genres_1 = 'Sci-Fi' OR genres_2 = 'Sci-Fi' OR genres_3 = 'Sci-Fi' THEN 'Sci-Fi'
    WHEN genres_1 = 'Sport' OR genres_2 = 'Sport' OR genres_3 = 'Sport' THEN 'Sport'
    WHEN genres_1 = 'Thriller' OR genres_2 = 'Thriller' OR genres_3 = 'Thriller' THEN 'Thriller'
    WHEN genres_1 = 'War' OR genres_2 = 'War' OR genres_3 = 'War' THEN 'War'
    WHEN genres_1 = 'Western' OR genres_2 = 'Western' OR genres_3 = 'Western' THEN 'Western'
    ELSE 'NA'
  END AS genre,
  COUNT(1) AS movie_count,
  ROUND(AVG(averagerating), 2) AS avg_rating,
  SUM(numvotes) AS vote_count
FROM "movie_database_platform"."imdb_title_basics_ratings"
GROUP BY 1
ORDER BY 1;
"""
BY_GENRES_IMDB_DICT = {
    "data_title": "imdb_by_genres",
    "data_type": IMDB_DATA_TYPE,
    "query": GET_BY_GENRES_IMDB_QUERY,
    "query_execution_id": "",
    "is_completed": False,
    "result_data": {}
}
IMDB_QUERY_DICT_LIST.append(BY_GENRES_IMDB_DICT)

# is adult by genres
GET_IS_ADULT_BY_GENRES_IMDB_QUERY = """
SELECT 
  CASE 
    WHEN genres_1 = 'Action' OR genres_2 = 'Action' OR genres_3 = 'Action' THEN 'Action'
    WHEN genres_1 = 'Adventure' OR genres_2 = 'Adventure' OR genres_3 = 'Adventure' THEN 'Adventure'
    WHEN genres_1 = 'Animation' OR genres_2 = 'Animation' OR genres_3 = 'Animation' THEN 'Animation'
    WHEN genres_1 = 'Biography' OR genres_2 = 'Biography' OR genres_3 = 'Biography' THEN 'Biography'
    WHEN genres_1 = 'Comedy' OR genres_2 = 'Comedy' OR genres_3 = 'Comedy' THEN 'Comedy'
    WHEN genres_1 = 'Crime' OR genres_2 = 'Crime' OR genres_3 = 'Crime' THEN 'Crime'
    WHEN genres_1 = 'Documentary' OR genres_2 = 'Documentary' OR genres_3 = 'Documentary' THEN 'Documentary'
    WHEN genres_1 = 'Drama' OR genres_2 = 'Drama' OR genres_3 = 'Drama' THEN 'Drama'
    WHEN genres_1 = 'Family' OR genres_2 = 'Family' OR genres_3 = 'Family' THEN 'Family'
    WHEN genres_1 = 'Fantasy' OR genres_2 = 'Fantasy' OR genres_3 = 'Fantasy' THEN 'Fantasy'
    WHEN genres_1 = 'Film-Noir' OR genres_2 = 'Film-Noir' OR genres_3 = 'Film-Noir' THEN 'Film-Noir'
    WHEN genres_1 = 'History' OR genres_2 = 'History' OR genres_3 = 'History' THEN 'History'
    WHEN genres_1 = 'Horror' OR genres_2 = 'Horror' OR genres_3 = 'Horror' THEN 'Horror'
    WHEN genres_1 = 'Music' OR genres_2 = 'Music' OR genres_3 = 'Music' THEN 'Music'
    WHEN genres_1 = 'Musical' OR genres_2 = 'Musical' OR genres_3 = 'Musical' THEN 'Musical'
    WHEN genres_1 = 'Mystery' OR genres_2 = 'Mystery' OR genres_3 = 'Mystery' THEN 'Mystery'
    WHEN genres_1 = 'Romance' OR genres_2 = 'Romance' OR genres_3 = 'Romance' THEN 'Romance'
    WHEN genres_1 = 'Sci-Fi' OR genres_2 = 'Sci-Fi' OR genres_3 = 'Sci-Fi' THEN 'Sci-Fi'
    WHEN genres_1 = 'Sport' OR genres_2 = 'Sport' OR genres_3 = 'Sport' THEN 'Sport'
    WHEN genres_1 = 'Thriller' OR genres_2 = 'Thriller' OR genres_3 = 'Thriller' THEN 'Thriller'
    WHEN genres_1 = 'War' OR genres_2 = 'War' OR genres_3 = 'War' THEN 'War'
    WHEN genres_1 = 'Western' OR genres_2 = 'Western' OR genres_3 = 'Western' THEN 'Western'
    ELSE 'NA'
  END AS genre,
  COUNT(1) AS movie_count,
  ROUND(AVG(averagerating), 2) AS avg_rating,
  SUM(numvotes) AS vote_count
FROM "movie_database_platform"."imdb_title_basics_ratings"
WHERE isadult = true
GROUP BY 1
ORDER BY 1;
"""
IS_ADULT_BY_GENRES_IMDB_DICT = {
    "data_title": "imdb_is_adult_by_genres",
    "data_type": IMDB_DATA_TYPE,
    "query": GET_IS_ADULT_BY_GENRES_IMDB_QUERY,
    "query_execution_id": "",
    "is_completed": False,
    "result_data": {}
}
IMDB_QUERY_DICT_LIST.append(IS_ADULT_BY_GENRES_IMDB_DICT)