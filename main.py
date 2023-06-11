import json
from movie_app import MovieApp
from storage_json import StorageJson
from storage_csv import StorageCsv

JSON_FILE = "masterschool\movie-app\OMDB_movies.json"
CSV_FILE = "masterschool\movie-app\movies.csv"


def main():
    """Defines the entry point of the app."""
    storage = StorageCsv(CSV_FILE)
    movie_app = MovieApp(storage)
    movie_app.run()


if __name__ == "__main__":
    main()
