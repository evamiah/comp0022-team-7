create database movie_db;
use movie_db;

CREATE TABLE movies (
    movie_id INT PRIMARY KEY NOT NULL, 
    title VARCHAR(200),
    release_year INT,
    overview VARCHAR(1000),
    poster_path VARCHAR(200)
    );

CREATE TABLE genres (
    genre_id INT PRIMARY KEY NOT NULL,
    genre VARCHAR(50)
    );

CREATE TABLE movie_genre (
    movie_id INT,
    genre_id INT,
    CONSTRAINT PK_movie_genre PRIMARY KEY (movie_id, genre_id),
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
    FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
    );

CREATE TABLE movie_ratings (
    user_id INT NOT NULL,
    movie_id INT NOT NULL,
    rating FLOAT NOT NULL,
    time_stamp INT, 
    PRIMARY KEY (user_id, movie_id),
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
    );

CREATE TABLE rt_ratings (
    movie_id INT NOT NULL,
    tomatometer INT,
    audience_score INT,
    CONSTRAINT PK_rt_ratings PRIMARY KEY (movie_id),
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
);

CREATE TABLE movie_links (
    movie_id INT NOT NULL,
    imdb_id VARCHAR(20) UNIQUE,
    tmdb_id VARCHAR(20),
    CONSTRAINT PK_movie_links PRIMARY KEY (movie_id),
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
    );

CREATE TABLE movie_tags (
    user_id INT NOT NULL,
    movie_id INT NOT NULL,
    tag VARCHAR(100),
    time_stamp INT, 
    PRIMARY KEY (user_id, movie_id, tag),
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
    );

INSERT INTO genres (genre_id, genre) VALUES
(1, 'Action'),
(2, 'Adventure'),
(3, 'Animation'),
(4, 'Children'),
(5, 'Comedy'),
(6, 'Crime'),
(7, 'Documentary'),
(8, 'Drama'),
(9, 'Fantasy'),
(10, 'Film-Noir'),
(11, 'Horror'),
(12, 'Musical'),
(13, 'Mystery'),
(14, 'Romance'),
(15, 'Sci-Fi'),
(16, 'Thriller'),
(17, 'War'),
(18, 'Western'),
(19, 'IMAX'),
(20, '(no genres listed)');

CREATE TABLE people (
    person_id INT NOT NULL AUTO_INCREMENT,
    full_name VARCHAR(50),
    PRIMARY KEY(person_id)
    );

INSERT INTO people (person_id, full_name) VALUES
(1, 'N/A');


CREATE TABLE movie_cast (
    movie_id INT NOT NULL,
    actor_id INT NOT NULL,
    CONSTRAINT PK_movie_cast PRIMARY KEY (movie_id, actor_id),
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
    FOREIGN KEY (actor_id) REFERENCES people(person_id)
    );

CREATE TABLE movie_directing (
    movie_id INT NOT NULL,
    director_id INT NOT NULL,
    CONSTRAINT PK_movie_directing PRIMARY KEY (movie_id, director_id),
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
    FOREIGN KEY (director_id) REFERENCES people(person_id)
);