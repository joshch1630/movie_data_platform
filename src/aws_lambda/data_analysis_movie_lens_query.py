MOVIE_LENS_DATA_TYPE = "movie_lens_type"
MOVIE_LENS_QUERY_DICT_LIST = []

###########################
########### Year ##########
###########################

# by year
GET_BY_YEAR_MOVIE_LENS_QUERY = """
SELECT year AS year, COUNT(1) AS movie_count, ROUND(AVG(avg_rating), 2) AS avg_rating, SUM(vote_count) AS vote_count
FROM "movie_database_platform"."movie_lens_movies_ratings" 
GROUP BY year
ORDER BY year;
"""
BY_YEAR_MOVIE_LENS_DICT = {
    "data_title": "movie_lens_by_year",
    "data_type": MOVIE_LENS_DATA_TYPE,
    "query": GET_BY_YEAR_MOVIE_LENS_QUERY,
    "query_execution_id": "",
    "is_completed": False,
    "result_data": {}
}
MOVIE_LENS_QUERY_DICT_LIST.append(BY_YEAR_MOVIE_LENS_DICT)

# is adult by year 
GET_IS_ADULT_BY_YEAR_MOVIE_LENS_QUERY = """
SELECT year AS year, COUNT(1) AS movie_count, ROUND(AVG(avg_rating), 2) AS avg_rating, SUM(vote_count) AS vote_count
FROM "movie_database_platform"."movie_lens_movies_ratings" 
WHERE genres_1 = 'Adult' OR genres_2 = 'Adult' OR genres_3 = 'Adult' OR genres_4 = 'Adult' OR genres_5 = 'Adult' OR genres_6 = 'Adult'
GROUP BY year
ORDER BY year;
"""
IS_ADULT_BY_YEAR_MOVIE_LENS_DICT = {
    "data_title": "movie_lens_is_adult_by_year",
    "data_type": MOVIE_LENS_DATA_TYPE,
    "query": GET_IS_ADULT_BY_YEAR_MOVIE_LENS_QUERY,
    "query_execution_id": "",
    "is_completed": False,
    "result_data": {}
}
MOVIE_LENS_QUERY_DICT_LIST.append(IS_ADULT_BY_YEAR_MOVIE_LENS_DICT)

# rating by year
for i in range(0, 10):
    GET_RATING_BY_YEAR_MOVIE_LENS_QUERY = """
    SELECT year AS year, COUNT(1) AS movie_count, ROUND(AVG(avg_rating), 2) AS avg_rating, SUM(vote_count) AS vote_count
    FROM "movie_database_platform"."movie_lens_movies_ratings" 
    WHERE avg_rating >= {} AND avg_rating < {}
    GROUP BY year
    ORDER BY year;
    """
    RATING_BY_YEAR_MOVIE_LENS_DICT = {
        "data_title": "movie_lens_rating_{}_to_{}_by_year".format(i, i+0.5),
        "data_type": MOVIE_LENS_DATA_TYPE,
        "query": GET_RATING_BY_YEAR_MOVIE_LENS_QUERY.format(i, i+0.5),
        "query_execution_id": "",
        "is_completed": False,
        "result_data": {}
    }
    MOVIE_LENS_QUERY_DICT_LIST.append(RATING_BY_YEAR_MOVIE_LENS_DICT)

# genres by year
GENRES_LIST = ["Action", "Adventure", "Animation", "Biography", "Comedy", "Crime", "Documentary", "Drama", "Family", "Fantasy",
               "Film-Noir", "History", "Horror", "Music", "Musical", "Mystery", "Romance", "Sci-Fi", "Sport", "Thriller", "War", "Western"]
for genres in GENRES_LIST:
    GET_GENRES_BY_YEAR_MOVIE_LENS_QUERY = """
    SELECT year AS year, COUNT(1) AS movie_count, ROUND(AVG(avg_rating), 2) AS avg_rating, SUM(vote_count) AS vote_count
    FROM "movie_database_platform"."movie_lens_movies_ratings" 
    WHERE genres_1 = '{}' OR genres_2 = '{}' OR genres_3 = '{}' OR genres_4 = '{}' OR genres_5 = '{}' OR genres_6 = '{}'
    GROUP BY year
    ORDER BY year;
    """
    GENRES_BY_YEAR_MOVIE_LENS_DICT = {
        "data_title": "movie_lens_genres_{}_by_year".format(genres),
        "data_type": MOVIE_LENS_DATA_TYPE,
        "query": GET_GENRES_BY_YEAR_MOVIE_LENS_QUERY.format(genres, genres, genres, genres, genres, genres),
        "query_execution_id": "",
        "is_completed": False,
        "result_data": {}
    }
    MOVIE_LENS_QUERY_DICT_LIST.append(GENRES_BY_YEAR_MOVIE_LENS_DICT)

###########################
########## Rating #########
###########################

# by rating
GET_BY_RATING_MOVIE_LENS_QUERY = """
SELECT 
  CASE 
    WHEN avg_rating >= 4.5 AND avg_rating <= 5 THEN '4.5-5'
    WHEN avg_rating >= 4 AND avg_rating < 4.5 THEN '4-4.5'
    WHEN avg_rating >= 3.5 AND avg_rating < 4 THEN '3.5-4'
    WHEN avg_rating >= 3 AND avg_rating < 3.5 THEN '3-3.5'
    WHEN avg_rating >= 2.5 AND avg_rating < 3 THEN '2.5-3'
    WHEN avg_rating >= 2 AND avg_rating < 2.5 THEN '2-2.5'
    WHEN avg_rating >= 1.5 AND avg_rating < 2 THEN '1.5-2'
    WHEN avg_rating >= 1 AND avg_rating < 1.5 THEN '1-1.5'
    WHEN avg_rating >= 0.5 AND avg_rating < 1 THEN '0.5-1'
    WHEN avg_rating >= 0 AND avg_rating < 0.5 THEN '0-0.5'
    ELSE 'NA'
  END AS rating,
  COUNT(1) AS movie_count,
  SUM(vote_count) AS vote_count
FROM "movie_database_platform"."movie_lens_movies_ratings"
GROUP BY 1
ORDER BY 1;
"""
BY_RATING_MOVIE_LENS_DICT = {
    "data_title": "movie_lens_by_rating",
    "data_type": MOVIE_LENS_DATA_TYPE,
    "query": GET_BY_RATING_MOVIE_LENS_QUERY,
    "query_execution_id": "",
    "is_completed": False,
    "result_data": {}
}
MOVIE_LENS_QUERY_DICT_LIST.append(BY_RATING_MOVIE_LENS_DICT)

# is adult by rating
GET_IS_ADULT_BY_RATING_MOVIE_LENS_QUERY = """
SELECT 
  CASE 
    WHEN avg_rating >= 4.5 AND avg_rating <= 5 THEN '4.5-5'
    WHEN avg_rating >= 4 AND avg_rating < 4.5 THEN '4-4.5'
    WHEN avg_rating >= 3.5 AND avg_rating < 4 THEN '3.5-4'
    WHEN avg_rating >= 3 AND avg_rating < 3.5 THEN '3-3.5'
    WHEN avg_rating >= 2.5 AND avg_rating < 3 THEN '2.5-3'
    WHEN avg_rating >= 2 AND avg_rating < 2.5 THEN '2-2.5'
    WHEN avg_rating >= 1.5 AND avg_rating < 2 THEN '1.5-2'
    WHEN avg_rating >= 1 AND avg_rating < 1.5 THEN '1-1.5'
    WHEN avg_rating >= 0.5 AND avg_rating < 1 THEN '0.5-1'
    WHEN avg_rating >= 0 AND avg_rating < 0.5 THEN '0-0.5'
    ELSE 'NA'
  END AS rating,
  COUNT(1) AS movie_count,
  SUM(vote_count) AS vote_count
FROM "movie_database_platform"."movie_lens_movies_ratings"
WHERE genres_1 = 'Adult' OR genres_2 = 'Adult' OR genres_3 = 'Adult' OR genres_4 = 'Adult' OR genres_5 = 'Adult' OR genres_6 = 'Adult'
GROUP BY 1
ORDER BY 1;
"""
IS_ADULT_BY_RATING_MOVIE_LENS_DICT = {
    "data_title": "movie_lens_is_adult_by_rating",
    "data_type": MOVIE_LENS_DATA_TYPE,
    "query": GET_IS_ADULT_BY_RATING_MOVIE_LENS_QUERY,
    "query_execution_id": "",
    "is_completed": False,
    "result_data": {}
}
MOVIE_LENS_QUERY_DICT_LIST.append(IS_ADULT_BY_RATING_MOVIE_LENS_DICT)

# genres by rating
GENRES_LIST = ["Action", "Adventure", "Animation", "Biography", "Comedy", "Crime", "Documentary", "Drama", "Family", "Fantasy",
               "Film-Noir", "History", "Horror", "Music", "Musical", "Mystery", "Romance", "Sci-Fi", "Sport", "Thriller", "War", "Western"]
for genres in GENRES_LIST:
    GET_GENRES_BY_RATING_MOVIE_LENS_QUERY = """
    SELECT 
      CASE 
        WHEN avg_rating >= 4.5 AND avg_rating <= 5 THEN '4.5-5'
        WHEN avg_rating >= 4 AND avg_rating < 4.5 THEN '4-4.5'
        WHEN avg_rating >= 3.5 AND avg_rating < 4 THEN '3.5-4'
        WHEN avg_rating >= 3 AND avg_rating < 3.5 THEN '3-3.5'
        WHEN avg_rating >= 2.5 AND avg_rating < 3 THEN '2.5-3'
        WHEN avg_rating >= 2 AND avg_rating < 2.5 THEN '2-2.5'
        WHEN avg_rating >= 1.5 AND avg_rating < 2 THEN '1.5-2'
        WHEN avg_rating >= 1 AND avg_rating < 1.5 THEN '1-1.5'
        WHEN avg_rating >= 0.5 AND avg_rating < 1 THEN '0.5-1'
        WHEN avg_rating >= 0 AND avg_rating < 0.5 THEN '0-0.5'
        ELSE 'NA'
      END AS rating,
      COUNT(1) AS movie_count,
      SUM(vote_count) AS vote_count
    FROM "movie_database_platform"."movie_lens_movies_ratings"
    WHERE genres_1 = '{}' OR genres_2 = '{}' OR genres_3 = '{}' OR genres_4 = '{}' OR genres_5 = '{}' OR genres_6 = '{}' 
    GROUP BY 1
    ORDER BY 1;
    """
    GENRES_BY_RATING_MOVIE_LENS_DICT = {
        "data_title": "movie_lens_genres_{}_by_rating".format(genres),
        "data_type": MOVIE_LENS_DATA_TYPE,
        "query": GET_GENRES_BY_RATING_MOVIE_LENS_QUERY.format(genres, genres, genres, genres, genres, genres),
        "query_execution_id": "",
        "is_completed": False,
        "result_data": {}
    }
    MOVIE_LENS_QUERY_DICT_LIST.append(GENRES_BY_RATING_MOVIE_LENS_DICT)

###########################
########## Genres #########
###########################

# by genres
GET_BY_GENRES_MOVIE_LENS_QUERY = """
SELECT 
  CASE 
    WHEN genres_1 = 'Action' OR genres_2 = 'Action' OR genres_3 = 'Action' OR genres_4 = 'Action' OR genres_5 = 'Action' OR genres_6 = 'Action' THEN 'Action'
    WHEN genres_1 = 'Adventure' OR genres_2 = 'Adventure' OR genres_3 = 'Adventure' OR genres_4 = 'Adventure' OR genres_5 = 'Adventure' OR genres_6 = 'Adventure' THEN 'Adventure'
    WHEN genres_1 = 'Animation' OR genres_2 = 'Animation' OR genres_3 = 'Animation' OR genres_4 = 'Animation' OR genres_5 = 'Animation' OR genres_6 = 'Animation' THEN 'Animation'
    WHEN genres_1 = 'Biography' OR genres_2 = 'Biography' OR genres_3 = 'Biography' OR genres_4 = 'Biography' OR genres_5 = 'Biography' OR genres_6 = 'Biography' THEN 'Biography'
    WHEN genres_1 = 'Comedy' OR genres_2 = 'Comedy' OR genres_3 = 'Comedy' OR genres_4 = 'Comedy' OR genres_5 = 'Comedy' OR genres_6 = 'Comedy' THEN 'Comedy'
    WHEN genres_1 = 'Crime' OR genres_2 = 'Crime' OR genres_3 = 'Crime' OR genres_4 = 'Crime' OR genres_5 = 'Crime' OR genres_6 = 'Crime' THEN 'Crime'
    WHEN genres_1 = 'Documentary' OR genres_2 = 'Documentary' OR genres_3 = 'Documentary' OR genres_4 = 'Documentary' OR genres_5 = 'Documentary' OR genres_6 = 'Documentary' THEN 'Documentary'
    WHEN genres_1 = 'Drama' OR genres_2 = 'Drama' OR genres_3 = 'Drama' OR genres_4 = 'Drama' OR genres_5 = 'Drama' OR genres_6 = 'Drama' THEN 'Drama'
    WHEN genres_1 = 'Family' OR genres_2 = 'Family' OR genres_3 = 'Family' OR genres_4 = 'Family' OR genres_5 = 'Family' OR genres_6 = 'Family' THEN 'Family'
    WHEN genres_1 = 'Fantasy' OR genres_2 = 'Fantasy' OR genres_3 = 'Fantasy' OR genres_4 = 'Fantasy' OR genres_5 = 'Fantasy' OR genres_6 = 'Fantasy' THEN 'Fantasy'
    WHEN genres_1 = 'Film-Noir' OR genres_2 = 'Film-Noir' OR genres_3 = 'Film-Noir' OR genres_4 = 'Film-Noir' OR genres_5 = 'Film-Noir' OR genres_6 = 'Film-Noir' THEN 'Film-Noir'
    WHEN genres_1 = 'History' OR genres_2 = 'History' OR genres_3 = 'History' OR genres_4 = 'History' OR genres_5 = 'History' OR genres_6 = 'History' THEN 'History'
    WHEN genres_1 = 'Horror' OR genres_2 = 'Horror' OR genres_3 = 'Horror' OR genres_4 = 'Horror' OR genres_5 = 'Horror' OR genres_6 = 'Horror' THEN 'Horror'
    WHEN genres_1 = 'Music' OR genres_2 = 'Music' OR genres_3 = 'Music' OR genres_4 = 'Music' OR genres_5 = 'Music' OR genres_6 = 'Music' THEN 'Music'
    WHEN genres_1 = 'Musical' OR genres_2 = 'Musical' OR genres_3 = 'Musical' OR genres_4 = 'Musical' OR genres_5 = 'Musical' OR genres_6 = 'Musical' THEN 'Musical'
    WHEN genres_1 = 'Mystery' OR genres_2 = 'Mystery' OR genres_3 = 'Mystery' OR genres_4 = 'Mystery' OR genres_5 = 'Mystery' OR genres_6 = 'Mystery' THEN 'Mystery'
    WHEN genres_1 = 'Romance' OR genres_2 = 'Romance' OR genres_3 = 'Romance' OR genres_4 = 'Romance' OR genres_5 = 'Romance' OR genres_6 = 'Romance' THEN 'Romance'
    WHEN genres_1 = 'Sci-Fi' OR genres_2 = 'Sci-Fi' OR genres_3 = 'Sci-Fi' OR genres_4 = 'Sci-Fi' OR genres_5 = 'Sci-Fi' OR genres_6 = 'Sci-Fi' THEN 'Sci-Fi'
    WHEN genres_1 = 'Sport' OR genres_2 = 'Sport' OR genres_3 = 'Sport' OR genres_4 = 'Sport' OR genres_5 = 'Sport' OR genres_6 = 'Sport' THEN 'Sport'
    WHEN genres_1 = 'Thriller' OR genres_2 = 'Thriller' OR genres_3 = 'Thriller' OR genres_4 = 'Thriller' OR genres_5 = 'Thriller' OR genres_6 = 'Thriller' THEN 'Thriller'
    WHEN genres_1 = 'War' OR genres_2 = 'War' OR genres_3 = 'War' OR genres_4 = 'War' OR genres_5 = 'War' OR genres_6 = 'War' THEN 'War'
    WHEN genres_1 = 'Western' OR genres_2 = 'Western' OR genres_3 = 'Western' OR genres_4 = 'Western' OR genres_5 = 'Western' OR genres_6 = 'Western' THEN 'Western'
    ELSE 'NA'
  END AS genre,
  COUNT(1) AS movie_count,
  ROUND(AVG(avg_rating), 2) AS avg_rating,
  SUM(vote_count) AS vote_count
FROM "movie_database_platform"."movie_lens_movies_ratings"
GROUP BY 1
ORDER BY 1;
"""
BY_GENRES_MOVIE_LENS_DICT = {
    "data_title": "movie_lens_by_genres",
    "data_type": MOVIE_LENS_DATA_TYPE,
    "query": GET_BY_GENRES_MOVIE_LENS_QUERY,
    "query_execution_id": "",
    "is_completed": False,
    "result_data": {}
}
MOVIE_LENS_QUERY_DICT_LIST.append(BY_GENRES_MOVIE_LENS_DICT)

# is adult by genres
GET_IS_ADULT_BY_GENRES_MOVIE_LENS_QUERY = """
SELECT 
  CASE 
    WHEN genres_1 = 'Action' OR genres_2 = 'Action' OR genres_3 = 'Action' OR genres_4 = 'Action' OR genres_5 = 'Action' OR genres_6 = 'Action' THEN 'Action'
    WHEN genres_1 = 'Adventure' OR genres_2 = 'Adventure' OR genres_3 = 'Adventure' OR genres_4 = 'Adventure' OR genres_5 = 'Adventure' OR genres_6 = 'Adventure' THEN 'Adventure'
    WHEN genres_1 = 'Animation' OR genres_2 = 'Animation' OR genres_3 = 'Animation' OR genres_4 = 'Animation' OR genres_5 = 'Animation' OR genres_6 = 'Animation' THEN 'Animation'
    WHEN genres_1 = 'Biography' OR genres_2 = 'Biography' OR genres_3 = 'Biography' OR genres_4 = 'Biography' OR genres_5 = 'Biography' OR genres_6 = 'Biography' THEN 'Biography'
    WHEN genres_1 = 'Comedy' OR genres_2 = 'Comedy' OR genres_3 = 'Comedy' OR genres_4 = 'Comedy' OR genres_5 = 'Comedy' OR genres_6 = 'Comedy' THEN 'Comedy'
    WHEN genres_1 = 'Crime' OR genres_2 = 'Crime' OR genres_3 = 'Crime' OR genres_4 = 'Crime' OR genres_5 = 'Crime' OR genres_6 = 'Crime' THEN 'Crime'
    WHEN genres_1 = 'Documentary' OR genres_2 = 'Documentary' OR genres_3 = 'Documentary' OR genres_4 = 'Documentary' OR genres_5 = 'Documentary' OR genres_6 = 'Documentary' THEN 'Documentary'
    WHEN genres_1 = 'Drama' OR genres_2 = 'Drama' OR genres_3 = 'Drama' OR genres_4 = 'Drama' OR genres_5 = 'Drama' OR genres_6 = 'Drama' THEN 'Drama'
    WHEN genres_1 = 'Family' OR genres_2 = 'Family' OR genres_3 = 'Family' OR genres_4 = 'Family' OR genres_5 = 'Family' OR genres_6 = 'Family' THEN 'Family'
    WHEN genres_1 = 'Fantasy' OR genres_2 = 'Fantasy' OR genres_3 = 'Fantasy' OR genres_4 = 'Fantasy' OR genres_5 = 'Fantasy' OR genres_6 = 'Fantasy' THEN 'Fantasy'
    WHEN genres_1 = 'Film-Noir' OR genres_2 = 'Film-Noir' OR genres_3 = 'Film-Noir' OR genres_4 = 'Film-Noir' OR genres_5 = 'Film-Noir' OR genres_6 = 'Film-Noir' THEN 'Film-Noir'
    WHEN genres_1 = 'History' OR genres_2 = 'History' OR genres_3 = 'History' OR genres_4 = 'History' OR genres_5 = 'History' OR genres_6 = 'History' THEN 'History'
    WHEN genres_1 = 'Horror' OR genres_2 = 'Horror' OR genres_3 = 'Horror' OR genres_4 = 'Horror' OR genres_5 = 'Horror' OR genres_6 = 'Horror' THEN 'Horror'
    WHEN genres_1 = 'Music' OR genres_2 = 'Music' OR genres_3 = 'Music' OR genres_4 = 'Music' OR genres_5 = 'Music' OR genres_6 = 'Music' THEN 'Music'
    WHEN genres_1 = 'Musical' OR genres_2 = 'Musical' OR genres_3 = 'Musical' OR genres_4 = 'Musical' OR genres_5 = 'Musical' OR genres_6 = 'Musical' THEN 'Musical'
    WHEN genres_1 = 'Mystery' OR genres_2 = 'Mystery' OR genres_3 = 'Mystery' OR genres_4 = 'Mystery' OR genres_5 = 'Mystery' OR genres_6 = 'Mystery' THEN 'Mystery'
    WHEN genres_1 = 'Romance' OR genres_2 = 'Romance' OR genres_3 = 'Romance' OR genres_4 = 'Romance' OR genres_5 = 'Romance' OR genres_6 = 'Romance' THEN 'Romance'
    WHEN genres_1 = 'Sci-Fi' OR genres_2 = 'Sci-Fi' OR genres_3 = 'Sci-Fi' OR genres_4 = 'Sci-Fi' OR genres_5 = 'Sci-Fi' OR genres_6 = 'Sci-Fi' THEN 'Sci-Fi'
    WHEN genres_1 = 'Sport' OR genres_2 = 'Sport' OR genres_3 = 'Sport' OR genres_4 = 'Sport' OR genres_5 = 'Sport' OR genres_6 = 'Sport' THEN 'Sport'
    WHEN genres_1 = 'Thriller' OR genres_2 = 'Thriller' OR genres_3 = 'Thriller' OR genres_4 = 'Thriller' OR genres_5 = 'Thriller' OR genres_6 = 'Thriller' THEN 'Thriller'
    WHEN genres_1 = 'War' OR genres_2 = 'War' OR genres_3 = 'War' OR genres_4 = 'War' OR genres_5 = 'War' OR genres_6 = 'War' THEN 'War'
    WHEN genres_1 = 'Western' OR genres_2 = 'Western' OR genres_3 = 'Western' OR genres_4 = 'Western' OR genres_5 = 'Western' OR genres_6 = 'Western' THEN 'Western'
    ELSE 'NA'
  END AS genre,
  COUNT(1) AS movie_count,
  ROUND(AVG(avg_rating), 2) AS avg_rating,
  SUM(vote_count) AS vote_count
FROM "movie_database_platform"."movie_lens_movies_ratings"
WHERE genres_1 = 'Adult' OR genres_2 = 'Adult' OR genres_3 = 'Adult' OR genres_4 = 'Adult' OR genres_5 = 'Adult' OR genres_6 = 'Adult'
GROUP BY 1
ORDER BY 1;
"""
IS_ADULT_BY_GENRES_MOVIE_LENS_DICT = {
    "data_title": "movie_lens_is_adult_by_genres",
    "data_type": MOVIE_LENS_DATA_TYPE,
    "query": GET_IS_ADULT_BY_GENRES_MOVIE_LENS_QUERY,
    "query_execution_id": "",
    "is_completed": False,
    "result_data": {}
}
MOVIE_LENS_QUERY_DICT_LIST.append(IS_ADULT_BY_GENRES_MOVIE_LENS_DICT)
