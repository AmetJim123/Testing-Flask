from flask import (Flask, redirect, url_for)

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Hello, this is my first proyect in Flask</h1>"

@app.route("/user/<name>/")
def user(name):
    return f"Hey, long time no see, eh {name}.."

@app.route("/admin")
def admin():
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run()
