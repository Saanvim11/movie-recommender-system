import streamlit as st
import pickle
import pandas as pd
import requests
import os
import gdown

# Google Drive file IDs for large pickle files
movies_dict_id = '1QWMYBbLqqA3eojJ1EqHXJ5OnY1dN6QIL'
similarity_id = '12k93xi1Ys_Wi3fcMPJ4qxB6ADoaCRuU3'

# Function to download a file if it's not already present
def download_file(file_id, output):
    if not os.path.exists(output):
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, output, quiet=False)

# Download model files
with st.spinner("Downloading model files..."):
    download_file(movies_dict_id, 'movies_dict.pkl')
    download_file(similarity_id, 'similarity.pkl')

# Load the model data
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# TMDB API Key
API_KEY = 'bf660f694cf51e95d19a22c3bc4e25ea'

# Function to fetch poster using TMDB API
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
        data = requests.get(url)
        data.raise_for_status()
        poster_path = data.json().get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/150x200?text=No+Poster"
    except Exception:
        return "https://via.placeholder.com/150x200?text=Error"

# Movie recommendation logic
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_posters

# Streamlit UI
st.title('🎬 Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie to get recommendations',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
