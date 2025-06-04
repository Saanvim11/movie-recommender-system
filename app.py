# import streamlit as st
# import pickle
# import pandas  as pd
# import requests
# from requests.adapters import HTTPAdapter
# from requests.packages.urllib3.util.retry import Retry
#
# session = requests.Session()
# retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
# session.mount('https://', HTTPAdapter(max_retries=retries))
#
# def fetch_poster(movie_id):
#     headers = {
#         "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzZGYzZjEyYTE4ZDJiZGVmZmYwODdmNDFjN2RhNWM5NSIsIm5iZiI6MTc0OTAyODA0OC4yNjgsInN1YiI6IjY4NDAwY2QwZmZmYmQwYTJiZjdmNGU1YiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.-U2NB2vvX08p5RFkr7O_brNyS8bJuzpJncEN3ip5Vlg",
#         "accept": "application/json"
#     }
#     url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
#     response = session.get(url, headers=headers)
#     data=response.json()
#     return "https://image.tmdb.org/t/p/w500/"+data['poster_path']
#
# def recommend(movie):
#     movie_index = movies[movies['title'] == movie].index[0]
#     distances = similarity[movie_index]
#     movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
#
#     recommended_movies=[]
#     recommended_movies_posters=[]
#     for i in movies_list:
#         movie_id=movies.iloc[i[0]].movie_id
#         recommended_movies.append(movies.iloc[i[0]].title)
#         recommended_movies_posters.append(fetch_poster(movie_id))
#     return recommended_movies, recommended_movies_posters
#
#
# movies_dict=pickle.load(open('movies_dict.pkl','rb'))
# movies=pd.DataFrame(movies_dict)
#
# similarity=pickle.load(open('similarity.pkl','rb'))
#
# st.title('Movie Recommender System')
#
# selected_movie_name = st.selectbox(
#     'Select a movie to get recommendations',
#     movies['title'].values)
# if st.button('Recommend'):
#     names,posters=recommend(selected_movie_name)
#     col1,col2,col3,col4,col5=st.columns(5)
#     with col1:
#         st.text(names[0])
#         st.image(posters[0])
#     with col2:
#         st.text(names[1])
#         st.image(posters[1])
#     with col3:
#         st.text(names[2])
#         st.image(posters[2])
#     with col4:
#         st.text(names[3])
#         st.image(posters[3])
#     with col5:
#         st.text(names[4])
#         st.image(posters[4])
import streamlit as st
import pickle
import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Setup session with retries
session = requests.Session()
retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
session.mount('https://', HTTPAdapter(max_retries=retries))

# Safe poster fetch function
def fetch_poster(movie_id):
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzZGYzZjEyYTE4ZDJiZGVmZmYwODdmNDFjN2RhNWM5NSIsIm5iZiI6MTc0OTAyODA0OC4yNjgsInN1YiI6IjY4NDAwY2QwZmZmYmQwYTJiZjdmNGU1YiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.-U2NB2vvX08p5RFkr7O_brNyS8bJuzpJncEN3ip5Vlg",
        "accept": "application/json"
    }
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"

    try:
        response = session.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
        else:
            return "https://via.placeholder.com/500x750.png?text=No+Poster"
    except Exception as e:
        print(f"Error fetching poster for movie_id {movie_id}: {e}")
        return "https://via.placeholder.com/500x750.png?text=Error"

# Recommend movies based on similarity
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# Load data
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.title('🎬 Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie to get recommendations',
    movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.text(names[idx])
            st.image(posters[idx])
