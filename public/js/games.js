/* Mysterious games — Memory Match, Guess the Theorist, Leaderboard */
(function(){
"use strict";

/* ================= tabs ================= */
function switchTab(name){
  document.querySelectorAll(".game-tabs .chip-btn").forEach(function(b){
    b.classList.toggle("active", b.getAttribute("data-tab") === name);
  });
  ["memory","theorist","category","board"].forEach(function(t){
    document.getElementById("tab-" + t).style.display = t === name ? "" : "none";
  });
  if(name === "board") loadBoard();
  if(name === "theorist" && !theoristStarted) startTheorist();
  if(name === "category" && window.catStartGame && !window.catGameStarted()) window.catStartGame();
}
document.addEventListener("DOMContentLoaded", function(){
  document.querySelectorAll(".game-tabs .chip-btn").forEach(function(b){
    b.addEventListener("click", function(){ switchTab(b.getAttribute("data-tab")); });
  });
  initMemory();
});

/* ================= MEMORY MATCH ================= */
var PAIRS = [
  ["Neuron", "A nerve cell that carries messages in the brain"],
  ["Classical conditioning", "Learning by association — like Pavlov's dogs salivating at a bell"],
  ["Cognitive dissonance", "Mental discomfort when beliefs and actions don't match"],
  ["Amygdala", "The brain's alarm centre for fear and emotion"],
  ["Reinforcement", "A reward or consequence that makes a behaviour more likely"],
  ["Attachment", "The deep emotional bond between a child and caregiver"],
  ["Placebo effect", "Feeling better because you believe a treatment works"],
  ["Growth mindset", "Believing your abilities can improve with effort"]
];

var memCards = [], memFirst = null, memLock = false, memMoves = 0, memFound = 0;

function shuffle(a){
  for(var i = a.length - 1; i > 0; i--){
    var j = Math.floor(Math.random() * (i + 1));
    var t = a[i]; a[i] = a[j]; a[j] = t;
  }
  return a;
}

function initMemory(){
  document.getElementById("mem-restart").addEventListener("click", startMemory);
  try{
    var best = localStorage.getItem("mysterious_mem_best");
    if(best) document.getElementById("mem-best").textContent = best;
  }catch(e){}
  startMemory();
}

function startMemory(){
  memCards = [];
  PAIRS.forEach(function(p, i){
    memCards.push({pair:i, text:p[0], kind:"term"});
    memCards.push({pair:i, text:p[1], kind:"def"});
  });
  shuffle(memCards);
  memFirst = null; memLock = false; memMoves = 0; memFound = 0;
  document.getElementById("mem-moves").textContent = "0";
  document.getElementById("mem-pairs").textContent = "0 / 8";
  document.getElementById("mem-msg").innerHTML = '<p class="small">Match each psychology term with its simple definition.</p>';
  var board = document.getElementById("mem-board");
  board.innerHTML = "";
  memCards.forEach(function(c, i){
    var btn = document.createElement("button");
    btn.className = "mem-card";
    btn.setAttribute("aria-label", "Memory card " + (i + 1));
    btn.innerHTML = '<div class="mem-inner">' +
      '<div class="mem-face mem-front">🧠</div>' +
      '<div class="mem-face mem-back">' + esc(c.text) + "</div></div>";
    btn.addEventListener("click", function(){ flipCard(btn, c); });
    board.appendChild(btn);
  });
}

function flipCard(btn, card){
  if(memLock || btn.classList.contains("flipped") || btn.classList.contains("matched")) return;
  btn.classList.add("flipped");
  if(!memFirst){ memFirst = {btn:btn, card:card}; return; }
  memMoves++;
  document.getElementById("mem-moves").textContent = memMoves;
  var first = memFirst; memFirst = null;
  if(first.card.pair === card.pair){
    memLock = true;
    setTimeout(function(){
      first.btn.classList.add("matched");
      btn.classList.add("matched");
      memFound++;
      document.getElementById("mem-pairs").textContent = memFound + " / 8";
      memLock = false;
      if(memFound === 8) memoryWin();
    }, 500);
  }else{
    memLock = true;
    setTimeout(function(){
      first.btn.classList.remove("flipped");
      btn.classList.remove("flipped");
      memLock = false;
    }, 900);
  }
}

async function memoryWin(){
  // score: fewer moves = higher score
  var score = Math.max(100, 1200 - memMoves * 40);
  document.getElementById("mem-msg").innerHTML =
    '<div class="alert alert-ok">🎉 You matched all 8 pairs in <strong>' + memMoves +
    "</strong> moves! Score: <strong>" + score + "</strong></div>";
  try{
    var best = parseInt(localStorage.getItem("mysterious_mem_best") || "0", 10);
    if(score > best){ localStorage.setItem("mysterious_mem_best", score); document.getElementById("mem-best").textContent = score; }
  }catch(e){}
  if(window.zehenUser){
    try{
      var r = await api("/api/games/play", {method:"POST", body:{game:"memory", score:score}});
      toast("+" + (r.xp || 0) + " XP earned! 🏆", "ok");
      window.zehenRefreshUser();
    }catch(e){ toast(e.message, "err"); }
  }else{
    document.getElementById("mem-msg").innerHTML +=
      '<p class="small"><a href="auth.html">Log in</a> to save your XP and join the leaderboard.</p>';
  }
}

/* ================= GUESS THE THEORIST ================= */
var THEORISTS = [
  {name:"Sigmund Freud", clue:"I said much of our behaviour is driven by the unconscious mind, and I developed psychoanalysis with the id, ego and superego."},
  {name:"Ivan Pavlov", clue:"I rang a bell every time I fed my dogs — soon they salivated at the bell alone. I discovered classical conditioning."},
  {name:"B. F. Skinner", clue:"I studied how rewards and punishments shape behaviour, using my famous 'Skinner box' with rats and pigeons."},
  {name:"Abraham Maslow", clue:"I drew a pyramid of human needs — from food and safety up to self-actualisation at the very top."},
  {name:"Jean Piaget", clue:"I watched children play and described four stages of how thinking develops, from sensorimotor to formal operations."},
  {name:"Erik Erikson", clue:"I described eight psychosocial stages of life, each with a crisis to resolve — like identity vs. role confusion in teens."},
  {name:"Albert Bandura", clue:"My Bobo doll experiment showed children copy aggressive behaviour they observe — I called it social learning theory."},
  {name:"Aaron Beck", clue:"I founded cognitive therapy, showing that distorted automatic thoughts fuel depression and anxiety."},
  {name:"Carl Rogers", clue:"I believed people grow best with unconditional positive regard, and I created person-centred therapy."},
  {name:"Stanley Milgram", clue:"My obedience experiment showed ordinary people would give electric shocks when an authority figure told them to."},
  {name:"Lev Vygotsky", clue:"I emphasised that culture and social interaction shape thinking, and described the zone of proximal development."},
  {name:"Mary Ainsworth", clue:"With my 'Strange Situation' I identified attachment styles — secure, avoidant and ambivalent — in infants."}
];
var thRounds = [], thIdx = 0, thScore = 0, theoristStarted = false, thAnswered = false;

function startTheorist(){
  theoristStarted = true;
  thRounds = shuffle(THEORISTS.slice()).slice(0, 10);
  thIdx = 0; thScore = 0;
  renderTheorist();
}

function theoristOptions(correct){
  var others = shuffle(THEORISTS.filter(function(t){ return t.name !== correct.name; })).slice(0, 3);
  return shuffle([correct].concat(others));
}

function renderTheorist(){
  var box = document.getElementById("theorist-box");
  if(thIdx >= thRounds.length){ return theoristEnd(box); }
  thAnswered = false;
  var t = thRounds[thIdx];
  var opts = theoristOptions(t);
  box.innerHTML =
    '<p class="small">Round ' + (thIdx + 1) + " of " + thRounds.length + " · Score: <strong>" + thScore + "</strong></p>" +
    '<div class="progress"><div style="width:' + Math.round(((thIdx + 1) / thRounds.length) * 100) + '%"></div></div>' +
    '<div class="quiz-q" style="font-size:1.15rem">🕵️ ' + esc(t.clue) + "</div>" +
    '<div id="th-opts">' + opts.map(function(o){
      return '<button class="option" data-name="' + esc(o.name) + '">' + esc(o.name) + "</button>";
    }).join("") + "</div>";
  box.querySelectorAll("#th-opts .option").forEach(function(b){
    b.addEventListener("click", function(){
      if(thAnswered) return;
      thAnswered = true;
      var right = b.getAttribute("data-name") === t.name;
      if(right) thScore++;
      box.querySelectorAll("#th-opts .option").forEach(function(x){
        x.disabled = true;
        if(x.getAttribute("data-name") === t.name){ x.classList.add("selected"); x.style.borderColor = "var(--green)"; x.style.background = "#f0faf5"; }
        else if(x === b){ x.style.borderColor = "var(--red)"; x.style.background = "#fdf1f1"; }
      });
      var note = document.createElement("div");
      note.className = "alert " + (right ? "alert-ok" : "alert-err");
      note.style.marginTop = "1rem";
      note.innerHTML = (right ? "✓ Correct! " : "✗ It was <strong>" + esc(t.name) + "</strong>. ") +
        '<button class="btn btn-primary btn-sm" id="th-next" style="margin-left:.6rem">Next →</button>';
      box.appendChild(note);
      document.getElementById("th-next").addEventListener("click", function(){ thIdx++; renderTheorist(); });
    });
  });
}

async function theoristEnd(box){
  var score = thScore * 100;
  var pct = Math.round((thScore / thRounds.length) * 100);
  var emoji = pct >= 80 ? "🌟" : pct >= 50 ? "👍" : "📖";
  box.innerHTML =
    '<div style="text-align:center">' +
      '<div style="font-size:3rem">' + emoji + "</div>" +
      "<h2>Game over!</h2>" +
      "<p class='lead'>You named <strong>" + thScore + " / " + thRounds.length + "</strong> theorists correctly.</p>" +
      '<p>Score: <strong>' + score + "</strong></p>" +
      '<div style="display:flex;gap:.7rem;justify-content:center;flex-wrap:wrap">' +
        '<button class="btn btn-terra" id="th-again">↻ Play again</button>' +
        '<button class="btn btn-ghost" id="th-board">🏆 Leaderboard</button>' +
      "</div>" +
    "</div>";
  document.getElementById("th-again").addEventListener("click", function(){ startTheorist(); });
  document.getElementById("th-board").addEventListener("click", function(){ switchTab("board"); });
  if(window.zehenUser){
    try{
      var r = await api("/api/games/play", {method:"POST", body:{game:"theorist", score:score}});
      toast("+" + (r.xp || 0) + " XP earned! 🏆", "ok");
      window.zehenRefreshUser();
    }catch(e){ toast(e.message, "err"); }
  }else{
    toast("Log in to save XP and join the leaderboard", "err");
  }
}

/* ================= LEADERBOARD ================= */
async function loadBoard(){
  var box = document.getElementById("board-box");
  loadingBox(box, "Loading leaderboard…");
  try{
    var rows = await api("/api/leaderboard");
    if(!rows || !rows.length){
      box.innerHTML = '<div class="alert alert-info">No players yet — play a game and be the first! 🎮</div>';
      return;
    }
    box.innerHTML =
      '<div class="card" style="padding:0;overflow:hidden">' +
      '<table class="ltable"><thead><tr><th>#</th><th>Player</th><th>Level</th><th>XP</th><th class="hide-s">Streak</th></tr></thead><tbody>' +
      rows.map(function(r, i){
        var medal = i === 0 ? "🥇" : i === 1 ? "🥈" : i === 2 ? "🥉" : (i + 1);
        var rowCls = i === 0 ? ' class="rank-1 top"' : i < 3 ? ' class="top"' : "";
        return "<tr" + rowCls + '><td class="rank">' + medal + "</td>" +
          '<td style="font-weight:700">' + esc(r.avatar || "🧠") + " " + esc(r.displayName) +
          (r.country ? ' <span class="small">' + esc(r.country) + "</span>" : "") + "</td>" +
          "<td>" + esc(r.level) + "</td><td><strong>" + esc(r.xp) + "</strong></td>" +
          '<td class="hide-s">🔥 ' + esc(r.streak || 0) + "</td></tr>";
      }).join("") +
      "</tbody></table></div>" +
      '<p class="small" style="margin-top:1rem">Rankings update as players earn XP from notes, quizzes and games.</p>';
  }catch(e){
    errorBox(box, "Could not load the leaderboard: " + e.message);
  }
}
})();
