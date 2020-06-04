DROP DATABASE IF EXISTS demo;
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

CREATE TABLE users (
    id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(30) NOT NULL
    );

INSERT INTO users
    (username)
VALUES
    ('SQL'),
    ('Exploiters'),
    ('Should'),
    ('Know'),
    ('SQL');
