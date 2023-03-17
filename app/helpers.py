import req5

NO_POSTER_FILE = "/static/poster_unavailable.jpg"
NO_OVERVIEW_TEXT = "This movie's overview is currently unavailable."
NO_CAST_TEXT = "Cast information unavailale."
NO_DIRECTOR_TEXT = "Directing information unavailable."
INVALID_ID = "Movie does not exist in the database."

class MovieViewer:
    def __init__(self, info, cast=[], director=[], invalid_movie=False):
        self.info = info
        self.cast = cast
        self.director = director
        self.invalid = invalid_movie

    def get_movie_id(self):
        return self.info[0]

    def get_title(self):
        return self.info[1]
    
    def get_year(self):
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
        return req5.getQry(self.info[0])
    
    def get_viewing_data(self):
        data = {}
        data['invalid'] = self.invalid
        if not self.invalid:
            data['id'] = self.get_movie_id()
            data['title'] = self.get_title()
            data['year'] = self.get_year()
            data['overview'] = self.get_overview()
            data['poster'] = self.get_poster()
            data['cast'] = self.get_cast()
            data['director'] = self.get_director()
            data['predictedRating'] = self.get_predicted_rating()
        else:
            data['info'] = INVALID_ID
        return data
    
