"""LumaScreen — JavaScript for the full SPA experience."""

JS = r"""
const DEFAULT_USERS = [
  { email: "admin@lumascreen.com", password: "admin123", name: "Admin", role: "admin", plan: "Premium", joined: 2024 },
  { email: "user@lumascreen.com", password: "user123", name: "Demo User", role: "user", plan: "Basic", joined: 2024 }
];

function getUsersDB() {
  const stored = localStorage.getItem("lumascreen_users");
  if (!stored) { localStorage.setItem("lumascreen_users", JSON.stringify(DEFAULT_USERS)); return DEFAULT_USERS; }
  try { return JSON.parse(stored); } catch(e) { return DEFAULT_USERS; }
}

function saveUsersDB(users) { localStorage.setItem("lumascreen_users", JSON.stringify(users)); }

let registeredUsers = getUsersDB();
let currentUser = null;
let heroIndex = 0;
let heroTotal = 0;
let heroTimer = null;
let searchDropdown = null;
let navigationHistory = ['home'];

const TRANSLATIONS = {
  en: {
    home: "Home", hollywood: "Hollywood", bollywood: "Bollywood", anime: "Anime", kids: "Kids", plans: "Plans", news: "News", account: "Account"
  },
  ur: {
    home: "ہوم", hollywood: "ہالی ووڈ", bollywood: "بالی ووڈ", anime: "اینیمی", kids: "بچے", plans: "پلانز", news: "نیوز", account: "اکاؤنٹ"
  },
  hi: {
    home: "होम", hollywood: "हॉलीवुड", bollywood: "बॉलीवुड", anime: "एनीमे", kids: "किड्स", plans: "प्लैन", news: "न्यूज़", account: "अकाउंट"
  }
};

function saveAppLanguage(lang) {
  localStorage.setItem("lumascreen_lang", lang);
  
  const footerSelect = document.getElementById('footer-lang-select');
  const prefSelect = document.getElementById('pref-app-lang');
  if (footerSelect) footerSelect.value = lang;
  if (prefSelect) prefSelect.value = lang;

  const texts = TRANSLATIONS[lang] || TRANSLATIONS.en;
  const tabHome = document.getElementById('tab-home');
  const tabHw = document.getElementById('tab-hollywood');
  const tabBw = document.getElementById('tab-bollywood');
  const tabAnime = document.getElementById('tab-anime');
  const tabKids = document.getElementById('tab-kids');
  const tabSub = document.getElementById('tab-subscription');
  const tabNews = document.getElementById('tab-news');
  const tabAcc = document.getElementById('tab-account');

  if (tabHome) tabHome.textContent = texts.home;
  if (tabHw) tabHw.textContent = texts.hollywood;
  if (tabBw) tabBw.textContent = texts.bollywood;
  if (tabAnime) tabAnime.textContent = texts.anime;
  if (tabKids) tabKids.textContent = texts.kids;
  if (tabSub) tabSub.textContent = texts.plans;
  if (tabNews) tabNews.textContent = texts.news;
  if (tabAcc) tabAcc.textContent = texts.account;

  showToast("🌐 Language updated successfully!");
}

function initSplash() {
  const bar = document.getElementById('loader-bar');
  const txt = document.getElementById('loader-text');
  let pct = 0;
  const messages = ['Loading movies & anime...','Fetching latest releases...','Preparing your experience...','Almost ready...'];
  const interval = setInterval(() => {
    pct += 2;
    if (bar) bar.style.width = pct + '%';
    if (txt) txt.textContent = messages[Math.floor(pct / 25)] || 'Almost ready...';
    if (pct >= 100) {
      clearInterval(interval);
      setTimeout(() => {
        const splash = document.getElementById('splash');
        if (splash) { 
          splash.style.opacity = '0'; 
          setTimeout(() => { 
            splash.classList.add('hidden'); 
            checkAutoLogin(); 
          }, 800); 
        }
      }, 300);
    }
  }, 40);
}

function showAuthPage() {
  const ap = document.getElementById('auth-page');
  if (ap) ap.classList.remove('hidden');
  const app = document.getElementById('main-app');
  if (app) app.style.display = 'none';
}

function checkAutoLogin() {
  const sessionUser = localStorage.getItem("lumascreen_current_user");
  const authPage = document.getElementById('auth-page');
  const mainApp = document.getElementById('main-app');

  if (sessionUser) {
    try {
      currentUser = JSON.parse(sessionUser);
      if (authPage) authPage.classList.add('hidden');
      if (mainApp) mainApp.style.display = 'block';
      enterApp();
    } catch(e) {
      localStorage.removeItem("lumascreen_current_user");
      showAuthPage();
    }
  } else {
    showAuthPage();
  }
}

function togglePassword(inputId, btn) {
  const input = document.getElementById(inputId);
  if (!input) return;
  const eyeOpen = `<svg viewBox="0 0 24 24" width="18" height="18" stroke="currentColor" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>`;
  const eyeClosed = `<svg viewBox="0 0 24 24" width="18" height="18" stroke="currentColor" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path><line x1="1" y1="1" x2="23" y2="23"></line></svg>`;
  if (input.type === 'password') {
    input.type = 'text';
    btn.innerHTML = eyeClosed;
  } else {
    input.type = 'password';
    btn.innerHTML = eyeOpen;
  }
}

function showSignup() { document.getElementById('login-form').classList.add('hidden'); document.getElementById('signup-form').classList.remove('hidden'); }
function showLogin() { document.getElementById('signup-form').classList.add('hidden'); document.getElementById('login-form').classList.remove('hidden'); }

function doLogin() {
  const email = document.getElementById('login-email').value.trim().toLowerCase();
  const pass  = document.getElementById('login-pass').value;
  const err   = document.getElementById('login-error');
  if (!email || !pass) { showErr(err, '⚠️ Please fill in all fields.'); return; }
  registeredUsers = getUsersDB();
  const found = registeredUsers.find(u => u.email.toLowerCase() === email && u.password === pass);
  if (!found) { showErr(err, '❌ Invalid email or password.'); return; }
  currentUser = { ...found };
  localStorage.setItem("lumascreen_current_user", JSON.stringify(currentUser));
  enterApp();
  showToast('👋 Welcome back, ' + currentUser.name + '!');
}

function doSignup() {
  const name  = document.getElementById('signup-name').value.trim();
  const email = document.getElementById('signup-email').value.trim().toLowerCase();
  const pass  = document.getElementById('signup-pass').value;
  const pass2 = document.getElementById('signup-pass2').value;
  const err   = document.getElementById('signup-error');
  if (!name || !email || !pass || !pass2) { showErr(err, '⚠️ Please fill in all fields.'); return; }
  if (pass !== pass2) { showErr(err, '⚠️ Passwords do not match.'); return; }
  registeredUsers = getUsersDB();
  if (registeredUsers.find(u => u.email.toLowerCase() === email)) { showErr(err, '❌ Email already registered. Please login.'); return; }
  const newUser = { email: email, password: pass, name: name, role: 'user', plan: 'Basic', joined: new Date().getFullYear() };
  registeredUsers.push(newUser); 
  saveUsersDB(registeredUsers);
  currentUser = { ...newUser };
  localStorage.setItem("lumascreen_current_user", JSON.stringify(currentUser));
  enterApp();
  showToast('🎉 Account registered successfully!');
}

function showErr(el, msg) { if (el) { el.style.display = 'block'; el.textContent = msg; } }

function enterApp() {
  const authPage = document.getElementById('auth-page');
  if (authPage) authPage.classList.add('hidden');
  const mainApp = document.getElementById('main-app');
  if (mainApp) mainApp.style.display = 'block';
  
  const initialEl = document.getElementById('nav-user-initial');
  if (initialEl && currentUser && currentUser.name) {
    initialEl.textContent = currentUser.name.charAt(0).toUpperCase();
  }

  const nameEl = document.getElementById('profile-name');
  const emailEl = document.getElementById('profile-email');
  const initialAvatar = document.getElementById('profile-initial');
  const planEl = document.getElementById('profile-plan');
  
  const editName = document.getElementById('edit-name');
  const editEmail = document.getElementById('edit-email');

  if (currentUser) {
    if (nameEl) nameEl.textContent = currentUser.name || 'User';
    if (emailEl) emailEl.textContent = currentUser.email || 'user@example.com';
    if (initialAvatar) initialAvatar.textContent = (currentUser.name || 'U').charAt(0).toUpperCase();
    if (planEl) planEl.textContent = (currentUser.plan || 'Basic') + ' Plan';
    
    if (editName) editName.value = currentUser.name || '';
    if (editEmail) editEmail.value = currentUser.email || '';
  }

  const savedLang = localStorage.getItem("lumascreen_lang");
  if (savedLang) { saveAppLanguage(savedLang); }

  showTab('home');
  setTimeout(initHero, 100);
  setupLiveSearch();
  loadContinueWatching();
  initSliders();
}

function saveProfile() {
  const newName = document.getElementById('edit-name').value.trim();
  const newPass = document.getElementById('edit-pass').value;
  const newPass2 = document.getElementById('edit-pass2').value;

  if (newPass && newPass !== newPass2) { showToast('⚠️ New passwords do not match!'); return; }

  if (newName) currentUser.name = newName;
  if (newPass) currentUser.password = newPass;

  registeredUsers = getUsersDB();
  const userIdx = registeredUsers.findIndex(u => u.email === currentUser.email);
  if (userIdx !== -1) {
    registeredUsers[userIdx] = currentUser;
    saveUsersDB(registeredUsers);
  }

  localStorage.setItem("lumascreen_current_user", JSON.stringify(currentUser));
  enterApp();
  showToast('✅ Profile updated successfully!');
}

function doLogout() {
  currentUser = null;
  localStorage.removeItem("lumascreen_current_user");
  const mainApp = document.getElementById('main-app');
  if (mainApp) mainApp.style.display = 'none';
  showAuthPage();
  showLogin();
  showToast('👋 Logged out successfully');
}

function showTab(tab) {
  if (navigationHistory[navigationHistory.length - 1] !== tab) { navigationHistory.push(tab); }
  document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
  const activeTab = document.getElementById('tab-' + tab);
  if (activeTab) activeTab.classList.add('active');
  ['home','hollywood','bollywood','anime','kids','subscription','news','account','search-results','admin'].forEach(p => {
    const el = document.getElementById('page-' + p);
    if (el) el.classList.add('hidden');
  });
  const target = document.getElementById('page-' + tab);
  if (target) target.classList.remove('hidden');
  window.scrollTo({ top: 0, behavior: 'smooth' });
  setTimeout(initSliders, 50);
}

function goBack() {
  if (navigationHistory.length > 1) {
    navigationHistory.pop();
    const prev = navigationHistory.pop() || 'home';
    showTab(prev);
  } else { showTab('home'); }
}

function slideRow(rowId, direction) {
  const container = document.getElementById(rowId);
  if (!container) return;
  container.scrollBy({ left: direction * 600, behavior: 'smooth' });
}

function initSliders() {
  document.querySelectorAll('.slider-container').forEach(container => {
    // Agar ye top-quick-bar hai, toh arrow hide mat karo, isay skip karo
    if (container.classList.contains('top-quick-bar')) {
      const leftArrow = container.querySelector('.arrow-left');
      if (leftArrow) leftArrow.style.display = 'flex'; // Hamesha dikhao
      return; 
    }

    // Sirf movie sliders ke liye logic
    const slider = container.querySelector('.movies-slider');
    const leftArrow = container.querySelector('.arrow-left');
    
    if (slider && leftArrow) {
      const updateArrow = () => {
        if (slider.scrollLeft > 10) {
          leftArrow.style.display = 'flex';
        } else {
          leftArrow.style.display = 'none';
        }
      };
      
      updateArrow();
      slider.removeEventListener('scroll', updateArrow);
      slider.addEventListener('scroll', updateArrow);
    }
  });
}

function initHero() {
  const slides = document.querySelectorAll('.hero-slide');
  heroTotal = slides.length;
  if (heroTotal === 0) return;
  slides[0].classList.add('active-slide');
  if (heroTimer) clearInterval(heroTimer);
  heroTimer = setInterval(nextHero, 5000);
}
function updateHero() {
  document.querySelectorAll('.hero-slide').forEach((s, i) => s.classList.toggle('active-slide', i === heroIndex));
  document.querySelectorAll('.hero-dot').forEach((d, i) => d.classList.toggle('active', i === heroIndex));
}
function nextHero() { heroIndex = (heroIndex + 1) % heroTotal; updateHero(); }
function prevHero() { heroIndex = (heroIndex - 1 + heroTotal) % heroTotal; updateHero(); }
function goHero(i)  { heroIndex = i; updateHero(); if(heroTimer){clearInterval(heroTimer);heroTimer=setInterval(nextHero,5000);} }

function showMovieDetail(movieId) {
  let modal = document.getElementById('movie-modal');
  let body = document.getElementById('modal-body-content');
 
  if (!modal || !body) {
    modal = document.createElement('div');
    modal.id = 'movie-modal';
 
    const modalContent = document.createElement('div');
    body = document.createElement('div');
    body.id = 'modal-body-content';
 
    modalContent.appendChild(body);
    modal.appendChild(modalContent);
    document.body.appendChild(modal);
  }
 
  modal.style.cssText = 'position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.85); z-index:99999; display:flex; align-items:center; justify-content:center; padding:20px; backdrop-filter:blur(10px); overflow-y:auto;';
 
  const modalBox = modal.firstElementChild;
  if (modalBox) {
    modalBox.style.cssText = 'background:#141722; width:100%; max-width:650px; border-radius:16px; overflow:hidden; border:1px solid rgba(255,215,0,0.3); box-shadow:0 20px 50px rgba(0,0,0,0.8); position:relative; max-height:90vh; overflow-y:auto;';
  }
 
  modal.onclick = function(event) { if (event.target === modal) closeModal(); };
 
  modal.style.display = 'flex';
  modal.classList.remove('hidden');
  document.body.style.overflow = 'hidden';
  body.innerHTML = '<div style="text-align:center;padding:60px;color:#fff;font-size:18px;">Loading...</div>';
 
  const m = window.movieDataMap && window.movieDataMap[movieId];
  if (!m) {
    body.innerHTML = '<div style="text-align:center;padding:60px;color:#ff6b6b;">Error: Movie details missing.</div>';
    return;
  }
 
  const backdrop = m.backdrop_path ? 'https://image.tmdb.org/t/p/w1280' + m.backdrop_path : '';
  const safeTitle = (m.title || 'Unknown').replace(/'/g, "\\'").replace(/"/g, '&quot;');
  const vote = m.vote_average ? m.vote_average.toFixed(1) : 'N/A';
  const releaseDate = m.release_date || 'N/A';
  const overview = m.overview || 'No description available.';
 
  body.innerHTML = `
    <div style="position:relative; background:#000;">
      ${backdrop ? `<img src="${backdrop}" style="width:100%;height:260px;object-fit:cover;">` : `<div style="width:100%;height:100px;background:#000;"></div>`}
      <button onclick="closeModal()" style="position:absolute;top:16px;right:16px;background:rgba(0,0,0,0.8);color:#fff;border:1px solid rgba(255,255,255,0.3);width:36px;height:36px;border-radius:50%;cursor:pointer;z-index:100;font-size:16px;line-height:1;">✕</button>
    </div>
    <div style="padding:28px;">
      <h2 style="font-size:26px;font-weight:900;color:#fff;margin-bottom:8px;">${m.title}</h2>
      <div style="color:#FFD700;font-weight:600;margin-bottom:16px;font-size:14px;">⭐ ${vote} &bull; 📅 ${releaseDate}</div>
      <p style="color:#aaa;font-size:14px;line-height:1.6;margin-bottom:24px;">${overview}</p>
      <button onclick="watchMovie('${safeTitle}', ${m.id})" style="width:100%;padding:16px;background:linear-gradient(135deg, #FFF099, #FFD700);color:#000;border:none;border-radius:10px;font-weight:800;cursor:pointer;font-size:16px;">▶ Stream Movie Online</button>
    </div>
  `;
}

function watchMovie(title, tmdbId) {
  const body = document.getElementById('modal-body-content');
  if (!body) return;
  
  const searchUrl = 'https://www.google.com/search?q=' + encodeURIComponent(title + ' watch online streaming free');
  
  body.innerHTML = `
    <div style="padding:40px 24px; text-align:center;">
      <h3 style="color:#FFD700;margin-bottom:20px;font-size:24px;font-weight:900;">🎬 ${title}</h3>
      <p style="color:#ccc;margin-bottom:32px;line-height:1.6;font-size:15px;">
        Direct embedding is restricted. Click the secure button below to launch the streaming source in a new window.
      </p>
      <a href="${searchUrl}" target="_blank" style="display:inline-block;padding:16px 36px;background:linear-gradient(135deg, #FFF099, #FFD700);color:#000;border-radius:10px;font-weight:800;text-decoration:none;font-size:16px;box-shadow:0 6px 20px rgba(255,215,0,0.3);">
        ▶ Open Secure Stream
      </a>
      <br><br><br>
      <button onclick="showMovieDetail(${tmdbId})" style="background:transparent;color:#888;border:1px solid #444;padding:10px 20px;border-radius:8px;cursor:pointer;">⬅ Back to Details</button>
    </div>
  `;
}

function closeModal() {
  const modal = document.getElementById('movie-modal');
  if (modal) {
    modal.style.display = 'none';
    modal.classList.add('hidden');
  }
  document.body.style.overflow = '';
}

function filterByGenreName(genreName) {
  showTab('search-results');
  document.getElementById('search-query-label').textContent = '"' + genreName + ' Genre"';
  const allMovies = Object.values(window.movieDataMap || {});
  const results = allMovies.filter(m => (m.genre_ids || []).some(id => {
    const gName = (window.genreMap || {})[id];
    return gName && gName.toLowerCase() === genreName.toLowerCase();
  }));
  const grid = document.getElementById('search-results-grid');
  if (results.length === 0) {
    grid.innerHTML = `<div class="no-results"><div class="nr-icon">🎬</div><h3>No movies found for ${genreName}</h3></div>`;
  } else {
    grid.innerHTML = `<div class="movies-grid" style="padding:0;width:100%">${results.map(m => buildCardHTML(m)).join('')}</div>`;
  }
  setTimeout(initSliders, 50);
}

function setupLiveSearch() {
  const wrap = document.querySelector('.nav-search-wrap');
  if (!wrap || document.getElementById('search-dropdown')) return;
  searchDropdown = document.createElement('div');
  searchDropdown.id = 'search-dropdown';
  searchDropdown.className = 'search-dropdown';
  wrap.appendChild(searchDropdown);
  const input = document.getElementById('nav-search-input');
  if (input) { input.addEventListener('input', (e) => handleLiveSearch(e.target.value.trim())); }
}

function handleLiveSearch(q) {
  if (!q || q.length < 2) { searchDropdown.style.display = 'none'; return; }
  const movies = Object.values(window.movieDataMap || {});
  const filtered = movies.filter(m => (m.title || '').toLowerCase().includes(q.toLowerCase()));
  if (filtered.length === 0) { searchDropdown.style.display = 'none'; return; }
  searchDropdown.innerHTML = filtered.slice(0, 5).map(m => `
    <div class="search-item" onclick="showMovieDetail(${m.id}); searchDropdown.style.display='none';" style="display:flex;gap:12px;padding:10px 14px;cursor:pointer;border-bottom:1px solid rgba(255,255,255,0.04)">
      <img src="${m.poster_path ? 'https://image.tmdb.org/t/p/w200' + m.poster_path : ''}" style="width:36px;height:52px;border-radius:4px;object-fit:cover">
      <div><div style="font-weight:700;font-size:13px;color:#fff">${m.title}</div><div style="font-size:11px;color:var(--text2)">⭐ ${m.vote_average?m.vote_average.toFixed(1):''}</div></div>
    </div>`).join('');
  searchDropdown.style.display = 'block';
}

function doSearch() {
  const input = document.getElementById('nav-search-input');
  const q = input ? input.value.trim() : '';
  if (!q) return;
  if (searchDropdown) searchDropdown.style.display = 'none';
  showTab('search-results');
  document.getElementById('search-query-label').textContent = '"' + q + '"';
  const allMovies = Object.values(window.movieDataMap || {});
  const results = allMovies.filter(m => (m.title || '').toLowerCase().includes(q.toLowerCase()));
  const grid = document.getElementById('search-results-grid');
  grid.innerHTML = results.length === 0 ? `<div class="no-results"><h3>No results for "${q}"</h3></div>` : `<div class="movies-grid" style="padding:0;width:100%">${results.map(m => buildCardHTML(m)).join('')}</div>`;
  setTimeout(initSliders, 50);
}

function buildCardHTML(m) {
  const title = (m.title||'Unknown').replace(/"/g,'&quot;');
  const poster = m.poster_path ? 'https://image.tmdb.org/t/p/w500'+m.poster_path : 'https://placehold.co/220x330/1a1a2e/FFD700?text=No+Poster';
  const vote = m.vote_average||0;
  const date = (m.release_date||'').slice(0,4);
  const overview = ((m.overview||'No description.')+'').slice(0,120)+'…';
  const tags = (m.genre_ids||[]).slice(0,2).map(id=>(window.genreMap||{})[id]?`<span class="genre-tag">${(window.genreMap||{})[id]}</span>`:'').join('');
  return `<div class="movie-card" onclick="showMovieDetail(${m.id})">
    <div class="card-poster-wrap"><img src="${poster}" alt="${title}" loading="lazy">
    <span class="rating-badge">⭐ ${vote.toFixed(1)}</span></div>
    <div class="card-info"><div class="card-title">${title}</div><div class="card-year">${date}</div>
    <div class="card-genres">${tags}</div><div class="card-overview">${overview}</div></div></div>`;
}

function loadContinueWatching() {
  const history = JSON.parse(localStorage.getItem('lumascreen_watch_history') || '[]');
  const section = document.getElementById('continue-watching-section');
  const slider = document.getElementById('continue-slider');
  if (history.length > 0 && section && slider) {
    section.style.display = 'block';
    slider.innerHTML = history.map(id => buildCardHTML(window.movieDataMap[id])).join('');
  }
}

function showToast(msg) {
  const t = document.createElement('div');
  t.style.cssText = 'position:fixed;bottom:30px;right:30px;background:#141722;border:1px solid rgba(255,215,0,0.3);padding:14px 20px;border-radius:12px;color:#fff;z-index:9999;box-shadow:0 8px 25px rgba(0,0,0,0.5)';
  t.innerHTML = msg; document.body.appendChild(t);
  setTimeout(() => t.remove(), 3000);
}

function subscribePlan(plan, price) { showToast(`🎉 Subscribed to ${plan} (${price}/mo)!`); }

window.addEventListener('load', () => { initSplash(); });
"""