# Movie Recommender System 🎬

> Movie Recommender System is a content-based filtering app that suggests similar movies based on text features extracted from movie metadata. It uses a Streamlit interface and TMDB posters to give users a simple, visual recommendation experience.

---

## 🛠 Tech Stack

| Layer | Technologies |
|---|---|
| **Modeling** | Content-Based Filtering, CountVectorizer, Cosine Similarity |
| **Backend / Logic** | Python, Pickle, Requests |
| **Frontend** | Streamlit |
| **Data** | Pandas, CSV, Pickled Artifacts |
| **API** | The Movie Database (TMDB) API |
| **Development** | Jupyter Notebook |

---

## ✨ Key Features

- 🎯 Movie recommendations based on content similarity
- 🖥 Simple Streamlit user interface
- 🎞 Poster previews fetched from TMDB
- 📚 Preprocessed movie dataset saved in pickle format
- ⚡ Fast loading with ready-made model artifacts
- 🧪 Notebook-based model building and experimentation

---

## 📁 Project Structure

```text
movie_recommender_system-main/
├── app.py
├── dataset.csv
├── movies_list.pkl
├── similarity.pkl.gz
├── main.py
├── test.py
├── Main.ipynb
├── Untitled.ipynb
├── img.jpg
└── frontend/
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Internet connection for poster loading

### Install Dependencies

```bash
pip install streamlit pandas requests scikit-learn
```

### Run the App

```bash
streamlit run app.py
```

Open the local URL shown in the terminal, usually:

```text
http://localhost:8501
```

---

## 🤖 Recommendation Algorithm

This project uses **content-based filtering**.

### How it works

1. Movie metadata is cleaned and combined into a `tags` column
2. `CountVectorizer` converts the tags into numerical vectors
3. `cosine_similarity` measures how similar each movie is to every other movie
4. The similarity matrix is saved in `similarity.pkl`
5. The app uses the movie title selected by the user to find and show similar movies

---

## 📦 Data Files

| File | Purpose |
|---|---|
| `dataset.csv` | Raw movie dataset |
| `movies_list.pkl` | Preprocessed movie table used by the app |
| `similarity.pkl.gz` | Compressed saved similarity matrix |

---

## 🎯 Main App Flow

- Load the movie list from `movies_list.pkl`
- Let the user choose a movie from a dropdown
- Find similar movies using the content-based model
- Fetch movie posters from TMDB
- Display the final recommendations in the Streamlit UI

---

## 🧪 Supporting Files

- `Main.ipynb` contains the model-building workflow
- `Untitled.ipynb` contains experimentation and alternate notebook work
- `main.py` is a simple CSV inspection script
- `test.py` is a console-based horror movie demo
- `frontend/` contains a separate Streamlit component scaffold

---

## 📝 Notes

- The project depends on TMDB for poster images.
- If you change file locations, update the file paths in `app.py`.
- The recommendation quality depends on the cleaned metadata stored in the dataset and pickle files.
