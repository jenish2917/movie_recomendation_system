import streamlit as st
import pickle
import pandas as pd
import requests
import json

# Set page configuration
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

# Load data
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    response = requests.get(url)
    data = json.loads(response.text)
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path'] 

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse = True, key = lambda x : x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movies.iloc[i[0]].id))
        
    return recommended_movies, recommended_movies_posters

# Custom CSS
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }
        .main-header {
            font-size: 3rem;
            color: #1E3A8A;
            text-align: center;
            margin: 1rem 0 2rem;
            padding: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
            font-weight: 800;
        }
        .movie-card {
            background-color: white;
            border-radius: 10px;
            padding: 1rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
            height: 100%;
        }
        .movie-card:hover {
            transform: translateY(-5px);
        }
        .movie-title {
            font-weight: bold;
            text-align: center;
            margin-bottom: 0.5rem;
            font-size: 1rem;
            height: 3em;
            overflow: hidden;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
        }
        .stButton > button {
            background-color: #1E3A8A;
            color: white;
            border-radius: 20px;
            padding: 0.5rem 2rem;
            font-size: 1.2rem;
            border: none;
            width: 100%;
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #2563EB;
            transform: scale(1.02);
        }
        .selection-container {
            background-color: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
        }
        .footer {
            text-align: center;
            margin-top: 3rem;
            padding: 1rem;
            color: #666;
            font-size: 0.8rem;
        }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown("<h1 class='main-header'>🎬 Movie Recommendation System</h1>", unsafe_allow_html=True)

# Movie selection section
st.markdown("<div class='selection-container'>", unsafe_allow_html=True)
st.markdown("### Select a movie you like")
st.markdown("We'll recommend similar movies you might enjoy!")
selected_movie_name = st.selectbox(
    'Choose a movie from our database:',
    movies['title'].values
)

# Center the recommend button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    recommend_button = st.button('Get Recommendations')
st.markdown("</div>", unsafe_allow_html=True)

# Display recommendations
if recommend_button:
    with st.spinner('Finding movies you might like...'):
        names, posters = recommend(selected_movie_name)
        
    st.markdown("### Recommended Movies for You")
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.markdown(f"""
            <div class='movie-card'>
                <div class='movie-title'>{names[i]}</div>
                <img src='{posters[i]}' width='100%'>
            </div>
            """, unsafe_allow_html=True)

# Footer
# st.markdown("Thank you!", unsafe_allow_html=True)