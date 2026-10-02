/* Mysterious quiz runner — one question at a time, submit at end, then review */
(function(){
"use strict";

var slug = qp("slug");
var questions = [];
var idx = 0;
var answers = [];      // answers[i] = chosen option index or null
var submitted = false;
var quizTitle = "";

function boot(){
  var body = document.getElementById("quiz-body");
  if(!slug){ errorBox(body, "No quiz selected. Go back and pick a quiz."); return; }
  load();
}

async function load(){
  var body = document.getElementById("quiz-body");
  loadingBox(body, "Loading quiz…");
  try{
    var d = await api("/api/quizzes/" + encodeURIComponent(slug));
    var q = d.quiz || d;
    quizTitle = q.title || "Quiz";
    questions = q.questions || [];
    answers = questions.map(function(){ return null; });
    idx = 0;
    submitted = false;
    document.title = quizTitle + " — Mysterious";
    render();
  }catch(e){
    errorBox(body, "Could not load this quiz: " + e.message);
  }
}

function render(){
  var body = document.getElementById("quiz-body");
  if(!questions.length){
    body.innerHTML = '<div class="alert alert-info">This quiz has no questions yet.</div>';
    return;
  }
  if(submitted) return; // review rendered separately

  var q = questions[idx];
  var pct = Math.round(((idx + 1) / questions.length) * 100);
  var answeredCount = answers.filter(function(a){ return a !== null; }).length;

  var html =
    "<h1 style='margin:.4rem 0'>" + esc(quizTitle) + "</h1>" +
    '<p class="small">Question ' + (idx + 1) + " of " + questions.length +
    " · answered " + answeredCount + "/" + questions.length + "</p>" +
    '<div class="progress"><div style="width:' + pct + '%"></div></div>' +
    '<div class="card">' +
      '<div class="quiz-q">' + esc(q.q) + "</div>" +
      '<div id="opts">' + q.options.map(function(o, i){
        var sel = answers[idx] === i ? " selected" : "";
        return '<button class="option' + sel + '" data-i="' + i + '">' + esc(o) + "</button>";
      }).join("") + "</div>" +
    "</div>" +
    '<div style="display:flex;gap:.7rem;margin-top:1.2rem;flex-wrap:wrap">' +
      (idx > 0 ? '<button class="btn btn-plain" id="q-prev">← Back</button>' : "") +
      '<span style="flex:1"></span>' +
      (idx < questions.length - 1
        ? '<button class="btn btn-primary" id="q-next">Next →</button>'
        : '<button class="btn btn-terra" id="q-submit">Submit quiz ✓</button>') +
    "</div>" +
    '<div class="chip-row" style="margin-top:1.2rem">' +
      questions.map(function(_, i){
        var st = answers[i] !== null ? " active" : "";
        return '<button class="chip-btn' + st + '" data-jump="' + i + '" style="min-width:2.6rem">' + (i + 1) + "</button>";
      }).join("") +
    "</div>";

  body.innerHTML = html;

  body.querySelectorAll("#opts .option").forEach(function(b){
    b.addEventListener("click", function(){
      answers[idx] = parseInt(b.getAttribute("data-i"), 10);
      render();
    });
  });
  body.querySelectorAll("[data-jump]").forEach(function(b){
    b.addEventListener("click", function(){ idx = parseInt(b.getAttribute("data-jump"), 10); render(); });
  });
  var prev = document.getElementById("q-prev");
  if(prev) prev.addEventListener("click", function(){ if(idx > 0){ idx--; render(); } });
  var next = document.getElementById("q-next");
  if(next) next.addEventListener("click", function(){
    if(idx < questions.length - 1){ idx++; render(); }
  });
  var sub = document.getElementById("q-submit");
  if(sub) sub.addEventListener("click", submitQuiz);
}

async function submitQuiz(){
  var body = document.getElementById("quiz-body");
  var unanswered = answers.filter(function(a){ return a === null; }).length;
  if(unanswered > 0){
    if(!window.confirm("You have " + unanswered + " unanswered question" + (unanswered > 1 ? "s" : "") + ". Submit anyway?")) return;
    answers = answers.map(function(a){ return a === null ? -1 : a; });
  }
  if(!window.zehenUser){
    window.location.href = "auth.html?next=" + encodeURIComponent("quiz.html?slug=" + slug);
    return;
  }
  body.innerHTML = '<div class="card"><div class="loading-box"><span class="spinner"></span> Checking your answers…</div></div>';
  try{
    var r = await api("/api/quizzes/" + encodeURIComponent(slug) + "/submit", {
      method:"POST", body:{answers: answers}
    });
    submitted = true;
    window.zehenRefreshUser();
    renderReview(r);
  }catch(e){
    toast(e.message, "err");
    render();
  }
}

function renderReview(r){
  var body = document.getElementById("quiz-body");
  var pct = Math.round((r.score / r.total) * 100);
  var emoji = pct >= 80 ? "🌟" : pct >= 50 ? "👍" : "💪";
  var html =
    '<div class="card" style="text-align:center;margin-bottom:1.4rem">' +
      '<div style="font-size:3rem">' + emoji + "</div>" +
      "<h2>Your score: " + esc(r.score) + " / " + esc(r.total) + "</h2>" +
      '<p class="lead">+' + esc(r.xp) + " XP earned" + (r.leveledUp ? " · 🎉 <strong>Level up!</strong>" : "") + "</p>" +
      '<div style="display:flex;gap:.7rem;justify-content:center;flex-wrap:wrap">' +
        '<button class="btn btn-primary" id="q-retry">Try again</button>' +
        '<a class="btn btn-ghost" href="quizzes.html">More quizzes</a>' +
      "</div>" +
    "</div>" +
    "<h3>Review</h3>" +
    questions.map(function(q, i){
      var res = (r.results && r.results[i]) || {};
      var mine = answers[i];
      var ok = !!res.correct;
      return '<div class="result-row ' + (ok ? "right" : "wrong") + '">' +
        '<div class="verdict">' + (ok ? "✓ Correct" : "✗ Not quite") + " — Q" + (i + 1) + "</div>" +
        '<div style="font-weight:700;margin-bottom:.4rem">' + esc(q.q) + "</div>" +
        (mine >= 0 ? '<div class="small">Your answer: ' + esc(q.options[mine] || "—") + "</div>" : "") +
        (!ok && res.correctIndex !== undefined && q.options[res.correctIndex]
          ? '<div class="small"><strong>Correct answer:</strong> ' + esc(q.options[res.correctIndex]) + "</div>" : "") +
        (res.explanation ? '<div class="expl">💡 ' + esc(res.explanation) + "</div>" : "") +
      "</div>";
    }).join("");

  body.innerHTML = html;
  document.getElementById("q-retry").addEventListener("click", function(){
    answers = questions.map(function(){ return null; });
    idx = 0;
    submitted = false;
    render();
  });
  window.scrollTo({top:0, behavior:"smooth"});
}

document.addEventListener("DOMContentLoaded", boot);
})();
