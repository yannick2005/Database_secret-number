from random import randint
from flask import Flask, make_response, render_template, request, redirect, url_for
from models import db, User


app = Flask(__name__)
db.create_all()


@app.route("/", methods=["GET"])
def index():
    email_address = request.cookie.get("email")
    if email_address:
        user = db.query(User).filter_by(email=email_address).first()
    else:
        user = None

    return render_template("Index.html", user=user)


@app.route("/calculate", methods=["POST"])
def calculate():
    guess = int(request.form.get("guess"))
    email_address = int(request.cookies.get("email_address"))

    user = db.query(User).filter_by(email=email_address).first()

    if guess == user.secret_number:
        new_secret = randint(1, 30)
        user.secret_number = new_secret
        db.add(user)
        db.commit()
    elif guess > user.secret_number:
        msg = "Your guess is too big ..."
        return render_template("result.html", message=msg)
    elif guess < user.secret_number:
        msg = "Your guess is too small ..."

    return render_template("result.html", message=msg)


@app.route("/login", methods=["POST"])
def login():
    name = request.form.get("user-name")
    email = request.form.get("user-email")

    secret_number = randint(1, 30)

    user = db.query(User).filter_by(email=email).first()

    if not user:
        user = User(name=name, email=email, secret_number=secret_number)
        db.add(user)
        db.commit()

    response = make_response(redirect(url_for("Index")))
    response.set_cookie("email", email)

    return response


if __name__ == '__main__':
    app.run()
