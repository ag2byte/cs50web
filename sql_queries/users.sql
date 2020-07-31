CREATE TABLE users
(
    id SERIAL PRIMARY KEY,
    username VARCHAR(35) UNIQUE,
    password VARCHAR(35)
)