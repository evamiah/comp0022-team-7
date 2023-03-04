from flask import Flask, render_template
from typing import List, Dict
import mysql.connector
import json
import csv
from ast import literal_eval

NO_OVERVIEW_VALUE = "N/A"
NO_CREDITS_VALUE = "N/A"

# for debugging
import logging
logging.basicConfig(level=logging.DEBUG)

config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'movie_db'
    }

# helper function to make sure the titles are in the right format and to extract the date 
def format_title(title):
    # remove quotes and whitespace at beginning and end
    title = title.replace("\"", "")
    title = title.strip()
    
    # check if there is a date
    if title[-1] == ')':
        # separate date and title 
        date = int(title[-5:-1])
        title = title[:-6]
    else:
        date = 0    

    return title, date

# fills overview value when empty
def check_overview(overview):
    if overview == '':
        return NO_OVERVIEW_VALUE
    else:
        return overview

# helper function to convert the pipe-separated list of genres to a list of genre ids 
def extract_genre_ids(genres, cursor):
    genres = genres.split('|')
    genre_ids = []
    # append a genre_id for each genre
    for genre in genres:
        query = 'SELECT genre_id FROM genres WHERE genre = ' + '\'' +  genre + '\''
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            genre_id = result[0]
            genre_ids.append(genre_id)
        # check if there are no genres 
        else:
            genre_ids.append(20)
            break
    return genre_ids

def insert_new_people(names, cursor):
    for name in names:
        query = 'SELECT person_id FROM people WHERE full_name = ' + '\'' +  name + '\''
        cursor.execute(query)
        result = cursor.fetchone()
        if not result:
            cursor.execute('INSERT INTO people (full_name) VALUES (%s)', (name))
            cursor.execute(query)

def get_person_id(names, cursor):
    people_ids = []
    for name in names:
        query = 'SELECT person_id FROM people WHERE full_name = ' + '\'' +  name + '\''
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            person_id = result[0]
            people_ids.append(person_id)
        # check if there are no cast/crew members
        else:
            people_ids.append(0)
            break
    return people_ids

def empty_credits(credits):
    return (credits == '') or (credits == [''])

def format_credits(credits):
    if credits != '':
        credits = literal_eval(credits)
    else:
        return ''

def load_movies():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    
    # populate the table
    with open('data/movies.csv', 'r') as movies_csv:
        movies_csv_r = csv.reader(movies_csv)

        # skip the first line
        next(movies_csv_r)

        for line in movies_csv_r:
            id = line[0]
            title, date = format_title(line[1])
            overview = check_overview(line[3])
            poster = line[4]
            cursor.execute('INSERT INTO movies (movie_id, title, release_year, overview, poster_path) VALUES (%s, %s, %s, %s, %s);', (id, title, date, overview, poster))

    connection.commit()
    cursor.close()
    connection.close()

def load_movie_genre():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    
    # populate the table
    with open('data/movies.csv', 'r') as movies_csv:
        movies_csv_r = csv.reader(movies_csv)

        # skip the first line
        next(movies_csv_r)

        for line in movies_csv_r:
            movie_id = line[0]
            genres = line[2]
            genre_ids = extract_genre_ids(genres, cursor)

            for genre_id in genre_ids:
                cursor.execute('INSERT INTO movie_genre (movie_id, genre_id) VALUES (%s, %s);', (movie_id, genre_id))
        
    connection.commit()
    cursor.close()
    connection.close()

def load_movie_ratings():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    # populate the table
    with open('data/ratings.csv', 'r') as ratings_csv:
        ratings_csv_r = csv.reader(ratings_csv)

        # skip the first line
        next(ratings_csv_r)

        for line in ratings_csv_r:
            user_id = line[0]
            movie_id = line[1]
            rating = line[2]
            timestamp = line[3]

            cursor.execute('INSERT INTO movie_ratings (user_id, movie_id, rating, time_stamp) VALUES (%s, %s, %s, %s);', (user_id, movie_id, rating, timestamp))   

    connection.commit()
    cursor.close()
    connection.close()

def load_movie_links():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    # populate the table
    with open('data/links.csv', 'r') as links_csv:
        links_csv_r = csv.reader(links_csv)

        # skip the first line
        next(links_csv_r)

        for line in links_csv_r:
            movie_id = line[0]
            imdb_id = str(line[1])
            tmdb_id = str(line[2])

            # some movies don't have tmdb links
            if tmdb_id == '':
                cursor.execute('INSERT INTO movie_links (movie_id, imdb_id, tmdb_id) VALUES (%s, %s, NULL);', (movie_id, imdb_id))
            else:
                cursor.execute('INSERT INTO movie_links (movie_id, imdb_id, tmdb_id) VALUES (%s, %s, %s);', (movie_id, imdb_id, tmdb_id))

    connection.commit()
    cursor.close()
    connection.close()

def load_movie_tags():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    # populate the table
    with open('data/tags.csv', 'r') as tags_csv:
        tags_csv_r = csv.reader(tags_csv)

        # skip the first line
        next(tags_csv_r)

        for line in tags_csv_r:
            user_id = line[0]
            movie_id = line[1]
            tag = line[2]
            timestamp = line[3]

            cursor.execute('INSERT INTO movie_tags (user_id, movie_id, tag, time_stamp) VALUES (%s, %s, %s, %s);', (user_id, movie_id, tag, timestamp))

    connection.commit()
    cursor.close()
    connection.close()

def load_empty_credit():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('INSERT INTO people (person_id, full_name) VALUES (%s, %s);', (0, "N/A"))
    connection.commit()
    cursor.close()
    connection.close() 

def load_people():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    
    # populate the table
    with open('data/cast_crew.csv', 'r') as credits_csv:
        credits_csv_r = csv.reader(credits_csv)

        # skip the first line
        next(credits_csv_r)

        for line in credits_csv_r:
            cast = format_credits(line[1])
            director = format_credits(line[2])
            if not empty_credits(cast):
                insert_new_people(cast, cursor)
            if not empty_credits(director):
                insert_new_people(director)

    connection.commit()
    cursor.close()
    connection.close()

def load_cast():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    
    # populate the table
    with open('data/cast_crew.csv', 'r') as credits_csv:
        credits_csv_r = csv.reader(credits_csv)

        # skip the first line
        next(credits_csv_r)

        for line in credits_csv_r:
            movie_id = line[0]
            cast = format_credits(line[1])
            if not empty_credits(cast):
                cast_ids = get_person_id(cast, cursor)

                for person_id in cast_ids:
                    cursor.execute('INSERT INTO movie_cast (movie_id, actor_id) VALUES (%s, %s);', (movie_id, person_id))
            else:
                cursor.execute('INSERT INTO movie_cast (movie_id, actor_id) VALUES (%s, %s);', (movie_id, 0))
        
    connection.commit()
    cursor.close()
    connection.close()

def load_directors():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    
    # populate the table
    with open('data/cast_crew.csv', 'r') as credits_csv:
        credits_csv_r = csv.reader(credits_csv)

        # skip the first line
        next(credits_csv_r)

        for line in credits_csv_r:
            movie_id = line[0]
            directors = format_credits(line[2])
            if not empty_credits(directors):
                director_ids = get_person_id(directors, cursor)

                for person_id in director_ids:
                    cursor.execute('INSERT INTO movie_directing (movie_id, actor_id) VALUES (%s, %s);', (movie_id, person_id))
            else:
                cursor.execute('INSERT INTO movie_directing (movie_id, actor_id) VALUES (%s, %s);', (movie_id, 0))
        
    connection.commit()
    cursor.close()
    connection.close()