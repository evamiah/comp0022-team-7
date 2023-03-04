#helper functions to obtain additional data on movies
import pandas as pd
import tmdbsimple as tmdb
import rottentomatoes as rt

from requests.exceptions import HTTPError

tmdb.API_KEY = '1e97e6266061128613ab12764f041937';

'''
Sets default values for missing data.
'''
NO_TITLE = ''
NO_YEAR = 0
NO_OVERVIEW = ''
NO_POSTER = ''
NO_CAST = ''
NO_DIRECTOR = ''

def info_not_found(movie_id):
    return [movie_id, NO_OVERVIEW, NO_POSTER]

def credits_not_found(movie_id):
    return [movie_id, NO_CAST, NO_DIRECTOR]


'''
get_title(info) -> String
Uses TMDb API wrapper library to obtain movie's title
    - info: tmdb.Movie().info() in dict format
    - returns movie title string
'''
def get_title(info):
    title = info["title"]
    return title


'''
get_release_year(info) -> Int
Uses TMDb API wrapper library to obtain movie's release year
    - info: tmdb.Movie().info() in dict format
    - returns movie release year
'''
def get_release_year(info):
    year = info["release_date"][:4]
    return int(year)

'''
get_overview(info) -> String
Uses TMDb API wrapper library to obtain movie's overview
    - info: tmdb.Movie().info() in dict format
    - returns movie overview
'''
def get_overview(info):
    overview = info["overview"]
    return overview

'''
get_poster_path(info) -> String
Uses TMDb API wrapper library to obtain movie's poster path
    - info: tmdb.Movie().info() in dict format
    - returns movie poster path
    - poster image can be accessed at https://image.tmdb.org/t/p/w185/{{poster_path}} 
'''
def get_poster_path(info):
    poster = info["poster_path"]
    return poster


'''
get_cast(movie_id) -> List[String] 
Uses TMDb API wrapper library to obtain movie's lead actors
    - credits: tmdb.Movie().credits() in dict format
    - returns array of 5 lead actors, or all actors if there are less than 5 listed
'''
def get_cast(credits):
    cast = credits["cast"]
    members = 5
    if len(cast) < 5:
        members = len(cast)
    response = []
    for i in range(members):
        response.append(cast[i]["name"])
    return response;


'''
get_director(movie_id) -> List[String] 
Uses TMDb API wrapper library to obtain movie's director(s)
    - credits: tmdb.Movie().credits() in dict format
    - returns array of crew members under the Director job role
    - if there is not a crew member under the Director role, returns an empty array
'''
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
    df2 = pd.read_csv(file2)
    combo = pd.merge(df1, df2, on=value, how="left")
    combo.to_csv(out, index=False)

