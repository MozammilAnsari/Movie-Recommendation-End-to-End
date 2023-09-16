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
def recommend(movie, num_of_movies):
    movie_index = movies_df[movies_df['title']==movie].index[0]
    distance = list(enumerate(similarity[movie_index]))
    sorted_dist = sorted(distance,reverse=True,key=lambda x: x[1])[:num_of_movies]
    
    recommended_movies = []
    recommended_movies_poster = []
    for i in sorted_dist:
        movie_id = movies_df.iloc[i[0]]['movie_id']
        recommended_movies.append(movies_df.iloc[i[0]]['title'])
        # Fetch poster from api
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster


movies_list = movies_df['title'].values
def main():
    st.title("Movies Recommendation System")
    st.text("This recommendation system recommend you top 1 to 30 movies")

    num_of_movies = st.select_slider('Number of Movies: ', range(1,31))
    selected_movie_names = st.selectbox('Movies Option: ',movies_list)

# ... (previous code for loading recommendations and posters)

    if st.button('Recommend'):
        recommended, poster = recommend(selected_movie_names, num_of_movies)
        
        rows = int(num_of_movies * 0.80)
        cols = num_of_movies - rows
        
        # Calculate the width of each column
        col_width = 150  # Adjust this width as needed
        
        # Calculate the total width of all columns
        total_width = cols * col_width
        
        # Check if the total width exceeds the screen width
        if total_width > 700:
            # Reduce the column width to fit within the screen width
            col_width = int(700 / cols)
        
        for row in range(rows):
            start_idx = row * cols
            end_idx = start_idx + cols
            row_recommended = recommended[start_idx:end_idx]
            row_poster = poster[start_idx:end_idx]
            
            col_list = st.columns(cols)
            for col, movie, img_url in zip(col_list, row_recommended, row_poster):
                with col:
                    st.text(movie)
                    st.image(img_url, width=col_width)


if __name__=='__main__':
    main()
