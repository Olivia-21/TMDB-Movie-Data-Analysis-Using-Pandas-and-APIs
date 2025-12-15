# extract.py
import os
from dotenv import load_dotenv
import requests
import pandas as pd
import time
import logging
load_dotenv()


API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3/movie/"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json;charset=utf-8"
}

def fetch_movie_details(movie_ids):
    # Fetch movie details from TMDB API.
    movies_data = []

    for movie_id in movie_ids:
        url = f"{BASE_URL}{movie_id}?append_to_response=credits"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            movies_data.append(response.json())
            print(f" Fetched movie ID {movie_id}")
        else:
            print(f"Failed to fetch movie ID {movie_id}: {response.status_code}")

    return pd.DataFrame(movies_data)


def extract():
     # extract function
    movie_ids = [
        0, 299534, 19995, 140607, 299536, 597, 135397,
        420818, 24428, 168259, 99861, 284054, 12445,
        181808, 330457, 351286, 109445, 321612, 260513
    ]

    df = fetch_movie_details(movie_ids)
    print(df)
    return df
if __name__ == "__main__":
    extract()