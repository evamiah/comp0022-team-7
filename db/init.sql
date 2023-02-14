create database movie_db;
use movie_db;

CREATE TABLE movies_table (
    movie_id INT PRIMARY KEY, 
    title VARCHAR(100)
    );

INSERT INTO movies_table (movie_id, title) VALUES 
(1, 'The Dark Knight'),
(2, 'Home Alone'),
(3, 'The Lion King');