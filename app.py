"""
LumaScreen — Professional Movie Discovery App
Hollywood & Bollywood content, subscriptions, news, and account management.
"""
import sys
import asyncio

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import logging
import streamlit as st
import streamlit.components.v1 as components

from tmdb_helpers import (
    fetch_now_playing, fetch_bollywood, fetch_trending,
    fetch_movie_news, get_genres,
    movie_card_html, news_card_html, trending_card_html,
    build_movie_data_map_js,
)
from styles import CSS, LOGO_SVG, LOGO_SVG_SMALL
from scripts import JS

logger = logging.getLogger("lumascreen")

# Streamlit Page Configuration
st.set_page_config(
    page_title="LumaScreen — Movie Discovery",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Base Wrapper Styles
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }
    iframe {
        width: 100% !important;
        border: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ─────────────────────────────────────────────
# HTML Page Builders
# ─────────────────────────────────────────────

def _build_subscription_html() -> str:
    """Build the subscription plans page HTML."""
    plans = [
        {
            "icon": "🎬", "name": "Basic", "price": "₹199",
            "desc": "Perfect for casual movie lovers",
            "features": ["HD Streaming (720p)", "1 Screen at a time", "Hollywood Movies",
                         "Bollywood Movies", "Mobile & Tablet"],
            "no": ["4K Ultra HD", "Offline Downloads", "Priority Support"],
            "featured": False, "badge": None,
        },
        {
            "icon": "⭐", "name": "Standard", "price": "₹499",
            "desc": "Most popular — great value",
            "features": ["Full HD Streaming (1080p)", "2 Screens simultaneously",
                         "Hollywood & Bollywood", "Offline Downloads", "All Devices"],
            "no": ["4K Ultra HD", "Priority Support"],
            "featured": True, "badge": "POPULAR",
        },
        {
            "icon": "👑", "name": "Premium", "price": "₹999",
            "desc": "The ultimate cinema experience",
            "features": ["4K Ultra HD + HDR", "4 Screens simultaneously",
                         "Hollywood & Bollywood", "Unlimited Downloads",
                         "All Devices", "Priority Support", "Early Access"],
            "no": [],
            "featured": False, "badge": "BEST",
        },
    ]
    cards = ""
    for p in plans:
        feat_li = "".join(f'<li>{f}</li>' for f in p["features"])
        no_li   = "".join(f'<li class="no">{f}</li>' for f in p["no"])
        badge   = f'<div class="plan-badge">{p["badge"]}</div>' if p["badge"] else ""
        featured_cls = " featured" if p["featured"] else ""
        cards += f"""
        <div class="plan-card{featured_cls}">
          {badge}
          <div class="plan-icon">{p["icon"]}</div>
          <div class="plan-name">{p["name"]}</div>
          <div class="plan-price">{p["price"]}<span>/mo</span></div>
          <div class="plan-desc">{p["desc"]}</div>
          <ul class="plan-features">{feat_li}{no_li}</ul>
          <button class="plan-btn" onclick="subscribePlan('{p['name']}','{p['price']}')">
            Get {p["name"]}
          </button>
        </div>"""
    return f"""
    <div class="sub-page">
      <div class="sub-header">
        <h2>Choose Your <span>Plan</span></h2>
        <p>Unlock unlimited movies, series, and exclusive content</p>
      </div>
      <div class="sub-plans">{cards}</div>
    </div>"""


def _build_account_html() -> str:
    """Build the account/profile page HTML."""
    return """
    <div class="account-page">
      <div class="profile-card">
        <div class="profile-avatar" id="profile-initial">U</div>
        <div class="profile-info">
          <h3 id="profile-name">User</h3>
          <p id="profile-email">user@example.com</p>
          <span class="profile-badge" id="profile-plan">Basic Plan</span>
        </div>
      </div>

      <div class="account-section">
        <h4>📊 Your Stats</h4>
        <div class="stats-grid">
          <div class="stat-card"><div class="stat-num">42</div><div class="stat-label">Movies Watched</div></div>
          <div class="stat-card"><div class="stat-num">8</div><div class="stat-label">Watchlist</div></div>
          <div class="stat-card"><div class="stat-num">5</div><div class="stat-label">Reviews</div></div>
        </div>
      </div>

      <div class="account-section">
        <h4>✏️ Edit Profile</h4>
        <div class="edit-form">
          <div class="form-row">
            <div class="form-group">
              <label>Full Name</label>
              <input type="text" id="edit-name" placeholder="Your name">
            </div>
            <div class="form-group">
              <label>Email Address</label>
              <input type="email" id="edit-email" placeholder="your@email.com">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>New Password</label>
              <input type="password" id="edit-pass" placeholder="Leave blank to keep current">
            </div>
            <div class="form-group">
              <label>Confirm Password</label>
              <input type="password" id="edit-pass2" placeholder="Confirm new password">
            </div>
          </div>
          <button class="save-btn" onclick="saveProfile()">💾 Save Changes</button>
          <button class="logout-btn" onclick="doLogout()">🚪 Logout</button>
        </div>
      </div>

      <div class="account-section">
        <h4>🕐 Recently Watched</h4>
        <div style="color:#aaa;font-size:14px;padding:20px 0;text-align:center">
          ▶ Your watch history will appear here after you start watching movies.
        </div>
      </div>

      <div class="account-section">
        <h4>🔔 Notifications</h4>
        <div style="display:flex;flex-direction:column;gap:12px">
          <label style="display:flex;align-items:center;gap:12px;cursor:pointer;color:#aaa;font-size:14px">
            <input type="checkbox" checked style="accent-color:#FFD700;width:16px;height:16px">
            New movie releases
          </label>
          <label style="display:flex;align-items:center;gap:12px;cursor:pointer;color:#aaa;font-size:14px">
            <input type="checkbox" checked style="accent-color:#FFD700;width:16px;height:16px">
            Subscription renewal reminders
          </label>
          <label style="display:flex;align-items:center;gap:12px;cursor:pointer;color:#aaa;font-size:14px">
            <input type="checkbox" style="accent-color:#FFD700;width:16px;height:16px">
            Promotional offers
          </label>
        </div>
      </div>
    </div>"""


def _build_filter_bar(section_id: str) -> str:
    """Build a reusable filter bar for movie sections."""
    genres = ["All", "Action", "Drama", "Comedy", "Horror", "Romance",
              "Thriller", "Sci-Fi", "Animation", "Adventure"]
    genre_opts = "".join(f'<option value="{g}">{g}</option>' for g in genres)
    return f"""
    <div class="filter-bar">
      <span class="filter-label">🎭 Genre:</span>
      <select class="filter-select" id="filter-genre-{section_id}">{genre_opts}</select>
      <span class="filter-label">⭐ Min Rating:</span>
      <select class="filter-select" id="filter-rating-{section_id}">
        <option value="0">Any</option>
        <option value="5">5+</option>
        <option value="6">6+</option>
        <option value="7">7+</option>
        <option value="8">8+</option>
      </select>
      <input class="filter-search" id="filter-search-{section_id}" placeholder="Search in results..." type="text">
      <button class="filter-btn" onclick="applyFilter('{section_id}')">🔍 Filter</button>
    </div>"""


# ─────────────────────────────────────────────
# Render Application View
# ─────────────────────────────────────────────

def render_app():
    # Fetch all data from TMDB
    genre_map   = get_genres() or {}
    trending    = fetch_trending() or []
    now_playing = fetch_now_playing() or []
    bollywood   = fetch_bollywood() or []
    news_movies = fetch_movie_news() or []

    # Build JS data maps
    all_movies = trending + now_playing + bollywood + news_movies
    movie_map_js = build_movie_data_map_js(all_movies)
    genre_map_js = (
        "window.genreMap = {"
        + ",".join(f'{k}:"{v}"' for k, v in genre_map.items())
        + "};\n"
    )

    # Hero carousel
    hero_slides = "".join(trending_card_html(m, genre_map) for m in trending[:5])
    hero_dots   = "".join(
        f'<div class="hero-dot{"" if i else " active"}" onclick="goHero({i})"></div>'
        for i in range(min(5, len(trending)))
    )
    if not hero_slides:
        hero_slides = """<div class="hero-slide" style="background:#090a0f">
          <div class="hero-overlay"><div class="hero-content">
            <h1 class="hero-title">Welcome to LumaScreen</h1>
            <p class="hero-overview">Set your TMDB_API_KEY to load live movie data.</p>
          </div></div></div>"""
        hero_dots = '<div class="hero-dot active"></div>'

    # Hollywood grid
    hw_cards = "".join(movie_card_html(m, genre_map) for m in now_playing)
    if not hw_cards:
        hw_cards = '<div style="grid-column:1/-1;text-align:center;padding:60px;color:#aaa">⚠️ Add TMDB_API_KEY environment variable to load movies</div>'

    # Bollywood grid
    bw_cards = "".join(movie_card_html(m, genre_map) for m in bollywood)
    if not bw_cards:
        bw_cards = '<div style="grid-column:1/-1;text-align:center;padding:60px;color:#aaa">⚠️ Add TMDB_API_KEY environment variable to load movies</div>'

    # News cards
    news_cards = "".join(news_card_html(m) for m in news_movies)
    if not news_cards:
        news_cards = '<div style="text-align:center;padding:60px;color:#aaa">⚠️ Add TMDB_API_KEY environment variable to load news</div>'

    # Trending row on home
    trending_cards = "".join(movie_card_html(m, genre_map) for m in trending[:8])

    # Pages
    sub_html     = _build_subscription_html()
    account_html = _build_account_html()

    # Filter bars
    hw_filter = _build_filter_bar("hollywood")
    bw_filter = _build_filter_bar("bollywood")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>LumaScreen</title>
  <style>{CSS}</style>
</head>
<body>

<!-- ══════════════════════════════════════════
     SPLASH SCREEN (10 seconds)
══════════════════════════════════════════ -->
<div id="splash">
  <div class="splash-logo-wrap">
    {LOGO_SVG}
    <div class="splash-name">LumaScreen</div>
    <div class="splash-tagline">Watch &bull; Discover &bull; Enjoy</div>
  </div>
  <div class="splash-loader">
    <div class="loader-bar-bg">
      <div class="loader-bar" id="loader-bar"></div>
    </div>
    <div class="loader-text" id="loader-text">Loading movies...</div>
  </div>
</div>

<!-- ══════════════════════════════════════════
     AUTH PAGE (Login + Signup with Eye Toggle)
══════════════════════════════════════════ -->
<div id="auth-page" class="hidden">
  <div class="auth-card">
    <div class="auth-logo">
      {LOGO_SVG_SMALL}
      <span class="auth-logo-name">LumaScreen</span>
      <span class="auth-logo-tag">Watch &bull; Discover &bull; Enjoy</span>
    </div>

    <!-- Login Form -->
    <div id="login-form">
      <div class="auth-title">Welcome Back 👋</div>
      <div class="auth-error" id="login-error"></div>
      <div class="auth-form">
        <div class="form-group">
          <label>Email Address</label>
          <input type="email" id="login-email" placeholder="you@example.com">
        </div>
        <div class="form-group">
          <label>Password</label>
          <div class="password-input-wrap">
            <input type="password" id="login-pass" placeholder="Enter your password"
                   onkeydown="if(event.key==='Enter')doLogin()">
            <button type="button" class="pwd-toggle-btn" onclick="togglePassword('login-pass', this)" title="Show/Hide Password">
              <svg viewBox="0 0 24 24" width="18" height="18" stroke="currentColor" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
            </button>
          </div>
        </div>
        <button class="auth-btn" onclick="doLogin()">🎬 Login to LumaScreen</button>
      </div>
      <div class="auth-switch">
        Don't have an account? <a onclick="showSignup()">Sign Up Free</a>
      </div>
    </div>

    <!-- Signup Form -->
    <div id="signup-form" class="hidden">
      <div class="auth-title">Create Account ✨</div>
      <div class="auth-error" id="signup-error"></div>
      <div class="auth-form">
        <div class="form-group">
          <label>Full Name</label>
          <input type="text" id="signup-name" placeholder="Your full name">
        </div>
        <div class="form-group">
          <label>Email Address</label>
          <input type="email" id="signup-email" placeholder="you@example.com">
        </div>
        <div class="form-group">
          <label>Password</label>
          <div class="password-input-wrap">
            <input type="password" id="signup-pass" placeholder="Min. 6 characters">
            <button type="button" class="pwd-toggle-btn" onclick="togglePassword('signup-pass', this)" title="Show/Hide Password">
              <svg viewBox="0 0 24 24" width="18" height="18" stroke="currentColor" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
            </button>
          </div>
        </div>
        <div class="form-group">
          <label>Confirm Password</label>
          <div class="password-input-wrap">
            <input type="password" id="signup-pass2" placeholder="Repeat password"
                   onkeydown="if(event.key==='Enter')doSignup()">
            <button type="button" class="pwd-toggle-btn" onclick="togglePassword('signup-pass2', this)" title="Show/Hide Password">
              <svg viewBox="0 0 24 24" width="18" height="18" stroke="currentColor" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
            </button>
          </div>
        </div>
        <button class="auth-btn" onclick="doSignup()">🚀 Create Account</button>
      </div>
      <div class="auth-switch">
        Already have an account? <a onclick="showLogin()">Login</a>
      </div>
    </div>
  </div>
</div>

<!-- ══════════════════════════════════════════
     MAIN APP
══════════════════════════════════════════ -->
<div id="main-app">

  <!-- NAVBAR -->
  <nav class="navbar">
    <div class="nav-brand" onclick="showTab('home')">
      {LOGO_SVG_SMALL}
      <span class="nav-brand-name">LumaScreen</span>
    </div>
    <div class="nav-tabs">
      <button class="nav-tab active" id="tab-home" onclick="showTab('home')">
        <svg viewBox="0 0 24 24"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
        Home
      </button>
      <button class="nav-tab" id="tab-hollywood" onclick="showTab('hollywood')">
        <svg viewBox="0 0 24 24"><rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"></rect><line x1="7" y1="2" x2="7" y2="22"></line><line x1="17" y1="2" x2="17" y2="22"></line><line x1="2" y1="12" x2="22" y2="12"></line><line x1="2" y1="7" x2="7" y2="7"></line><line x1="2" y1="17" x2="7" y2="17"></line><line x1="17" y1="17" x2="22" y2="17"></line><line x1="17" y1="7" x2="22" y2="7"></line></svg>
        Hollywood
      </button>
      <button class="nav-tab" id="tab-bollywood" onclick="showTab('bollywood')">
        <svg viewBox="0 0 24 24"><polygon points="23 7 16 12 23 17 23 7"></polygon><rect x="1" y="5" width="15" height="14" rx="2" ry="2"></rect></svg>
        Bollywood
      </button>
      <button class="nav-tab" id="tab-subscription" onclick="showTab('subscription')">
        <svg viewBox="0 0 24 24"><rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect><line x1="1" y1="10" x2="23" y2="10"></line></svg>
        Plans
      </button>
      <button class="nav-tab" id="tab-news" onclick="showTab('news')">
        <svg viewBox="0 0 24 24"><path d="M19 20H5a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v1m2 13a2 2 0 0 1-2-2V7m2 13a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z"></path></svg>
        News
      </button>
      <button class="nav-tab" id="tab-account" onclick="showTab('account')">
        <svg viewBox="0 0 24 24"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
        Account
      </button>
      <button class="nav-tab admin-tab" id="tab-admin" onclick="openAdminPanel()" style="display:none;color:#e50914">
        <svg viewBox="0 0 24 24"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
        Admin
      </button>
    </div>
    <div class="nav-right">
      <div class="nav-search-wrap">
        <svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        <input class="nav-search" id="nav-search-input" type="text" placeholder="Search movies..."
               onkeydown="if(event.key==='Enter')doSearch()">
      </div>
      <button class="nav-user-btn" id="nav-user-btn" onclick="showTab('account')" title="My Account">
        <span id="nav-user-initial">U</span>
      </button>
    </div>
  </nav>

  <!-- ── HOME PAGE ── -->
  <div id="page-home">
    <!-- Hero Carousel -->
    <div class="hero-section">
      {hero_slides}
      <button class="hero-nav-btn hero-prev" onclick="prevHero()">&#8249;</button>
      <button class="hero-nav-btn hero-next" onclick="nextHero()">&#8250;</button>
      <div class="hero-dots">{hero_dots}</div>
    </div>

    <!-- Trending Section -->
    <div class="section-wrap">
      <div class="section-header">
        <div class="section-title">🔥 <span>Trending</span> This Week</div>
        <a class="see-all" onclick="showTab('hollywood')">See All →</a>
      </div>
    </div>
    <div class="movies-grid">{trending_cards}</div>

    <!-- Quick Links -->
    <div class="section-wrap" style="padding-bottom:32px">
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px">
        <div onclick="showTab('hollywood')" style="background:linear-gradient(135deg,#141722,#1d2233);border:1px solid rgba(255,215,0,0.2);border-radius:16px;padding:24px;cursor:pointer;text-align:center;transition:transform 0.2s" onmouseover="this.style.transform='translateY(-4px)'" onmouseout="this.style.transform=''">
          <div style="font-size:36px;margin-bottom:8px">🎥</div>
          <div style="font-weight:700;font-size:16px">Hollywood</div>
          <div style="color:#94a3b8;font-size:13px;margin-top:4px">Latest English Movies</div>
        </div>
        <div onclick="showTab('bollywood')" style="background:linear-gradient(135deg,#141722,#1d2233);border:1px solid rgba(255,215,0,0.2);border-radius:16px;padding:24px;cursor:pointer;text-align:center;transition:transform 0.2s" onmouseover="this.style.transform='translateY(-4px)'" onmouseout="this.style.transform=''">
          <div style="font-size:36px;margin-bottom:8px">🎞️</div>
          <div style="font-weight:700;font-size:16px">Bollywood</div>
          <div style="color:#94a3b8;font-size:13px;margin-top:4px">Latest Hindi Movies</div>
        </div>
        <div onclick="showTab('subscription')" style="background:linear-gradient(135deg,#141722,#1d2233);border:1px solid rgba(255,215,0,0.2);border-radius:16px;padding:24px;cursor:pointer;text-align:center;transition:transform 0.2s" onmouseover="this.style.transform='translateY(-4px)'" onmouseout="this.style.transform=''">
          <div style="font-size:36px;margin-bottom:8px">💳</div>
          <div style="font-weight:700;font-size:16px">Subscribe</div>
          <div style="color:#94a3b8;font-size:13px;margin-top:4px">Plans from ₹199/mo</div>
        </div>
        <div onclick="showTab('news')" style="background:linear-gradient(135deg,#141722,#1d2233);border:1px solid rgba(255,215,0,0.2);border-radius:16px;padding:24px;cursor:pointer;text-align:center;transition:transform 0.2s" onmouseover="this.style.transform='translateY(-4px)'" onmouseout="this.style.transform=''">
          <div style="font-size:36px;margin-bottom:8px">📰</div>
          <div style="font-weight:700;font-size:16px">Movie News</div>
          <div style="color:#94a3b8;font-size:13px;margin-top:4px">Latest from the industry</div>
        </div>
      </div>
    </div>
  </div>

  <!-- ── HOLLYWOOD PAGE ── -->
  <div id="page-hollywood" class="hidden">
    <div class="section-wrap">
      <div class="section-header">
        <div class="section-title">🎥 <span>Hollywood</span> — Now Playing</div>
      </div>
    </div>
    {hw_filter}
    <div class="movies-grid" id="grid-hollywood">{hw_cards}</div>
  </div>

  <!-- ── BOLLYWOOD PAGE ── -->
  <div id="page-bollywood" class="hidden">
    <div class="section-wrap">
      <div class="section-header">
        <div class="section-title">🎞️ <span>Bollywood</span> — Latest Releases</div>
      </div>
    </div>
    {bw_filter}
    <div class="movies-grid" id="grid-bollywood">{bw_cards}</div>
  </div>

  <!-- ── SUBSCRIPTION PAGE ── -->
  <div id="page-subscription" class="hidden">
    {sub_html}
  </div>

  <!-- ── NEWS PAGE ── -->
  <div id="page-news" class="hidden">
    <div class="news-page">
      <div class="section-wrap" style="padding-bottom:24px">
        <div class="section-header">
          <div class="section-title">📰 <span>Movie</span> News &amp; Upcoming</div>
        </div>
      </div>
      <div class="news-grid">{news_cards}</div>
    </div>
  </div>

  <!-- ── ACCOUNT PAGE ── -->
  <div id="page-account" class="hidden">
    {account_html}
  </div>

  <!-- ── SEARCH RESULTS PAGE ── -->
  <div id="page-search-results" class="hidden">
    <div class="search-results-page">
      <h2>🔍 Search Results for <span id="search-query-label"></span></h2>
      <div id="search-results-grid"></div>
    </div>
  </div>

  <!-- ── ADMIN PANEL ── -->
  <div id="page-admin" class="hidden">
    <div class="admin-page">
      <div class="admin-header">
        <h2>🔐 Admin <span>Control Panel</span></h2>
        <p>Manage users, roles, and subscriptions</p>
      </div>

      <!-- Stats Row -->
      <div class="admin-stats">
        <div class="admin-stat-card">
          <div class="admin-stat-num" id="admin-stat-users">0</div>
          <div class="admin-stat-label">👥 Total Users</div>
        </div>
        <div class="admin-stat-card">
          <div class="admin-stat-num" id="admin-stat-admins">0</div>
          <div class="admin-stat-label">🔐 Admins</div>
        </div>
        <div class="admin-stat-card">
          <div class="admin-stat-num" id="admin-stat-premium">0</div>
          <div class="admin-stat-label">👑 Premium</div>
        </div>
        <div class="admin-stat-card">
          <div class="admin-stat-num" id="admin-stat-std">0</div>
          <div class="admin-stat-label">⭐ Standard</div>
        </div>
      </div>

      <!-- Add User Form -->
      <div class="admin-section">
        <h4>➕ Add New User</h4>
        <div class="admin-add-form">
          <input type="text"     id="admin-new-name"  placeholder="Full Name" class="admin-input">
          <input type="email"    id="admin-new-email" placeholder="Email" class="admin-input">
          <input type="password" id="admin-new-pass"  placeholder="Password" class="admin-input">
          <select id="admin-new-plan" class="admin-input">
            <option value="Basic">Basic</option>
            <option value="Standard">Standard</option>
            <option value="Premium">Premium</option>
          </select>
          <select id="admin-new-role" class="admin-input">
            <option value="user">User</option>
            <option value="admin">Admin</option>
          </select>
          <button class="admin-add-btn" onclick="adminAddUser()">➕ Add User</button>
        </div>
      </div>

      <!-- Users Table -->
      <div class="admin-section">
        <h4>👥 All Users</h4>
        <div class="admin-table-wrap">
          <table class="admin-table">
            <thead>
              <tr>
                <th>Name</th><th>Email</th><th>Role</th><th>Plan</th><th>Joined</th><th>Actions</th>
              </tr>
            </thead>
            <tbody id="admin-users-table">
              <tr><td colspan="6" style="text-align:center;color:#aaa;padding:20px">Loading...</td></tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Credentials Info Box -->
      <div class="admin-section">
        <h4>🔑 Default Login Credentials</h4>
        <div class="creds-grid">
          <div class="cred-card admin-cred">
            <div class="cred-role">🔐 ADMIN</div>
            <div class="cred-row"><span>Email:</span><code>admin@lumascreen.com</code></div>
            <div class="cred-row"><span>Password:</span><code>admin123</code></div>
          </div>
          <div class="cred-card user-cred">
            <div class="cred-role">👤 USER</div>
            <div class="cred-row"><span>Email:</span><code>user@lumascreen.com</code></div>
            <div class="cred-row"><span>Password:</span><code>user123</code></div>
          </div>
          <div class="cred-card user-cred">
            <div class="cred-role">👤 USER</div>
            <div class="cred-row"><span>Email:</span><code>priya@lumascreen.com</code></div>
            <div class="cred-row"><span>Password:</span><code>priya123</code></div>
          </div>
          <div class="cred-card user-cred">
            <div class="cred-role">👤 USER</div>
            <div class="cred-row"><span>Email:</span><code>rahul@lumascreen.com</code></div>
            <div class="cred-row"><span>Password:</span><code>rahul123</code></div>
          </div>
        </div>
      </div>
    </div>
  </div>

</div><!-- /main-app -->

<!-- ══════════════════════════════════════════
     MOVIE DETAIL MODAL
══════════════════════════════════════════ -->
<div id="movie-modal" class="modal-overlay hidden" onclick="if(event.target===this)closeModal()">
  <div class="modal-box">
    <div id="modal-body-content"></div>
  </div>
</div>

<!-- ══════════════════════════════════════════
     JAVASCRIPT
══════════════════════════════════════════ -->
<script>
{movie_map_js}
{genre_map_js}
{JS}
</script>

</body>
</html>"""

    # Embed full application in Streamlit view
    components.html(html, height=1200, scrolling=True)


if __name__ == "__main__":
    render_app()