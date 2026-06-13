import pickle
from urllib.parse import quote

import requests
import streamlit as st


WIKIPEDIA_HEADERS = {
    "User-Agent": "MovieRecommenderSystem/1.0 (https://example.com)"
}

st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)


BACKGROUND_IMAGE_URL = (
    "https://upload.wikimedia.org/wikipedia/commons/a/a5/"
    "Dracula_%281931_film_poster_-_Style_B%29.jpg"
)


@st.cache_data(show_spinner=False)
def load_data():
    movies = pickle.load(open("movies_list.pkl", "rb"))
    similarity = pickle.load(open("similarity.pkl", "rb"))
    return movies, similarity


movies, similarity = load_data()
movies_list = movies["title"].values


background_css = """
    <style>
        .stApp {{
            background: #050507;
            color: #f5f5f5;
        }}

        .bg-layer {{
            position: fixed;
            inset: 0;
            z-index: -2;
            overflow: hidden;
        }}

        .bg-layer::before {{
            content: "";
            position: absolute;
            inset: -10%;
            background-image: url("__BACKGROUND_IMAGE__");
            background-size: cover;
            background-position: center;
            filter: brightness(0.28) saturate(1.15) contrast(1.08);
            transform-origin: center center;
            animation: zoomPulse 18s ease-in-out infinite alternate;
        }}

        .bg-layer::after {{
            content: "";
            position: absolute;
            inset: 0;
            background:
                radial-gradient(circle at top, rgba(140, 0, 0, 0.22), transparent 35%),
                linear-gradient(180deg, rgba(0, 0, 0, 0.2), rgba(0, 0, 0, 0.88));
        }}

        @keyframes zoomPulse {{
            from {{
                transform: scale(1);
            }}
            to {{
                transform: scale(1.12);
            }}
        }}

        .hero {{
            padding: 2rem 2.2rem;
            border-radius: 24px;
            background: rgba(12, 12, 14, 0.62);
            border: 1px solid rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(14px);
            box-shadow: 0 18px 60px rgba(0, 0, 0, 0.45);
            margin-bottom: 1.4rem;
        }}

        .hero h1 {{
            margin: 0;
            font-size: clamp(2.2rem, 4vw, 4.6rem);
            font-weight: 800;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            color: #ff3b3b;
            text-shadow: 0 0 18px rgba(255, 0, 0, 0.35);
        }}

        .hero p {{
            margin: 0.65rem 0 0;
            max-width: 720px;
            color: rgba(255, 255, 255, 0.82);
            font-size: 1.02rem;
            line-height: 1.6;
        }}

        .section-title {{
            margin: 1.2rem 0 0.75rem;
            font-size: 1rem;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            color: rgba(255, 255, 255, 0.8);
        }}

        div[data-baseweb="select"] > div {{
            background: rgba(18, 18, 20, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 14px;
        }}

        div[data-baseweb="select"] * {{
            color: #f7f7f7 !important;
        }}

        .stButton > button {{
            background: linear-gradient(135deg, #b31217 0%, #6a0000 100%);
            color: #ffffff;
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 14px;
            padding: 0.7rem 1.2rem;
            font-weight: 700;
            letter-spacing: 0.05em;
            box-shadow: 0 10px 28px rgba(179, 18, 23, 0.25);
            transition: transform 180ms ease, box-shadow 180ms ease, filter 180ms ease;
        }

        .stButton > button:hover {{
            transform: translateY(-1px) scale(1.02);
            box-shadow: 0 16px 34px rgba(179, 18, 23, 0.38);
            filter: brightness(1.08);
        }}

        div[data-testid="stImage"] img {{
            border-radius: 18px;
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.45);
            border: 1px solid rgba(255, 255, 255, 0.08);
            transition: transform 180ms ease, box-shadow 180ms ease;
        }}

        div[data-testid="stImage"] img:hover {{
            transform: translateY(-3px) scale(1.02);
            box-shadow: 0 18px 42px rgba(0, 0, 0, 0.58);
        }}

        .movie-caption {{
            margin-top: 0.45rem;
            color: rgba(255, 255, 255, 0.9);
            font-size: 0.95rem;
            text-align: center;
        }}
    </style>
    <div class="bg-layer"></div>
    """.replace("__BACKGROUND_IMAGE__", BACKGROUND_IMAGE_URL)

st.markdown(background_css, unsafe_allow_html=True)


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


st.markdown(
    """
    <div class="hero">
        <h1>Movie Recommender System</h1>
    </div>
    """,
    unsafe_allow_html=True,
)


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


st.markdown('<div class="section-title">Select a movie</div>', unsafe_allow_html=True)
selectvalue = st.selectbox("Select movie from dropdown", movies_list, label_visibility="collapsed")
show_recommend = st.button("Show Recommendations")

if show_recommend:
    with st.spinner("Finding similar movies..."):
        movie_name, movie_poster = recommend(selectvalue)

    st.markdown('<div class="section-title">Recommended Movies</div>', unsafe_allow_html=True)
    cols = st.columns(5)

    for idx, col in enumerate(cols):
        with col:
            st.image(movie_poster[idx], width="stretch")
            st.markdown(f"<div class='movie-caption'>{movie_name[idx]}</div>", unsafe_allow_html=True)
