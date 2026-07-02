from flask import Blueprint, render_template, redirect, url_for, session

routes = Blueprint("routes", __name__)


# INDEX
@routes.route("/")
def index():
    return render_template("index.html")


# SEARCH
@routes.route("/search")
def search_results():
    return render_template("search_results.html")


# BOOK DETAIL
@routes.route("/book/<book_id>")
def book_detail(book_id):
    return render_template("book_detail.html", book_id=book_id)


# LIBRARY
@routes.route("/library")
def your_library():
    return render_template("your_library.html")


# AUTH - LOGIN
@routes.route("/auth/login", methods=["GET", "POST"])
def login():
    return render_template("auth/login.html")


# AUTH - SIGNUP
@routes.route("/auth/signup", methods=["GET", "POST"])
def signup():
    return render_template("auth/signup.html")


# AUTH - LOGOUT
@routes.route("/auth/logout")
def logout():
    session.clear()
    return redirect(url_for("routes.login"))