# Instead of flask we use this streamlit
from http.client import responses

import streamlit as st
import pickle
import pandas as pd
import requests
import time
import random
import functools

# Your TMDB API Key (Replace with your actual key)
API_KEY = "your_actual_api_key_here"


# Function to fetch movie poster with error handling
@functools.lru_cache(maxsize=100)  # Cache up to 100 API responses
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"

    for attempt in range(5):  # Retry up to 5 times
        try:
            response = requests.get(url, timeout=5)  # Set a timeout for requests
            response.raise_for_status()  # Raise error for bad responses (e.g., 404, 500)

            data = response.json()
            if 'poster_path' in data and data['poster_path']:
                return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
            else:
                return "https://via.placeholder.com/500x750?text=No+Image+Available"

        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1}: API request failed - {e}")
            time.sleep(2)  # Wait 2 seconds before retrying

    return "https://via.placeholder.com/500x750?text=Image+Not+Available"


# Function to recommend movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)

        time.sleep(random.uniform(1, 3))  # Random delay between 1 to 3 seconds
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters


# Load movie data
with open('movie_dict.pkl', 'rb') as file:
    movies_dict = pickle.load(file)
movies = pd.DataFrame(movies_dict)

# Load similarity matrix
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.title("🎬 Movie Recommender System")

selected_movie_name = st.selectbox(
    '📌 Select a Movie:',
    movies['title'].values
)

if st.button('🔍 Recommend'):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)  # Create 5 columns for recommended movies
    for col, name, poster in zip(cols, names, posters):
        with col:
            st.image(poster, use_column_width=True)
            st.markdown(f"**{name}**")
