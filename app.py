from flask import Flask, render_template


app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/search")
def search_results():
    return render_template("search_results.html")


@app.get("/book/<book_id>")
def book_detail(book_id):
    return render_template("book_detail.html", book_id=book_id)


@app.get("/library")
def your_library():
    return render_template("your_library.html")


@app.get("/login")
def login():
    return render_template("auth/login.html")


@app.get("/signup")
def signup():
    return render_template("auth/signup.html")


if __name__ == "__main__":
    app.run(debug=True)