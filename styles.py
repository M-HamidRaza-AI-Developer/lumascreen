"""LumaScreen — Professional CSS styles and SVG logo assets."""

LOGO_SVG = """<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg" class="splash-svg">
  <defs>
    <radialGradient id="splashGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FFD700" stop-opacity="0.5"/>
      <stop offset="100%" stop-color="#FFD700" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="splashGold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFF3B0"/>
      <stop offset="50%" stop-color="#FFD700"/>
      <stop offset="100%" stop-color="#FF9900"/>
    </linearGradient>
  </defs>
  <circle cx="60" cy="60" r="58" fill="url(#splashGlow)"/>
  <circle cx="60" cy="60" r="48" fill="#12131A" stroke="url(#splashGold)" stroke-width="4"/>
  <circle cx="60" cy="60" r="28" fill="none" stroke="url(#splashGold)" stroke-width="2" stroke-dasharray="6 6" opacity="0.7"/>
  <circle cx="60" cy="60" r="12" fill="url(#splashGold)"/>
</svg>"""

LOGO_SVG_SMALL = """<svg width="34" height="34" viewBox="0 0 34 34" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle; filter: drop-shadow(0 0 10px rgba(255, 215, 0, 0.7));">
  <circle cx="17" cy="17" r="15" fill="#181A24" stroke="#FFD700" stroke-width="2.5"/>
  <circle cx="17" cy="17" r="8" fill="none" stroke="#FFF099" stroke-width="1.5" stroke-dasharray="3 3"/>
  <circle cx="17" cy="17" r="4" fill="#FFD700"/>
</svg>"""
CSS = """
* { margin:0; padding:0; box-sizing:border-box; }
:root {
  --bg:#090a0f; --bg2:#11131a; --bg3:#181a24;
  --gold:#FFD700; --gold2:#FFA500;
  --text:#FFFFFF; --text2:#94a3b8;
  --card-bg:#141722; --accent:#e50914; --radius:12px;
}
body { background:var(--bg); color:var(--text); font-family:'Segoe UI',Roboto,Helvetica,Arial,sans-serif; overflow-x:hidden; }
.hidden { display:none !important; }

#splash {
  position:fixed; inset:0; background:var(--bg);
  display:flex; flex-direction:column; align-items:center; justify-content:center;
  z-index:9999; transition:opacity 0.8s ease;
}
.splash-logo-wrap { text-align:center; animation:fadeInUp 1s ease; }
.splash-svg { width:120px; height:120px; margin-bottom:20px; filter:drop-shadow(0 0 24px rgba(255, 215, 0, 0.6)); }
.splash-name {
  font-size:52px; font-weight:900; letter-spacing:4px;
  background:linear-gradient(135deg,#FFF099,#FFD700,#FFA500);
  -webkit-background-clip:text; -webkit-text-fill-color:transparent;
}
.splash-tagline { color:var(--text2); font-size:13px; letter-spacing:6px; margin-top:8px; text-transform:uppercase; font-weight:600; }
.splash-loader { margin-top:50px; width:280px; }
.loader-bar-bg { background:rgba(255,255,255,0.08); border-radius:50px; height:5px; overflow:hidden; }
.loader-bar { height:5px; border-radius:50px; background:linear-gradient(90deg,#FFF099,#FFD700,#FFA500); width:0%; transition:width 0.1s linear; }
.loader-text { color:var(--text2); font-size:13px; text-align:center; margin-top:12px; letter-spacing:1px; }

#auth-page {
  min-height:100vh; display:flex; align-items:center; justify-content:center;
  background:radial-gradient(ellipse at center, #1a1a2e 0%, #090a0f 75%);
}
.auth-card {
  background:rgba(20, 23, 34, 0.85); backdrop-filter:blur(20px); border-radius:24px; padding:48px 40px;
  width:100%; max-width:420px; box-shadow:0 24px 60px rgba(0,0,0,0.6);
  border:1px solid rgba(255,215,0,0.2);
}
.auth-logo { text-align:center; margin-bottom:32px; }
.auth-logo-name {
  font-size:28px; font-weight:900; letter-spacing:2px;
  background:linear-gradient(135deg,#FFF099,#FFD700);
  -webkit-background-clip:text; -webkit-text-fill-color:transparent;
  display:block; margin-top:8px;
}
.auth-logo-tag { color:var(--text2); font-size:11px; letter-spacing:4px; display:block; margin-top:4px; font-weight:600; }
.auth-title { font-size:22px; font-weight:700; margin-bottom:24px; }
.auth-form .form-group { margin-bottom:18px; }
.auth-form label { display:block; color:var(--text2); font-size:13px; margin-bottom:6px; font-weight:500; }
.auth-form input {
  width:100%; padding:13px 16px; background:#0d0f17; border:1px solid rgba(255,255,255,0.1);
  border-radius:10px; color:var(--text); font-size:15px; outline:none; transition:border-color 0.2s;
}
.auth-form input:focus { border-color:var(--gold); }

.password-input-wrap { position: relative; display: flex; align-items: center; width: 100%; }
.password-input-wrap input { width: 100%; padding-right: 44px !important; }
.pwd-toggle-btn {
  position: absolute; right: 12px; background: transparent; border: none; cursor: pointer; color: var(--text2);
  display: flex; align-items: center; justify-content: center; padding: 4px;
}
.pwd-toggle-btn:hover { color: var(--gold); }
.pwd-toggle-btn svg { width: 18px; height: 18px; stroke: currentColor; fill: none; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }

.auth-btn {
  width:100%; padding:14px; background:linear-gradient(135deg,#FFF099,#FFD700,#FFA500);
  border:none; border-radius:10px; color:#000; font-size:16px; font-weight:700;
  cursor:pointer; margin-top:8px; letter-spacing:0.5px;
}
.auth-switch { text-align:center; margin-top:20px; color:var(--text2); font-size:14px; }
.auth-switch a { color:var(--gold); text-decoration:none; font-weight:600; cursor:pointer; }
.auth-error { background:rgba(229,9,20,0.15); border:1px solid #e50914; border-radius:8px; padding:10px 14px; color:#ff6b6b; font-size:13px; margin-bottom:16px; display:none; }

#main-app { display:none; min-height:100vh; }

.navbar {
  position:sticky; top:0; z-index:1000;
  background:rgba(9, 10, 15, 0.85); backdrop-filter:blur(16px);
  border-bottom:1px solid rgba(255,215,0,0.12);
  padding:0 28px; height:68px; display:flex; align-items:center; justify-content:space-between;
}
.nav-brand { display:flex; align-items:center; gap:12px; cursor:pointer; }
.nav-brand-name {
  font-size:22px; font-weight:900; letter-spacing:1px;
  background:linear-gradient(135deg,#FFF099,#FFD700,#FFA500);
  -webkit-background-clip:text; -webkit-text-fill-color:transparent;
}
.nav-tabs {
  display:flex; align-items:center; gap:6px;
  background:rgba(255,255,255,0.03); padding:4px; border-radius:12px;
  border:1px solid rgba(255,255,255,0.06);
}
.nav-tab {
  display:inline-flex; align-items:center; gap:8px;
  padding:8px 16px; border-radius:8px; cursor:pointer; font-size:13px; font-weight:600;
  color:var(--text2); border:none; background:transparent; transition:all 0.2s;
}
.nav-tab svg { width:16px; height:16px; stroke:currentColor; fill:none; stroke-width:2; stroke-linecap:round; stroke-linejoin:round; }
.nav-tab:hover { color:#fff; background:rgba(255,255,255,0.06); }
.nav-tab.active {
  color:#090a0f; background:linear-gradient(135deg,#FFF099,#FFD700);
  font-weight:700; box-shadow:0 2px 12px rgba(255,215,0,0.35);
}
.nav-tab.active svg { stroke:#090a0f; }
.nav-right { display:flex; align-items:center; gap:16px; }

.nav-search-wrap { position:relative; display:flex; align-items:center; }
.nav-search-wrap svg { position:absolute; left:12px; width:16px; height:16px; stroke:var(--text2); fill:none; stroke-width:2; pointer-events:none; }
.nav-search {
  background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.1); border-radius:20px;
  padding:8px 14px 8px 36px; color:var(--text); font-size:13px; width:210px; outline:none; transition:all 0.3s;
}
.nav-search:focus { border-color:var(--gold); width:270px; background:rgba(255,255,255,0.08); }

.nav-user-btn {
  width: 36px; height: 36px; border-radius: 50%; background: linear-gradient(135deg,#FFF099,#FFD700,#FFA500);
  border: 2px solid rgba(255,215,0,0.4); cursor: pointer; display: flex; align-items: center; justify-content: center;
  color: #000; font-weight: 900; font-size: 14px; transition: transform 0.2s, box-shadow 0.2s;
}
.nav-user-btn:hover { transform: scale(1.08); box-shadow: 0 0 12px rgba(255,215,0,0.5); }

.search-dropdown {
  position: absolute;
  top: calc(100% + 12px);
  right: 0;
  width: 340px;
  background: #141722;
  border: 1px solid rgba(255, 215, 0, 0.3);
  border-radius: 14px;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.85);
  backdrop-filter: blur(16px);
  z-index: 99999;
  overflow: hidden;
  display: none;
}
.search-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  cursor: pointer;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  transition: background 0.2s ease;
}
.search-item:last-child { border-bottom: none; }
.search-item:hover { background: rgba(255, 215, 0, 0.12); }

.top-quick-bar {
  background: rgba(20, 23, 34, 0.95);
  border-bottom: 1px solid rgba(255,215,0,0.15);
  padding: 10px 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  overflow-x: auto;
  white-space: nowrap;
  position: sticky;
  top: 68px;
  z-index: 999;
  backdrop-filter: blur(10px);
}
.top-quick-bar::-webkit-scrollbar { display: none; }
.back-arrow-btn {
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,215,0,0.3);
  color: var(--gold);
  width: 32px;
  height: 32px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  flex-shrink: 0;
  transition: all 0.2s;
}
.back-arrow-btn:hover { background: var(--gold); color: #000; }
.quick-pill {
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  color: var(--text2);
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}
.quick-pill:hover { background: rgba(255,215,0,0.15); color: var(--gold); border-color: rgba(255,215,0,0.3); }

.hero-section { position:relative; height:520px; overflow:hidden; background:#090a0f; }
.hero-slide { position:absolute; inset:0; background-size:cover; background-position:center top; transition:opacity 0.8s ease; opacity:0; }
.hero-slide.active-slide { opacity:1; z-index:1; }
.hero-overlay {
  position:absolute; inset:0;
  background:linear-gradient(to right,rgba(9,10,15,0.96) 30%,rgba(9,10,15,0.2) 100%);
  display:flex; align-items:center;
}
.hero-content { padding:0 60px; max-width:620px; }
.hero-genres { margin-bottom:12px; display:flex; gap:6px; flex-wrap:wrap; }
.hero-title { font-size:42px; font-weight:900; line-height:1.1; margin-bottom:12px; }
.hero-rating { margin-bottom:12px; font-weight:700; color:var(--gold); }
.hero-overview { color:var(--text2); font-size:14px; line-height:1.6; margin-bottom:24px; }
.hero-btn {
  padding:14px 32px; background:linear-gradient(135deg,#FFF099,#FFD700,#FFA500);
  border:none; border-radius:10px; color:#000; font-size:15px; font-weight:700;
  cursor:pointer; transition:transform 0.2s,box-shadow 0.2s;
}
.hero-btn:hover { transform:translateY(-2px); box-shadow:0 8px 25px rgba(255,215,0,0.4); }
.hero-dots { position:absolute; bottom:20px; left:50%; transform:translateX(-50%); display:flex; gap:8px; z-index:2; }
.hero-dot { width:8px; height:8px; border-radius:50%; background:rgba(255,255,255,0.3); cursor:pointer; transition:all 0.2s; }
.hero-dot.active { background:var(--gold); width:24px; border-radius:4px; }
.hero-nav-btn {
  position:absolute; top:50%; transform:translateY(-50%);
  background:rgba(0,0,0,0.5); border:1px solid rgba(255,215,0,0.3);
  color:var(--gold); width:44px; height:44px; border-radius:50%; cursor:pointer;
  font-size:20px; display:flex; align-items:center; justify-content:center; transition:all 0.2s; z-index:2;
}
.hero-nav-btn:hover { background:rgba(255,215,0,0.2); }
.hero-prev { left:20px; }
.hero-next { right:20px; }

.section-wrap { padding:36px 32px 0; }
.section-header { display:flex; align-items:center; justify-content:space-between; margin-bottom:20px; }
.section-title { font-size:22px; font-weight:800; letter-spacing:-0.3px; }
.section-title span { color:var(--gold); }

.slider-container { position: relative; display: flex; align-items: center; margin-bottom: 24px; }
.movies-slider { display: flex; gap: 16px; overflow-x: auto; scroll-behavior: smooth; padding: 10px 32px 20px; width: 100%; }
.movies-slider::-webkit-scrollbar { display: none; }
.movies-slider .movie-card { min-width: 180px; max-width: 180px; flex-shrink: 0; }
.slider-arrow {
  position: absolute; top: 45%; transform: translateY(-50%); width: 42px; height: 42px;
  background: rgba(9, 10, 15, 0.9); border: 1px solid rgba(255, 215, 0, 0.4); color: var(--gold);
  border-radius: 50%; cursor: pointer; z-index: 10; display: flex; align-items: center; justify-content: center; font-size: 22px; transition: all 0.2s;
}
.slider-arrow:hover { background: var(--gold); color: #000; box-shadow: 0 0 15px rgba(255, 215, 0, 0.6); }
.arrow-left { left: 8px; }
.arrow-right { right: 8px; }

.genre-pill {
  background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);
  padding: 12px 24px; border-radius: 12px; color: #fff; font-weight: 600; cursor: pointer;
  display: inline-flex; align-items: center; gap: 10px; transition: 0.3s; white-space: nowrap;
  font-family: inherit; font-size: 14px; user-select: none;
}
.genre-pill:hover { background: var(--gold); color: #000; transform: translateY(-4px); }

.movies-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(175px,1fr)); gap:20px; padding:0 32px 32px; }
.movie-card {
  background:var(--card-bg); border-radius:var(--radius); overflow:hidden;
  cursor:pointer; transition:transform 0.25s,box-shadow 0.25s,border-color 0.25s; border:1px solid rgba(255,255,255,0.06);
}
.movie-card:hover { transform:translateY(-6px) scale(1.02); box-shadow:0 16px 35px rgba(0,0,0,0.6); border-color:rgba(255,215,0,0.4); }
.card-poster-wrap { position:relative; aspect-ratio:2/3; overflow:hidden; background:#0c0d12; }
.card-poster-wrap img { width:100%; height:100%; object-fit:cover; transition:transform 0.3s; }
.movie-card:hover .card-poster-wrap img { transform:scale(1.05); }
.rating-badge {
  position:absolute; top:8px; right:8px; padding:3px 8px;
  border-radius:20px; font-size:11px; font-weight:700; color:#fff; background:rgba(0,0,0,0.7); backdrop-filter:blur(4px);
}
.card-info { padding:12px; }
.card-title { font-size:13px; font-weight:700; margin-bottom:4px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.card-year { color:var(--text2); font-size:11px; margin-bottom:6px; }
.card-genres { display:flex; flex-wrap:wrap; gap:4px; margin-bottom:6px; }
.genre-tag { background:rgba(255,215,0,0.1); color:var(--gold); font-size:10px; padding:2px 7px; border-radius:20px; border:1px solid rgba(255,215,0,0.2); }
.card-overview { color:var(--text2); font-size:11px; line-height:1.4; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; }

.account-page { padding: 40px 32px; max-width: 800px; margin: 0 auto; }
.profile-card { background: var(--card-bg); border-radius: 20px; padding: 32px; border: 1px solid rgba(255,215,0,0.2); margin-bottom: 24px; display: flex; align-items: center; gap: 24px; }
.profile-avatar { width: 80px; height: 80px; border-radius: 50%; background: linear-gradient(135deg,#FFF099,#FFD700); display: flex; align-items: center; justify-content: center; font-size: 32px; font-weight: 900; color: #000; flex-shrink: 0; }
.profile-info h3 { font-size: 22px; font-weight: 700; margin-bottom: 4px; color: #fff; }
.profile-info p { color: var(--text2); font-size: 14px; }
.profile-badge { display: inline-block; background: rgba(255,215,0,0.1); color: var(--gold); border: 1px solid rgba(255,215,0,0.3); padding: 3px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; margin-top: 8px; }
.account-section { background: var(--card-bg); border-radius: 16px; padding: 24px; margin-bottom: 20px; border: 1px solid rgba(255,215,0,0.1); }
.account-section h4 { font-size: 16px; font-weight: 700; margin-bottom: 16px; color: var(--gold); }
.stats-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
.stat-card { background: #0d0f17; border-radius: 12px; padding: 20px; text-align: center; border: 1px solid rgba(255,215,0,0.05); }
.stat-num { font-size: 28px; font-weight: 900; color: var(--gold); }
.stat-label { color: var(--text2); font-size: 12px; margin-top: 4px; }
.edit-form .form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px; }
.edit-form .form-group { display: flex; flex-direction: column; gap: 6px; }
.edit-form label { color: var(--text2); font-size: 13px; font-weight: 500; }
.edit-form input { background: #0d0f17; border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; color: var(--text); padding: 10px 14px; font-size: 14px; outline: none; }
.edit-form input:focus { border-color: var(--gold); }
.settings-select { background: #0d0f17; border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px; color: var(--text); padding: 10px 14px; font-size: 14px; outline: none; width: 100%; cursor: pointer; }
.save-btn { padding: 10px 28px; background: linear-gradient(135deg,#FFF099,#FFD700); border: none; border-radius: 8px; color: #000; font-size: 14px; font-weight: 700; cursor: pointer; }
.logout-btn { padding: 10px 28px; background: transparent; border: 2px solid #e50914; border-radius: 8px; color: #e50914; font-size: 14px; font-weight: 700; cursor: pointer; margin-left: 12px; }
.logout-btn:hover { background: #e50914; color: #fff; }

.sub-page { padding:40px 32px; max-width:960px; margin:0 auto; }
.sub-header { text-align:center; margin-bottom:48px; }
.sub-header h2 { font-size:36px; font-weight:900; margin-bottom:12px; }
.sub-header h2 span { color:var(--gold); }
.sub-header p { color:var(--text2); font-size:15px; }
.sub-plans { display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:24px; }
.plan-card { background:var(--card-bg); border-radius:20px; padding:36px 28px; border:1px solid rgba(255,215,0,0.15); transition:all 0.3s; position:relative; overflow:hidden; text-align:center; }
.plan-card.featured { border-color:var(--gold); background:linear-gradient(135deg,#141722,#1d2233); }
.plan-badge { position:absolute; top:16px; right:16px; background:linear-gradient(135deg,#FFF099,#FFD700); color:#000; font-size:11px; font-weight:800; padding:4px 12px; border-radius:20px; }
.plan-name { font-size:22px; font-weight:800; margin-bottom:8px; }
.plan-price { font-size:40px; font-weight:900; color:var(--gold); margin-bottom:4px; }
.plan-price span { font-size:16px; color:var(--text2); font-weight:400; }
.plan-desc { color:var(--text2); font-size:13px; margin-bottom:24px; }
.plan-features { list-style:none; margin-bottom:28px; text-align:left; }
.plan-features li { padding:8px 0; border-bottom:1px solid rgba(255,255,255,0.05); font-size:14px; color:var(--text2); }
.plan-features li::before { content:"✓ "; color:var(--gold); font-weight:700; }
.plan-features li.no::before { content:"✗ "; color:#555; }
.plan-features li.no { color:#555; }
.plan-btn { width:100%; padding:14px; border-radius:10px; font-size:15px; font-weight:700; cursor:pointer; background:var(--gold); border:none; color:#000; }

.cta-newsletter {
  background: linear-gradient(135deg, #141722, #1a1e2e);
  border: 1px solid rgba(255, 215, 0, 0.25); border-radius: 20px; padding: 48px 32px; margin: 60px 32px 20px; text-align: center; box-shadow: 0 16px 40px rgba(0,0,0,0.5);
}
.cta-newsletter h3 {
  font-size: 28px; font-weight: 900; margin-bottom: 10px;
  background: linear-gradient(135deg, #FFF099, #FFD700); -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.cta-newsletter p { color: var(--text2); font-size: 14px; margin-bottom: 24px; }
.cta-form { display: flex; gap: 12px; max-width: 480px; margin: 0 auto; justify-content: center; }
.cta-input {
  flex: 1; padding: 12px 18px; background: #0d0f17; border: 1px solid rgba(255,255,255,0.15);
  border-radius: 10px; color: #fff; font-size: 14px; outline: none;
}
.cta-input:focus { border-color: var(--gold); }
.cta-btn {
  padding: 12px 28px; background: linear-gradient(135deg, #FFF099, #FFD700);
  border: none; border-radius: 10px; color: #000; font-weight: 800; cursor: pointer; transition: transform 0.2s;
}
.cta-btn:hover { transform: scale(1.03); }

.luma-footer-wrap { padding: 40px 20px 60px; max-width: 1100px; margin: 60px auto 0; }
.luma-banner { background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 12px; padding: 16px 24px; display: flex; align-items: center; gap: 12px; color: #c4c4c4; font-size: 14px; margin-bottom: 36px; }
.luma-banner svg { width: 18px; height: 18px; fill: var(--gold); flex-shrink: 0; }
.luma-banner a { color: #fff; text-decoration: underline; cursor: pointer; }
.luma-join-wrap { text-align: center; margin-bottom: 60px; }
.luma-join-btn { background: linear-gradient(135deg, #FFF099 0%, #FFD700 100%); color: #000; font-size: 17px; font-weight: 800; padding: 14px 44px; border-radius: 30px; border: none; cursor: pointer; box-shadow: 0 4px 20px rgba(255, 215, 0, 0.35); transition: transform 0.2s; }
.luma-join-btn:hover { transform: scale(1.04); }
.luma-footer { color: #808080; font-size: 13px; }
.luma-footer-contact { margin-bottom: 28px; }
.luma-footer-contact a { color: #808080; text-decoration: underline; }
.luma-footer-contact a:hover { color: var(--gold); }
.luma-links-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px 24px; margin-bottom: 36px; }
.luma-links-grid a { color: #808080; text-decoration: none; font-size: 13px; transition: color 0.2s; }
.luma-links-grid a:hover { text-decoration: underline; color: var(--gold); }

.search-results-page { padding:32px; }
.search-results-page h2 { font-size:24px; font-weight:700; margin-bottom:20px; }
.search-results-page h2 span { color:var(--gold); }
.no-results { text-align:center; padding:80px 20px; color:var(--text2); grid-column:1/-1; }
.no-results .nr-icon { font-size:64px; margin-bottom:16px; }
.no-results h3 { font-size:20px; margin-bottom:8px; color:var(--text); }

/* ============================================
   RESPONSIVE / MOBILE-FIRST FIXES
   ============================================ */

/* ---------- TABLET (max-width: 1024px) ---------- */
@media (max-width: 1024px) {
  .nav-tabs { gap: 2px; padding: 3px; }
  .nav-tab { padding: 7px 12px; font-size: 12px; }
  .nav-search { width: 160px; }
  .nav-search:focus { width: 200px; }
  .movies-grid { grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 14px; }
  .hero-section { height: 440px; }
  .hero-content { max-width: 500px; padding: 0 40px; }
}

/* ---------- MOBILE (max-width: 768px) ---------- */
@media (max-width: 768px) {
  .navbar {
    padding: 10px 14px;
    height: auto;
    flex-wrap: wrap;
    gap: 10px;
    justify-content: space-between;
  }
  .nav-brand { order: 1; }
  .nav-right { order: 2; gap: 10px; justify-content: flex-end; }
  .nav-brand-name { font-size: 18px; }
  
  .nav-tabs {
    order: 3;
    width: 100%;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
    justify-content: flex-start;
  }
  .nav-tabs::-webkit-scrollbar { display: none; }
  .nav-tab { white-space: nowrap; flex-shrink: 0; }

  /* PROFESSIONAL MOBILE SEARCH & DROPDOWN FIX */
  .nav-search-wrap { position: relative !important; flex: 1; max-width: 180px; }
  .nav-search { width: 110px !important; font-size: 12px; padding: 7px 10px 7px 32px; transition: width 0.3s ease; }
  .nav-search:focus { width: 175px !important; background: rgba(255,255,255,0.12) !important; }
  
  .search-dropdown {
    position: absolute !important;
    top: calc(100% + 8px) !important;
    left: 0 !important;
    right: auto !important;
    width: 270px !important;
    max-width: 88vw !important;
  }

  .top-quick-bar { padding: 8px 14px; gap: 10px; top: auto; }
  .quick-pill { font-size: 11px; padding: 5px 11px; }

  .hero-section { height: 380px; }
  .hero-content { padding: 0 20px; max-width: 100%; }
  .hero-title { font-size: 28px; }
  .hero-overview { font-size: 12px; -webkit-line-clamp: 3; line-clamp: 3; overflow: hidden; display: -webkit-box; -webkit-box-orient: vertical; }
  .hero-btn { padding: 11px 24px; font-size: 13px; }
  .hero-nav-btn { width: 34px; height: 34px; font-size: 16px; }
  .hero-prev { left: 8px; }
  .hero-next { right: 8px; }

  .section-wrap { padding: 24px 16px 0; }
  .section-title { font-size: 18px; }

  .movies-grid { grid-template-columns: repeat(auto-fill, minmax(120px, 1fr)); gap: 10px; padding: 0 16px 24px; }
  .movies-slider .movie-card { min-width: 130px; max-width: 130px; }
  .card-title { font-size: 12px; }
  .card-overview { display: none; }

  .genre-pill { padding: 9px 16px; font-size: 12px; }

  .auth-card { padding: 32px 22px; }
  .auth-title { font-size: 19px; }

  .account-page { padding: 24px 16px; }
  .profile-card { flex-direction: column; text-align: center; gap: 14px; padding: 24px; }
  .edit-form .form-row { grid-template-columns: 1fr; }
  .stats-grid { grid-template-columns: repeat(3, 1fr); gap: 10px; }
  .stat-num { font-size: 20px; }

  .sub-plans { grid-template-columns: 1fr; }
  .sub-header h2 { font-size: 26px; }

  .cta-newsletter { margin: 40px 16px 20px; padding: 32px 20px; }
  .cta-form { flex-direction: column; }
  .luma-links-grid { grid-template-columns: repeat(2, 1fr); }
}

/* ---------- SMALL MOBILE (max-width: 480px) ---------- */
@media (max-width: 480px) {
  .movies-grid { grid-template-columns: repeat(auto-fill, minmax(100px, 1fr)); gap: 8px; }
  .movies-slider .movie-card { min-width: 110px; max-width: 110px; }
  .hero-section { height: 340px; }
  .hero-title { font-size: 22px; }
  .hero-genres .genre-tag { font-size: 9px; padding: 2px 6px; }
  .nav-search { width: 95px !important; }
  .nav-search:focus { width: 155px !important; }
  .splash-name { font-size: 36px; }
  .stats-grid { grid-template-columns: 1fr; }
}
"""