import pickle
import streamlit as st
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=b0ff212b4d9ea564bce25634e5898a6c&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/original"+data['poster_path']

movies_df = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))
def recommend(movie):
    movie_index = movies_df[movies_df['title']==movie].index[0]
    distance = list(enumerate(similarity[movie_index]))
    sorted_dist = sorted(distance,reverse=True,key=lambda x: x[1])[:10]
    
    recommended_movies = []
    recommended_movies_poster = []
    for i in sorted_dist:
        movie_id = movies_df.iloc[i[0]]['movie_id']
        recommended_movies.append(movies_df.iloc[i[0]]['title'])
        # Fetch poster from api
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster


movies_list = movies_df['title'].values
st.title("Recommendation System")
st.text("This recommendation engine is made by")
st.header("Mozammil")

selected_movie_names = st.selectbox('Options',movies_list)

if st.button('Recommend'):
    recommended, poster = recommend(selected_movie_names)
    
    rows = 2
    cols = 5
    for row in range(rows):
        start_idx = row * cols
        end_idx = start_idx + cols
        row_recommended = recommended[start_idx:end_idx]
        row_poster = poster[start_idx:end_idx]
        
        col_list = st.columns(cols)
        for col, movie, img_url in zip(col_list, row_recommended, row_poster):
            with col:
                st.text(movie)
                st.image(img_url)