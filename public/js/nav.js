/* ============================================================
   ZEHEN shared module — injected into every page.
   - api(path, opts): fetch with credentials:'include', JSON bodies
   - esc(s): escape user-generated content before HTML injection
   - toast(msg, kind): small notification
   - Nav: shared header/footer, auth state, XP/level/streak,
     Admin link only for admins.
   ============================================================ */
(function(){
"use strict";

/* ---------- escaping ---------- */
function esc(s){
  if(s===null||s===undefined) return "";
  return String(s).replace(/[&<>"']/g,function(c){
    return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c];
  });
}
window.esc = esc;

/* ---------- api helper ---------- */
async function api(path, opts){
  opts = opts || {};
  var headers = Object.assign({"Accept":"application/json"}, opts.headers || {});
  var body = opts.body;
  if(body && typeof body === "object" && !(body instanceof FormData)){
    headers["Content-Type"] = "application/json";
    body = JSON.stringify(body);
  }
  var res = await fetch(path, Object.assign({}, opts, {
    credentials: "include",
    headers: headers,
    body: body
  }));
  var data = null;
  try{ data = await res.json(); }catch(e){ data = null; }
  if(!res.ok){
    var msg = (data && (data.message || data.error)) || ("Request failed (" + res.status + ")");
    var err = new Error(msg);
    err.status = res.status;
    err.data = data;
    throw err;
  }
  return data;
}
window.api = api;

/* ---------- toast ---------- */
function toast(msg, kind){
  var zone = document.querySelector(".toast-zone");
  if(!zone){
    zone = document.createElement("div");
    zone.className = "toast-zone";
    document.body.appendChild(zone);
  }
  var t = document.createElement("div");
  t.className = "toast" + (kind ? " " + kind : "");
  t.textContent = msg;
  zone.appendChild(t);
  setTimeout(function(){ t.style.opacity = "0"; t.style.transition = "opacity .3s"; }, 3400);
  setTimeout(function(){ t.remove(); }, 3800);
}
window.toast = toast;

/* ---------- query params ---------- */
function qp(name){
  return new URLSearchParams(window.location.search).get(name);
}
window.qp = qp;

/* ---------- auth state ---------- */
window.zehenUser = null;
window.zehenUserLoaded = false;

async function loadUser(){
  try{
    var d = await api("/api/auth/me");
    window.zehenUser = d.user || d;
  }catch(e){
    if(e.status !== 401){ /* keep silent; page shows its own errors */ }
    window.zehenUser = null;
  }
  window.zehenUserLoaded = true;
  renderNav();
  document.dispatchEvent(new CustomEvent("zehen:user", {detail: window.zehenUser}));
}
window.zehenRefreshUser = loadUser;

/* ---------- nav ---------- */
var NAV_LINKS = [
  ["index.html","Home"],
  ["notes.html","Notes"],
  ["quizzes.html","Quizzes"],
  ["games.html","Games"],
  ["videos.html","Videos"],
  ["infographics.html","Infographics"],
  ["community.html","Community"],
  ["feed.html","Feed"]
];

function pageOf(path){
  return (path || window.location.pathname).split("/").pop().split("?")[0] || "index.html";
}

function renderNav(){
  var header = document.getElementById("zehen-nav");
  if(!header) return;
  var user = window.zehenUser;
  var current = pageOf();
  var links = NAV_LINKS.map(function(l){
    var active = current === l[0] ? ' class="active"' : "";
    return '<a href="' + l[0] + '"' + active + ">" + l[1] + "</a>";
  }).join("");
  if(user && user.isAdmin){
    links += '<a href="admin.html"' + (current === "admin.html" ? ' class="active"' : "") + ">Admin</a>";
  }
  var right;
  if(user){
    right =
      '<span class="xp-pill" title="Level ' + esc(user.level) + '"><span class="lvl">Lvl ' + esc(user.level) + '</span> <span class="hide-s">' + esc(user.xp) + ' XP</span></span>' +
      '<span class="xp-pill streak-pill" title="Day streak">🔥 <span class="hide-s">' + esc(user.streak) + '</span></span>' +
      '<a class="btn btn-ghost btn-sm" href="profile.html">' + esc(user.avatar || "🧠") + ' ' + esc(user.displayName) + "</a>" +
      '<button class="btn btn-plain btn-sm" id="zehen-logout">Log out</button>';
  }else{
    right = '<a class="btn btn-primary btn-sm" href="auth.html">Log in / Sign up</a>';
  }
  header.className = "nav";
  header.innerHTML =
    '<div class="nav-inner">' +
      '<a class="logo" href="index.html"><span class="mark">🧠</span><span>Mysterious<small class="sig">by Attiya Batool · Founder &amp; Admin</small></span></a>' +
      '<button class="nav-toggle" id="zehen-nav-toggle" aria-label="Menu">☰</button>' +
      '<nav class="nav-links" id="zehen-nav-links">' + links + "</nav>" +
      '<div class="nav-user">' + right + "</div>" +
    "</div>";
  var toggle = document.getElementById("zehen-nav-toggle");
  var linksEl = document.getElementById("zehen-nav-links");
  if(toggle && linksEl){
    toggle.addEventListener("click", function(){ linksEl.classList.toggle("open"); });
    linksEl.addEventListener("click", function(e){
      if(e.target.tagName === "A") linksEl.classList.remove("open");
    });
  }
  var lo = document.getElementById("zehen-logout");
  if(lo){
    lo.addEventListener("click", async function(){
      try{ await api("/api/auth/logout", {method:"POST"}); }catch(e){}
      window.zehenUser = null;
      window.location.href = "index.html";
    });
  }
}

/* ---------- footer ---------- */
function renderFooter(){
  var f = document.getElementById("zehen-footer");
  if(!f) return;
  f.innerHTML =
    '<div class="wrap">' +
      '<div style="display:flex;gap:2rem;flex-wrap:wrap;justify-content:space-between;width:100%">' +
        '<div><div class="flogo">🧠 Mysterious</div><div class="fsig">by Attiya Batool · Founder &amp; Admin</div><p style="color:rgba(255,255,255,.65);margin:.5rem 0 0;max-width:20rem">A calm corner of the internet to learn psychology — notes, quizzes, games and a friendly community.</p></div>' +
        '<div><strong style="color:#fff">Explore</strong><br>' +
          '<a href="notes.html">Notes library</a><br><a href="quizzes.html">Quizzes</a><br><a href="games.html">Games &amp; leaderboard</a><br><a href="videos.html">3D videos</a><br><a href="infographics.html">Infographics</a></div>' +
        '<div><strong style="color:#fff">Community</strong><br>' +
          '<a href="community.html">Study rooms</a><br><a href="profile.html">Your profile</a><br><a href="auth.html">Join Mysterious</a></div>' +
        '<div>' +
          '<style>.socbtn{display:inline-flex;align-items:center;justify-content:center;width:42px;height:42px;border-radius:50%;margin:.6rem .45rem 0 0;transition:transform .2s,box-shadow .2s}.socbtn:hover{transform:translateY(-3px) scale(1.08);box-shadow:0 6px 16px rgba(0,0,0,.4)}.socbtn svg{width:20px;height:20px}</style>' +
          '<div>' +
            '<a class="socbtn" style="background:#0A66C2" title="LinkedIn" aria-label="LinkedIn" href="https://www.linkedin.com/in/attiya-batool-14119338a/" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" fill="#fff"><path d="M20.45 20.45h-3.55v-5.57c0-1.33-.03-3.04-1.85-3.04-1.86 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.56h.05c.47-.9 1.63-1.85 3.36-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12zM7.12 20.45H3.56V9h3.56v11.45z"/></svg></a>' +
            '<a class="socbtn" style="background:#16161a;border:1px solid rgba(255,255,255,.28)" title="TikTok" aria-label="TikTok" href="https://www.tiktok.com/@mysterious.girl.609" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" fill="#fff"><path d="M16.6 3c.4 2.1 1.8 3.6 4 3.9v3.1c-1.5 0-2.9-.5-4-1.3v6.6c0 3.9-2.9 6.7-6.6 6.7-3.6 0-6.5-2.9-6.5-6.5s2.9-6.5 6.6-6.5c.3 0 .7 0 1 .1v3.3c-.3-.1-.7-.2-1-.2-1.9 0-3.4 1.5-3.4 3.3s1.5 3.3 3.4 3.3c1.9 0 3.3-1.4 3.3-3.5V3h3.2z"/></svg></a>' +
            '<a class="socbtn" style="background:linear-gradient(45deg,#F58529,#DD2A7B,#8134AF,#515BD4)" title="Instagram" aria-label="Instagram" href="https://www.instagram.com/mysterious.girl.609" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2"><rect x="2.5" y="2.5" width="19" height="19" rx="5.5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.5" cy="6.5" r="1.3" fill="#fff" stroke="none"/></svg></a>' +
          '</div></div>' +
      "</div>" +
      '<div class="fine">© 2026 Mysterious — learn the mind, one day at a time.</div>' +
    "</div>";
}

/* ---------- helpers for pages ---------- */
function loadingBox(el, text){
  if(typeof el === "string") el = document.getElementById(el);
  if(el) el.innerHTML = '<div class="loading-box"><span class="spinner"></span> ' + esc(text || "Loading…") + "</div>";
}
window.loadingBox = loadingBox;

function errorBox(el, msg){
  if(typeof el === "string") el = document.getElementById(el);
  if(el) el.innerHTML = '<div class="alert alert-err">' + esc(msg || "Something went wrong. Please try again.") + "</div>";
}
window.errorBox = errorBox;

function requireLogin(redirectTo){
  if(window.zehenUserLoaded && !window.zehenUser){
    window.location.href = "auth.html?next=" + encodeURIComponent(redirectTo || window.location.pathname + window.location.search);
    return false;
  }
  return true;
}
window.requireLogin = requireLogin;

/* boot */
document.addEventListener("DOMContentLoaded", function(){
  renderFooter();
  loadUser();
});
})();

/* ---------- anonymous visit tracking (one beacon per page view) ---------- */
(function(){
  "use strict";
  try{
    if(/\/admin\.html$/.test(window.location.pathname)) return; // keep admin data clean
    var tz = "";
    try{ tz = Intl.DateTimeFormat().resolvedOptions().timeZone || ""; }catch(e){}
    var ua = navigator.userAgent || "";
    var device = /Mobi|Android|iPhone|iPad|Mobile/i.test(ua) ? "mobile" : "desktop";
    var payload = JSON.stringify({ page: window.location.pathname || "/", timezone: tz, device: device });
    if(navigator.sendBeacon){
      navigator.sendBeacon("/api/track", new Blob([payload], {type:"application/json"}));
    }else if(window.fetch){
      fetch("/api/track", {method:"POST", headers:{"Content-Type":"application/json"}, body:payload, keepalive:true}).catch(function(){});
    }
  }catch(e){/* tracking must never break the page */}
})();
