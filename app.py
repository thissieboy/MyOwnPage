from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from sqlalchemy.orm import sessionmaker, scoped_session
from tabledef import *

engine = create_engine('postgres://gncnnimdwioftz:f07c4547a77132b37d2a7fee253a01a6653450279db56e61486e00cba9f53bab@ec2-54-75-230-41.eu-west-1.compute.amazonaws.com:5432/db7kja37bk7gc', echo=True)
db = scoped_session(sessionmaker(bind=engine))
app = Flask(__name__)

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('search.html')

@app.route('/login', methods=['POST'])
def do_admin_login():

    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])

    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
    result = query.first()

    if result:
        session['logged_in'] = True
        return home()
    else:
        flash('wrong password!')
        return home()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route('/search', methods=['GET'])
def search():
    if request.method == "GET":
        if not session.get("logged_in"):
            flash("You are not logged in")
            return redirect(url_for('home'), "303")
        else:
            query = request.args.get('q')
            page = request.args.get('page')
            if query is None:
                return render_template("search.html", message="No results.")
            text = f"%{query}%".lower()
            # finding how many pages prepare
            pages_res = db.execute(
                "SELECT id FROM books WHERE LOWER(original_title) LIKE :title OR LOWER(authors) LIKE :authors OR original_publication_year LIKE :year ORDER BY id",
                {"title": text, "authors": text, "year": text}).fetchall()
            pages = math.ceil(len(pages_res) / 10)

            if page is None or int(page) <= 0:
                off = int(0)
                page = int(1)
            else:
                off = 10 * (int(page) - 1)

            res = db.execute(
                "SELECT * FROM books WHERE LOWER(original_title) LIKE :title OR LOWER(authors) LIKE :authors OR original_publication_year LIKE :year ORDER BY id LIMIT 10 OFFSET :offset",
                {"title": text, "authors": text, "year": text, "offset": off}).fetchall()
            books = []
            for b_id, g_id, isbn, isbn13, authors, year, title, rating, r_count, image_url, small_image_url in res:
                new_book = Book(b_id, g_id, isbn, isbn13, authors.split(', '), year, title, rating, r_count, image_url, small_image_url)
                new_book.trim_authors()
                books.append(new_book)

            return render_template("search.html", results=books, page=int(page), query=query, pages=int(pages), username=session["user_name"])

    elif request.method == "POST":
        return redirect(url_for('index'), 303)



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        if session.get("logged_in"):
            flash("You are already logged in")
            return home()
        else:
            return render_template("register.html")


    if request.method == "POST":
        xusername = request.form.get("username")
        xpassword = request.form.get("password")

        db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
                    {"username": xusername, "password": xpassword})
        db.commit()
        flash("Register succesfull")
        return render_template("home.html")


app.secret_key = os.urandom(12)
app.run(debug=True,host='0.0.0.0', port=4000)
