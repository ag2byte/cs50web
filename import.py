# this program imports data from csv file and adds it to the table: books
import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


def main():
    f = open("books.csv")
    reader = csv.reader(f)
    first_row = next(reader)  # moving reader to 2nd row
    i = 1
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",  # :isbn etc are placeholders
                   {"isbn": isbn, "title": title, "author": author, "year": int(year)})  # dictionary
        print(
            f"Added book {isbn}{title} {i} of 5000")
        i += 1
    db.commit()


if __name__ == "__main__":
    main()
