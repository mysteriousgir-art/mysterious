/* Mysterious admin panel */
(function(){
"use strict";

function pick(obj){
  for(var i = 1; i < arguments.length; i++){
    var k = arguments[i];
    if(obj && obj[k] !== undefined && obj[k] !== null) return obj[k];
  }
  return undefined;
}

function showTab(name){
  document.querySelectorAll("[data-atab]").forEach(function(b){
    b.classList.toggle("active", b.getAttribute("data-atab") === name);
  });
  ["dash","users","notes","quizzes","communities","reports"].forEach(function(t){
    document.getElementById("atab-" + t).style.display = t === name ? "" : "none";
  });
  if(name === "dash") loadDash();
  if(name === "users") loadUsers("");
  if(name === "notes") loadNotes();
  if(name === "quizzes") loadQuizzes();
  if(name === "communities") loadCommunities();
  if(name === "reports") loadReports();
}

function gate(){
  var gate = document.getElementById("admin-gate");
  if(window.zehenUser && window.zehenUser.isAdmin){
    gate.innerHTML = "";
    document.getElementById("admin-ui").style.display = "";
    showTab("dash");
  }else if(window.zehenUser){
    gate.innerHTML = '<div class="alert alert-err">⛔ <strong>Access denied.</strong> This area is for the site admin only.</div>';
  }else{
    gate.innerHTML = '<div class="alert alert-info">🔒 Please <a href="auth.html?next=' +
      encodeURIComponent("admin.html") + '">log in</a> as an admin to continue.</div>';
  }
}

/* ================= modal ================= */
function openModal(title, bodyHtml, onMount){
  var root = document.getElementById("modal-root");
  root.innerHTML =
    '<div class="modal-back" id="modal-back"><div class="modal" role="dialog">' +
      "<h3>" + esc(title) + "</h3>" +
      '<div id="modal-body">' + bodyHtml + "</div>" +
      '<div style="text-align:right;margin-top:1.2rem"><button class="btn btn-plain" id="modal-close">Cancel</button></div>' +
    "</div></div>";
  var close = function(){ root.innerHTML = ""; };
  document.getElementById("modal-close").addEventListener("click", close);
  document.getElementById("modal-back").addEventListener("click", function(e){
    if(e.target.id === "modal-back") close();
  });
  if(onMount) onMount(close);
}

/* ================= DASHBOARD ================= */
async function loadDash(){
  var box = document.getElementById("atab-dash");
  loadingBox(box, "Loading dashboard…");
  try{
    var s = await api("/api/admin/stats");
    var totalUsers = pick(s, "totalUsers", "users", "total_users") || 0;
    var new7 = pick(s, "newUsers7d", "new7d", "signups7dCount") || 0;
    var new30 = pick(s, "newUsers30d", "new30d") || 0;
    var dau = pick(s, "dau", "dailyActive", "activeToday") || 0;
    var openReports = pick(s, "openReports", "reports") || 0;
    var totalMessages = pick(s, "totalMessages", "messages") || 0;

    var signups = pick(s, "signups7d", "signups", "dailySignups") || [];
    var topCountries = pick(s, "topCountries", "countries") || [];
    var topNotes = pick(s, "topNotes", "notes") || [];
    var topQuizzes = pick(s, "topQuizzes", "quizzes") || [];

    box.innerHTML =
      '<div class="stat-grid">' +
        statCard(totalUsers, "Total users") +
        statCard(new7, "New · 7 days") +
        statCard(new30, "New · 30 days") +
        statCard(dau, "Active today") +
        statCard(openReports, "Open reports") +
        statCard(totalMessages, "Chat messages") +
      "</div>" +
      '<div class="grid grid-2">' +
        '<div class="card"><h3>📈 Signups — last 7 days</h3><canvas id="chart-signups" style="width:100%;height:220px"></canvas></div>' +
        '<div class="card"><h3>🌍 Top countries</h3><div id="dash-countries"></div></div>' +
      "</div>" +
      '<div class="grid grid-2" style="margin-top:1.4rem">' +
        '<div class="card"><h3>📚 Top notes</h3><div id="dash-notes"></div></div>' +
        '<div class="card"><h3>🧩 Top quizzes</h3><div id="dash-quizzes"></div></div>' +
      "</div>";

    drawBars(document.getElementById("chart-signups"), normSeries(signups));
    document.getElementById("dash-countries").innerHTML = listOrEmpty(
      topCountries.map(function(c){ return esc(pick(c,"country","name") || "?") + " — <strong>" + esc(pick(c,"count","users") || 0) + "</strong>"; }));
    document.getElementById("dash-notes").innerHTML = listOrEmpty(
      topNotes.map(function(n){ return esc(pick(n,"title","name") || "?") + " — <strong>" + esc(pick(n,"readCount","reads","count") || 0) + " reads</strong>"; }));
    document.getElementById("dash-quizzes").innerHTML = listOrEmpty(
      topQuizzes.map(function(q){ return esc(pick(q,"title","name") || "?") + " — <strong>" + esc(pick(q,"playCount","plays","count") || 0) + " plays</strong>"; }));

    var badge = document.getElementById("rep-badge");
    if(badge && openReports > 0) badge.innerHTML = '<span class="chip terra">' + esc(openReports) + "</span>";
  }catch(e){
    errorBox(box, "Could not load dashboard: " + e.message);
  }
}

function statCard(n, label){
  return '<div class="stat"><div class="n">' + esc(n) + '</div><div class="l">' + esc(label) + "</div></div>";
}
function listOrEmpty(items){
  return items.length ? "<ul class='task-list'>" + items.map(function(i){ return "<li>" + i + "</li>"; }).join("") + "</ul>"
    : '<p class="small">Nothing to show yet.</p>';
}

function normSeries(data){
  // accept [{date,count}] | [{day,count}] | [counts]
  var out = [];
  if(!Array.isArray(data)) return out;
  data.slice(-7).forEach(function(d, i){
    if(typeof d === "number") out.push({label:"D" + (i + 1), value:d});
    else out.push({
      label: shortDay(pick(d, "date", "day", "label") || ("D" + (i + 1))),
      value: pick(d, "count", "value", "signups") || 0
    });
  });
  while(out.length < 7) out.unshift({label:"—", value:0});
  return out;
}
function shortDay(label){
  var d = new Date(label);
  if(!isNaN(d)) return d.toLocaleDateString(undefined, {weekday:"short"});
  return String(label).slice(0, 6);
}

function drawBars(canvas, series){
  if(!canvas) return;
  var W = 560, H = 220, pad = 34;
  canvas.width = W; canvas.height = H;
  var ctx = canvas.getContext("2d");
  ctx.clearRect(0, 0, W, H);
  var max = Math.max.apply(null, series.map(function(s){ return s.value; }).concat([1]));
  var bw = (W - pad * 2) / series.length;
  ctx.font = "11px sans-serif"; ctx.textAlign = "center";
  series.forEach(function(s, i){
    var h = (H - pad * 2) * (s.value / max);
    var x = pad + i * bw + bw * 0.18;
    var y = H - pad - h;
    ctx.fillStyle = "#0f766e";
    var r = 6;
    ctx.beginPath();
    ctx.moveTo(x, y + r);
    ctx.arcTo(x, y, x + r, y, r);
    ctx.arcTo(x + bw * 0.64, y, x + bw * 0.64, y + r, r);
    ctx.lineTo(x + bw * 0.64, y + h);
    ctx.lineTo(x, y + h);
    ctx.closePath(); ctx.fill();
    ctx.fillStyle = "#334155";
    ctx.fillText(String(s.value), x + bw * 0.32, y - 6);
    ctx.fillStyle = "#64748b";
    ctx.fillText(s.label, x + bw * 0.32, H - pad + 16);
  });
}

/* ================= USERS ================= */
var userSearchTimer = null;
async function loadUsers(q){
  var box = document.getElementById("atab-users");
  box.innerHTML =
    '<div class="toolbar"><input class="input" id="user-q" placeholder="Search users by name or email…" value="' + esc(q || "") + '"></div>' +
    '<div id="user-table"><div class="loading-box"><span class="spinner"></span> Loading users…</div></div>';
  var inp = document.getElementById("user-q");
  inp.addEventListener("input", function(){
    clearTimeout(userSearchTimer);
    userSearchTimer = setTimeout(function(){ fetchUsers(inp.value); }, 350);
  });
  fetchUsers(q);
}

async function fetchUsers(q){
  var box = document.getElementById("user-table");
  try{
    var users = await api("/api/admin/users" + (q ? "?q=" + encodeURIComponent(q) : ""));
    if(!users || !users.length){
      box.innerHTML = '<div class="alert alert-info">No users found.</div>';
      return;
    }
    box.innerHTML = '<div class="card" style="padding:0;overflow-x:auto"><table class="atable"><thead><tr>' +
      "<th>User</th><th>Email</th><th>Country</th><th>XP</th><th>Level</th><th>Status</th><th>Action</th>" +
      "</tr></thead><tbody>" +
      users.map(function(u){
        var banned = !!pick(u, "banned", "isBanned");
        return "<tr>" +
          "<td><strong>" + esc(u.avatar || "🧠") + " " + esc(u.displayName) + "</strong></td>" +
          "<td>" + esc(u.email || "—") + "</td>" +
          "<td>" + esc(u.country || "—") + "</td>" +
          "<td>" + esc(u.xp || 0) + "</td>" +
          "<td>" + esc(u.level || 1) + "</td>" +
          "<td>" + (banned ? '<span class="chip terra">Banned</span>' : '<span class="chip">Active</span>') + "</td>" +
          '<td><button class="btn ' + (banned ? "btn-primary" : "btn-danger") + ' btn-sm" data-uid="' + esc(u.id) + '" data-ban="' + (banned ? "0" : "1") + '">' +
            (banned ? "Unban" : "Ban") + "</button></td></tr>";
      }).join("") + "</tbody></table></div>";
    box.querySelectorAll("[data-uid]").forEach(function(btn){
      btn.addEventListener("click", async function(){
        var uid = btn.getAttribute("data-uid");
        var ban = btn.getAttribute("data-ban") === "1";
        if(ban && !window.confirm("Ban this user? They will not be able to log in.")) return;
        btn.disabled = true;
        try{
          await api("/api/admin/users/" + encodeURIComponent(uid) + (ban ? "/ban" : "/unban"), {method:"POST"});
          toast(ban ? "User banned" : "User unbanned", ban ? "err" : "ok");
          fetchUsers(document.getElementById("user-q").value);
        }catch(e){ toast(e.message, "err"); btn.disabled = false; }
      });
    });
  }catch(e){
    errorBox(box, "Could not load users: " + e.message);
  }
}

/* ================= NOTES CRUD ================= */
async function loadNotes(){
  var box = document.getElementById("atab-notes");
  box.innerHTML = '<div style="margin-bottom:1.2rem"><button class="btn btn-terra" id="note-add">＋ Add note</button></div>' +
    '<div id="note-list"><div class="loading-box"><span class="spinner"></span> Loading notes…</div></div>';
  document.getElementById("note-add").addEventListener("click", function(){ noteForm(null); });
  try{
    var notes = await api("/api/notes");
    var list = document.getElementById("note-list");
    if(!notes || !notes.length){ list.innerHTML = '<div class="alert alert-info">No notes yet.</div>'; return; }
    list.innerHTML = '<div class="card" style="padding:0;overflow-x:auto"><table class="atable"><thead><tr>' +
      "<th>Title</th><th>Category</th><th>Reads</th><th>Actions</th></tr></thead><tbody>" +
      notes.map(function(n){
        return "<tr><td><strong>" + esc(n.title) + "</strong><br><span class='small'>/" + esc(n.slug) + "</span></td>" +
          "<td>" + esc(n.category) + "</td><td>" + esc(n.readCount || 0) + "</td>" +
          '<td style="white-space:nowrap"><button class="btn btn-ghost btn-sm" data-nedit="' + esc(n.id || n.slug) + '">Edit</button> ' +
          '<button class="btn btn-danger btn-sm" data-ndel="' + esc(n.id || n.slug) + '">Delete</button></td></tr>';
      }).join("") + "</tbody></table></div>";
    list.querySelectorAll("[data-nedit]").forEach(function(b){
      b.addEventListener("click", async function(){
        var id = b.getAttribute("data-nedit");
        var n = notes.find(function(x){ return String(x.id || x.slug) === id; });
        if(!n.slug){ toast("Cannot edit: note slug unknown", "err"); return; }
        try{
          var full = await api("/api/notes/" + encodeURIComponent(n.slug));
          noteForm(full.note || full);
        }catch(e){ toast(e.message, "err"); }
      });
    });
    list.querySelectorAll("[data-ndel]").forEach(function(b){
      b.addEventListener("click", async function(){
        if(!window.confirm("Delete this note permanently?")) return;
        try{
          await api("/api/admin/notes/" + encodeURIComponent(b.getAttribute("data-ndel")), {method:"DELETE"});
          toast("Note deleted", "ok"); loadNotes();
        }catch(e){ toast(e.message, "err"); }
      });
    });
  }catch(e){
    errorBox(document.getElementById("note-list"), "Could not load notes: " + e.message);
  }
}

function noteForm(note){
  var isEdit = !!note;
  var pts = (note && note.points) || [{point:"", example:""}];
  openModal(isEdit ? "Edit note" : "Add note",
    '<div class="field"><label>Slug (URL-friendly, e.g. what-is-memory)</label>' +
      '<input class="input" id="nf-slug" value="' + esc(note ? note.slug : "") + '"' + (isEdit ? " disabled" : "") + '></div>' +
    '<div class="field"><label>Title</label><input class="input" id="nf-title" value="' + esc(note ? note.title : "") + '"></div>' +
    '<div class="field"><label>Category</label><input class="input" id="nf-cat" value="' + esc(note ? note.category : "") + '" placeholder="e.g. Cognitive Psychology"></div>' +
    '<div class="field"><label>Summary</label><textarea class="input" id="nf-sum" style="min-height:4rem">' + esc(note ? note.summary : "") + "</textarea></div>" +
    '<div class="field"><label>Points (each with an example)</label><div id="nf-points"></div>' +
      '<button type="button" class="btn btn-plain btn-sm" id="nf-addpt">＋ Add point</button></div>' +
    '<div id="nf-msg"></div>' +
    '<button class="btn btn-terra" id="nf-save">' + (isEdit ? "Save changes" : "Create note") + "</button>",
    function(close){
      var ptsBox = document.getElementById("nf-points");
      function ptRow(p){
        var row = document.createElement("div");
        row.className = "card";
        row.style.cssText = "padding:.9rem;margin-bottom:.7rem";
        row.innerHTML =
          '<div class="field" style="margin-bottom:.6rem"><label>Point</label><input class="input pt-p" value="' + esc(p.point || "") + '"></div>' +
          '<div class="field" style="margin-bottom:.6rem"><label>Example</label><input class="input pt-e" value="' + esc(p.example || "") + '"></div>' +
          '<button type="button" class="btn btn-plain btn-sm pt-del">Remove</button>';
        row.querySelector(".pt-del").addEventListener("click", function(){ row.remove(); });
        return row;
      }
      pts.forEach(function(p){ ptsBox.appendChild(ptRow(p)); });
      document.getElementById("nf-addpt").addEventListener("click", function(){ ptsBox.appendChild(ptRow({})); });
      document.getElementById("nf-save").addEventListener("click", async function(){
        var btn = this;
        var points = Array.prototype.map.call(ptsBox.querySelectorAll(".card"), function(row){
          return {
            point: row.querySelector(".pt-p").value.trim(),
            example: row.querySelector(".pt-e").value.trim()
          };
        }).filter(function(p){ return p.point; });
        var payload = {
          slug: document.getElementById("nf-slug").value.trim().toLowerCase().replace(/[^a-z0-9-]+/g, "-"),
          title: document.getElementById("nf-title").value.trim(),
          category: document.getElementById("nf-cat").value.trim(),
          summary: document.getElementById("nf-sum").value.trim(),
          points: points
        };
        var msg = document.getElementById("nf-msg");
        if(!payload.slug || !payload.title || !payload.category || !points.length){
          msg.innerHTML = '<div class="alert alert-err">Slug, title, category and at least one point are required.</div>';
          return;
        }
        btn.disabled = true; btn.innerHTML = '<span class="spinner"></span> Saving…';
        try{
          if(isEdit) await api("/api/admin/notes/" + encodeURIComponent(note.id || note.slug), {method:"PUT", body:payload});
          else await api("/api/admin/notes", {method:"POST", body:payload});
          toast(isEdit ? "Note updated" : "Note created", "ok");
          close(); loadNotes();
        }catch(e){
          msg.innerHTML = '<div class="alert alert-err">' + esc(e.message) + "</div>";
          btn.disabled = false; btn.textContent = isEdit ? "Save changes" : "Create note";
        }
      });
    });
}

/* ================= QUIZZES CRUD ================= */
async function loadQuizzes(){
  var box = document.getElementById("atab-quizzes");
  box.innerHTML = '<div style="margin-bottom:1.2rem"><button class="btn btn-terra" id="quiz-add">＋ Add quiz</button></div>' +
    '<div id="quiz-list"><div class="loading-box"><span class="spinner"></span> Loading quizzes…</div></div>';
  document.getElementById("quiz-add").addEventListener("click", function(){ quizForm(null); });
  try{
    var quizzes = await api("/api/quizzes");
    var list = document.getElementById("quiz-list");
    if(!quizzes || !quizzes.length){ list.innerHTML = '<div class="alert alert-info">No quizzes yet.</div>'; return; }
    list.innerHTML = '<div class="card" style="padding:0;overflow-x:auto"><table class="atable"><thead><tr>' +
      "<th>Title</th><th>Questions</th><th>Plays</th><th>Actions</th></tr></thead><tbody>" +
      quizzes.map(function(q){
        return "<tr><td><strong>" + esc(q.title) + "</strong><br><span class='small'>/" + esc(q.slug) + "</span></td>" +
          "<td>" + esc(q.questionCount || 0) + "</td><td>" + esc(q.playCount || 0) + "</td>" +
          '<td style="white-space:nowrap"><button class="btn btn-ghost btn-sm" data-qedit="' + esc(q.id || q.slug) + '">Edit</button> ' +
          '<button class="btn btn-danger btn-sm" data-qdel="' + esc(q.id || q.slug) + '">Delete</button></td></tr>';
      }).join("") + "</tbody></table></div>";
    list.querySelectorAll("[data-qedit]").forEach(function(b){
      b.addEventListener("click", async function(){
        var id = b.getAttribute("data-qedit");
        var q = quizzes.find(function(x){ return String(x.id || x.slug) === id; });
        try{
          var full = await api("/api/quizzes/" + encodeURIComponent(q.slug));
          quizForm(full.quiz || full);
        }catch(e){ toast(e.message, "err"); }
      });
    });
    list.querySelectorAll("[data-qdel]").forEach(function(b){
      b.addEventListener("click", async function(){
        if(!window.confirm("Delete this quiz permanently?")) return;
        try{
          await api("/api/admin/quizzes/" + encodeURIComponent(b.getAttribute("data-qdel")), {method:"DELETE"});
          toast("Quiz deleted", "ok"); loadQuizzes();
        }catch(e){ toast(e.message, "err"); }
      });
    });
  }catch(e){
    errorBox(document.getElementById("quiz-list"), "Could not load quizzes: " + e.message);
  }
}

function quizForm(quiz){
  var isEdit = !!quiz;
  var qs = (quiz && quiz.questions) || [{q:"", options:["","","",""], answer:0, explanation:""}];
  openModal(isEdit ? "Edit quiz" : "Add quiz",
    '<div class="field"><label>Slug (URL-friendly)</label>' +
      '<input class="input" id="qf-slug" value="' + esc(quiz ? quiz.slug : "") + '"' + (isEdit ? " disabled" : "") + '></div>' +
    '<div class="field"><label>Title</label><input class="input" id="qf-title" value="' + esc(quiz ? quiz.title : "") + '"></div>' +
    '<div class="field"><label>Related note slug (optional)</label><input class="input" id="qf-note" value="' + esc(quiz ? (quiz.noteSlug || "") : "") + '" placeholder="e.g. what-is-memory"></div>' +
    '<div class="field"><label>Questions</label><div id="qf-qs"></div>' +
      '<button type="button" class="btn btn-plain btn-sm" id="qf-addq">＋ Add question</button></div>' +
    '<div id="qf-msg"></div>' +
    '<button class="btn btn-terra" id="qf-save">' + (isEdit ? "Save changes" : "Create quiz") + "</button>",
    function(close){
      var qBox = document.getElementById("qf-qs");
      function qRow(qq, n){
        var row = document.createElement("div");
        row.className = "card";
        row.style.cssText = "padding:.9rem;margin-bottom:.7rem";
        var opts = (qq.options || ["","","",""]).concat(["","","",""]).slice(0, 4);
        row.innerHTML =
          "<h4>Question " + n + "</h4>" +
          '<div class="field" style="margin-bottom:.6rem"><label>Question</label><textarea class="input q-q" style="min-height:3.5rem">' + esc(qq.q || "") + "</textarea></div>" +
          opts.map(function(o, i){
            return '<div class="field" style="margin-bottom:.5rem"><label>Option ' + (i + 1) + "</label>" +
              '<input class="input q-o" data-i="' + i + '" value="' + esc(o) + '"></div>';
          }).join("") +
          '<div class="field" style="margin-bottom:.6rem"><label>Correct option</label>' +
            '<select class="input q-a">' + [0,1,2,3].map(function(i){
              return '<option value="' + i + '"' + ((qq.answer || 0) === i ? " selected" : "") + ">Option " + (i + 1) + "</option>";
            }).join("") + "</select></div>" +
          '<div class="field" style="margin-bottom:.6rem"><label>Explanation</label><input class="input q-e" value="' + esc(qq.explanation || "") + '"></div>' +
          '<button type="button" class="btn btn-plain btn-sm q-del">Remove question</button>';
        row.querySelector(".q-del").addEventListener("click", function(){ row.remove(); renumber(); });
        return row;
      }
      function renumber(){
        Array.prototype.forEach.call(qBox.querySelectorAll(".card h4"), function(h, i){
          h.textContent = "Question " + (i + 1);
        });
      }
      qs.forEach(function(qq, i){ qBox.appendChild(qRow(qq, i + 1)); });
      document.getElementById("qf-addq").addEventListener("click", function(){
        qBox.appendChild(qRow({q:"", options:["","","",""], answer:0, explanation:""}, qBox.children.length + 1));
      });
      document.getElementById("qf-save").addEventListener("click", async function(){
        var btn = this;
        var questions = Array.prototype.map.call(qBox.querySelectorAll(".card"), function(row){
          var options = Array.prototype.map.call(row.querySelectorAll(".q-o"), function(o){ return o.value.trim(); });
          return {
            q: row.querySelector(".q-q").value.trim(),
            options: options,
            answer: parseInt(row.querySelector(".q-a").value, 10),
            explanation: row.querySelector(".q-e").value.trim()
          };
        }).filter(function(qq){ return qq.q && qq.options.every(function(o){ return o; }); });
        var payload = {
          slug: document.getElementById("qf-slug").value.trim().toLowerCase().replace(/[^a-z0-9-]+/g, "-"),
          title: document.getElementById("qf-title").value.trim(),
          noteSlug: document.getElementById("qf-note").value.trim() || undefined,
          questions: questions
        };
        var msg = document.getElementById("qf-msg");
        if(!payload.slug || !payload.title || !questions.length){
          msg.innerHTML = '<div class="alert alert-err">Slug, title and at least one complete question (all 4 options filled) are required.</div>';
          return;
        }
        btn.disabled = true; btn.innerHTML = '<span class="spinner"></span> Saving…';
        try{
          if(isEdit) await api("/api/admin/quizzes/" + encodeURIComponent(quiz.id || quiz.slug), {method:"PUT", body:payload});
          else await api("/api/admin/quizzes", {method:"POST", body:payload});
          toast(isEdit ? "Quiz updated" : "Quiz created", "ok");
          close(); loadQuizzes();
        }catch(e){
          msg.innerHTML = '<div class="alert alert-err">' + esc(e.message) + "</div>";
          btn.disabled = false; btn.textContent = isEdit ? "Save changes" : "Create quiz";
        }
      });
    });
}

/* ================= REPORTS ================= */
async function loadReports(){
  var box = document.getElementById("atab-reports");
  loadingBox(box, "Loading reports…");
  try{
    var reports = await api("/api/admin/reports");
    var open = (reports || []).filter(function(r){ return !r.resolved; });
    if(!reports || !reports.length){
      box.innerHTML = '<div class="alert alert-ok">🌿 No reports. The community is peaceful.</div>';
      return;
    }
    box.innerHTML =
      (open.length ? '<div class="alert alert-err">⚠️ <strong>' + open.length + "</strong> open report" + (open.length > 1 ? "s" : "") + " need" + (open.length > 1 ? "" : "s") + " review.</div>" : "") +
      '<div class="card" style="padding:0;overflow-x:auto"><table class="atable"><thead><tr>' +
      "<th>Reported user</th><th>Reason</th><th>When</th><th>Status</th><th>Action</th></tr></thead><tbody>" +
      reports.map(function(r){
        var id = r.id;
        return "<tr>" +
          "<td><strong>" + esc(r.displayName || r.reportedName || "User " + (r.userId || "?")) + "</strong>" +
          (r.userId ? '<br><span class="small">id: ' + esc(r.userId) + "</span>" : "") + "</td>" +
          '<td style="max-width:22rem">' + esc(r.reason || "—") + "</td>" +
          "<td>" + esc(r.at ? new Date(r.at).toLocaleString() : "—") + "</td>" +
          "<td>" + (r.resolved ? '<span class="chip">Resolved</span>' : '<span class="chip terra">Open</span>') + "</td>" +
          '<td>' + (!r.resolved ? '<button class="btn btn-primary btn-sm" data-resolve="' + esc(id) + '">Resolve</button>' : "—") + "</td></tr>";
      }).join("") + "</tbody></table></div>";
    box.querySelectorAll("[data-resolve]").forEach(function(b){
      b.addEventListener("click", async function(){
        b.disabled = true;
        try{
          await api("/api/admin/reports/" + encodeURIComponent(b.getAttribute("data-resolve")) + "/resolve", {method:"POST"});
          toast("Report resolved", "ok");
          loadReports();
        }catch(e){ toast(e.message, "err"); b.disabled = false; }
      });
    });
  }catch(e){
    errorBox(box, "Could not load reports: " + e.message);
  }
}

/* ================= COMMUNITIES ================= */
async function loadCommunities(){
  var box = document.getElementById("atab-communities");
  loadingBox(box, "Loading communities…");
  try{
    var rooms = await api("/api/chat/rooms");
    var html =
      '<div class="card" style="margin-bottom:1.2rem"><h3 style="margin-top:0">➕ New community</h3>' +
      '<div style="display:grid;gap:.7rem;max-width:32rem">' +
      '<input class="input" id="nc-name" placeholder="Community name (e.g. Anxiety Support Circle)" maxlength="80">' +
      '<textarea class="input" id="nc-desc" placeholder="Short description…" rows="2" maxlength="300"></textarea>' +
      '<label style="display:flex;gap:.5rem;align-items:center;font-size:.92rem"><input type="checkbox" id="nc-approval" checked> Require admin approval before members can send messages</label>' +
      '<div><button class="btn btn-primary" id="nc-create">Create community</button></div>' +
      "</div></div>" +
      '<div class="card" style="padding:0;overflow-x:auto"><table class="atable"><thead><tr>' +
      "<th>Community</th><th>Approval</th><th>Pending</th><th>Action</th></tr></thead><tbody>" +
      (rooms || []).map(function(r){
        return "<tr>" +
          '<td><strong>🏠 ' + esc(r.name) + "</strong><br>" +
          '<span class="small">#' + esc(r.slug) + "</span>" +
          (r.description ? '<br><span class="small">' + esc(r.description) + "</span>" : "") + "</td>" +
          "<td>" + (r.requires_approval ? '<span class="chip terra">Approval on</span>' : '<span class="chip">Open</span>') + "</td>" +
          '<td><button class="btn btn-ghost btn-sm" data-members="' + esc(r.slug) + '">View requests</button><div id="mem-' + esc(r.slug) + '" style="margin-top:.5rem"></div></td>' +
          '<td><button class="btn btn-plain btn-sm" data-delroom="' + esc(r.slug) + '">Delete</button></td></tr>';
      }).join("") + "</tbody></table></div>";
    if(!(rooms || []).length) html += '<p class="small">No communities yet — create the first one above. 🌿</p>';
    box.innerHTML = html;

    document.getElementById("nc-create").addEventListener("click", async function(){
      var name = document.getElementById("nc-name").value.trim();
      var description = document.getElementById("nc-desc").value.trim();
      var requires_approval = document.getElementById("nc-approval").checked;
      if(!name){ toast("Please give the community a name.", "err"); return; }
      this.disabled = true;
      try{
        await api("/api/chat/rooms", {method:"POST", body:{name:name, description:description, requires_approval:requires_approval}});
        toast("Community created! 🎉", "ok");
        loadCommunities();
      }catch(e){ toast(e.message, "err"); this.disabled = false; }
    });

    box.querySelectorAll("[data-delroom]").forEach(function(b){
      b.addEventListener("click", async function(){
        var slug = b.getAttribute("data-delroom");
        if(!window.confirm("Delete this community and all its messages?")) return;
        b.disabled = true;
        try{
          await api("/api/chat/rooms?slug=" + encodeURIComponent(slug), {method:"DELETE"});
          toast("Community deleted.", "ok");
          loadCommunities();
        }catch(e){ toast(e.message, "err"); b.disabled = false; }
      });
    });

    box.querySelectorAll("[data-members]").forEach(function(b){
      b.addEventListener("click", async function(){
        var slug = b.getAttribute("data-members");
        var target = document.getElementById("mem-" + slug);
        b.disabled = true;
        try{
          var members = await api("/api/chat/rooms/members?slug=" + encodeURIComponent(slug));
          var pending = (members || []).filter(function(m){ return m.approved !== 1; });
          var approved = (members || []).filter(function(m){ return m.approved === 1; });
          target.innerHTML =
            (pending.length ?
              '<div style="margin-bottom:.6rem"><strong>⏳ Pending (' + pending.length + ")</strong>" +
              pending.map(function(m){
                return '<div style="display:flex;gap:.5rem;align-items:center;margin:.3rem 0">' +
                  "<span>" + esc(m.avatar || "🧠") + " " + esc(m.displayName) + "</span>" +
                  '<button class="btn btn-primary btn-sm" data-approve="' + esc(m.user_id) + '" data-slug="' + esc(slug) + '">Allow</button>' +
                  '<button class="btn btn-plain btn-sm" data-reject="' + esc(m.user_id) + '" data-slug="' + esc(slug) + '">Decline</button></div>';
              }).join("") + "</div>"
            : '<p class="small">No pending requests. 🌿</p>') +
            (approved.length ? '<div><strong>✅ Members (' + approved.length + ")</strong><br>" +
              approved.map(function(m){ return '<span class="chip" style="margin:.15rem">' + esc(m.avatar || "🧠") + " " + esc(m.displayName) + "</span>"; }).join("") + "</div>" : "");
          target.querySelectorAll("[data-approve],[data-reject]").forEach(function(x){
            x.addEventListener("click", async function(){
              x.disabled = true;
              try{
                await api("/api/chat/rooms/members", {method:"POST", body:{
                  slug: x.getAttribute("data-slug"),
                  user_id: x.getAttribute("data-approve") || x.getAttribute("data-reject"),
                  approved: x.hasAttribute("data-approve") ? 1 : 0
                }});
                toast(x.hasAttribute("data-approve") ? "Member approved ✅" : "Request declined.", "ok");
                b.disabled = false;
                b.click();
              }catch(e){ toast(e.message, "err"); x.disabled = false; }
            });
          });
        }catch(e){ toast(e.message, "err"); }
        b.disabled = false;
      });
    });
  }catch(e){
    errorBox(box, "Could not load communities: " + e.message);
  }
}

/* ================= boot ================= */
document.addEventListener("DOMContentLoaded", function(){
  document.querySelectorAll("[data-atab]").forEach(function(b){
    b.addEventListener("click", function(){ showTab(b.getAttribute("data-atab")); });
  });
  if(window.zehenUserLoaded) gate();
  else document.addEventListener("zehen:user", gate, {once:true});
});
})();
