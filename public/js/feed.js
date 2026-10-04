/* Mysterious feed — posts, reactions, comments, shares, follows */
(function(){
"use strict";

var feedType = "following";
var nextBefore = 0;
var pendingImage = null; // {dataUrl}
var REACTIONS = [
  ["like", "👍"],
  ["love", "❤️"],
  ["insightful", "💡"],
  ["celebrate", "🎉"]
];

function timeAgo(iso){
  var s = Math.floor((Date.now() - new Date(iso).getTime()) / 1000);
  if (s < 60) return "just now";
  if (s < 3600) return Math.floor(s / 60) + "m ago";
  if (s < 86400) return Math.floor(s / 3600) + "h ago";
  return Math.floor(s / 86400) + "d ago";
}

function reactionBar(p){
  return REACTIONS.map(function(r){
    var on = p.myReaction === r[0];
    return '<button class="chip-btn' + (on ? " active" : "") + '" data-react="' + r[0] + '" data-id="' + p.id + '" title="' + r[0] + '">' +
      r[1] + "</button>";
  }).join("") +
  '<span class="small" style="margin-left:.4rem"><span id="lc-' + p.id + '">' + p.likeCount + "</span> reactions</span>";
}

function sharedHtml(sp){
  if(!sp) return "";
  return '<div class="card" style="margin:.7rem 0 0;padding:.8rem;background:rgba(0,0,0,.03)">' +
    '<div class="small" style="margin-bottom:.3rem">📣 <strong>' + esc(sp.author ? sp.author.displayName : "?") + "</strong>" +
    ' <span style="opacity:.6">· ' + timeAgo(sp.createdAt) + "</span></div>" +
    "<p style='margin:.3rem 0'>" + esc(sp.body) + "</p>" +
    (sp.imageUrl ? '<img src="' + esc(sp.imageUrl) + '" alt="Shared post image" style="max-width:100%;border-radius:.6rem;margin-top:.4rem">' : "") +
    "</div>";
}

function postCard(p){
  var mine = window.zehenUser && String(window.zehenUser.id) === String(p.author ? p.author.userId : 0);
  var h = '<article class="card" data-post="' + p.id + '" style="margin-bottom:1rem">';
  h += '<div style="display:flex;gap:.7rem;align-items:center">';
  h += '<div style="font-size:2rem">' + esc(p.author ? p.author.avatar : "🧠") + "</div>";
  h += '<div><a href="profile.html?id=' + (p.author ? p.author.userId : 0) + '"><strong>' +
    esc(p.author ? p.author.displayName : "?") + "</strong></a>";
  h += ' <span class="small" style="opacity:.65">· ' + timeAgo(p.createdAt) + " · " +
    (p.visibility === "followers" ? "👥 followers" : "🌍 public") + "</span></div></div>";
  if(p.body) h += "<p style='margin:.7rem 0'>" + esc(p.body) + "</p>";
  if(p.imageUrl) h += '<img src="' + esc(p.imageUrl) + '" alt="Post image" style="max-width:100%;border-radius:.6rem">';
  h += sharedHtml(p.sharedPost);
  h += '<div style="display:flex;gap:.35rem;flex-wrap:wrap;align-items:center;margin-top:.8rem">' + reactionBar(p) + "</div>";
  h += '<div style="display:flex;gap:.6rem;flex-wrap:wrap;margin-top:.6rem;align-items:center">';
  h += '<button class="btn btn-plain btn-sm" data-comments="' + p.id + '">💬 Comments (<span id="cc-' + p.id + '">' + p.commentCount + "</span>)</button>";
  h += '<button class="btn btn-plain btn-sm" data-share="' + p.id + '">🔁 Share' + (p.shareCount ? " (" + p.shareCount + ")" : "") + "</button>";
  if(mine) h += '<button class="btn btn-plain btn-sm" data-del="' + p.id + '">🗑️ Delete</button>';
  else h += '<button class="btn btn-plain btn-sm" data-report="' + p.id + '">🚩 Report</button>';
  h += "</div>";
  h += '<div class="comments-box" id="cb-' + p.id + '" style="display:none;margin-top:.7rem"></div>';
  h += '<div class="report-box" id="rb-' + p.id + '" style="display:none;margin-top:.7rem">' +
    '<div style="display:flex;gap:.5rem"><input class="input" id="ri-' + p.id + '" maxlength="300" placeholder="Reason for reporting…">' +
    '<button class="btn btn-primary btn-sm" data-report-send="' + p.id + '">Send</button></div></div>';
  h += "</article>";
  return h;
}

async function loadFeed(reset){
  var box = document.getElementById("feed-box");
  if(reset){ nextBefore = 0; box.innerHTML = '<p class="small">Loading…</p>'; }
  try{
    var url = "/api/posts?feed=" + feedType + "&limit=20" + (nextBefore ? "&before=" + nextBefore : "");
    var d = await api(url);
    var html = reset ? "" : box.innerHTML;
    if(!d.posts.length && reset) html = '<div class="card"><p>No posts yet. Be the first to share something! 🌱</p></div>';
    d.posts.forEach(function(p){ html += postCard(p); });
    box.innerHTML = html;
    nextBefore = d.nextBefore || 0;
    document.getElementById("feed-more").style.display = nextBefore ? "" : "none";
  }catch(e){
    box.innerHTML = '<div class="alert alert-err">' + esc(e.message) + "</div>";
  }
}

function fileToDataUrl(file){
  return new Promise(function(resolve, reject){
    var r = new FileReader();
    r.onload = function(){ resolve(r.result); };
    r.onerror = reject;
    r.readAsDataURL(file);
  });
}

async function submitPost(){
  var body = document.getElementById("post-body").value.trim();
  var vis = document.getElementById("post-visibility").value;
  var msg = document.getElementById("post-msg");
  if(!body && !pendingImage){ msg.innerHTML = '<div class="alert alert-err">Write something or add a photo first.</div>'; return; }
  var btn = document.getElementById("post-submit");
  btn.disabled = true; btn.textContent = "Posting…";
  try{
    var payload = { body: body, visibility: vis };
    if(pendingImage) payload.imageData = pendingImage;
    await api("/api/posts", { method: "POST", body: payload });
    document.getElementById("post-body").value = "";
    pendingImage = null;
    document.getElementById("post-preview").innerHTML = "";
    document.getElementById("post-image").value = "";
    msg.innerHTML = "";
    toast("Posted! ✨", "ok");
    loadFeed(true);
  }catch(e){
    msg.innerHTML = '<div class="alert alert-err">' + esc(e.message) + "</div>";
  }
  btn.disabled = false; btn.textContent = "Post";
}

async function toggleReact(postId, kind){
  try{
    var card = document.querySelector('[data-post="' + postId + '"]');
    var current = card.querySelector('[data-react].active');
    var currentKind = current ? current.getAttribute("data-react") : null;
    var d;
    if(currentKind === kind){
      d = await api("/api/posts/" + postId + "/react", { method: "DELETE" });
    }else{
      d = await api("/api/posts/" + postId + "/react", { method: "POST", body: { kind: kind } });
    }
    var newKind = d.kind || null;
    card.querySelectorAll("[data-react]").forEach(function(b){
      b.classList.toggle("active", b.getAttribute("data-react") === newKind);
    });
    document.getElementById("lc-" + postId).textContent = d.likeCount;
  }catch(e){ toast(e.message, "err"); }
}

async function toggleComments(postId){
  var box = document.getElementById("cb-" + postId);
  if(box.style.display === "none"){
    box.style.display = "";
    box.innerHTML = '<p class="small">Loading comments…</p>';
    try{
      var d = await api("/api/posts/" + postId + "/comments");
      var h = d.map(function(c){
        return '<div style="display:flex;gap:.5rem;margin:.5rem 0">' +
          '<div>' + esc(c.author ? c.author.avatar : "🧠") + "</div>" +
          '<div><strong>' + esc(c.author ? c.author.displayName : "?") + '</strong> ' +
          '<span class="small" style="opacity:.6">' + timeAgo(c.createdAt) + "</span><br>" + esc(c.body) + "</div></div>";
      }).join("");
      if(!d.length) h = '<p class="small">No comments yet.</p>';
      h += '<div style="display:flex;gap:.5rem;margin-top:.6rem"><input class="input" id="ci-' + postId + '" maxlength="300" placeholder="Write a comment…">' +
        '<button class="btn btn-primary btn-sm" data-comment-send="' + postId + '">Reply</button></div>';
      box.innerHTML = h;
    }catch(e){ box.innerHTML = '<div class="alert alert-err">' + esc(e.message) + "</div>"; }
  }else{
    box.style.display = "none";
  }
}

async function sendComment(postId){
  var inp = document.getElementById("ci-" + postId);
  var text = inp.value.trim();
  if(!text) return;
  try{
    await api("/api/posts/" + postId + "/comments", { method: "POST", body: { body: text } });
    var box = document.getElementById("cb-" + postId);
    box.style.display = "none";
    toggleComments(postId);
    var cc = document.getElementById("cc-" + postId);
    cc.textContent = String(Number(cc.textContent) + 1);
  }catch(e){ toast(e.message, "err"); }
}

async function sharePost(postId){
  try{
    await api("/api/posts/" + postId + "/share", { method: "POST", body: {} });
    toast("Shared to your feed! 🔁", "ok");
    loadFeed(true);
  }catch(e){ toast(e.message, "err"); }
}

async function deletePost(postId){
  if(!confirm("Delete this post?")) return;
  try{
    await api("/api/posts/" + postId, { method: "DELETE" });
    var card = document.querySelector('[data-post="' + postId + '"]');
    if(card) card.remove();
    toast("Post deleted.", "ok");
  }catch(e){ toast(e.message, "err"); }
}

async function sendReport(postId){
  var inp = document.getElementById("ri-" + postId);
  var reason = inp.value.trim();
  if(!reason){ toast("Please write a reason.", "err"); return; }
  try{
    await api("/api/reports", { method: "POST", body: { postId: postId, reason: reason } });
    document.getElementById("rb-" + postId).style.display = "none";
    toast("Report sent. The admin will review it.", "ok");
  }catch(e){ toast(e.message, "err"); }
}

function bootFeed(){
  if(!window.zehenUser){
    document.getElementById("feed-box").innerHTML =
      '<div class="card"><p>Please <a href="auth.html?next=feed.html">log in</a> to see the feed and share posts. 🌱</p></div>';
    document.getElementById("composer").style.display = "none";
    document.querySelector(".game-tabs").style.display = "none";
    return;
  }
  document.getElementById("composer-avatar").textContent = window.zehenUser.avatar || "🧠";

  document.querySelectorAll(".game-tabs .chip-btn").forEach(function(b){
    b.addEventListener("click", function(){
      document.querySelectorAll(".game-tabs .chip-btn").forEach(function(x){ x.classList.remove("active"); });
      b.classList.add("active");
      feedType = b.getAttribute("data-feed");
      loadFeed(true);
    });
  });

  document.getElementById("post-image").addEventListener("change", async function(){
    var f = this.files[0];
    if(!f) return;
    if(f.size > 1500 * 1024){ toast("Photo is too large (max 1.5 MB).", "err"); this.value = ""; return; }
    try{
      pendingImage = await fileToDataUrl(f);
      document.getElementById("post-preview").innerHTML =
        '<img src="' + pendingImage + '" alt="Preview" style="max-width:12rem;border-radius:.6rem">' +
        ' <button class="btn btn-plain btn-sm" id="img-clear">✖</button>';
      document.getElementById("img-clear").addEventListener("click", function(){
        pendingImage = null;
        document.getElementById("post-preview").innerHTML = "";
        document.getElementById("post-image").value = "";
      });
    }catch(e){ toast("Could not read that photo.", "err"); }
  });

  document.getElementById("post-submit").addEventListener("click", submitPost);
  document.getElementById("feed-more").addEventListener("click", function(){ loadFeed(false); });

  document.getElementById("feed-box").addEventListener("click", function(e){
    var t = e.target.closest("[data-react],[data-comments],[data-share],[data-del],[data-report],[data-comment-send],[data-report-send]");
    if(!t) return;
    var id = t.getAttribute("data-react") ? t.getAttribute("data-id") :
      t.getAttribute("data-comments") || t.getAttribute("data-share") ||
      t.getAttribute("data-del") || t.getAttribute("data-report") ||
      t.getAttribute("data-comment-send") || t.getAttribute("data-report-send");
    if(t.hasAttribute("data-react")) toggleReact(id, t.getAttribute("data-react"));
    else if(t.hasAttribute("data-comments")) toggleComments(id);
    else if(t.hasAttribute("data-comment-send")) sendComment(id);
    else if(t.hasAttribute("data-share")) sharePost(id);
    else if(t.hasAttribute("data-del")) deletePost(id);
    else if(t.hasAttribute("data-report")){
      var rb = document.getElementById("rb-" + id);
      rb.style.display = rb.style.display === "none" ? "" : "none";
    }
    else if(t.hasAttribute("data-report-send")) sendReport(id);
  });

  loadFeed(true);
}
document.addEventListener("DOMContentLoaded", function(){
  if(window.zehenUserLoaded){ bootFeed(); }
  else{ document.addEventListener("zehen:user", bootFeed, {once:true}); }
});
})();
