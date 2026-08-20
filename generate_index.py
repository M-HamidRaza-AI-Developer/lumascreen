import os
import webbrowser
from scripts import JS
from styles import CSS, LOGO_SVG, LOGO_SVG_SMALL
from tmdb_helpers import (
    build_movie_data_map_js,
    fetch_anime,
    fetch_bollywood,
    fetch_kids,
    fetch_movie_news,
    fetch_now_playing,
    fetch_trending,
    fetch_upcoming,
    get_genres,
    movie_card_html,
    news_card_html,
    trending_card_html,
)

def _build_subscription_html():
  plans = [
      {
          "icon": "🎬", "name": "Basic", "price": "₹199", "desc": "Perfect for casual movie lovers",
          "features": ["HD Streaming (720p)", "1 Screen at a time", "Hollywood & Bollywood", "Anime & Kids Animation", "Mobile & Tablet"],
          "no": ["4K Ultra HD", "Offline Downloads", "Priority Support"], "featured": False, "badge": None
      },
      {
          "icon": "⭐", "name": "Standard", "price": "₹499", "desc": "Most popular — great value",
          "features": ["Full HD (1080p)", "2 Screens simultaneously", "All Movie Categories", "Offline Downloads", "All Devices"],
          "no": ["4K Ultra HD", "Priority Support"], "featured": True, "badge": "POPULAR"
      },
      {
          "icon": "👑", "name": "Premium", "price": "₹999", "desc": "The ultimate cinema experience",
          "features": ["4K Ultra HD + HDR", "4 Screens simultaneously", "All Categories & Anime", "Unlimited Downloads", "All Devices", "Priority Support", "Early Access"],
          "no": [], "featured": False, "badge": "BEST"
      }
  ]
  cards = ""
  for p in plans:
    feat_li = "".join(f"<li>{f}</li>" for f in p["features"])
    no_li = "".join(f'<li class="no">{f}</li>' for f in p["no"])
    badge = f'<div class="plan-badge">{p["badge"]}</div>' if p["badge"] else ""
    featured_cls = " featured" if p["featured"] else ""
    cards += f"""
        <div class="plan-card{featured_cls}">
          {badge}
          <div class="plan-icon">{p["icon"]}</div>
          <div class="plan-name">{p["name"]}</div>
          <div class="plan-price">{p["price"]}<span>/mo</span></div>
          <div class="plan-desc">{p["desc"]}</div>
          <ul class="plan-features">{feat_li}{no_li}</ul>
          <button class="plan-btn" onclick="subscribePlan('{p['name']}','{p['price']}')">Get {p["name"]}</button>
        </div>"""
  return f"""<div class="sub-page"><div class="sub-header"><h2>Choose Your <span>Plan</span></h2><p>Unlock unlimited movies, series, and exclusive content</p></div><div class="sub-plans">{cards}</div></div>"""

def _build_account_html():
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
        <h4>⚙️ App & Language Settings</h4>
        <div class="edit-form">
          <div class="form-row">
            <div class="form-group">
              <label>🌐 Default App Language</label>
              <select class="settings-select" id="pref-app-lang" onchange="saveAppLanguage(this.value)">
                <option value="en">English</option>
                <option value="ur">Urdu (اردو)</option>
                <option value="hi">Hindi (हिंदी)</option>
              </select>
            </div>
            <div class="form-group">
              <label>🎥 Preferred Video Quality</label>
              <select class="settings-select" id="pref-quality">
                <option value="auto">Auto (Adaptive HD)</option>
                <option value="4k">4K Ultra HD</option>
                <option value="1080p">1080p Full HD</option>
                <option value="720p">720p Data Saver</option>
              </select>
            </div>
          </div>
        </div>
      </div>
      <div class="account-section">
        <h4>✏️ Edit Profile & Password</h4>
        <div class="edit-form">
          <div class="form-row">
            <div class="form-group"><label>Full Name</label><input type="text" id="edit-name" placeholder="Your name"></div>
            <div class="form-group"><label>Email Address</label><input type="email" id="edit-email" placeholder="your@email.com" readonly></div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>New Password</label>
              <div class="password-input-wrap">
                <input type="password" id="edit-pass" placeholder="Leave blank to keep current">
                <button type="button" class="pwd-toggle-btn" onclick="togglePassword('edit-pass', this)" title="Show/Hide Password">
                  <svg viewBox="0 0 24 24"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
                </button>
              </div>
            </div>
            <div class="form-group">
              <label>Confirm New Password</label>
              <div class="password-input-wrap">
                <input type="password" id="edit-pass2" placeholder="Confirm new password">
                <button type="button" class="pwd-toggle-btn" onclick="togglePassword('edit-pass2', this)" title="Show/Hide Password">
                  <svg viewBox="0 0 24 24"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
                </button>
              </div>
            </div>
          </div>
          <div style="margin-top:20px;">
            <button class="save-btn" onclick="saveProfile()">💾 Save Changes</button>
            <button class="logout-btn" onclick="doLogout()">🚪 Logout</button>
          </div>
        </div>
      </div>
    </div>"""

def _build_filter_bar(section_id):
  genres = ["All", "Action", "Drama", "Comedy", "Horror", "Romance", "Thriller", "Sci-Fi", "Animation", "Adventure"]
  genre_opts = "".join(f'<option value="{g}">{g}</option>' for g in genres)
  return f"""<div class="filter-bar"><span class="filter-label">🎭 Genre:</span><select class="filter-select" id="filter-genre-{section_id}">{genre_opts}</select><span class="filter-label">⭐ Min Rating:</span><select class="filter-select" id="filter-rating-{section_id}"><option value="0">Any</option><option value="5">5+</option><option value="6">6+</option><option value="7">7+</option><option value="8">8+</option></select><input class="filter-search" id="filter-search-{section_id}" placeholder="Search in results..." type="text"><button class="filter-btn" onclick="applyFilter('{section_id}')">🔍 Filter</button></div>"""

genre_map = get_genres() or {}
trending = fetch_trending() or []
now_playing = fetch_now_playing() or []
upcoming_movies = fetch_upcoming() or []
bollywood = fetch_bollywood() or []
anime_movies = fetch_anime() or []
kids_movies = fetch_kids() or []
news_movies = fetch_movie_news() or []

all_movies = trending + now_playing + upcoming_movies + bollywood + anime_movies + kids_movies + news_movies
movie_map_js = build_movie_data_map_js(all_movies)
genre_map_js = "window.genreMap = {" + ",".join(f'{k}:"{v}"' for k, v in genre_map.items()) + "};\n"

hero_slides = "".join(trending_card_html(m, genre_map) for m in trending[:6]) or '<div class="hero-slide" style="background:#090a0f;height:350px;display:flex;align-items:center;justify-content:center"><h2>Welcome to LumaScreen</h2></div>'
hero_dots = "".join(f'<div class="hero-dot{"" if i else " active"}" onclick="goHero({i})"></div>' for i in range(min(6, len(trending)))) or '<div class="hero-dot active"></div>'

hw_cards = "".join(movie_card_html(m, genre_map) for m in now_playing) or '<div style="grid-column:1/-1;text-align:center;padding:40px;color:#aaa">No Movies Found</div>'
bw_cards = "".join(movie_card_html(m, genre_map) for m in bollywood) or '<div style="grid-column:1/-1;text-align:center;padding:40px;color:#aaa">No Movies Found</div>'
anime_cards = "".join(movie_card_html(m, genre_map) for m in anime_movies) or '<div style="grid-column:1/-1;text-align:center;padding:40px;color:#aaa">No Anime Found</div>'
kids_cards = "".join(movie_card_html(m, genre_map) for m in kids_movies) or '<div style="grid-column:1/-1;text-align:center;padding:40px;color:#aaa">No Kids Movies Found</div>'

coming_soon_cards = "".join(movie_card_html(m, genre_map) for m in upcoming_movies) or '<div style="text-align:center;padding:40px;color:#aaa">No Upcoming Movies Found</div>'
news_articles_cards = "".join(news_card_html(m) for m in news_movies) or '<div style="text-align:center;padding:40px;color:#aaa">No News Found</div>'

trending_cards = "".join(movie_card_html(m, genre_map) for m in trending)
top_rated_movies = sorted(all_movies, key=lambda x: x.get("vote_average", 0), reverse=True)
top_rated_cards = "".join(movie_card_html(m, genre_map) for m in top_rated_movies)

full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>LumaScreen — Movie & Anime Discovery</title>
  <style>{CSS}</style>
</head>
<body>

<div id="splash">
  <div class="splash-logo-wrap">
    {LOGO_SVG}
    <div class="splash-name">LumaScreen</div>
    <div class="splash-tagline">Watch &bull; Discover &bull; Enjoy</div>
  </div>
  <div class="splash-loader">
    <div class="loader-bar-bg"><div class="loader-bar" id="loader-bar"></div></div>
    <div class="loader-text" id="loader-text">Loading movies & anime...</div>
  </div>
</div>

<div id="auth-page" class="hidden">
  <div class="auth-card">
    <div class="auth-logo">
      {LOGO_SVG_SMALL}
      <span class="auth-logo-name">LumaScreen</span>
      <span class="auth-logo-tag">Watch &bull; Discover &bull; Enjoy</span>
    </div>
    <div id="login-form">
      <div class="auth-title">Welcome Back 👋</div>
      <div class="auth-error" id="login-error"></div>
      <div class="auth-form">
        <div class="form-group"><label>Email Address</label><input type="email" id="login-email" placeholder="you@example.com"></div>
        <div class="form-group">
          <label>Password</label>
          <div class="password-input-wrap">
            <input type="password" id="login-pass" placeholder="Enter your password" onkeydown="if(event.key==='Enter')doLogin()">
            <button type="button" class="pwd-toggle-btn" onclick="togglePassword('login-pass', this)" title="Show/Hide Password">
              <svg viewBox="0 0 24 24"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
            </button>
          </div>
        </div>
        <button class="auth-btn" onclick="doLogin()">🎬 Login to LumaScreen</button>
      </div>
      <div class="auth-switch">Don't have an account? <a onclick="showSignup()">Sign Up Free</a></div>
    </div>
    <div id="signup-form" class="hidden">
      <div class="auth-title">Create Account ✨</div>
      <div class="auth-error" id="signup-error"></div>
      <div class="auth-form">
        <div class="form-group"><label>Full Name</label><input type="text" id="signup-name" placeholder="Your full name"></div>
        <div class="form-group"><label>Email Address</label><input type="email" id="signup-email" placeholder="you@example.com"></div>
        <div class="form-group">
          <label>Password</label>
          <div class="password-input-wrap">
            <input type="password" id="signup-pass" placeholder="Min. 6 characters">
            <button type="button" class="pwd-toggle-btn" onclick="togglePassword('signup-pass', this)" title="Show/Hide Password">
              <svg viewBox="0 0 24 24"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
            </button>
          </div>
        </div>
        <div class="form-group">
          <label>Confirm Password</label>
          <div class="password-input-wrap">
            <input type="password" id="signup-pass2" placeholder="Repeat password" onkeydown="if(event.key==='Enter')doSignup()">
            <button type="button" class="pwd-toggle-btn" onclick="togglePassword('signup-pass2', this)" title="Show/Hide Password">
              <svg viewBox="0 0 24 24"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
            </button>
          </div>
        </div>
        <button class="auth-btn" onclick="doSignup()">🚀 Create Account</button>
      </div>
      <div class="auth-switch">Already have an account? <a onclick="showLogin()">Login</a></div>
    </div>
  </div>
</div>

<div id="main-app">
  <nav class="navbar">
    <div class="nav-brand" onclick="showTab('home')">
      {LOGO_SVG_SMALL}
      <span class="nav-brand-name">LumaScreen</span>
    </div>
    <div class="nav-tabs">
      <button class="nav-tab active" id="tab-home" onclick="showTab('home')">Home</button>
      <button class="nav-tab" id="tab-hollywood" onclick="showTab('hollywood')">Hollywood</button>
      <button class="nav-tab" id="tab-bollywood" onclick="showTab('bollywood')">Bollywood</button>
      <button class="nav-tab" id="tab-anime" onclick="showTab('anime')">Anime</button>
      <button class="nav-tab" id="tab-kids" onclick="showTab('kids')">Kids</button>
      <button class="nav-tab" id="tab-subscription" onclick="showTab('subscription')">Plans</button>
      <button class="nav-tab" id="tab-news" onclick="showTab('news')">News</button>
      <button class="nav-tab" id="tab-account" onclick="showTab('account')">Account</button>
    </div>
    <div class="nav-right">
      <div class="nav-search-wrap">
        <svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        <input class="nav-search" id="nav-search-input" placeholder="Search movies..." onkeydown="if(event.key==='Enter')doSearch()">
      </div>
      <button class="nav-user-btn" id="nav-user-btn" onclick="showTab('account')" title="Account Profile">
        <span id="nav-user-initial">U</span>
      </button>
    </div>
  </nav>

  <!-- TOP QUICK-SWITCH BAR WITH BACK ARROW -->
  <div class="top-quick-bar">
    <button class="back-arrow-btn" onclick="goBack()" title="Go Back">‹</button>
    <div class="quick-pill" onclick="showTab('home')">🏠 Home</div>
    <div class="quick-pill" onclick="filterByGenreName('Action')">🔥 Action</div>
    <div class="quick-pill" onclick="filterByGenreName('Comedy')">🎟️ Comedy</div>
    <div class="quick-pill" onclick="filterByGenreName('Horror')">💀 Horror</div>
    <div class="quick-pill" onclick="filterByGenreName('Romance')">💖 Romance</div>
    <div class="quick-pill" onclick="filterByGenreName('Sci-Fi')">🌌 Sci-Fi</div>
    <div class="quick-pill" onclick="filterByGenreName('Thriller')">⚡ Thriller</div>
    <div class="quick-pill" onclick="filterByGenreName('Animation')">✨ Animation</div>
    <div class="quick-pill" onclick="filterByGenreName('Drama')">🎭 Drama</div>
    <div class="quick-pill" onclick="showTab('hollywood')">🎥 Hollywood</div>
    <div class="quick-pill" onclick="showTab('bollywood')">🎞️ Bollywood</div>
    <div class="quick-pill" onclick="filterByGenreName('Animation')">⚡ Anime</div>
    <div class="quick-pill" onclick="showTab('kids')">🎈 Kids</div>
  </div>

  <!-- HOME PAGE -->
  <div id="page-home">
    <div class="hero-section">
      {hero_slides}
      <button class="hero-nav-btn hero-prev" onclick="prevHero()">&#8249;</button>
      <button class="hero-nav-btn hero-next" onclick="nextHero()">&#8250;</button>
      <div class="hero-dots">{hero_dots}</div>
    </div>

    <!-- 1. GENRES SECTION -->
    <div class="section-wrap">
      <div class="section-header"><div class="section-title">🎭 <span>Explore</span> Genres</div></div>
      <div style="display:flex; gap:15px; flex-wrap:wrap; padding:10px 0 20px;">
        <button class="genre-pill" onclick="filterByGenreName('Action')">🔥 Action</button>
        <button class="genre-pill" onclick="filterByGenreName('Comedy')">🎟️ Comedy</button>
        <button class="genre-pill" onclick="filterByGenreName('Horror')">💀 Horror</button>
        <button class="genre-pill" onclick="filterByGenreName('Romance')">💖 Romance</button>
        <button class="genre-pill" onclick="filterByGenreName('Sci-Fi')">🌌 Sci-Fi</button>
        <button class="genre-pill" onclick="filterByGenreName('Thriller')">⚡ Thriller</button>
        <button class="genre-pill" onclick="filterByGenreName('Animation')">✨ Animation</button>
        <button class="genre-pill" onclick="filterByGenreName('Drama')">🎭 Drama</button>
      </div>
    </div>

    <!-- 2. CONTINUE WATCHING -->
    <div class="section-wrap" id="continue-watching-section" style="display:none;">
      <div class="section-header"><div class="section-title">▶️ <span>Continue</span> Watching</div></div>
      <div class="slider-container">
        <button class="slider-arrow arrow-left" onclick="slideRow('continue-slider', -1)">&#8249;</button>
        <div class="movies-slider" id="continue-slider"></div>
        <button class="slider-arrow arrow-right" onclick="slideRow('continue-slider', 1)">&#8250;</button>
      </div>
    </div>

    <!-- 3. COMING SOON SECTION -->
    <div class="section-wrap">
      <div class="section-header"><div class="section-title">🗓️ <span>Coming</span> Soon</div></div>
    </div>
    <div class="slider-container">
      <button class="slider-arrow arrow-left" onclick="slideRow('coming-soon-slider', -1)">&#8249;</button>
      <div class="movies-slider" id="coming-soon-slider">{coming_soon_cards}</div>
      <button class="slider-arrow arrow-right" onclick="slideRow('coming-soon-slider', 1)">&#8250;</button>
    </div>

    <!-- 4. TRENDING MOVIES -->
    <div class="section-wrap">
      <div class="section-header"><div class="section-title">🔥 <span>Trending</span> Movies</div></div>
    </div>
    <div class="slider-container">
      <button class="slider-arrow arrow-left" onclick="slideRow('trending-slider', -1)">&#8249;</button>
      <div class="movies-slider" id="trending-slider">{trending_cards}</div>
      <button class="slider-arrow arrow-right" onclick="slideRow('trending-slider', 1)">&#8250;</button>
    </div>

    <!-- 5. TOP RATED CINEMA -->
    <div class="section-wrap">
      <div class="section-header"><div class="section-title">⭐ <span>Top Rated</span> Cinema</div></div>
    </div>
    <div class="slider-container">
      <button class="slider-arrow arrow-left" onclick="slideRow('home-top-rated-grid', -1)">&#8249;</button>
      <div class="movies-slider" id="home-top-rated-grid">{top_rated_cards}</div>
      <button class="slider-arrow arrow-right" onclick="slideRow('home-top-rated-grid', 1)">&#8250;</button>
    </div>

    <!-- 6. NEWSLETTER / CTA & FULL FOOTER -->
    <div class="cta-newsletter">
      <h3>Get Notified About New Movies 📬</h3>
      <p>Subscribe to our newsletter and never miss Hollywood, Bollywood & Anime releases.</p>
      <div class="cta-form">
        <input type="email" class="cta-input" id="newsletter-email" placeholder="Enter your email address...">
        <button class="cta-btn" onclick="showToast('🎉 Subscribed successfully!')">Subscribe</button>
      </div>
    </div>

    <div class="luma-footer-wrap">
      <div class="luma-banner">
        <svg viewBox="0 0 24 24"><path d="M4 6H20V9H13V19H9V9H4V6Z"/></svg>
        <span>Read about LumaScreen originals, anime, and watch exclusive trailers on <a href="javascript:void(0)" onclick="showTab('news')">LumaScreen.com</a>.</span>
      </div>
      <div class="luma-join-wrap">
        <button class="luma-join-btn" onclick="showTab('subscription')">Join Now</button>
      </div>
      <footer class="luma-footer">
        <div style="margin-bottom: 24px;">
          <div style="display: inline-flex; align-items: center; background: rgba(255,255,255,0.07); border: 1px solid rgba(255,255,255,0.15); border-radius: 6px; padding: 8px 14px; cursor: pointer;">
            <span style="margin-right: 8px; font-size: 14px;">🌐</span>
            <select id="footer-lang-select" onchange="saveAppLanguage(this.value)" style="background: transparent; color: #fff; border: none; outline: none; font-size: 14px; cursor: pointer;">
              <option value="en" style="background: #141722; color: #fff;">English</option>
              <option value="ur" style="background: #141722; color: #fff;">Urdu (اردو)</option>
              <option value="hi" style="background: #141722; color: #fff;">Hindi (हिंदी)</option>
            </select>
          </div>
        </div>

        <div class="luma-footer-contact"><a href="javascript:void(0)" onclick="showToast('📞 Support: support@lumascreen.com')">Questions? Contact us.</a></div>
        <div class="luma-links-grid">
          <a href="javascript:void(0)" onclick="showTab('home')">FAQ</a>
          <a href="javascript:void(0)" onclick="showTab('news')">Help Center</a>
          <a href="javascript:void(0)" onclick="showTab('account')">Account</a>
          <a href="javascript:void(0)" onclick="showTab('news')">Media Center</a>
          <a href="javascript:void(0)">Investor Relations</a>
          <a href="javascript:void(0)">Jobs</a>
          <a href="javascript:void(0)" onclick="showTab('home')">Ways to Watch</a>
          <a href="javascript:void(0)">Terms of Use</a>
          <a href="javascript:void(0)">Privacy</a>
          <a href="javascript:void(0)" onclick="showTab('account')">Cookie Preferences</a>
          <a href="javascript:void(0)">Corporate Information</a>
          <a href="javascript:void(0)" onclick="showToast('📞 Support: support@lumascreen.com')">Contact Us</a>
        </div>
        
        <div style="margin-top: 24px; color: #777; font-size: 14px;">
          LumaScreen Pakistan
        </div>

        <div style="margin-top: 12px; color: #555; font-size: 12px;">
          © 2026 LumaScreen Inc. All rights reserved.
        </div>
      </footer>
    </div>
  </div>

  <div id="page-hollywood" class="hidden"><div class="section-wrap"><div class="section-title">🎥 <span>Hollywood</span> Movies</div></div>{_build_filter_bar("hollywood")}<div class="movies-grid" style="margin-top:20px">{hw_cards}</div></div>
  <div id="page-bollywood" class="hidden"><div class="section-wrap"><div class="section-title">🎞️ <span>Bollywood</span> Movies</div></div>{_build_filter_bar("bollywood")}<div class="movies-grid" style="margin-top:20px">{bw_cards}</div></div>
  <div id="page-anime" class="hidden"><div class="section-wrap"><div class="section-title">⚡ <span>Anime</span> Animation</div></div>{_build_filter_bar("anime")}<div class="movies-grid" style="margin-top:20px">{anime_cards}</div></div>
  <div id="page-kids" class="hidden"><div class="section-wrap"><div class="section-title">🎈 <span>Kids & Family</span></div></div>{_build_filter_bar("kids")}<div class="movies-grid" style="margin-top:20px">{kids_cards}</div></div>
  <div id="page-subscription" class="hidden">{_build_subscription_html()}</div>
  <div id="page-news" class="hidden"><div class="news-page"><div class="section-wrap"><div class="section-title">📰 <span>Movie</span> News & Articles</div></div><div class="movies-grid" style="margin-top:20px">{news_articles_cards}</div></div></div>
  <div id="page-account" class="hidden">{_build_account_html()}</div>
  <div id="page-search-results" class="hidden"><div class="search-results-page"><h2>Search Results for <span id="search-query-label"></span></h2><div id="search-results-grid"></div></div></div>
</div>

<div id="movie-modal" class="modal-overlay hidden" onclick="if(event.target===this)closeModal()">
  <div class="modal-box"><div id="modal-body-content"></div></div>
</div>

<script>
{movie_map_js}
{genre_map_js}
{JS}
</script>
</body>
</html>"""

with open("index.html", "w", encoding="utf-8") as f:
  f.write(full_html)

print("Generated index.html successfully with language selector footer and LumaScreen Pakistan!")
webbrowser.open("file://" + os.path.realpath("index.html"))