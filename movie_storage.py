import json

JSON_FILE = "OMDB_movies.json"


def list_movies():
    """
    Returns a dictionary of dictionaries that
    contains the movies information in the database.

    The function loads the information from the JSON
    file and returns the data. 

    For example, the function may return:
    {
      "Titanic": {
        "rating": 9,
        "year": 1999
      },
      "..." {
        ...
      },
    }
    """
    with open(JSON_FILE, "r") as jfile:
        movies_lst = json.load(jfile)
    return movies_lst


def save_db(movies):
    """Saves the list of movies to a json file."""
    saved = 0
    moviesdb = json.dumps(movies)
    with open(JSON_FILE, "w") as jfile:
        jfile.write(moviesdb)
        saved = 1
    return saved
