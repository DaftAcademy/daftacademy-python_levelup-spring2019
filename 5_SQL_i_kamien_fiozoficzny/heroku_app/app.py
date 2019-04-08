import os

from flask import Flask, abort, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import models
from models import Base

DATABASE_URL = os.environ['DATABASE_URL']

# engine = create_engine("postgresql://postgres:postgres@localhost:5432/chinook")
engine = create_engine(DATABASE_URL)

db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

Base.query = db_session.query_property()

app = Flask(__name__)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route("/artists", methods=["GET", "PATCH"])
def artists():
    if request.method == "GET":
        return get_artists()
    elif request.method == "PATCH":
        return patch_artist()
    abort(405)


def get_artists():
    artists = db_session.query(models.Artist).order_by(models.Artist.name)
    return "<br>".join(
        f"{idx}. {artist.name}" for idx, artist in enumerate(artists)
    )


# Aaron Goldberg , 202
def patch_artist():
    data = request.json
    artist_id = data.get("artist_id")
    new_name = data.get("name")
    if artist_id is None:
        abort(404)
    artist = (
        db_session.query(models.Artist)
        .filter(models.Artist.artist_id == artist_id)
        .with_for_update()
        .one()
    )
    artist.name = new_name
    db_session.add(artist)
    db_session.commit()
    return "OK"


@app.route("/albums")
def get_albums():
    albums = db_session.query(models.Album).order_by(models.Album.title)
    return render_template("albums.html", albums=albums)


@app.route("/playlists")
def get_playlists():
    playlists = db_session.query(models.Playlist).order_by(
        models.Playlist.name
    )
    return render_template("playlists.html", playlists=playlists)


if __name__ == "__main__":
    app.run(debug=False)
