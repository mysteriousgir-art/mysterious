/* Mysterious community — study rooms + DMs over REST polling (3s).
   Replaces the old socket.io transport; UI and behaviour are unchanged. */
(function(){
"use strict";

var me = null;
var view = null;            // {type:'room'|'dm', id, name, avatar}
var rooms = [];
var convs = [];
var blocks = [];
var pollTimer = null;
var lastId = 0;
var renderedIds = null;     // Set of message ids already in the DOM
var pendingTemp = null;     // {body, el} optimistic echo awaiting server echo
var tempCounter = 0;
var roomAccess = { requires_approval: 0, approved: null }; // current room's approval state

function gate(){
  var g = document.getElementById("chat-gate");
  if(me){
    g.innerHTML = "";
    document.getElementById("chat-ui").style.display = "";
    connect();
  }else{
    document.getElementById("chat-ui").style.display = "none";
    g.innerHTML = '<div class="alert alert-info">🔒 Please <a href="auth.html?next=' +
      encodeURIComponent("community.html") + '">log in</a> to join the community chat.</div>';
  }
}

function connect(){
  loadSidebar();
  // deep link: community.html?dm=<id>
  var dmId = qp("dm");
  if(dmId){ openDM(dmId); }
  else { window.addEventListener("hashchange", routeHash); routeHash(); }
}

function routeHash(){
  var h = (window.location.hash || "").replace(/^#/, "");
  if(h.indexOf("room/") === 0){
    var slug = decodeURIComponent(h.slice(5));
    var r = rooms.find(function(x){ return x.slug === slug; });
    if(r) openRoom(r.slug, r.name, r.description);
  }else if(h.indexOf("dm/") === 0){
    openDM(decodeURIComponent(h.slice(3)));
  }
}

/* ---------- sidebar ---------- */
async function loadSidebar(){
  try{
    var r = await Promise.all([
      api("/api/chat/rooms").catch(function(){ return []; }),
      api("/api/chat/conversations").catch(function(){ return []; }),
      api("/api/blocks").catch(function(){ return []; })
    ]);
    rooms = r[0] || []; convs = r[1] || []; blocks = r[2] || [];
    renderRooms(); renderConvs(); renderBlocks();
    if(!view && !qp("dm")){
      var h = (window.location.hash || "").replace(/^#/, "");
      if(!h && rooms.length) openRoom(rooms[0].slug, rooms[0].name, rooms[0].description);
      else routeHash();
    }
  }catch(e){
    toast("Could not load chat lists: " + e.message, "err");
  }
}

function renderRooms(){
  var box = document.getElementById("room-list");
  if(!rooms.length){ box.innerHTML = '<p class="small">No study rooms yet.</p>'; return; }
  box.innerHTML = rooms.map(function(r){
    var active = view && view.type === "room" && view.id === r.slug ? " active" : "";
    return '<a class="room-item' + active + '" href="#room/' + encodeURIComponent(r.slug) + '">' +
      '<div class="name">🏠 ' + esc(r.name) + "</div>" +
      (r.description ? '<div class="desc">' + esc(r.description) + "</div>" : "") +
    "</a>";
  }).join("");
}

function timeAgo(at){
  if(!at) return "";
  var s = Math.floor((Date.now() - new Date(at).getTime()) / 1000);
  if(s < 60) return "just now";
  if(s < 3600) return Math.floor(s / 60) + "m ago";
  if(s < 86400) return Math.floor(s / 3600) + "h ago";
  return Math.floor(s / 86400) + "d ago";
}

function renderConvs(){
  var box = document.getElementById("conv-list");
  if(!convs.length){ box.innerHTML = '<p class="small">No conversations yet.<br>Visit someone\'s profile to start one.</p>'; return; }
  box.innerHTML = convs.map(function(c){
    var active = view && view.type === "dm" && String(view.id) === String(c.userId) ? " active" : "";
    return '<a class="conv-item' + active + '" href="#dm/' + encodeURIComponent(c.userId) + '">' +
      '<div class="name">' + esc(c.avatar || "🧠") + " " + esc(c.displayName) + "</div>" +
      '<div class="last">' + esc(c.lastBody || "") + (c.at ? " · " + esc(timeAgo(c.at)) : "") + "</div>" +
    "</a>";
  }).join("");
}

function renderBlocks(){
  var box = document.getElementById("block-list");
  if(!blocks.length){ box.innerHTML = '<p class="small">Nobody blocked. 🌿</p>'; return; }
  box.innerHTML = blocks.map(function(b){
    return '<div class="item"><span style="font-size:1.4rem">' + esc(b.avatar || "🧠") + '</span>' +
      '<span class="nm">' + esc(b.displayName) + "</span>" +
      '<button class="btn btn-plain btn-sm" data-unblock="' + esc(b.userId) + '">Unblock</button></div>';
  }).join("");
  box.querySelectorAll("[data-unblock]").forEach(function(btn){
    btn.addEventListener("click", async function(){
      var uid = btn.getAttribute("data-unblock");
      btn.disabled = true;
      try{
        await api("/api/blocks/" + encodeURIComponent(uid), {method:"DELETE"});
        toast("User unblocked", "ok");
        blocks = blocks.filter(function(b){ return String(b.userId) !== String(uid); });
        renderBlocks();
      }catch(e){ toast(e.message, "err"); btn.disabled = false; }
    });
  });
}

/* ---------- views ---------- */
function openRoom(slug, name, description){
  view = {type:"room", id:slug, name:name || slug};
  setHead("🏠 " + (name || slug), description || "", false);
  roomAccess = { requires_approval: 0, approved: null };
  checkRoomAccess(slug);
  join();
}

/* ---------- room approval flow ---------- */
async function checkRoomAccess(slug){
  try{
    var s = await api("/api/chat/rooms/join?slug=" + encodeURIComponent(slug));
    roomAccess = { requires_approval: s.requires_approval ? 1 : 0, approved: s.approved };
  }catch(e){
    roomAccess = { requires_approval: 0, approved: 1 }; // fail open for reading; send API still enforces
  }
  applyAccessUI();
}

function applyAccessUI(){
  var inputRow = document.getElementById("chat-input-row");
  var gate = document.getElementById("room-gate");
  if(!view || view.type !== "room"){ if(gate) gate.style.display = "none"; return; }
  var needApproval = roomAccess.requires_approval === 1 && roomAccess.approved !== 1;
  if(!needApproval){
    inputRow.style.display = "";
    if(gate) gate.style.display = "none";
    return;
  }
  inputRow.style.display = "none";
  if(!gate) return;
  gate.style.display = "";
  if(roomAccess.approved === 0){
    gate.innerHTML = '<div class="alert alert-info" style="margin:0">⏳ <strong>Waiting for admin approval.</strong> You can read messages, but only approved members can send messages here.</div>';
  }else{
    gate.innerHTML = '<div class="alert alert-info" style="margin:0;display:flex;gap:.8rem;align-items:center;flex-wrap:wrap">' +
      '<span>🔒 <strong>Admin approval needed</strong> to send messages in this community.</span>' +
      '<button class="btn btn-primary btn-sm" id="room-req-btn">Request permission</button></div>';
    var b = document.getElementById("room-req-btn");
    if(b) b.addEventListener("click", requestRoomAccess);
  }
}

async function requestRoomAccess(){
  if(!view || view.type !== "room") return;
  var b = document.getElementById("room-req-btn");
  if(b) b.disabled = true;
  try{
    var r = await api("/api/chat/rooms/join", {method:"POST", body:{slug: view.id}});
    roomAccess.approved = r.approved;
    applyAccessUI();
    toast(r.approved === 1 ? "You can now send messages here 🌿" : "Request sent! The admin will review it soon. 🌿", "ok");
  }catch(e){
    toast(e.message, "err");
    if(b) b.disabled = false;
  }
}

async function openDM(userId){
  var name = "Chat", avatar = "🧠";
  var known = convs.find(function(c){ return String(c.userId) === String(userId); });
  if(known){ name = known.displayName; avatar = known.avatar; }
  else{
    try{
      var p = await api("/api/users/" + encodeURIComponent(userId) + "/public");
      name = p.displayName || name; avatar = p.avatar || avatar;
    }catch(e){ /* fall through with defaults */ }
  }
  view = {type:"dm", id:userId, name:name, avatar:avatar};
  setHead(avatar + " " + name, "Private conversation", true);
  join();
}

function setHead(title, sub, isDM){
  var head = document.getElementById("chat-head");
  head.innerHTML = "<h3>" + esc(title) + "</h3>" +
    (isDM ? '<div class="actions">' +
      '<button class="btn btn-plain btn-sm" id="dm-block">🚫 Block</button>' +
      '<button class="btn btn-plain btn-sm" id="dm-report">⚠️ Report</button>' +
    "</div>" : "");
  var b = document.getElementById("dm-block");
  if(b) b.addEventListener("click", blockCurrent);
  var rp = document.getElementById("dm-report");
  if(rp) rp.addEventListener("click", reportCurrent);
}

/* ---------- polling transport ---------- */

function historyUrl(since){
  var u = "/api/chat/messages?type=" + encodeURIComponent(view.type) +
    "&id=" + encodeURIComponent(view.id);
  if(since > 0) u += "&since=" + encodeURIComponent(since);
  return u;
}

function stopPoll(){
  if(pollTimer){ clearInterval(pollTimer); pollTimer = null; }
  pendingTemp = null;
}

async function join(){
  stopPoll();
  lastId = 0;
  renderedIds = new Set();
  document.getElementById("chat-body").innerHTML = '<div class="loading-box"><span class="spinner"></span> Joining…</div>';
  if(view.type === "dm"){
    document.getElementById("chat-input-row").style.display = "";
    document.getElementById("room-gate").style.display = "none";
  }else{
    applyAccessUI(); // rooms: input visibility follows approval state
  }
  renderRooms(); renderConvs();
  try{
    var d = await api(historyUrl(0));
    renderHistory((d && d.messages) || []);
  }catch(e){
    if(e.status === 403){
      document.getElementById("chat-body").innerHTML = '<div class="empty-chat">You can\'t view this conversation.</div>';
      document.getElementById("chat-input-row").style.display = "none";
    }else if(e.status === 401){
      window.location.href = "auth.html?next=" + encodeURIComponent("community.html");
      return;
    }else{
      document.getElementById("chat-body").innerHTML = '<div class="empty-chat">⚠️ Could not load messages. Please refresh.</div>';
      toast(e.message, "err");
    }
    return;
  }
  pollTimer = setInterval(pollOnce, 3000);
}

async function pollOnce(){
  if(!view) return;
  try{
    var d = await api(historyUrl(lastId));
    var msgs = (d && d.messages) || [];
    msgs.forEach(function(m){
      // drop the optimistic echo once the real message arrives
      if(pendingTemp && m.fromId === me.id && m.body === pendingTemp.body){
        if(pendingTemp.el && pendingTemp.el.parentNode) pendingTemp.el.parentNode.removeChild(pendingTemp.el);
        pendingTemp = null;
      }
      appendMsg(m);
    });
    if(msgs.length) scrollBottom();
  }catch(e){
    if(e.status === 401){
      stopPoll();
      window.location.href = "auth.html?next=" + encodeURIComponent("community.html");
    }
    // transient poll errors are silent; the next tick retries
  }
}

function renderHistory(msgs){
  var body = document.getElementById("chat-body");
  if(!msgs.length){
    body.innerHTML = '<div class="empty-chat">No messages yet — say hello! 👋</div>';
    return;
  }
  body.innerHTML = "";
  msgs.forEach(appendMsg);
  scrollBottom();
}

function appendMsg(m){
  if(!m) return;
  if(m.id && renderedIds && renderedIds.has(m.id)) return; // dedupe
  if(m.id && renderedIds) renderedIds.add(m.id);
  if(m.id && m.id > lastId) lastId = m.id;
  var body = document.getElementById("chat-body");
  var empty = body.querySelector(".empty-chat");
  if(empty) empty.remove();
  var mine = me && String(m.fromId) === String(me.id);
  var d = document.createElement("div");
  d.className = "msg" + (mine ? " mine" : "");
  if(!m.id) d.setAttribute("data-temp", "1");
  var when = m.at ? new Date(m.at).toLocaleString() : "";
  d.innerHTML = '<span class="who">' + esc(mine ? "You" : (m.fromName || "Someone")) + "</span>" +
    '<span class="text">' + esc(m.body) + "</span>" +
    (when ? '<span class="at">' + esc(when) + "</span>" : "");
  body.appendChild(d);
  return d;
}

function scrollBottom(){
  var body = document.getElementById("chat-body");
  body.scrollTop = body.scrollHeight;
}

async function send(){
  var inp = document.getElementById("chat-input");
  var body = inp.value.trim();
  if(!body || !view) return;
  inp.value = "";
  // optimistic echo
  var tempEl = appendMsg({fromId: me.id, fromName: me.displayName, body: body, at: new Date().toISOString()});
  pendingTemp = { body: body, el: tempEl };
  scrollBottom();
  try{
    await api("/api/chat/send", {method:"POST", body:{type: view.type, id: view.id, body: body}});
    pollOnce(); // pick up the real message quickly
  }catch(e){
    // roll back the optimistic echo on failure
    if(tempEl && tempEl.parentNode) tempEl.parentNode.removeChild(tempEl);
    pendingTemp = null;
    inp.value = body;
    toast(e.message, "err");
  }
}

/* ---------- block / report ---------- */
async function blockCurrent(){
  if(!view || view.type !== "dm") return;
  if(!window.confirm("Block " + view.name + "? You won't see their messages anymore.")) return;
  try{
    await api("/api/blocks", {method:"POST", body:{userId: view.id}});
    toast(view.name + " blocked", "ok");
    blocks.push({userId: view.id, displayName: view.name, avatar: view.avatar});
    renderBlocks();
    convs = convs.filter(function(c){ return String(c.userId) !== String(view.id); });
    renderConvs();
    stopPoll();
    view = null;
    document.getElementById("chat-body").innerHTML = '<div class="empty-chat">User blocked. Pick another room or conversation. 🌿</div>';
    document.getElementById("chat-input-row").style.display = "none";
    setHead("Pick a room or conversation", "", false);
  }catch(e){ toast(e.message, "err"); }
}

async function reportCurrent(){
  if(!view || view.type !== "dm") return;
  var reason = window.prompt("Why are you reporting " + view.name + "? (short reason)", "");
  if(reason === null) return;
  reason = reason.trim();
  if(!reason){ toast("Please give a short reason for the report.", "err"); return; }
  try{
    await api("/api/reports", {method:"POST", body:{userId: view.id, reason: reason}});
    toast("Report sent. Thank you — an admin will review it. 🌿", "ok");
  }catch(e){ toast(e.message, "err"); }
}

/* ---------- boot ---------- */
document.addEventListener("DOMContentLoaded", function(){
  document.getElementById("chat-send").addEventListener("click", send);
  document.getElementById("chat-input").addEventListener("keydown", function(e){
    if(e.key === "Enter") send();
  });
  if(window.zehenUserLoaded){
    me = window.zehenUser;
    if(me) gate();
    else window.location.href = "auth.html?next=" + encodeURIComponent("community.html");
  }else{
    document.addEventListener("zehen:user", function(){
      me = window.zehenUser;
      if(me) gate();
      else window.location.href = "auth.html?next=" + encodeURIComponent("community.html");
    }, {once:true});
  }
});
})();
