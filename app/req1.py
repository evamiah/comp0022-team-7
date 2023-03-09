import datetime

def getQuery(query, title, startYear, endYear, rating, genre, andOrOr, sortBy):
    if ((startYear != None) and (endYear != None)):
        if (int(startYear) > int(endYear)):
            new_startYear = endYear
            endYear = startYear
            startYear = new_startYear
        else:
            startYear = startYear
            endYear = endYear
        year_check = 1
    elif ((startYear == None) and (endYear != None)):
        startYear = 1900
        year_check = 1
    elif ((startYear != None) and (endYear == None)):
        today = datetime.date.today()
        endYear = today.year
        year_check = 1
    elif ((startYear == None) and (endYear == None)):
        year_check = 0

    if (rating == None):
        rating_check = 0
    else:
        rating_check = 1

    if ((title == None) and (genre == None)):
        title_genre_check = 0
    elif ((title == None) and (genre != None)):
        genre_type = ','.join(genre)
        title_genre_check = 1
    elif ((title != None) and (genre == None)):
        title_genre_check = 2
    elif ((title != None) and (genre != None)):
        genre_type = ','.join(genre)
        title_genre_check = 3

    temp = ""
    for genre_elem in genre:
        temp = temp + " (g.genre=" + genre_elem + ") AND "
        
    temp = temp[:-5]

    if (((title_genre_check == 1) or (title_genre_check == 3)) and (andOrOr == "and") and (temp != "")):
        query = whereAnd(query)
        query = query + temp

    if (((title_genre_check == 1) or (title_genre_check == 3)) and (andOrOr == "or")):
        query = whereAnd(query)
        query = query + " (1 IN (" + genre_type + "))"

    if ((title_genre_check == 2) or (title_genre_check == 3)):
        query = whereAnd(query)
        query = query + " m.title LIKE '%" + title + "%'"

    if(rating_check == 1):
        query = whereAnd(query)
        query = query +  " mr.rating = " + rating

    if(year_check == 1):
        query = whereAnd(query)
        query = query + " m.release_year BETWEEN " + startYear + " AND " + endYear

    if (sortBy != None):
        query = getOrderBy(query,sortBy)
    return query

def whereAnd(query):
    if "WHERE" in query:
        query = query + " AND"
    else:
        query = query + " WHERE"
    return query

def getOrderBy(query,sortBy):
    if (sortBy=="title"):
        query = query + " ORDER BY m.title"
    elif (sortBy=="year"):
        query = query + " ORDER BY m.release_year"
    elif (sortBy=="genre"):
        query = query + " ORDER BY g.genre"
    elif(sortBy=="rating"):
        query = query + " ORDER BY mr.rating"
    if (sortBy[-4:] == "desc"):
        query = query + " DESC"
    return query

title = "hi"
startYear = "1900"
endYear = "2000"
genre = ["Action"]
rating = "4.5"
andOrOr = "and"
sortBy = "title"
query = "SELECT * FROM ml_movies"
query = getQuery(query, title, startYear, endYear, rating, genre, andOrOr, sortBy)
print(query)