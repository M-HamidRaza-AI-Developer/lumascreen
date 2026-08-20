"""
LumaScreen — TMDB API helpers and HTML builder utilities.
"""

import os
import logging
import requests

logger = logging.getLogger("lumascreen")

TMDB_API_KEY = os.getenv("TMDB_API_KEY", "9df755b98dbf5687eb0c8246b34d266a")
TMDB_BASE    = "https://api.themoviedb.org/3"
TMDB_IMG     = "https://image.tmdb.org/t/p/w500"
TMDB_IMG_BIG = "https://image.tmdb.org/t/p/w1280"

# Fallback sample movie data in case of offline/network/DNS errors
FALLBACK_MOVIES = [
    {
        "id": 1,
        "title": "LumaScreen Exclusive Sample",
        "overview": "This is a placeholder movie because internet connection to TMDB is currently offline or unreachable.",
        "poster_path": "",
        "backdrop_path": "",
        "vote_average": 8.5,
        "release_date": "2026-01-01",
        "genre_ids": [28, 12],
        "original_language": "en"
    }
]

def tmdb_get(endpoint: str, params: dict = None) -> dict:
    if not TMDB_API_KEY:
        return {"results": FALLBACK_MOVIES}
    url = f"{TMDB_BASE}{endpoint}"
    p = {"api_key": TMDB_API_KEY, "language": "en-US"}
    if params:
        p.update(params)
    try:
        resp = requests.get(url, params=p, timeout=5)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        logger.warning(f"⚠️ TMDB offline/network warning on {endpoint}: {e}. Using fallback data.")
        return {"results": FALLBACK_MOVIES, "genres": [{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}]}

def fetch_now_playing() -> list:
    movies = []
    for page in range(1, 4):
        data = tmdb_get("/movie/now_playing", {"page": page})
        movies.extend(data.get("results", []))
    return movies if movies else FALLBACK_MOVIES

def fetch_upcoming() -> list:
    movies = []
    for page in range(1, 3):
        data = tmdb_get("/movie/upcoming", {"page": page})
        movies.extend(data.get("results", []))
    return movies if movies else FALLBACK_MOVIES

def fetch_bollywood() -> list:
    movies = []
    for page in range(1, 4):
        data = tmdb_get("/discover/movie", {
            "with_original_language": "hi",
            "sort_by": "popularity.desc",
            "page": page
        })
        movies.extend(data.get("results", []))
    return movies if movies else FALLBACK_MOVIES

def fetch_anime() -> list:
    movies = []
    for page in range(1, 4):
        data = tmdb_get("/discover/movie", {
            "with_genres": "16",
            "with_original_language": "ja",
            "sort_by": "popularity.desc",
            "page": page
        })
        movies.extend(data.get("results", []))
    return movies if movies else FALLBACK_MOVIES

def fetch_kids() -> list:
    movies = []
    for page in range(1, 4):
        data = tmdb_get("/discover/movie", {
            "with_genres": "10751,16",
            "sort_by": "popularity.desc",
            "page": page
        })
        movies.extend(data.get("results", []))
    return movies if movies else FALLBACK_MOVIES

def fetch_trending() -> list:
    movies = []
    for page in range(1, 4):
        data = tmdb_get("/trending/movie/week", {"page": page})
        movies.extend(data.get("results", []))
    return movies if movies else FALLBACK_MOVIES

def fetch_movie_news() -> list:
    data = tmdb_get("/movie/upcoming", {"page": 1})
    results = data.get("results", [])
    return results[:15] if results else FALLBACK_MOVIES

def get_genres() -> dict:
    data = tmdb_get("/genre/movie/list")
    genres = data.get("genres", [])
    if not genres:
        return {28: "Action", 12: "Adventure", 16: "Animation", 10751: "Family"}
    return {g["id"]: g["name"] for g in genres}

def genre_tags_html(genre_ids: list, genre_map: dict) -> str:
    tags = [genre_map.get(gid, "") for gid in genre_ids[:3] if gid in genre_map]
    return "".join(f'<span class="genre-tag">{t}</span>' for t in tags)

def rating_badge(vote: float) -> str:
    color = "#27ae60" if vote >= 7 else "#f39c12" if vote >= 5 else "#e74c3c"
    return f'<span class="rating-badge" style="background:{color}">⭐ {vote:.1f}</span>'

def movie_card_html(movie: dict, genre_map: dict) -> str:
    title = (movie.get("title") or "Unknown").replace('"', '&quot;')
    poster = movie.get("poster_path")
    vote = movie.get("vote_average", 0)
    date = movie.get("release_date", "TBA")
    overview = (movie.get("overview") or "No description available.")[:110] + "…"
    gids = movie.get("genre_ids", [])
    mid = movie.get("id", 0)
    img_url = f"{TMDB_IMG}{poster}" if poster else "https://placehold.co/220x330/141722/FFD700?text=No+Poster"

    return f"""<div class="movie-card" onclick="showMovieDetail({mid})">
      <div class="card-poster-wrap">
        <img src="{img_url}" alt="{title}" loading="lazy">
        {rating_badge(vote)}
      </div>
      <div class="card-info">
        <div class="card-title">{title}</div>
        <div class="card-year">🗓️ {date}</div>
        <div class="card-genres">{genre_tags_html(gids, genre_map)}</div>
        <div class="card-overview">{overview}</div>
      </div>
    </div>"""

def news_card_html(movie: dict) -> str:
    title = (movie.get("title") or "Unknown").replace('"', '&quot;')
    backdrop = movie.get("backdrop_path") or movie.get("poster_path")
    date = movie.get("release_date", "TBA")
    overview = (movie.get("overview") or "")[:140] + "…"
    img_url = f"{TMDB_IMG}{backdrop}" if backdrop else "https://placehold.co/400x200/141722/FFD700?text=Coming+Soon"
    return f"""<div class="movie-card" onclick="showMovieDetail({movie.get('id', 0)})">
      <div class="card-poster-wrap">
        <img src="{img_url}" alt="{title}" loading="lazy">
        <span class="rating-badge" style="background:#e50914">🗓️ {date}</span>
      </div>
      <div class="card-info">
        <div class="card-title">{title}</div>
        <div class="card-year">Premiere: {date}</div>
        <div class="card-overview">{overview}</div>
      </div>
    </div>"""

def trending_card_html(movie: dict, genre_map: dict) -> str:
    title = (movie.get("title") or "Unknown").replace('"', '&quot;')
    backdrop = movie.get("backdrop_path")
    vote = movie.get("vote_average", 0)
    overview = (movie.get("overview") or "")[:160] + "…"
    gids = movie.get("genre_ids", [])
    mid = movie.get("id", 0)
    img_url = f"{TMDB_IMG_BIG}{backdrop}" if backdrop else "https://placehold.co/1280x720/090a0f/FFD700?text=Trending"
    color = "#27ae60" if vote >= 7 else "#f39c12" if vote >= 5 else "#e74c3c"

    return f"""<div class="hero-slide" style="background-image:url('{img_url}')">
      <div class="hero-overlay">
        <div class="hero-content">
          <div class="hero-genres">{genre_tags_html(gids, genre_map)}</div>
          <h1 class="hero-title">{title}</h1>
          <div class="hero-rating"><span class="rating-badge" style="background:{color};position:static">⭐ {vote:.1f}</span></div>
          <p class="hero-overview">{overview}</p>
          <button class="hero-btn" onclick="showMovieDetail({mid})">▶ Watch Now</button>
        </div>
      </div>
    </div>"""

def build_movie_data_map_js(movies: list) -> str:
    js = "window.movieDataMap = {};\n"
    for m in movies:
        mid = m.get("id")
        if not mid:
            continue
        title = (m.get("title") or "").replace('\\', '\\\\').replace('"', '\\"').replace("'", "\\'").replace("\n", " ")
        overview = (m.get("overview") or "").replace('\\', '\\\\').replace('"', '\\"').replace("'", "\\'").replace("\n", " ")
        vote = m.get("vote_average", 0)
        date = m.get("release_date", "")
        poster = m.get("poster_path", "") or ""
        backdrop = m.get("backdrop_path", "") or ""
        lang = m.get("original_language", "")
        gids = str(m.get("genre_ids", []))
        js += f'window.movieDataMap[{mid}]={{id:{mid},title:"{title}",overview:"{overview}",vote_average:{vote},release_date:"{date}",poster_path:"{poster}",backdrop_path:"{backdrop}",original_language:"{lang}",genre_ids:{gids},runtime:null,genres:[],credits:{{cast:[],crew:[]}}}};\n'
    return js