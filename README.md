# Project 1

This is a book review website where users can log in using a username and a password and give review about a book from a list of 5000 books.
The book can be searched via isbn no, title or author
### Structure:
- templates: contain all the html pages
            * layout.html = common html for all the pages 
            * signup.html = signup page
            * signin.html = signin page / landing page
            * search.html = used for searching a page(accessible only after user login) 
            * searchresult.hmtl = displays the results of searched item
            * book.html = details about the book selected . User can view and add reviews here
            * notif.html = common message page 

- static: contain all the css for the above pages
                * naming is similar to that of html naming

- sql_queries- contain the commands used to create the table in database
            * these are to be entered as they are for the project to write and read data
                * books.sql = table for all books
                * reviews.sql = table for all reviews
                * users.sql = table for all users
- requirements.txt- all the necessary requirements for running this app
- books.csv = csv of 5000 books
- import.py- importing data from books.csv and storing in books table of the database
- application.py- flask app controlling all the backend of the website
              - debug = True
              - run this using python import.py

## Important note- Before running application.py do set the DATABASE_URL and GOODREADS_KEY variables as per your databases



