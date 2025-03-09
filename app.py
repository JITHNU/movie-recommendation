import streamlit as st
import pickle
import pandas as pd
import requests 
import gdown

file_id = "16JwirbTk4hmyKe_fZegihJfogWJvC61v"
similarity_url = f"https://drive.google.com/uc?id={file_id}"

output = "similarity.pkl"
gdown.download(similarity_url, output, quiet=False)


movies_dict = pickle.load(open("movies.pkl", "rb"))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open("similarity.pkl", "rb"))

API_KEY="170e014ded60aab751346907ae5ca08a"

theme = st.sidebar.radio("Choose Theme", ["Light 🌞", "Dark 🌙"])


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if "poster_path" in data and data["poster_path"]:
        return f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
    return None  

def fetch_trailer(movie_id):
    trailer_url = None
    video_url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={API_KEY}"
    video_data = requests.get(video_url).json()
    
    for video in video_data.get("results", []):
        if video["type"] == "Trailer" and video["site"] == "YouTube":
            trailer_url = f"https://www.youtube.com/watch?v={video['key']}"
            break
    return trailer_url


def recommend(movie):

    if movie not in movies['title'].values:
        return[]
    index = movies[movies["title"] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movies = []
    recommended_posters = []
    recommended_trailers = []

    for i in distances[1:6]:  
        movie_id = movies.iloc[i[0]].movie_id  
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
        recommended_trailers.append(fetch_trailer(movie_id))
    
    sorted_recommended_movies = sorted(recommended_movies)
    sorted_recommended_posters = [recommended_posters[recommended_movies.index(movie)] for movie in sorted_recommended_movies]
    sorted_recommended_trailers = [recommended_trailers[recommended_movies.index(movie)] for movie in sorted_recommended_movies]

    return sorted_recommended_movies, sorted_recommended_posters,sorted_recommended_trailers

st.header("🎬 Movie Recommendation System")
movies_list = movies["title"].values
selectvalue = st.selectbox("Select a movie from dropdown", movies_list)

if st.button("Show Recommendations"):
    recommended_movies, recommended_posters,recommended_trailers = recommend(selectvalue)

    col1,col2,col3,col4,col5=st.columns(5)
    with col1:
        st.text(recommended_movies[0])
        st.image(recommended_posters[0])
        st.video(recommended_trailers[0])
    with col2:
        st.text(recommended_movies[1])
        st.image(recommended_posters[1])
        st.video(recommended_trailers[1])

    with col3:
        st.text(recommended_movies[2])
        st.image(recommended_posters[2])
        st.video(recommended_trailers[2])

    with col4:
        st.text(recommended_movies[3])
        st.image(recommended_posters[3])
        st.video(recommended_trailers[3])

    with col5:
        st.text(recommended_movies[4])
        st.image(recommended_posters[4])
        st.video(recommended_trailers[4])

if theme == "Dark 🌙":
    st.markdown(
        """
        <style>
            body, .stApp { background-color: black !important; color: white !important; }
            .stTextInput, .stButton > button { background-color: #222; color: white !important; }
            .stSelectbox label, .stSelectbox div[data-baseweb="select"] {
                background-color: #222 !important;
                color: white !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <style>
            body, .stApp { background-color: white !important; color: black !important; }
            .stTextInput, .stButton > button { background-color: #f0f0f0; color: black !important; }
            .stSelectbox label, .stSelectbox div[data-baseweb="select"] {
                background-color: #f0f0f0 !important;
                color: black !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )


def fetch_trending_movies():
    trending_url = f"https://api.themoviedb.org/3/trending/movie/week?api_key={API_KEY}"
    response = requests.get(trending_url).json()
    
    trending_movies = []
    trending_posters = []
    
    for movie in response.get("results", []):
        if movie.get("poster_path"):  
            trending_movies.append(movie["title"])
            trending_posters.append(f"https://image.tmdb.org/t/p/w500{movie['poster_path']}")  
    
    return trending_movies[:5], trending_posters[:5]  # Limit to 5 movies



st.subheader("🔥 Trending Movies This Week")
trending_movies, trending_posters = fetch_trending_movies()

trend_cols = st.columns(5)
for idx, col in enumerate(trend_cols):
    with col:
        st.text(trending_movies[idx])
        st.image(trending_posters[idx])