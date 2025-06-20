<h1>Recommendation System :</h1>
<p><strong>Recommendation Systems</strong> are machine learning algorithms that use data to recommend items or content to users based on their preferences, past behavior, or their combination. These systems can recommend various items, such as movies, books, music, products, etc.</p>

<h2>Types of Recommendation Systems:</h2>
<pre>
  Collaborative filtering
  Content-based filtering
  Hybrid recommendation systems
</pre>

<h3>Collaborative filtering:</h3>
<p>In this scenario, the emphasis is placed on customers and their experiences with the online platform and their opinions on products instead of the features of the items themselves. As a result, recommendation systems falling under this category leverage machine learning algorithms to gather feedback from users and comprehend what they prefer. This enables the system to suggest products other users with similar preferences purchase.</p>

<h3>Content-based filtering:</h3>
<p>Content-based filtering in recommender systems recommends items to users based on their previous actions or preferences. It analyzes item metadata to identify items with similar characteristics to those that the user has interacted with before. This approach examines the characteristics of the items users have expressed an interest in to recommend similar items, unlike collaborative filtering, which finds similarities among users. Content-based filtering is widely used in e-commerce, news feeds, music, and movie recommendations.</p>

<h3>Hybrid recommendation systems:</h3>
<p>Hybrid recommendation systems combine two or more recommendation strategies in different ways to leverage their complementary strengths.</p>

<hr>

<h2>🎬 Movie Recommendation System using Streamlit</h2>
<p>This project is a simple content-based movie recommendation system that uses movie metadata and similarity scores to suggest similar movies based on a user's selection.</p>

<h3>💻 Technologies Used:</h3>
<ul>
  <li>Python</li>
  <li>Streamlit</li>
  <li>Pandas</li>
  <li>Pickle</li>
  <li>Requests (API)</li>
  <li>TMDB (The Movie Database API)</li>
</ul>

<h3>🧠 How It Works:</h3>
<ol>
  <li>User selects a movie from a dropdown menu</li>
  <li>The system uses a similarity matrix to find the most similar movies</li>
  <li>TMDB API is used to fetch posters of the recommended movies</li>
  <li>Recommended movie titles and posters are displayed in a clean layout</li>
</ol>

<h3>🗂 Project Files:</h3>
<ul>
  <li><code>app.py</code> – Main Streamlit application</li>
  <li><code>movie_dict.pkl</code>, <code>similarity.pkl</code> – Preprocessed data files</li>
  <li><code>Procfile</code> & <code>setup.sh</code> – For deployment (e.g., on Heroku or Streamlit Cloud)</li>
  <li><code>requirements.txt</code> – Python dependencies</li>
</ul>

<h3>📄 Sample Code (app.py):</h3>
<pre><code>
import streamlit as st
import pickle
import pandas as pd
import requests
import time
import random
import functools

API_KEY = "your_actual_api_key_here"

@functools.lru_cache(maxsize=100)
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
    for attempt in range(5):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            if 'poster_path' in data and data['poster_path']:
                return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
            else:
                return "https://via.placeholder.com/500x750?text=No+Image+Available"
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1}: API request failed - {e}")
            time.sleep(2)
    return "https://via.placeholder.com/500x750?text=Image+Not+Available"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        time.sleep(random.uniform(1, 3))
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

movies = pd.DataFrame(pickle.load(open('movie_dict.pkl', 'rb')))
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title("🎬 Movie Recommender System")

selected_movie_name = st.selectbox('📌 Select a Movie:', movies['title'].values)

if st.button('🔍 Recommend'):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(5)
    for col, name, poster in zip(cols, names, posters):
        with col:
            st.image(poster, use_column_width=True)
            st.markdown(f"**{name}**")
</code></pre>


<h3>🧾 requirements.txt:</h3>
<pre><code>
streamlit
requests
pandas
</code></pre>

<h3>📌 Note:</h3>
<ul>
  <li>Make sure to replace <code>your_actual_api_key_here</code> in <code>app.py</code> with your valid TMDB API Key.</li>
  <li>All `.pkl` files must be in the same directory as <code>app.py</code>.</li>
</ul>

<h3>📎 GitHub Repository:</h3>
<p><a href="https://github.com/asim-kazi/Python_Projects/tree/main/Movie_Recommendation_System" target="_blank">https://github.com/asim-kazi/Python_Projects/tree/main/Movie_Recommendation_System</a></p>

<hr>
