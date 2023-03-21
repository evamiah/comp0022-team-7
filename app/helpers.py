import req5
from movie_details import aggregate_rating, list_genres, get_popularity, use_tmdb_year
import rating
from typing import List, Dict
import mysql.connector
# for debugging
import logging
logging.basicConfig(level=logging.DEBUG)

config = {
        'user': 'team7',
        'password': 'G3LqY5UUTo0fK6x7nc7Q',
        'host': 'db',
        'port': '3306',
        'database': 'movie_db'
    }

# default values to display for unavailable data
NO_POSTER_FILE = "/static/poster_unavailable.jpg"
NO_OVERVIEW_TEXT = "This movie's overview is currently unavailable."
NO_CAST_TEXT = "Cast information unavailale."
NO_DIRECTOR_TEXT = "Directing information unavailable."
INVALID_ID = "Movie does not exist in the database."
NO_RATING_TEXT = "N/A"
NO_PREDICTED = "-"

# helper function that gets the genre from a genre_id
def get_genre(genre_id) -> List[Dict]:
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    query = 'SELECT genre \
            FROM genres \
            WHERE genre_id = %s'
    cursor.execute(query, (genre_id,))
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

# helper class to obtain values to show on front-end in dict format
# initialised with movie info array [id, title, release_year, overview, poster_path]
class MovieViewer:
    def __init__(self, info, rotten_tomatoes=[], cast=[], director=[], invalid_movie=False):
        self.info = info
        self.rt = rotten_tomatoes
        self.cast = cast
        self.director = director
        self.invalid = invalid_movie

    def get_movie_id(self):
        return self.info[0]

    def get_title(self):
        return self.info[1]
    
    def get_year(self):
        if self.info[2] == 0:
            update = use_tmdb_year(self.get_movie_id())
            return update
        return self.info[2]
    
    def get_overview(self):
        if self.info[3] == '':
            return NO_OVERVIEW_TEXT
        else:
            return self.info[3]
    
    def get_poster(self):
        if self.info[4] == '':
            return NO_POSTER_FILE
        else:
            return "https://image.tmdb.org/t/p/w185/{}".format(self.info[4])

    def get_tomatometer(self):
        if not self.rt or (self.rt[0] == -1):
            return NO_RATING_TEXT
        else:
            return self.rt[0]

    def get_audience_score(self):
        if not self.rt or (self.rt[1] == -1):
            return NO_RATING_TEXT
        else:
            return self.rt[1]
    
    def get_cast(self):
        if not self.cast:
            return NO_CAST_TEXT
        else:
            return self.cast
    
    def get_director(self):
        if not self.cast:
            return NO_DIRECTOR_TEXT
        else:
            return self.director
    
    def get_predicted_rating(self):
        pred = req5.getQry(self.get_movie_id())
        if not pred:
            return NO_PREDICTED
        return pred[0][0]
    
    def get_agg_rating(self):
        return aggregate_rating(self.get_movie_id())[0]
    
    def get_genre_list(self):
        return list_genres(self.get_movie_id())[0]
    
    def get_popularity(self):
        return get_popularity(self.get_movie_id())[0]
    
    def get_viewing_data(self):
        data = {}
        data['invalid'] = self.invalid
        if not self.invalid:
            data['id'] = self.get_movie_id()
            data['title'] = self.get_title()
            data['year'] = self.get_year()
            data['overview'] = self.get_overview()
            data['poster'] = self.get_poster()
            data['tomatometer'] = self.get_tomatometer()
            data['audience_score'] = self.get_audience_score()
            data['cast'] = self.get_cast()
            data['director'] = self.get_director()
            data['predicted_rating'] = self.get_predicted_rating()
            data['user_rating'] = self.get_agg_rating()
            data['genre'] = self.get_genre_list()
            data['popularity'] = self.get_popularity()
        else:
            data['info'] = INVALID_ID
        return data

# helper class to obtain rating stats to show on front-end in dict format
# initialised with movie id and list of genres (id, name) tuples
class StatsViewer:
    def __init__(self, movie_id, genres):
        self.movie_id = movie_id
        self.genres = genres

    def get_user_rating_stats(self):
        users = {}
        users['low'] = round(rating.analyse_ratings('low',  self.movie_id)[0], 2)
        users['high'] = round(rating.analyse_ratings('high',  self.movie_id)[0], 2)
        return users
    
    def get_genre_ratings_stats(self, genre_id):
        genre_stats = {}
        genre_stats['low'] = round(rating.analyse_ratings_genre('low', self.movie_id, genre_id)[0], 2)
        genre_stats['high'] = round(rating.analyse_ratings_genre('high', self.movie_id, genre_id)[0], 2)
        return genre_stats
    
    def get_all_genre_stats(self):
        all_genres = {}
        for genre in self.genres:
            all_genres[genre[1]] = self.get_genre_ratings_stats(genre[0])
        return all_genres


    def get_movie_stats(self):
        stats = {}
        stats['users'] = self.get_user_rating_stats()
        stats['genres'] = self.get_all_genre_stats()
        return stats
