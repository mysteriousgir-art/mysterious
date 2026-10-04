/* Mysterious profile — own edit + public view */
(function(){
"use strict";

var AVATARS = ["🧠","💭","📚","🌱","🦉","🌙","⭐","🎨","🔬","💡","🌿","🧩"];
var COUNTRIES = [
  "Afghanistan","Australia","Austria","Bahrain","Bangladesh","Belgium","Brazil","Canada",
  "China","Denmark","Egypt","Finland","France","Germany","Greece","India","Indonesia",
  "Iran","Iraq","Ireland","Italy","Japan","Jordan","Kenya","Kuwait","Malaysia","Mexico",
  "Netherlands","New Zealand","Nigeria","Norway","Oman","Pakistan","Philippines",
  "Poland","Portugal","Qatar","Russia","Saudi Arabia","Singapore","South Africa",
  "South Korea","Spain","Sri Lanka","Sweden","Switzerland","Thailand","Turkey",
  "Ukraine","United Arab Emirates","United Kingdom","United States","Vietnam","Other"
];

var targetId = qp("id");          // public view when set
var editing = false;
var profile = null;
var pickedAvatar = null;

function statRow(){
  return '<div style="display:flex;gap:.7rem;flex-wrap:wrap;margin:1rem 0">' +
    '<span class="xp-pill"><span class="lvl">Lvl ' + esc(profile.level || 1) + '</span></span>' +
    '<span class="xp-pill">' + esc(profile.xp || 0) + ' XP</span>' +
    '<span class="xp-pill streak-pill">🔥 ' + esc(profile.streak || 0) + ' day streak</span>' +
    (profile.country ? '<span class="chip">📍 ' + esc(profile.country) + "</span>" : "") +
  "</div>";
}

function render(){
  var box = document.getElementById("profile-box");
  if(targetId){
    // ---- public read-only view ----
    document.title = profile.displayName + " — Mysterious";
    var isMe = window.zehenUser && String(window.zehenUser.id) === String(targetId);
    box.innerHTML =
      '<div class="profile-top"><div class="avatar-big">' + esc(profile.avatar || "🧠") + "</div>" +
      "<div><h2 style='margin-bottom:.2rem'>" + esc(profile.displayName) + "</h2>" +
      (profile.isAdmin ? '<span class="chip terra">👑 Founder &amp; Admin</span> ' : "") +
      '<p class="small" style="margin:0">' + esc(profile.bio || "Psychology learner on Mysterious 🌿") + "</p></div></div>" +
      statRow() +
      '<p class="small" id="follow-stats" style="margin:.4rem 0"><span class="chip">👥 <span id="follower-count">…</span> followers</span> ' +
      '<span class="chip">➡️ <span id="following-count">…</span> following</span></p>' +
      '<div style="display:flex;gap:.6rem;flex-wrap:wrap;margin-top:.6rem">' +
      (window.zehenUser && !isMe
        ? '<button class="btn btn-primary btn-sm" id="follow-btn">Follow</button>' +
          '<a class="btn btn-plain btn-sm" href="community.html?dm=' + encodeURIComponent(targetId) + '">💌 Message</a>'
        : "") +
      "</div>" +
      '<div id="follow-list" style="margin-top:.8rem"></div>' +
      (isMe ? '<p class="small" style="margin-top:1rem">This is you! <a href="profile.html">Edit your profile →</a></p>' : "");
    loadFollowInfo();
    return;
  }
  // ---- own profile ----
  if(!editing){
    document.title = "Your Profile — Mysterious";
    box.innerHTML =
      '<div class="profile-top"><div class="avatar-big">' + esc(profile.avatar || "🧠") + "</div>" +
      "<div><h2 style='margin-bottom:.2rem'>" + esc(profile.displayName) + "</h2>" +
      '<p class="small" style="margin:0">' + esc(profile.email || "") + "</p>" +
      '<p class="small" style="margin:0">' + esc(profile.bio || "No bio yet — tell the community a little about you!") + "</p></div></div>" +
      statRow() +
      '<button class="btn btn-primary" id="edit-btn">✏️ Edit profile</button>';
    document.getElementById("edit-btn").addEventListener("click", function(){ editing = true; render(); });
  }else{
    pickedAvatar = profile.avatar || "🧠";
    box.innerHTML =
      "<h2>Edit profile</h2>" +
      '<div class="field"><label>Avatar</label><div class="avatar-row" id="avatar-row">' +
        AVATARS.map(function(a){
          return '<button type="button" class="avatar-pick' + (a === pickedAvatar ? " sel" : "") + '" data-av="' + a + '">' + a + "</button>";
        }).join("") + "</div></div>" +
      '<div class="field"><label for="pf-name">Display name</label>' +
        '<input class="input" id="pf-name" maxlength="40" value="' + esc(profile.displayName || "") + '">' +
        '<div class="err">Display name needs 2–40 characters.</div></div>' +
      '<div class="field"><label for="pf-bio">Bio</label>' +
        '<textarea class="input" id="pf-bio" maxlength="300" placeholder="A line or two about you…">' + esc(profile.bio || "") + "</textarea>" +
        '<div class="hint">Max 300 characters.</div></div>' +
      '<div class="field"><label for="pf-country">Country</label>' +
        '<select class="input" id="pf-country">' +
          COUNTRIES.map(function(c){
            return '<option value="' + esc(c) + '"' + (c === profile.country ? " selected" : "") + ">" + esc(c) + "</option>";
          }).join("") + "</select></div>" +
      '<div style="display:flex;gap:.7rem;flex-wrap:wrap">' +
        '<button class="btn btn-primary" id="pf-save">💾 Save changes</button>' +
        '<button class="btn btn-plain" id="pf-cancel">Cancel</button></div>' +
      '<div id="pf-msg" style="margin-top:1rem"></div>';
    box.querySelectorAll("#avatar-row .avatar-pick").forEach(function(b){
      b.addEventListener("click", function(){
        pickedAvatar = b.getAttribute("data-av");
        box.querySelectorAll("#avatar-row .avatar-pick").forEach(function(x){
          x.classList.toggle("sel", x === b);
        });
      });
    });
    document.getElementById("pf-cancel").addEventListener("click", function(){ editing = false; render(); });
    document.getElementById("pf-save").addEventListener("click", save);
  }
}

async function save(){
  var name = document.getElementById("pf-name").value.trim();
  var bio = document.getElementById("pf-bio").value.trim();
  var country = document.getElementById("pf-country").value;
  var nameOk = name.length >= 2 && name.length <= 40;
  document.getElementById("pf-name").closest(".field").classList.toggle("invalid", !nameOk);
  if(!nameOk) return;
  var btn = document.getElementById("pf-save");
  var msg = document.getElementById("pf-msg");
  btn.disabled = true; btn.innerHTML = '<span class="spinner"></span> Saving…';
  try{
    var d = await api("/api/profile", {
      method:"PUT",
      body:{displayName: name, bio: bio, avatar: pickedAvatar, country: country}
    });
    profile = d.user || d;
    window.zehenRefreshUser();
    editing = false;
    render();
    toast("Profile updated! ✨", "ok");
  }catch(e){
    msg.innerHTML = '<div class="alert alert-err">' + esc(e.message) + "</div>";
    btn.disabled = false; btn.innerHTML = "💾 Save changes";
  }
}

/* ---- follow info on public profiles ---- */
var followState = { isFollowing: false, loaded: false };

async function loadFollowInfo(){
  try{
    var d = await api("/api/follows?userId=" + encodeURIComponent(targetId) + "&type=followers");
    document.getElementById("follower-count").textContent = d.followerCount;
    document.getElementById("following-count").textContent = d.followingCount;
    followState.isFollowing = !!d.isFollowing;
    followState.loaded = true;
    paintFollowBtn();
    renderFollowList(d.users || []);
  }catch(e){ /* counts stay as … */ }
}

function paintFollowBtn(){
  var b = document.getElementById("follow-btn");
  if(!b || !followState.loaded) return;
  b.textContent = followState.isFollowing ? "✓ Following" : "＋ Follow";
  b.className = followState.isFollowing ? "btn btn-plain btn-sm" : "btn btn-primary btn-sm";
}

function renderFollowList(users){
  var box = document.getElementById("follow-list");
  if(!box || !users.length) return;
  box.innerHTML = '<p class="small" style="margin-bottom:.4rem"><strong>Followers</strong></p>' +
    '<div style="display:flex;gap:.4rem;flex-wrap:wrap">' +
    users.slice(0, 12).map(function(x){
      return '<a class="chip" href="profile.html?id=' + x.userId + '">' + esc(x.avatar) + " " + esc(x.displayName) + "</a>";
    }).join("") + "</div>";
}

async function toggleFollow(){
  var b = document.getElementById("follow-btn");
  b.disabled = true;
  try{
    if(followState.isFollowing){
      await api("/api/follows/" + encodeURIComponent(targetId), { method: "DELETE" });
      followState.isFollowing = false;
    }else{
      await api("/api/follows", { method: "POST", body: { userId: Number(targetId) } });
      followState.isFollowing = true;
      toast("Following " + (profile.displayName || "them") + "! 🎉", "ok");
    }
    paintFollowBtn();
    loadFollowInfo();
  }catch(e){
    toast(e.message, "err");
  }
  b.disabled = false;
}

document.addEventListener("click", function(e){
  if(e.target && e.target.id === "follow-btn") toggleFollow();
});

async function boot(){
  var box = document.getElementById("profile-box");
  loadingBox(box, "Loading profile…");
  try{
    if(targetId){
      profile = await api("/api/users/" + encodeURIComponent(targetId) + "/public");
    }else{
      if(!window.zehenUser){
        window.location.href = "auth.html?next=" + encodeURIComponent("profile.html");
        return;
      }
      profile = await api("/api/profile");
    }
    render();
  }catch(e){
    if(e.status === 401 && !targetId){
      window.location.href = "auth.html?next=" + encodeURIComponent("profile.html");
    }else{
      errorBox(box, "Could not load this profile: " + e.message);
    }
  }
}

document.addEventListener("DOMContentLoaded", function(){
  if(window.zehenUserLoaded) boot();
  else document.addEventListener("zehen:user", boot, {once:true});
});
})();
