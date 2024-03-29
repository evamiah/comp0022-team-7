#helper functions to obtain additional data on movies
import pandas as pd
import tmdbsimple as tmdb
import rottentomatoes as rt
import requests
import config


from requests.exceptions import HTTPError

tmdb.API_KEY = config.tmdb_key;

'''
Sets default values for missing data.
'''
NO_DATA = ''
NO_YEAR = 0


def info_not_found(movie_id):
    return [movie_id, NO_DATA, NO_DATA]

def credits_not_found(movie_id):
    return [movie_id, NO_DATA, NO_DATA]

def rt_not_found(movie_id):
    return [movie_id, NO_DATA]



def get_title(info):
    title = info["title"]
    return title

'''
MOVIE INFO
'''

def get_release_year(info):
    year = info["release_date"][:4]
    return int(year)

def get_overview(info):
    overview = info["overview"]
    return overview

def get_poster_path(info):
    poster = info["poster_path"]
    return poster

'''
get_rt_ratings(movie_id, tmdb_id, title, year) -> String
Uses rottentomatoes-python library to obtain movie's rotten tomatoes scores
    - movie_id, tmdb_id, title, year from MovieLens movies and links files
    - returns tomatometer and audience scores or NO_DATA
'''
def get_rt_ratings(movie_id, tmdb_id, title, year):
    result = rt.search.search_results(title)
    filtered = rt.search.filter_searches(result)
    if not filtered and tmdb_id:
        #if not found because of badly formatted title, get tmdb title
        new_title = get_basic_info(tmdb_id, movie_id)[1]
        result = rt.search.search_results(new_title)
        filtered = rt.search.filter_searches(result)
    for link in filtered:
        if link.has_tomatometer and link.is_movie:
            try:
                response =  requests.get(link.url)
            except HTTPError:
                return NO_DATA
            
            t_title = rt.movie_title(title, response.text)
            y = rt.year_released(t_title, response.text)
            t_score = rt.tomatometer(t_title, response.text)["value"]
            a_score = rt.audience_score(t_title, response.text)["value"]
            if y == str(year):
                return [t_score, a_score]
    return NO_DATA



'''
MOVIE CREDITS
'''

# returns array of 5 lead actors, or all actors if there are less than 5 listed
def get_cast(credits):
    cast = credits["cast"]
    members = 5
    if len(cast) < 5:
        members = len(cast)
    response = []
    for i in range(members):
        response.append(cast[i]["name"])
    return response;


# returns array of crew members under the Director job role
def get_director(credits):
    crew = credits["crew"]
    response = []
    for i in crew:
        if i["job"] == "Director":
            response.append(i["name"])
    return response



'''
get_movie_info(tmdb_id, movie_id) -> List[String]
movie_id: movieID from MovieLens datasets 
tmdb_id: TMDb ID found in MovieLens' links.csv file
    - Uses TMDb API wrapper library to obtain the movie info dict
    - if movie is not found from TMDb request, returns info_not_found()
    - returns array with movie_id, overview and poster path
'''
def get_movie_info(tmdb_id, movie_id):
    try:
        movie_info = tmdb.Movies(tmdb_id).info()
    except HTTPError:
        return info_not_found(movie_id)
    overview = get_overview(movie_info)
    poster = get_poster_path(movie_info)
    return [movie_id, overview, poster]

'''
get_basic_info(tmdb_id, movie_id) -> List[String]
movie_id: movieID from MovieLens datasets 
tmdb_id: TMDb ID found in MovieLens' links.csv file
    - Uses TMDb API wrapper library to obtain movie missing title or year
    - if movie is not found from TMDb request, returns info_not_found()
    - returns array with movie_id, title and release
'''
def get_basic_info(tmdb_id, movie_id):
    try:
        movie_info = tmdb.Movies(tmdb_id).info()
    except HTTPError:
        return info_not_found(movie_id)
    title = get_title(movie_info)
    year = get_release_year(movie_info)
    return [movie_id, title, year]

'''
get_movie_credits(tmdb_id, movie_id) -> List[String]
movie_id: movieID from MovieLens datasets 
tmdb_id: TMDb ID found in MovieLens' links.csv file
    - Uses TMDb API wrapper library to obtain the movie credits (cast and crew) dict
    - if movie is not found from TMDb request, returns credits_not_found()
    - returns array with movie_id, overview and poster path
'''
def get_movie_credits(tmdb_id, movie_id):
    try:
        movie_credits = tmdb.Movies(tmdb_id).credits()
    except HTTPError:
        return credits_not_found(movie_id)
    cast = get_cast(movie_credits)
    director = get_director(movie_credits)
    return [movie_id, cast, director]

'''
csv_joiner(file1, file2, value, out)
helper function for csv scripts.
joins fields of two csv files, file1 and file2, on given field 'value'.
left join on file 1.
'''
def csv_joiner(file1, file2, value, out):
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2, dtype={'tmdbId':'str'})
    combo = pd.merge(df1, df2, on=value, how="left")
    combo.to_csv(out, index=False)

