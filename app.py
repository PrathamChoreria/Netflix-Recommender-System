import streamlit as st
import pickle
import pandas as pd
import requests
import base64


def fetch_pos(movie_id):
    response = requests.get(
        "https://api.themoviedb.org/3/movie/{}?api_key=SECRET_TOKEN".format(
            movie_id))
    data = response.json()
    print(data)
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommender(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    recommended = []
    for i in movie_list:
        movie_id = i[0]
        # poster getting
        recommended_poster = []
        recommended.append(movies.iloc[i[0]].title)
        ##poster
        ##recommended_poster.append(fetch_pos(movie_id))
    return recommended#,recommended_poster


def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
        
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('net.png')




similarity = movies_dict = pickle.load(open('similarity.pkl', 'rb'))
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
st.title("NETFLIX Movies Recommender")
st.header("HELLO!! WHAT ARE WE WATCHING TODAY")

selected_movie_name = st.selectbox("Choose from below", movies['title'].values)

if st.button("Recommend"):
    recommendation= recommender(selected_movie_name)#recommendation, posters = recommender(selected_movie_name)
    for i in recommendation:
        st.header(i)

