from flask import Flask, render_template, request, redirect, url_for, make_response
from models import db, User

app = Flask(__name__)
db.create_all()


@app.route("/", methods=["GET"])
def index():
    email_address = request.cookies.get("email")

    if email_address:
        user = db.query(User).filter_by(email=email_address).first()
    else:
        user = None


    return render_template("index.html", user=user)


@app.route("/login", methods=["POST"])
def login():
    name = request.form.get("user-name")
    email = request.form.get("user-email")
    password = request.form.get("user-password")

    user = User(name=name, email=email, password=password)

    db.add(user)
    db.commit()

    if password != user.password:
        return "WRONG PASSWORD! Go back and try again."

    response = make_response(redirect(url_for('index')))
    response.set_cookie("email", email)
    return response


if __name__ == "__main__":
    app.run(debug=True)
