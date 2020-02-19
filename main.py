from flask import Flask, render_template, request, redirect, url_for, make_response
import uuid
import hashlib
from models import db, User

app = Flask(__name__)
db.create_all()


@app.route("/", methods=["GET"])
def index():
    session_token = request.cookies.get("session_token")

    if session_token:
        user = db.query(User).filter_by(session_token=session_token).first()
    else:
        user = None

    return render_template("index.html", user=user)


@app.route("/login", methods=["POST"])
def login():
    name = request.form.get("user-name")
    email = request.form.get("user-email")
    password = request.form.get("user-password")

    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    user = User(name=name, email=email, password=hashed_password)

    if hashed_password != user.password:
        return "WRONG PASSWORD! Go back and try again."
    elif hashed_password==user.password:
        session_token = str(uuid.uuid4())

        user.session_token = session_token
        db.add(user)
        db.commit()

        response = make_response(redirect(url_for('index')))
        response.set_cookie("session_token", session_token, httponly=True, samesite='Strict')
        return response


if __name__ == "__main__":
    app.run(debug=True)
