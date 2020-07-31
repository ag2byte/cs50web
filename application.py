import os
import requests


from flask import Flask, session, render_template, request, redirect, url_for, jsonify, flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))  # this is the database object

# signin


@app.route("/", methods=['GET', 'POST'])
def signin():

    if request.method == 'POST':
        u_name = request.form.get("input1")
        pswd = request.form.get("input2")
        user = db.execute('SELECT * FROM users WHERE username = :username',
                          {"username": u_name}).fetchone()  # as there is unique user name
        if user is None:  # user does not exists
            return render_template('notif.html', message="User does not exists. Create your account", link="/signup", pagemessage="Sign-up")
        elif user['password'] == pswd:  # user exists
            session["user"] = user
            return redirect(url_for("search"))  # go to search page
        else:
            return render_template('notif.html', message="Incorrect Password", link="./", pagemessage="login")

    return render_template('signin.html')

# signup


@app.route("/signup", methods=['GET', 'POST'])  # this method
def signup():

    if request.method == "POST":
        u_name = request.form.get("input1")  # taking input
        pswd = request.form.get("input2")
        if db.execute("SELECT * FROM users WHERE username = :username",
                      {"username": u_name}).rowcount != 0:
            # user exists already

            return render_template('notif.html', message="User already exists", link="./", pagemessage="login")
        # else insert user into database

        db.execute("INSERT INTO users (username,password) VAlUES (:username,:password)",
                   {"username": u_name, "password": pswd})
        db.commit()
        # render this if signup is successful
        return render_template('notif.html', message="Signup successful", link="./", pagemessage="login")

    return render_template('signup.html')


# search
@app.route('/search', methods=['GET', 'POST'])
def search():
    if "user" in session:
        user = session["user"]
        if request.method == "POST":
            ser_type = request.form.get("searchtype")  # isbn,author,or title
            ser_item = request.form.get("searchfield")  # value
            result = []
            if ser_type == "isbn":
                result = db.execute('SELECT * from books where lower(isbn) LIKE LOWER(:term)',  # making queries case insensitive
                                    {"term": f"%{ser_item}%"}).fetchall()
            elif ser_type == "title":
                result = db.execute('SELECT * from books where lower(title) LIKE LOWER(:term)',
                                    {"term": f"%{ser_item}%"}).fetchall()
            elif ser_type == "author":
                result = db.execute('SELECT * from books where lower(author) LIKE LOWER(:term)',
                                    {"term": f"%{ser_item}%"}).fetchall()
            # if result:
            return render_template('searchresult.html', records=result, username=user['username'])

        return render_template('search.html', username=user['username'])
    else:
        return render_template('notif.html', message="You need to login first", link="./", pagemessage="login")

# books


@app.route('/books/<int:id>', methods=['GET', 'POST'])  # route to book id
def books(id):
    if "user" in session:  # check for user still logged in
        user = session['user']
        book = db.execute(
            'SELECT * FROM books WHERE id = :id ', {"id": id}).fetchone()  # go to this book
        grev = requests.get("https://www.goodreads.com/book/review_counts.json",
                            params={"key": os.getenv("GOODREADS_KEY"), "isbns": book['isbn']}).json()

        if book:  # check if book exists

            reviews = db.execute(
                'SELECT * from reviews WHERE book_id = :id ', {"id": book['id']}).fetchall()
            # adding review to database
            if request.method == "POST":
                new_rev = request.form.get('review_text')
                rating = request.form.get('rating')
                chk_ent = db.execute('SELECT * FROM reviews where username = :username AND book_id = :book_id',
                                     {"username": user['username'], "book_id": book['id']}).fetchone()
                if not chk_ent:

                    db.execute("INSERT INTO  reviews (book_id,user_id,username,rating,review) VALUES (:book_id,:user_id,:username,:rating,:review)",
                               {"book_id": book['id'], "user_id": user['id'], "username": user['username'], "rating": rating, "review": new_rev})
                    db.commit()
                    flash(
                        'Your review was added successfully. Refresh to view it.', "info")
                else:
                    flash('Cannot have more than one review', "error")

        return render_template('book.html', book=book, username=user['username'], reviews=reviews, grev=grev)

# api


@app.route('/api/<string:isbn>')
def api(isbn):
    # any one can access api, no need to log in
    res = db.execute('SELECT * from books WHERE isbn= :isbn',
                     {'isbn': isbn}).fetchone()
    if not res:
        # 404 error in json format
        return jsonify({"error": "404 error: isbn not found"}), 404
    # if present show the json format
    book_json = requests.get("https://www.goodreads.com/book/review_counts.json",
                             params={"key": os.getenv("GOODREADS_KEY"), "isbns": isbn}).json()
    # we only need some of the data not all the data from book_json
    average_score = book_json["books"][0]["average_rating"]
    review_count = book_json["books"][0]["reviews_count"]
    # returning json format
    return jsonify({
        "title": res['title'],
        "author": res['author'],
        "year": res['year'],
        "isbn": res['isbn'],
        "review_count": review_count,
        "average_score": average_score


    })


@app.route('/logout')  # logging out
def logout():
    session.pop("user", None)
    return render_template('notif.html', message="Logout successful. To login again, ", link="./", pagemessage="login")


if __name__ == "__main__":
    app.run(debug=True)  # debug mode is true
