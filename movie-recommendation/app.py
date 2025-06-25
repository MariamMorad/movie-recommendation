import streamlit as st
import pickle
import requests
import random

movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
m = movies["title"].values

st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .movie-title {
        font-size: 20px;
        font-weight: bold;
        text-align: center;
    }
    .movie-poster {
        width: 200px;
        height: 300px;
        object-fit: cover;
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    </style>
""", unsafe_allow_html=True)

st.header("Movie Recommender System 🎬")

selectvalue = st.selectbox("🎬 Select a movie", m)

if st.button("🎲 Suggest Random Movie"):
    selectvalue = random.choice(list(movies['title'].values))
    st.success(f"Suggested movie: {selectvalue}")

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path', '')
    rating = data.get('vote_average', 'N/A')
    overview = data.get('overview', 'No description available.')
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path if poster_path else ""
    return full_path, rating, overview

def recommend(movie):
    index = movies[movies["title"] == movie].index[0]
    listed = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda i: i[1])
    recommend_movie = []
    recommend_poster = []
    recommend_rating = []
    recommend_overview = []
    for i in listed[1:6]:
        movie_id = movies.iloc[i[0]].id
        title = movies.iloc[i[0]].title
        poster, rating, overview = fetch_poster(movie_id)
        recommend_movie.append(title)
        recommend_poster.append(poster)
        recommend_rating.append(rating)
        recommend_overview.append(overview)
    return recommend_movie, recommend_poster, recommend_rating, recommend_overview


if st.button("✨ Show Recommendations"):
    movie_name, movie_poster, movie_rating, movie_overview = recommend(selectvalue)
    col1, col2, col3, col4, col5 = st.columns(5)

    for idx, col in enumerate([col1, col2, col3, col4, col5]):
        with col:
            st.markdown(f"<div class='movie-title'>{movie_name[idx]}</div>", unsafe_allow_html=True)
            st.markdown(f"<img src='{movie_poster[idx]}' class='movie-poster'>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align:center;'>⭐ {movie_rating[idx]}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size:13px;text-align:center;'>{movie_overview[idx][:100]}...</p>", unsafe_allow_html=True)
