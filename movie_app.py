import random
import codecs
import requests
import json

FILE_HTML = "masterschool\movie-app\_static\index_template.html"
MOVIE_HTML = "masterschool\movie-app\movies.html"
API_KEY = "d4ba49c2"
JSON_FILE = "masterschool\movie-app\OMDB_movies.json"
URL = f"http://www.omdbapi.com/?apikey={API_KEY}&t="


class MovieApp:
    def __init__(self, storage):
        """Initialize the MovieApp with a storage object.

        Args:
            storage (object): The storage object used to interact with the movie database.
        """
        self._storage = storage

    def selections_dispatch(self):
        """Get the dispatcher dictionary for running all functions.

        Returns:
            dict: The dictionary mapping user choices to corresponding methods.
        """
        choice_dict = {
            "0": self.exit_movies,
            "1": self._command_list_movies,
            "2": self._command_add_movie,
            "3": self._command_delete_movie,
            "4": self._command_update_movie,
            "5": self._command_movie_stats,
            "6": self._command_random_movie,
            "7": self._command_search_movie,
            "8": self._command_sort_by_rating,
            "9": self._generate_website
        }
        return choice_dict

    def find_movie_in_api(self, title):
        """Retrieve movie info from the OMDB API.

        Args:
            title (str): The title of the movie to search for.

        Returns:
            dict: The movie data retrieved from the API as a dictionary.
        """
        response = requests.get(URL+title)
        try:
            response = requests.get(URL+title)
            response.raise_for_status()  # Raises an HTTPError for 4xx and 5xx status codes
        except requests.exceptions.HTTPError as errh:
            print("HTTP Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("Something went wrong:", err)
        if response.status_code == requests.codes.ok:
            data = response.json()
        return data

    def run(self):
        """Run the MovieApp's control interface that allows user selection of operations to run."""
        selections = """
        ********** My Movies Database **********

        Menu:
        0. Exit
        1. List movies
        2. Add movie
        3. Delete movie
        4. Update movie
        5. Stats
        6. Random movie
        7. Search movie
        8. Movies sorted by rating
        9. Generate Website

        """
        print(selections)
        choice = input("Enter choice (0-9): ")
        dispatch = self.selections_dispatch()
        while choice not in dispatch.keys():
            print(selections)
            choice = input("Enter choice (0-9): ")
        return dispatch[choice]()

    def return_to_menu(self):
        """Return the app to the menu of operations"""
        print(" ")
        con = input("Press enter to continue: ")
        self.run()

    def _command_list_movies(self):
        """Display the list of movies"""
        movies = self._storage.list_movies()
        print()
        print(f"{len(movies)} movies in total")
        for movie in movies:
            print(f"{movie['Title']}: {movie['Rating']}")
        con = input("""
    Press enter to continue: """)
        self.run()

    def _command_add_movie(self):
        """
        Add a movie to the movies database.

        Loads the information from the file, add the movie, and saves it.
        """
        movies = self._storage.list_movies()
        title = input("Enter new movie name: ")
        year = ""
        rating = ""
        poster = ""
        for movie in movies:
            if title in movie.values():
                print(
                    f"Error: The movie {title} already exists in the database.")
                self._command_add_movie()
        data = self.find_movie_in_api(title)
        if data is None:
            print("Failed to retrieve movie information from the OMDB API.")
            self.return_to_menu()
        if 'Title' in data:
            title = data['Title']
            rating = data['imdbRating']
            year = data['Year']
            poster = data['Poster']
            self._storage.add_movie(title, rating, year, poster)
        else:
            print("Failed to retrieve movie information from the OMDB API.")
        self.return_to_menu()

    def _command_delete_movie(self):
        """
        Delete a movie from the movies database.

        Loads the information from the file, deletes the movie, and saves it.
        """
        title = input("Enter movie name to delete: ")
        self._storage.delete_movie(title)
        self.return_to_menu()

    def _command_update_movie(self):
        """
        Update notes about a movie in the database.

        Loads the information from file, updates the movie, and saves it.
        """
        movies = self._storage.list_movies()
        title = input("Enter movie name: ")
        notes = input("Enter movie notes: ")
        self._storage.update_movie(title, notes)
        self.return_to_menu()

    def _command_movie_stats(self):
        """Display movie stats based on the ratings"""
        movies_lst = self._storage.list_movies()
        avg_rating = 0
        sum_rating = 0
        median_rating = 0
        sorted_val = []
        movie_ratings = []
        # calculates the average rating
        for movie in movies_lst:
            movie_ratings.append(float(movie['Rating']))
            sum_rating += float(movie['Rating'])
        avg_rating = sum_rating / len(movies_lst)
        sorted_val = sorted(movie_ratings)
        length = len(sorted_val)
        # for lists with an even number of items
        if length % 2 == 0:
            a = sorted_val[length // 2]
            b = sorted_val[(length//2) - 1]
            c = (a + b) / 2
            median_rating = c
        # for lists with an odd number of items
        if length % 2 > 0:
            median_rating = sorted_val[length//2]
        # evaluates max and min ratings to determine best/worst movie
        best_movie = ""
        worst_movie = ""
        best = max(movie_ratings)
        worst = min(movie_ratings)
        for movie in movies_lst:
            if float(movie['Rating']) == best:
                best_movie = movie['Title']
            if float(movie['Rating']) == worst:
                worst_movie = movie['Title']
        # displays summary of stats
        print(f"Average rating: {avg_rating}")
        print(f"Median rating: {median_rating}")
        print(f"Best movie: {best_movie}")
        print(f"Worst movie: {worst_movie}")
        self.return_to_menu()

    def _command_random_movie(self):
        """Select a random movie from the list of movies' dictionaries"""
        movies_lst = self._storage.list_movies()
        rand_movie = random.choice(movies_lst)
        print(
            f"Your movie for tonight: {rand_movie['Title']}, it's rated {rand_movie['Rating']}")
        self.return_to_menu(self)

    def _command_search_movie(self):
        """Search for movie titles using full title or substrings"""
        movies_lst = self._storage.list_movies()
        movie_name = input("Enter part of movie name: ").lower()
        for i in range(len(movies_lst)):
            name = movies_lst[i]['Title'].lower()
            rating = movies_lst[i]['Rating']
            if name.__contains__(movie_name):
                print(f"{movies_lst[i]['Title']}, {rating}")
        self.return_to_menu()

    def _command_sort_by_rating(self):
        """Sort movie titles based on ratings in descending order"""
        movies_lst = self._storage.list_movies()
        movies_lst = sorted(
            movies_lst, key=lambda x: x['Rating'], reverse=True)
        for movie in movies_lst:
            print(movie['Title'], movie['Rating'])
        self.return_to_menu()

    def exit_movies(self):
        """Exit the application"""
        print("Bye!")

    def read_html(self, html_file):
        """Read a html file and return the data as a string."""
        with open(html_file, "r") as file:
            data = file.read()
        return data

    def serialize_movie(self, movie_dict):
        """Provide a template for serializing a movie object"""
        output = ''
        output += '<li>\n<div class="movie">\n'
        if "imdb Link" in movie_dict:
            output += f'<a href="{movie_dict["imdb Link"]}" target="_blank">\n'
            output += f'<img class="movie-poster"\n'
            output += f'src="{movie_dict["Poster"]}"\ntitle=""/></a>\n'
        else:
            output += '<img class="movie-poster"\n'
            output += f'src="{movie_dict["Poster"]}"\ntitle=""/>\n'
        if "Notes" in movie_dict:
            output += '<div class="movie-notes-box">'
            for notes in movie_dict["Notes"]:
                output += f'<p>{notes}</p>\n'
            output += '</div>\n'
        output += f'<div class="movie-title">{movie_dict["Title"]}</div>\n'
        output += f'<div class="movie-year">{movie_dict["Year"]}</div>\n'
        output += f'<div class="movie-rating">{movie_dict["Rating"]}</div>\n'
        output += '</div>\n</li>\n'
        return output

    def display_movies(self):
        """Create a string containing the title, rating,
        release year, and poster derived from the API."""
        movies = self._storage.list_movies()
        # Define an empty string
        output = ""
        # Serialize movie objects
        for movie in movies:
            output += self.serialize_movie(movie)
        return output

    def _generate_website(self):
        """Generate a website from the list of movies in the database."""
        html_data = self.read_html(FILE_HTML)
        # Replace text placeholder with JSON data
        html_data = html_data.replace("__TEMPLATE_TITLE__", "OMDB Movie App")
        html_data = html_data.replace(
            "__TEMPLATE_MOVIE_GRID__", self.display_movies())
        # Write html_data to a new file
        with codecs.open(MOVIE_HTML, "w", encoding="utf-8") as file:
            file.write(html_data)
        print("Website was generated successfully.")
        self.return_to_menu()
