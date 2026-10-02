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
  ["community.html","Community"]
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
          '<a href="notes.html">Notes library</a><br><a href="quizzes.html">Quizzes</a><br><a href="games.html">Games &amp; leaderboard</a></div>' +
        '<div><strong style="color:#fff">Community</strong><br>' +
          '<a href="community.html">Study rooms</a><br><a href="profile.html">Your profile</a><br><a href="auth.html">Join Mysterious</a></div>' +
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
