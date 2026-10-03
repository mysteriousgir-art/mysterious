/* Mysterious home page */
(function(){
"use strict";

function noteCard(n){
  return '<a class="card hoverable" href="note.html?slug=' + encodeURIComponent(n.slug) + '">' +
    '<span class="chip">' + esc(n.category) + "</span>" +
    "<h3>" + esc(n.title) + "</h3>" +
    '<p class="small">' + esc(n.summary || "") + "</p>" +
    '<span class="meta">👁 ' + esc(n.readCount || 0) + ' reads →</span>' +
  "</a>";
}

async function loadTopNotes(){
  var box = document.getElementById("top-notes");
  loadingBox(box, "Loading notes…");
  try{
    var notes = await api("/api/notes");
    if(!notes || !notes.length){
      box.innerHTML = '<p class="small">No notes yet — check back soon.</p>';
      return;
    }
    box.innerHTML = notes.slice(0, 3).map(noteCard).join("");
  }catch(e){
    errorBox(box, "Could not load notes. " + e.message);
  }
}

var galItems = [];
var galFilter = "All";
var galShown = 12;
const GAL_PAGE = 12;

function galCard(g){
  return '<a href="' + esc(g.url) + '" target="_blank" rel="noopener">' +
    '<img src="' + esc(g.url) + '" alt="' + esc(g.title) + '" loading="lazy" onerror="this.style.display=\'none\'">' +
    '<div class="cap">' + esc(g.title) + "<small>" + esc(g.topic || "") + "</small></div>" +
  "</a>";
}

function renderGallery(){
  var box = document.getElementById("infographics");
  var filters = document.getElementById("gal-filters");
  var moreBox = document.getElementById("gal-more");
  var topics = ["All"];
  galItems.forEach(function(g){ if(g.topic && topics.indexOf(g.topic) < 0) topics.push(g.topic); });
  var list = galFilter === "All" ? galItems : galItems.filter(function(g){ return g.topic === galFilter; });
  if(filters){
    filters.innerHTML = topics.map(function(t){
      return '<button class="chip-btn' + (t === galFilter ? " active" : "") + '" data-gal="' + esc(t) + '">' + esc(t) + "</button>";
    }).join("");
    filters.querySelectorAll("[data-gal]").forEach(function(b){
      b.addEventListener("click", function(){ galFilter = b.getAttribute("data-gal"); galShown = GAL_PAGE; renderGallery(); });
    });
  }
  box.innerHTML = list.slice(0, galShown).map(galCard).join("") ||
    '<p class="small">No infographics in this category yet.</p>';
  if(moreBox){
    if(list.length > galShown){
      moreBox.innerHTML = '<button class="btn btn-ghost" id="gal-more-btn">Show more (' + (list.length - galShown) + " remaining)</button>";
      document.getElementById("gal-more-btn").addEventListener("click", function(){ galShown += GAL_PAGE; renderGallery(); });
    }else moreBox.innerHTML = "";
  }
}

async function loadInfographics(){
  var box = document.getElementById("infographics");
  loadingBox(box, "Loading infographics…");
  try{
    var items = await api("/api/infographics");
    if(!items || !items.length){
      box.innerHTML = '<p class="small">Infographics are on their way — check back soon.</p>';
      return;
    }
    galItems = items;
    galFilter = "All";
    galShown = GAL_PAGE;
    renderGallery();
  }catch(e){
    errorBox(box, "Could not load infographics. " + e.message);
  }
}

async function renderWidgets(){
  var user = window.zehenUser;
  var streakW = document.getElementById("streak-widget");
  var progW = document.getElementById("progress-widget");
  var joinW = document.getElementById("join-widget");
  if(user){
    joinW.style.display = "none";
    try{
      var p = await api("/api/me/progress");
      streakW.style.display = "";
      progW.style.display = "";
      document.getElementById("streak-count").textContent = p.streak || 0;
      document.getElementById("pw-xp").textContent = p.xp || 0;
      document.getElementById("pw-level").textContent = p.level || 1;
      var tasks = p.tasks || [];
      document.getElementById("pw-tasks").innerHTML = tasks.length
        ? tasks.map(function(t){
            return '<li class="' + (t.done ? "done" : "") + '"><span class="tick">✓</span> ' + esc(t.label) + "</li>";
          }).join("")
        : '<li class="small">No tasks yet today.</li>';
      var btn = document.getElementById("checkin-btn");
      btn.onclick = async function(){
        btn.disabled = true;
        try{
          var r = await api("/api/checkin", {method:"POST"});
          document.getElementById("streak-count").textContent = r.streak;
          if(r.already){
            document.getElementById("streak-sub").textContent = "Already checked in today — see you tomorrow! 🌱";
            toast("Already checked in today", "ok");
          }else{
            document.getElementById("streak-sub").textContent = "Checked in! +" + (r.xp || 0) + " XP. Come back tomorrow to grow your streak. 🌱";
            toast("Checked in! +" + (r.xp || 0) + " XP", "ok");
            window.zehenRefreshUser();
          }
        }catch(e){ toast(e.message, "err"); }
        btn.disabled = false;
      };
    }catch(e){
      streakW.style.display = "none";
      progW.style.display = "none";
    }
  }else{
    streakW.style.display = "none";
    progW.style.display = "none";
    joinW.style.display = "";
  }
}

document.addEventListener("DOMContentLoaded", function(){
  loadTopNotes();
  loadInfographics();
  if(window.zehenUserLoaded){ renderWidgets(); }
  else{
    document.addEventListener("zehen:user", renderWidgets, {once:true});
  }
});
})();
