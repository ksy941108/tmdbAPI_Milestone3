import os
import random
import flask
import json
from flask_login import login_user, current_user, LoginManager, UserMixin
from flask_login.utils import login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from tmdb import movie_info
from wikipedia import getURL
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


app = flask.Flask(__name__)
app.secret_key = "secret"
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

uri = os.getenv("DATABASE_URL")
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

db = SQLAlchemy(app)


class Authentication(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    register = db.Column(db.String(20))


class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_login = db.Column(db.String(20))
    title = db.Column(db.Integer)
    ratings = db.Column(db.Integer)
    comments = db.Column(db.String(500))


db.create_all()

# set up a separate route to serve the index.html file generated
# by create-react-app/npm run build.
# By doing this, we make it so you can paste in all your old app routes
# from Milestone 2 without interfering with the functionality here.

bp = flask.Blueprint(
    "bp",
    __name__,
    template_folder="./static/react",
)


@bp.route("/delete")
def delete():
    return flask.render_template("index.html")


@app.route("/review", methods=["GET", "POST"])
def review():
    movie_list = Movies.query.all()
    lists = []

    for i in movie_list:
        if i.user_login == current_user.register:
            lists.append(
                {
                    "movie_id": i.title,
                    "comment_list": i.comments,
                    "rating_list": i.ratings,
                }
            )
    return flask.jsonify(datas=lists)


@app.route("/save", methods=["GET", "POST"])
def save():
    datas = flask.request.json.get("datas")
    Movies.query.filter_by(user_login=current_user.register).delete()
    for data in datas:
        new_movie = Movies(
            user_login=current_user.register,
            title=data["movie_id"],
            ratings=data["rating_list"],
            comments=data["comment_list"],
        )
        db.session.add(new_movie)
    db.session.commit()
    new_data = Movies.query.filter_by(user_login=current_user.register).all()
    lists = []
    for i in new_data:
        lists.append(
            {
                "movie_id": i.title,
                "comment_list": i.comments,
                "rating_list": i.ratings,
            }
        )
    return flask.jsonify({"new_data": lists})


# route for serving React page

app.register_blueprint(bp)


@login_manager.user_loader
def load_user(register):
    return Authentication.query.get(register)


@app.route("/register", methods=["POST", "GET"])
def registration():
    user_id = flask.request.form.get("register_id")
    user_check = Authentication.query.filter_by(register=user_id).first()
    if user_check:
        flask.flash("Existing User ID")
        pass
    else:
        user_check = Authentication(register=user_id)
        db.session.add(user_check)
        db.session.commit()
    return flask.redirect(flask.request.referrer)


@app.route("/login", methods=["POST", "GET"])
def login():
    user_id = flask.request.form.get("login_id")
    user_check = Authentication.query.filter_by(register=user_id).first()
    if user_check:
        login_user(user_check)
        return flask.redirect(flask.url_for("main"))
    else:
        flask.flash("user id does not exist!")
        return flask.redirect(flask.request.referrer)


@app.route("/logout")
def logout():
    logout_user()
    return flask.redirect("/")


# Database
@app.route("/add", methods=["POST", "GET"])
def add():
    if flask.request.method == "POST":
        movie_title = flask.request.form.get("movie_title")
        movie_ratings = flask.request.form.get("ratings")
        movie_comments = flask.request.form.get("comments")
        user_login = current_user.register
        new_movie = Movies(
            user_login=user_login,
            title=movie_title,
            ratings=movie_ratings,
            comments=movie_comments,
        )
        db.session.add(new_movie)
        db.session.commit()

    return flask.redirect("/main")


# main page = login
@app.route("/")
def main_login():
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for("main"))
    return flask.render_template("login.html")


@app.route("/")

# main movie information page
@app.route("/main", methods=["POST", "GET"])
def main():
    if flask.request.method == "POST":
        data = flask.request.form.get("movie_title")
        db.session.add(data)
        db.session.commit()

    MOVIE_IDS = [634649, 141, 438631]  # Spiderman No Way Home  # Donnie Darko  # Dune
    data = flask.request.form.get("movie_title")
    random_id = random.choice(MOVIE_IDS)
    title, tagline, genre, posterImg = movie_info(random_id)
    url = getURL(title)
    movie_list = Movies.query.all()
    user_list = []
    comment_list = []
    rating_list = []

    for i in movie_list:
        if i.title == random_id:
            user_list.append(i.user_login)
            comment_list.append(i.comments)
            rating_list.append(i.ratings)

    num_movie = len(movie_list)
    num_comment = len(comment_list)

    return flask.render_template(
        "main.html",
        title=title,
        tagline=tagline,
        genre=genre,
        posterImg=posterImg,
        url=url,
        random_id=random_id,
        movie_list=movie_list,
        num_movie=num_movie,
        user_list=user_list,
        comment_list=comment_list,
        rating_list=rating_list,
        current_user=current_user.register,
        num_comment=num_comment,
    )


app.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8080)), debug=True)
