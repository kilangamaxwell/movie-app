import random
import codecs
import requests
from bs4 import BeautifulSoup
import html5lib
import movie_storage as ms

FILE_HTML = "_static/index_template.html"
MOVIE_HTML = "movies.html"
API_KEY = "d4ba49c2"
URL = f"http://www.omdbapi.com/?apikey={API_KEY}&t="


def find_imdb_link():
    """Retrieves link to imdb page for each movie."""
    url = 'https://imdb.com/chart/top'
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html5lib')
    movie_tags = soup.find_all('td', class_='titleColumn')
    movies_tl = []
    for tag in movie_tags:
        title = tag.find('a').text
        link = 'https://imdb.com' + tag.find('a')['href']
        movies_tl.append({
            'Title': title,
            'link': link
        })
    return movies_tl


def find_movie_in_api(title):
    """Retrieves movie info from the OMDB api."""
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


def read_html(html_file):
    """Reads a html file returns the data as a string."""
    with open(html_file, "r") as file:
        data = file.read()
    return data


def serialize_movie(movie_dict):
    """Provides template for serializing a movie object"""
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
            countries = movie_dict["Country"]
        output += '</div>\n'
    output += f'<div class="movie-title">{movie_dict["Title"]}</div>\n'
    output += f'<div class="movie-year">{movie_dict["Year"]}</div>\n'
    output += f'<div class="movie-rating">{movie_dict["Rating"]}</div>\n'
    output += '</div>\n</li>\n'
    return output


def display_movies():
    """Creates a string containing the title, rating,
      release year and poster
    derived from the api."""
    movies = ms.list_movies()
    # define an empty string
    output = ""
    # serialize animal objects
    for movie in movies:
        output += serialize_movie(movie)
    return output


def my_moviesDB():
    """Application's control Interface that allows user
      selection of operations to run"""

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
    while choice not in choice_dict.keys():
        print(selections)
        choice = input("Enter choice (0-9): ")
    choice_dict[choice]()


def list_movies():
    """Displays the list of movies"""
    movies = ms.list_movies()
    print()
    print(f"{len(movies)} movies in total")
    for movie in movies:
        print(f"{movie['Title']}: {movie['Rating']}")
    con = input("""
  Press enter to continue: """)
    my_moviesDB()


def add_movie():
    """
    Adds a movie to the movies database.
    Loads the information from the JSON file, add the movie,
    and saves it.
    """
    movies = ms.list_movies()
    title = input("Enter new movie name: ")
    for movie in movies:
        if title in movie.values():
            print(f"Error: The movie {title} already exists in the database.")
            add_movie()
    data = find_movie_in_api(title)
    if data is None:
        print("Failed to retrieve movie information from the OMDB API.")
        return_to_menu()

    movies_tl = find_imdb_link()
    imdbLink = ""
    if 'Country' in data:
        if data['Country'].__contains__(","):
            country = data['Country'].split(",")
        else:
            country = [data['Country']]
    else:
        country = []

    for mvs in movies_tl:
        if title in mvs['Title']:
            imdbLink = mvs['link']
    if 'Title' in data:
        if len(imdbLink) > 0:
            movies.append({
                'Title': data['Title'],
                'Rating': data['imdbRating'],
                'Year': data['Year'],
                'Poster': data['Poster'],
                'imdb Link': imdbLink,
                'Notes': [data['Plot']],
                'Country': country
            })
            ms.save_db(movies)
            print(f"Movie {title} successfully added")
        else:
            print("Movie not in imdb top 250")
            movies.append({
                'Title': data['Title'],
                'Rating': data['imdbRating'],
                'Year': data['Year'],
                'Poster': data['Poster'],
                'Country': country
            })
            ms.save_db(movies)
            print(f"Movie {title} successfully added")
    else:
        print("Failed to retrieve movie information from the OMDB API.")
    print(" ")
    con = input("Press enter to continue: ")
    my_moviesDB()


def del_movie():
    """
    Deletes a movie from the movies database.
    Loads the information from the JSON file, deletes the movie,
    and saves it.
    """
    title = input("Enter movie name to delete: ")
    movies = list_movies()
    s = 0
    for movie in movies:
        if movie['Title'] == title:
            movies.remove(movie)
            s = ms.save_db(movies)
    if s == 1:
        print(f"Movie {title} was successfully deleted.")
    else:
        print(f"Movie {title} doesn't exist!")
    return_to_menu()


def update_movie():
    """
    Updates notes about a movie in the database.
    Loads the information from the JSON file, updates the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = ms.list_movies()
    title = input("Enter movie name: ")
    # checks if movie exists in dictionary
    for movie in movies:
        if movie['Title'] == title:
            notes_lst = []
            notes = input("Enter movie notes: ")
            notes_lst.append(notes)
            movie['Notes'] = notes_lst
            s = ms.save_db(movies)
            if s == 1:
                print(f"Movie {title} successfully updated")
            else:
                print(f"Movie {movies} doesn't exist!")
    return_to_menu()


def return_to_menu():
    """Returns the app to the menu of operations"""
    print(" ")
    con = input("Press enter to continue: ")
    my_moviesDB()


def check_stats():
    """Displays movie stats based on the ratings"""
    movies_lst = ms.list_movies()
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
    return_to_menu()


def random_movie():
    """selects a random movie from list of movies' dictionaries"""
    movies_lst = ms.list_movies()
    rand_movie = random.choice(movies_lst)
    print(
        f"Your movie for tonight: {rand_movie['Title']}, it's rated {rand_movie['Rating']}")
    return_to_menu()


def search_movie():
    """searches for movie titles using full title or substrings"""
    movies_lst = ms.list_movies()
    movie_name = input("Enter part of movie name: ").lower()
    for i in range(len(movies_lst)):
        name = movies_lst[i]['Title'].lower()
        rating = movies_lst[i]['Rating']
        if name.__contains__(movie_name):
            print(f"{movies_lst[i]['Title']}, {rating}")
    return_to_menu()


def sort_by_rating():
    """Sorts movie titles based on ratings in descending order"""
    movies_lst = ms.list_movies()
    movies_lst = sorted(movies_lst, key=lambda x: x['Rating'], reverse=True)
    for movie in movies_lst:
        print(movie['Title'], movie['Rating'])
    return_to_menu()


def exit_movies():
    """Exits the application"""
    print("Bye!")


def generate_website():
    """Generates website from list of movies in the database."""
    html_data = read_html(FILE_HTML)
    # replace text placeholder with json data
    html_data = html_data.replace("__TEMPLATE_TITLE__", "OMDB Movie App")
    html_data = html_data.replace("__TEMPLATE_MOVIE_GRID__", display_movies())
    # write html_data to a new file
    with codecs.open(MOVIE_HTML, "w", encoding="utf-8") as file:
        file.write(html_data)
    print("Website was generated successfully.")
    return_to_menu()


"""Dispatcher dictionary for running all functions"""
choice_dict = {
    "0": exit_movies,
    "1": list_movies,
    "2": add_movie,
    "3": del_movie,
    "4": update_movie,
    "5": check_stats,
    "6": random_movie,
    "7": search_movie,
    "8": sort_by_rating,
    "9": generate_website
}


def main():
    my_moviesDB()


if __name__ == "__main__":
    main()
