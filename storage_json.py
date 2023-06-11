from istorage import IStorage
import json


class StorageJson(IStorage):
    def __init__(self, file_path):
        """
        Initializes a StorageJson instance.

        Args:
            file_path (str): The path to the JSON file used for storage.
        """
        self.file_path = file_path

    def save_db(self, movies):
        """Saves the list of movies to a json file."""
        saved = 0
        moviesdb = json.dumps(movies)
        with open(self.file_path, "w") as jfile:
            jfile.write(moviesdb)
            saved = 1
        return saved

    def list_movies(self):
        """
        Retrieves the list of movies from the JSON storage.

        Returns:
            list: List of movie objects.
        """
        with open(self.file_path, "r") as jfile:
            movies_lst = json.load(jfile)
        return movies_lst

    def add_movie(self, title, rating, year, poster):
        """
        Adds a new movie to the JSON storage.

        Args:
            title (str): The title of the movie.
            year (int): The year of release.
            rating (float): The rating of the movie.
            poster (str): The URL of the movie poster.
        """
        movies = self.list_movies()
        movies.append({
            'Title': title,
            'Rating': rating,
            'Year': year,
            'Poster': poster
        })
        try:
            self.save_db(movies)
            print(f"Movie {title} was successfully Added!")
        except Exception as error:
            print("Failed to save to file.", str(error))

    def delete_movie(self, title):
        """
        Deletes a movie from the JSON storage.

        Args:
            title (str): The title of the movie to be deleted.
        """
        movies = self.list_movies()
        s = 0
        for movie in movies:
            if movie['Title'] == title:
                movies.remove(movie)
                s = self.save_db(movies)
        if s == 1:
            print(f"Movie {title} was successfully deleted.")
        else:
            print(f"Movie {title} doesn't exist!")

    def update_movie(self, title, notes):
        """
        Updates movie notes in the JSON storage.

        Args:
            title (str): The title of the movie to be updated.
            notes (str): The notes to be updated for the movie.
        """
        movies = self.list_movies()
        for movie in movies:
            if movie['Title'] == title:
                notes_lst = []
                notes_lst.append(notes)
                movie['Notes'] = notes_lst
                s = self.save_db(movies)
                if s == 1:
                    print(f"Movie {title} successfully updated")
                else:
                    print(f"Movie {movies} doesn't exist!")
