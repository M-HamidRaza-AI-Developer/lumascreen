# 🎬 LumaScreen — Movie & Anime Discovery App

> **Watch • Discover • Enjoy**
> Hollywood, Bollywood & Anime movie discovery platform built with Python & Vanilla JavaScript.

---

## 📁 Project Files

```
lumascreen/
├── generate_index.py    ← Master Python script to generate index.html
├── scripts.py           ← All JavaScript (SPA routing, auth, multi-language, modal)
├── styles.py             ← All CSS styles + SVG logo assets
├── tmdb_helpers.py       ← TMDB API calls + HTML card builders (Trending, Upcoming, etc.)
└── README.md              ← This file
```

---

## 🚀 How to Run Locally in VS Code

### Step 1 — Place all files in one folder

Create a folder called `lumascreen/` and put all 4 core files inside it:

- `generate_index.py`
- `scripts.py`
- `styles.py`
- `tmdb_helpers.py`

### Step 2 — Set your TMDB API Key (optional)

Get a free API key at: [https://www.themoviedb.org/settings/api](https://www.themoviedb.org/settings/api)

**Windows (PowerShell):**
```powershell
$env:TMDB_API_KEY = "your_api_key_here"
```

### Step 3 — Generate and Start Local Server

Open your terminal inside the project folder and run the following commands:

```bash
python generate_index.py
python -m http.server 8000
```

---

## 🔐 Login Credentials

| Role | Email | Password |
|------|-------|----------|
| 🔐 Admin | admin@lumascreen.com | admin123 |
| 👤 User | user@lumascreen.com | user123 |

> You can also click **Sign Up Free** on the login page to register a new account with your own custom name, email, and password.

---

## ✨ Core Features

| Feature | Details |
|---------|---------|
| 🎬 Splash Screen | Animated loading screen with a golden film-reel logo |
| 🔐 Authentication | Secure Login & Sign-up system with persistent session storage |
| 🌐 Multi-Language | Real-time language switcher supporting English, Urdu (اردو), and Hindi (हिंदी) |
| 🗓️ Coming Soon | Real-time upcoming movie listings fetched directly from TMDB with official release dates |
| 🏠 Home Discovery | Auto-rotating hero carousel, trending movies grid, and genre filters |
| 🎥 Categories | Dedicated sections and filters for Hollywood, Bollywood, Anime, and Kids |
| 💳 Subscription Plans | Basic (₹199), Standard (₹499), and Premium (₹999) tiers |
| 👤 Account & Profile | Live profile details, stats, app settings, and secure password update with eye toggle |
| 🔍 Live Search | Instant search dropdown preview and detailed search results page |
| 🎭 Movie Modal | Interactive detail popup featuring cast info, ratings, overview, and video streaming |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend Generator | Python 3.x (Modular HTML generation architecture) |
| Movie Data API | TMDB (The Movie Database) API |
| UI Design | Modern CSS3 (Glassmorphism styling, responsive grids, and clean typography) |
| Client-Side Logic | Vanilla JavaScript (SPA navigation, LocalStorage state management) |