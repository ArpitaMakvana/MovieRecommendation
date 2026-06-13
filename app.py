import pickle
from urllib.parse import quote

import requests
import streamlit as st


WIKIPEDIA_HEADERS = {
    "User-Agent": "MovieRecommenderSystem/1.0 (https://example.com)"
}


@st.cache_data(show_spinner=False)
def load_data():
    movies = pickle.load(open("movies_list.pkl", "rb"))
    similarity = pickle.load(open("similarity.pkl", "rb"))
    return movies, similarity


movies, similarity = load_data()
movies_list = movies["title"].values


def fetch_real_poster(movie_title):
    search_url = "https://en.wikipedia.org/w/api.php"
    search_params = {
        "action": "opensearch",
        "search": movie_title,
        "limit": 1,
        "namespace": 0,
        "format": "json",
    }

    try:
        search_response = requests.get(
            search_url, params=search_params, headers=WIKIPEDIA_HEADERS, timeout=6
        )
        search_response.raise_for_status()
        search_data = search_response.json()
        if len(search_data) < 2 or not search_data[1]:
            return None

        page_title = search_data[1][0]
        summary_url = (
            "https://en.wikipedia.org/api/rest_v1/page/summary/"
            + quote(page_title.replace(" ", "_"))
        )
        summary_response = requests.get(
            summary_url, headers=WIKIPEDIA_HEADERS, timeout=6
        )
        summary_response.raise_for_status()
        summary_data = summary_response.json()

        image_url = (
            summary_data.get("originalimage", {}).get("source")
            or summary_data.get("thumbnail", {}).get("source")
        )
        if not image_url:
            return None

        poster_response = requests.get(image_url, headers=WIKIPEDIA_HEADERS, timeout=6)
        poster_response.raise_for_status()
        return poster_response.content
    except requests.RequestException:
        return None


@st.cache_data(show_spinner=False)
def get_poster_bytes(title):
    real_poster = fetch_real_poster(title)
    if real_poster:
        return real_poster

    with open("img.jpg", "rb") as image_file:
        return image_file.read()


def recommend(movie):
    index = movies[movies["title"] == movie].index[0]

    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda vector: vector[1],
    )

    recommend_movie = []
    recommend_poster = []

    for i in distances[1:6]:
        movie_index = i[0]
        movie_row = movies.iloc[movie_index]
        recommend_movie.append(movie_row.title)
        recommend_poster.append(get_poster_bytes(movie_row.title))

    return recommend_movie, recommend_poster


st.title("Movie Recommender System")
st.write("Choose a movie and get similar recommendations based on content features.")

selectvalue = st.selectbox("Select movie from dropdown", movies_list)
show_recommend = st.button("Show Recommendations")

if show_recommend:
    with st.spinner("Finding similar movies..."):
        movie_name, movie_poster = recommend(selectvalue)

    st.subheader("Recommended Movies")
    cols = st.columns(5)

    for idx, col in enumerate(cols):
        with col:
            st.image(movie_poster[idx], width="stretch")
            st.caption(movie_name[idx])
