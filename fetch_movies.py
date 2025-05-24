import requests

TMDB_API_KEY = "d3b7ed8dbc4cfb159498d11c18b247b4"

def fetch_single_movie_with_genres(movie_name):
    """
    Fetch movie info from TMDB API including genres and poster path.
    Returns a dict with title, overview, list of genres, and poster_path.
    """
    search_url = f"https://api.themoviedb.org/3/search/movie?query={movie_name}&api_key={TMDB_API_KEY}"
    response = requests.get(search_url)
    data = response.json()

    if not data.get('results'):
        return None

    movie = data['results'][0]
    movie_id = movie['id']

    details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}"
    details_response = requests.get(details_url)
    details_data = details_response.json()
    
    genres = [genre['name'] for genre in details_data.get('genres', [])]
    poster_path = details_data.get('poster_path')  # This is just the path, not full URL

    return {
        "title": movie['title'],
        "overview": movie['overview'],
        "genres": genres,
        "poster_path": poster_path
    }
