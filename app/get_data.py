from unittest import result
from django.http import response
import requests
import tmdbsimple as tmdb
import rottentomatoes as rt

tmdb.API_KEY = '1e97e6266061128613ab12764f041937';
rt_url = 'https://rotten-tomatoes-api.ue.r.appspot.com/search/'
rt_url_2 = 'https://rotten-tomatoes-api.ue.r.appspot.com/movie/'

debug_links = [
    (1,862),
    (2,8844),
    (3,15602),
    (4,31357),
    (5,11862)
]

def get_rating(title, year):
    print("Title:", title)
    results = requests.get(rt_url+title)
    results_2 = requests.get(rt_url_2+title)
    text_results = results.text
    text2 = results_2.text
    print("Text:", text_results)
    print("Text 2:", text2)
    print("No request", rt.tomatometer(title))
    if results != None:
        results = results.json()
        for movie in results["movies"]:
            if (movie["year"]==year):
                return movie["tomatometer"], movie["audience_score"]
    t = "N/A"
    a = "N/A"
    return t, a

def no_api_rating(title, year):
    result = rt.search.search_results(title)
    filtered = rt.search.filter_searches(result)
    for i in filtered:
    #for i in result:
        print(i)
        #if (i.has_tomatometer is True) and (i.is_movie is True):
        response =  requests.get(i.url)
        t_title = rt.movie_title(title, response.text)
        y = rt.year_released(t_title, response.text)
        t_score = rt.tomatometer(t_title, response.text)["value"]
        a_score = rt.audience_score(t_title, response.text)["value"]
        if t_title == title and y == year:
            print(t_title, y, t_score, a_score)
        #movie = rt.Movie(movie_title=title, force_url=i.url)
        #score = rt.tomatometer(movie)
        



def get_cast(movie_id):
    movie = tmdb.Movies(movie_id).credits()
    cast = movie["cast"]
    response = []
    for i in range(5):
        response.append(cast[i]["name"])
    return response;

def get_director(movie_id):
    movie = tmdb.Movies(movie_id).credits()
    crew = movie["crew"]
    response = []
    for i in crew:
        if i["job"] == "Director":
            response.append(i["name"])
    return response
        
    
def get_title(movie_id):
    movie = tmdb.Movies(movie_id).info()
    title = movie["title"]
    return title

def get_release_year(movie_id):
    movie = tmdb.Movies(movie_id).info()
    year = movie["release_date"][:4]
    return year

def main():
    movies = []
    for i in debug_links:
        title = get_title(i[1])
        year = get_release_year(i[1])
        #rating, audience = get_rating(title, year)
        cast = get_cast(i[1])
        director = get_director(i[1])
        movies.append([title, cast, director])

    
    for movie in movies:
        print("Title:", movie[0], "Cast:", movie[1], "Director(s):", movie[2])

def test():
    title = "Balto"
    year = "1995"
    no_api_rating(title, year)


main()
#test()