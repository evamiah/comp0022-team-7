from flask import Flask, render_template
from typing import List, Dict
import mysql.connector
import json
import csv

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

def load_movies():
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'movie_db'
    }
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
            cursor.execute('INSERT INTO movies (movie_id, title, release_year) VALUES (%s, %s, %s);', (id, title, date))

    connection.commit()
    cursor.close()
    connection.close()