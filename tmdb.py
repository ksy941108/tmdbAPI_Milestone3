import os
import requests
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

def movie_info(ids):

    movie_id = ids

    BASE_URL = "https://api.themoviedb.org/3/movie/{0}?response".format(movie_id)
    
    query_params = {
        "api_key": os.getenv("TMDB_KEY"),
    }

    response = requests.get(
        BASE_URL,
        params = query_params
    )
    
    jason = response.json()
    title = jason["title"]
    tagline = jason["tagline"]
    genre = jason["genres"][0]["name"]
    posterImg = jason["poster_path"]

    return title, tagline, genre, posterImg