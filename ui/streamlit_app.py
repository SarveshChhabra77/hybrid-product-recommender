import streamlit as st
import requests

# ==============================
# 🔑 CONFIG
# ==============================
API_URL = "http://127.0.0.1:8000"
OMDB_API_KEY = "dd385cb"   # your key

st.set_page_config(
    page_title="Hybrid Recommender System",
    page_icon="🎬",
    layout="wide"
)

# ==============================
# 🎨 PREMIUM BLACK UI
# ==============================
st.markdown("""
<style>

/* ===== Cinematic Black Background ===== */
.stApp {
    background: radial-gradient(circle at 20% 20%, #111 0%, #0a0a0a 40%, #000000 100%);
    color: #ffffff;
}

/* ===== Floating Glass Navbar ===== */
.navbar {
    position: sticky;
    top: 0;
    z-index: 999;
    backdrop-filter: blur(18px);
    background: rgba(20,20,20,0.75);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 16px 26px;
    border-radius: 16px;
    margin-bottom: 28px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.6);
    display:flex;
    justify-content: space-between;
    align-items: center;
}
.nav-title {
    font-size: 24px;
    font-weight: 800;
    letter-spacing: 0.5px;
}
.nav-sub {
    font-size: 14px;
    color: #9ca3af;
}

/* ===== Section Headers ===== */
h2, h3 {
    font-weight: 700 !important;
    letter-spacing: 0.4px;
}

/* ===== Glass Movie Card ===== */
.movie-card {
    background: linear-gradient(145deg, rgba(255,255,255,0.06), rgba(255,255,255,0.03));
    backdrop-filter: blur(20px);
    border-radius: 20px;
    padding: 16px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow:
        0 12px 40px rgba(0,0,0,0.65),
        inset 0 1px 0 rgba(255,255,255,0.05);
    transition: all 0.35s ease;
}
.movie-card:hover {
    transform: translateY(-10px) scale(1.035);
    box-shadow:
        0 20px 70px rgba(0,0,0,0.9),
        0 0 20px rgba(0,255,213,0.15);
}

/* ===== Poster ===== */
.poster-img {
    border-radius: 16px;
    width: 100%;
    margin-bottom: 12px;
}

/* ===== Poster Placeholder ===== */
.poster-placeholder {
    height: 260px;
    border-radius: 16px;
    background: linear-gradient(135deg,#111,#1a1a1a);
    display:flex;
    align-items:center;
    justify-content:center;
    font-size: 64px;
    margin-bottom: 12px;
    border: 1px solid rgba(255,255,255,0.05);
}

/* ===== Text ===== */
.title-text {
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 6px;
}
.genre-text {
    font-size: 13px;
    color: #9ca3af;
    margin-bottom: 8px;
}
.score-text {
    font-size: 13px;
    color: #00ffd5;
    margin-bottom: 8px;
}

/* ===== Rating Bar ===== */
.rating-bar {
    height: 8px;
    background: rgba(255,255,255,0.12);
    border-radius: 10px;
    overflow: hidden;
}
.rating-fill {
    height: 100%;
    background: linear-gradient(90deg,#00ffd5,#00ffa2,#00ffd5);
    box-shadow: 0 0 10px rgba(0,255,213,0.6);
}

/* ===== Buttons ===== */
.stButton>button {
    background: linear-gradient(135deg,#00ffd5,#00ffa2);
    color: black;
    border-radius: 12px;
    font-weight: 700;
    border: none;
}
.stButton>button:hover {
    box-shadow: 0 0 16px rgba(0,255,213,0.7);
}

/* ===== Divider ===== */
hr {
    border: none;
    height: 1px;
    background: linear-gradient(to right, transparent, rgba(255,255,255,0.2), transparent);
    margin: 40px 0;
}

</style>
""", unsafe_allow_html=True)

# ==============================
# 🧭 NAVBAR
# ==============================
st.markdown("""
<div class="navbar">
    <div class="nav-title">🎬 Hybrid Recommender System</div>
    <div class="nav-sub">Personalized Movie Intelligence Engine</div>
</div>
""", unsafe_allow_html=True)

# ==============================
# 🎞 Poster Fetcher (OMDb)
# ==============================
@st.cache_data(show_spinner=False)
def get_movie_poster(title):
    try:
        url = "http://www.omdbapi.com/"
        params = {"apikey": OMDB_API_KEY, "t": title}
        res = requests.get(url, params=params, timeout=10).json()
        poster = res.get("Poster")
        if poster and poster != "N/A":
            return poster
        return None
    except:
        return None

# ==============================
# 📦 Load Movies
# ==============================
@st.cache_data
def load_movies():
    res = requests.get(f"{API_URL}/movies")
    return res.json()["movies"]

movies_data = load_movies()
movie_options = {m["clean_title"]: m["movieId"] for m in movies_data}

# ==============================
# 👤 Personalized Recommendations
# ==============================
st.subheader("👤 Personalized Recommendations")

col1, col2 = st.columns(2)

with col1:
    user_id = st.selectbox("Select User", list(range(1, 51)))

with col2:
    top_n = st.slider("Number of Recommendations", 1, 20, 8)

if st.button("Get Recommendations 🚀"):
    with st.spinner("Generating recommendations..."):
        res = requests.post(
            f"{API_URL}/recommend",
            json={"user_id": int(user_id), "top_n": int(top_n)},
            timeout=30
        )
        data = res.json()
        recs = data.get("recommendations", [])

        if not recs:
            st.warning("No recommendations found.")
        else:
            cols = st.columns(4)
            for idx, movie in enumerate(recs):
                col = cols[idx % 4]
                poster = get_movie_poster(movie["title"])
                score_pct = min(max(movie["score"] * 20, 5), 100)

                with col:
                    st.markdown('<div class="movie-card">', unsafe_allow_html=True)

                    if poster:
                        st.image(poster, use_container_width=True)
                    else:
                        st.markdown('<div class="poster-placeholder">🎬</div>', unsafe_allow_html=True)

                    st.markdown(f'<div class="title-text">{movie["title"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="genre-text">{movie.get("genres","")}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="score-text">⭐ {movie["score"]:.4f}</div>', unsafe_allow_html=True)

                    st.markdown(
                        f'''
                        <div class="rating-bar">
                            <div class="rating-fill" style="width:{score_pct}%"></div>
                        </div>
                        ''',
                        unsafe_allow_html=True
                    )

                    st.markdown('</div>', unsafe_allow_html=True)

# ==============================
# 🔍 Similar Movies
# ==============================
st.divider()
st.subheader("🔍 Find Similar Movies")

movie_name = st.selectbox("Search Movie", list(movie_options.keys()))
movie_id = movie_options[movie_name]

if st.button("Show Similar Movies 🎞️"):
    with st.spinner("Finding similar movies..."):
        res = requests.get(f"{API_URL}/similar/{movie_id}", timeout=30)
        data = res.json()
        recs = data.get("similar_movies", [])

        if not recs:
            st.warning("No similar movies found.")
        else:
            cols = st.columns(4)
            for idx, movie in enumerate(recs):
                col = cols[idx % 4]
                poster = get_movie_poster(movie["title"])

                with col:
                    st.markdown('<div class="movie-card">', unsafe_allow_html=True)

                    if poster:
                        st.image(poster, use_container_width=True)
                    else:
                        st.markdown('<div class="poster-placeholder">🎬</div>', unsafe_allow_html=True)

                    st.markdown(f'<div class="title-text">{movie["title"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="genre-text">{movie.get("genres","")}</div>', unsafe_allow_html=True)

                    st.markdown('</div>', unsafe_allow_html=True)