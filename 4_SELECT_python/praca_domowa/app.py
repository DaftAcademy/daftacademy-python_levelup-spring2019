import sqlite3

from flask import Flask, g, request, jsonify
from wtforms import Form, StringField, validators, IntegerField

DATABASE = "database.db"


# look: http://flask.pocoo.org/docs/1.0/patterns/appfactories/
def create_app(config=None):
    app = Flask(__name__)

    # look: http://flask.pocoo.org/docs/1.0/patterns/sqlite3/
    def get_db():
        db = getattr(g, "_database", None)
        if db is None:
            db = g.db = sqlite3.connect(DATABASE)
        return db

    @app.teardown_appcontext
    def close_connection(exception):
        db = getattr(g, "_database", None)
        if db is not None:
            db.close()

    # look: http://flask.pocoo.org/docs/1.0/patterns/apierrors/
    class InvalidUsage(Exception):
        status_code = 400

        def __init__(self, error, status_code=None, payload=None):
            super().__init__(self)
            self.error = error
            if status_code is not None:
                self.status_code = status_code
            self.payload = payload

        def to_dict(self):
            rv = dict(self.payload or ())
            rv["error"] = self.error
            return rv

    @app.errorhandler(InvalidUsage)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.route("/tracks", methods=["GET", "POST"])
    def tracks():
        if request.method == "GET":
            return get_tracks()
        else:
            return post_new_track()

    # https://wtforms.readthedocs.io/en/stable/
    class TracksValidationForm(Form):
        artist = StringField(validators=[validators.optional()])
        per_page = IntegerField(
            validators=[validators.optional(), validators.number_range(min=1)]
        )
        page = IntegerField(
            validators=[validators.optional(), validators.number_range(min=1)]
        )

    def get_tracks():
        db = get_db()

        form = TracksValidationForm(request.args)

        if not form.validate():
            return jsonify(error=form.errors)

        per_page = form.data["per_page"] or -1
        limit = per_page

        page = form.data["page"] or 1
        page_index = page - 1
        offset = page_index * per_page

        tracks_rows = []

        if form.data["artist"]:
            tracks_rows = db.execute(
                "SELECT tracks.name FROM tracks "
                "JOIN albums ON tracks.AlbumId = albums.AlbumId "
                "JOIN artists ON albums.ArtistId = artists.ArtistId "
                "WHERE artists.Name = ? "
                "ORDER BY tracks.name COLLATE NOCASE "
                "LIMIT ? OFFSET ?;",
                (form.data["artist"], limit, offset),
            )
        else:
            tracks_rows = db.execute(
                "SELECT name FROM tracks "
                "ORDER BY name COLLATE NOCASE "
                "LIMIT ? OFFSET ?;",
                (limit, offset),
            )
        return jsonify([row[0] for row in tracks_rows.fetchall()])

    def post_new_track():
        db = get_db()

        new_track = request.get_json()
        if not new_track:
            raise InvalidUsage("JSON data are not provided")

        # Check if all required parameters are provided
        required_fields = (
            "album_id",
            "bytes",
            "composer",
            "genre_id",
            "media_type_id",
            "milliseconds",
            "name",
            "price",
        )
        missing_fields = set(required_fields) - new_track.keys()

        if missing_fields:
            raise InvalidUsage("missing fields: {}".format(missing_fields))

        album_id = new_track["album_id"]
        media_type_id = new_track["media_type_id"]
        genre_id = new_track["genre_id"]
        name = new_track["name"]
        composer = new_track["composer"]
        milliseconds = new_track["milliseconds"]
        track_bytes = new_track["bytes"]
        price = new_track["price"]

        try:
            db.execute(
                "INSERT INTO tracks "
                "(AlbumId, Bytes, Composer, GenreId, MediaTypeId, "
                "Milliseconds, Name, UnitPrice) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?);",
                (
                    album_id,
                    track_bytes,
                    composer,
                    genre_id,
                    media_type_id,
                    milliseconds,
                    name,
                    price,
                ),
            )
            db.commit()
        except sqlite3.IntegrityError as error:
            db.rollback()
            error_reason = error.args[0]

            if error_reason.startswith("FOREIGN KEY constraint failed"):
                raise InvalidUsage("Integrity error.")

            raise error

        db_track = db.execute(
            "SELECT TrackId, AlbumId, Bytes, Composer, GenreId, MediaTypeId, "
            "Milliseconds, Name, UnitPrice "
            "FROM tracks "
            "WHERE  name = ? AND AlbumId = ?",
            (name, album_id),
        ).fetchone()

        fields = ("track_id", ) + required_fields
        return jsonify(dict(zip(fields, db_track)))

    @app.route("/genres")
    def genres():
        db = get_db()
        # Only INNER JOIN or LEFT JOIN sqlite.
        genres_rows = db.execute(
            "SELECT genres.name, COUNT(tracks.TrackId) "
            "FROM genres "
            "LEFT JOIN tracks ON genres.GenreId = tracks.GenreId "
            "GROUP BY genres.name;"
        ).fetchall()
        return jsonify(dict(genres_rows))

    return app


if __name__ == "__main__":
    create_app().run(debug=True, use_debugger=False)
