import json
from movie_app import MovieApp
from storage_json import StorageJson

JSON_FILE = "masterschool\movie-app\OMDB_movies.json"


def main():
    """Defines the entry point of the app."""
    storage = StorageJson(JSON_FILE)
    movie_app = MovieApp(storage)
    movie_app.run()


if __name__ == "__main__":
    main()
