CREATE TABLE books
(
    id SERIAL PRIMARY KEY,
    isbn TEXT,
    title TEXT,
    author TEXT,
    year SMALLINT
)