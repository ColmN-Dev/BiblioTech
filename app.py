from flask import Flask, render_template


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search")
def search_results():
    return render_template("search_results.html")


@app.route("/book/<book_id>")
def book_detail(book_id):
    return render_template("book_detail.html", book_id=book_id)


@app.route("/library")
def your_library():
    return render_template("your_library.html")


@app.route("/auth/login", methods=["GET", "POST"])
def login():
    return render_template("auth/login.html")


@app.route("/auth/signup", methods=["GET", "POST"])
def signup():
    return render_template("auth/signup.html")


if __name__ == "__main__":
    app.run(debug=True)