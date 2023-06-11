from abc import ABC, abstractmethod


class IStorage(ABC):
    @abstractmethod
    def list_movies(self):
        """
        Abstract method to list all movies.

        Returns:
            list: List of movie objects.
        """
        pass

    @abstractmethod
    def add_movie(self, title, year, rating, poster):
        """
        Abstract method to add a new movie.

        Args:
            title (str): The title of the movie.
            year (int): The year of release.
            rating (float): The rating of the movie.
            poster (str): The URL of the movie poster.
        """
        pass

    @abstractmethod
    def delete_movie(self, title):
        """
        Abstract method to delete a movie.

        Args:
            title (str): The title of the movie to be deleted.
        """
        pass

    @abstractmethod
    def update_movie(self, title, notes):
        """
        Abstract method to update movie notes.

        Args:
            title (str): The title of the movie to be updated.
            notes (str): The notes to be updated for the movie.
        """
        pass
