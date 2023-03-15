import csv
from extension_scripts import *

'''
Creates csv file with movie's lead actors and directors
- movie IDs from MovieLens datasets
- TMDb IDs from MovieLens links.csv
'''
def get_people():
    with open('links.csv', 'r', encoding="utf-8") as links_csv:
        with open('cast_crew.csv', 'a', newline='', encoding="utf-8") as cc_csv:

            links_csv_r = csv.reader(links_csv)
            cc_csv_w = csv.writer(cc_csv, delimiter=';')

            #NOTE: uncomment if appending rows after interruption, replace range with last line written
            #for i in range(3128):
                #next(links_csv_r)
            
            #NOTE: comment out if appending after interruption
            # skip the headings
            next(links_csv_r)

            #NOTE: comment out if appending after interruption
            cc_csv_w.writerow(["movie_id", "lead_cast", "director"])

            for line in links_csv_r:
                movie_id = line[0]
                tmdb_id = line[2]
                if tmdb_id:
                    movie_credits = get_movie_credits(tmdb_id, movie_id)
                    #cast = get_cast(tmdb_id)
                    #director = get_director(tmdb_id)
                    cc_csv_w.writerow(movie_credits)
                else:
                    cc_csv_w.writerow(credits_not_found(movie_id))

'''
Creates csv file with movie's overview and poster path
- movie IDs from MovieLens datasets
- TMDb IDs from MovieLens links.csv
'''
def get_info():
    with open('links.csv', 'r', encoding="utf-8") as links_csv:
        with open('movie_info.csv', 'a', newline='', encoding="utf-8") as info_csv:
            links_csv_r = csv.reader(links_csv)
            info_csv_w = csv.writer(info_csv)
            
            #NOTE: uncomment if appending rows after interruption, replace range with last line written
            #for i in range(5013):
                #next(links_csv_r)
            
            #NOTE: comment out if appending after interruption
            # skip the headings
            next(links_csv_r)

            #NOTE: comment out if appending after interruption
            info_csv_w.writerow(["movie_id", "overview", "poster_path"])

            for line in links_csv_r:
                movie_id = line[0]
                tmdb_id = line[2]
                if tmdb_id:
                    movie_info = get_movie_info(tmdb_id, movie_id)
                    info_csv_w.writerow(movie_info)
                else:
                    info_csv_w.writerow(info_not_found(movie_id))

