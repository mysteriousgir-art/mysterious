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

async function loadInfographics(){
  var box = document.getElementById("infographics");
  loadingBox(box, "Loading infographics…");
  try{
    var items = await api("/api/infographics");
    if(!items || !items.length){
      box.innerHTML = '<p class="small">Infographics are on their way — check back soon.</p>';
      return;
    }
    box.innerHTML = items.map(function(g){
      return '<a href="' + esc(g.url) + '" target="_blank" rel="noopener">' +
        '<img src="' + esc(g.url) + '" alt="' + esc(g.title) + '" loading="lazy" onerror="this.style.display=\'none\'">' +
        '<div class="cap">' + esc(g.title) + "<small>" + esc(g.topic || "") + "</small></div>" +
      "</a>";
    }).join("");
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
