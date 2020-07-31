CREATE TABLE reviews
(
    id SERIAL PRIMARY KEY,
    book_id INT REFERENCES books(id),
    user_id SMALLINT REFERENCES users(id),
    username VARCHAR NOT NULL,
    rating int NOT NULL,
    review varchar NOT NULL
)

