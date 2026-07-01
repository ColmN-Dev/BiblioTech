from flask import render_template, redirect, url_for, session

# INDEX
@app.route("/")
def index():
    return render_template("index.html")


# SEARCH
@app.route("/search")
def search_results():
    return render_template("search_results.html")


# BOOK DETAIL
@app.route("/book/<book_id>")
def book_detail(book_id):
    return render_template("book_detail.html", book_id=book_id)


# LIBRARY
@app.route("/library")
def your_library():
    return render_template("your_library.html")


# AUTH - LOGIN
@app.route("/auth/login", methods=["GET", "POST"])
def login():
    return render_template("auth/login.html")


# AUTH - SIGNUP
@app.route("/auth/signup", methods=["GET", "POST"])
def signup():
    return render_template("auth/signup.html")


# AUTH - LOGOUT
@app.route("/auth/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))
