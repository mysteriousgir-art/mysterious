/* Mysterious single-note page */
(function(){
"use strict";

var slug = qp("slug");
var claimed = false;

function pointHtml(p, i){
  return '<div class="note-point">' +
    "<h3><span class='num'>" + (i + 1) + "</span> " + esc(p.point) + "</h3>" +
    (p.example ? '<div class="example-box"><span class="tag">💡 Example</span>' + esc(p.example) + "</div>" : "") +
  "</div>";
}

async function boot(){
  var body = document.getElementById("note-body");
  if(!slug){ errorBox(body, "No note selected. Go back to the library and pick a note."); return; }
  loadingBox(body, "Loading note…");
  try{
    var d = await api("/api/notes/" + encodeURIComponent(slug));
    var n = d.note || d;
    document.title = n.title + " — Mysterious";
    body.innerHTML =
      '<span class="chip">' + esc(n.category) + '</span> ' +
      '<span class="meta">' + esc(n.readCount || 0) + ' reads</span>' +
      "<h1 style='margin:.5rem 0 .8rem'>" + esc(n.title) + "</h1>" +
      '<p class="lead">' + esc(n.summary || "") + "</p>" +
      '<div id="points">' + (n.points || []).map(pointHtml).join("") + "</div>" +
      '<div id="read-zone" style="margin-top:1.6rem"></div>';
    renderReadZone();
  }catch(e){
    errorBox(body, "Could not load this note: " + e.message);
  }
}

function renderReadZone(){
  var z = document.getElementById("read-zone");
  if(!z) return;
  if(!window.zehenUser){
    z.innerHTML = '<div class="alert alert-info">📝 <a href="auth.html?next=' +
      encodeURIComponent("note.html?slug=" + slug) + '">Log in</a> to mark this note as read and earn <strong>+20 XP</strong>.</div>';
    return;
  }
  if(claimed){
    z.innerHTML = '<div class="alert alert-ok">✓ Marked as read — +20 XP added. Keep learning! 🌱</div>';
    return;
  }
  z.innerHTML = '<button class="btn btn-terra btn-lg" id="mark-read">✓ Mark as read <span class="small" style="color:#fff;opacity:.9">(+20 XP)</span></button>';
  document.getElementById("mark-read").addEventListener("click", async function(){
    var btn = this;
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner"></span> Saving…';
    try{
      var r = await api("/api/notes/" + encodeURIComponent(slug) + "/read", {method:"POST"});
      claimed = true;
      window.zehenRefreshUser();
      if(r.leveledUp){
        toast("🎉 Level up! You reached level " + r.level, "ok");
      }else{
        toast("Nice work! +20 XP", "ok");
      }
      renderReadZone();
    }catch(e){
      toast(e.message, "err");
      btn.disabled = false;
      btn.textContent = "✓ Mark as read (+20 XP)";
    }
  });
}

document.addEventListener("DOMContentLoaded", function(){
  boot();
  document.addEventListener("zehen:user", renderReadZone, {once:true});
  if(window.zehenUserLoaded) renderReadZone();
});
})();
