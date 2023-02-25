create database movie_db;
use movie_db;

CREATE TABLE movies_table (
    movie_id INT PRIMARY KEY, 
    title VARCHAR(100)
    );

CREATE TABLE movies (
    movie_id INT PRIMARY KEY, 
    title VARCHAR(200),
    release_year INT
    );

CREATE TABLE genres (
    genre_id INT PRIMARY KEY,
    genre VARCHAR(50)
    );

CREATE TABLE movie_genre (
    movie_id INT,
    genre_id INT,
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
    FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
    );

INSERT INTO movies_table (movie_id, title) VALUES 
(1, 'The Dark Knight'),
(2, 'Home Alone'),
(3, 'The Lion King');

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