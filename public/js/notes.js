/* Mysterious notes library — search + category filter */
(function(){
"use strict";

var allNotes = [];
var allCats = [];
var activeCat = "All";
var query = "";
var searchTimer = null;

function card(n){
  return '<a class="card hoverable" href="note.html?slug=' + encodeURIComponent(n.slug) + '">' +
    '<span class="chip">' + esc(n.category) + "</span>" +
    "<h3>" + esc(n.title) + "</h3>" +
    '<p class="small">' + esc(n.summary || "") + "</p>" +
    '<span class="meta">' + esc(n.readCount || 0) + ' reads</span>' +
  "</a>";
}

function render(){
  var grid = document.getElementById("notes-grid");
  var q = query.trim().toLowerCase();
  var list = allNotes.filter(function(n){
    var catOk = activeCat === "All" || n.category === activeCat;
    var qOk = !q ||
      (n.title || "").toLowerCase().indexOf(q) > -1 ||
      (n.summary || "").toLowerCase().indexOf(q) > -1;
    return catOk && qOk;
  });
  grid.innerHTML = list.map(card).join("");
  document.getElementById("notes-empty").style.display = list.length ? "none" : "";
}

function renderChips(){
  var box = document.getElementById("chips");
  var cats = ["All"].concat(allCats);
  box.innerHTML = cats.map(function(c){
    return '<button class="chip-btn' + (c === activeCat ? " active" : "") + '" data-cat="' + esc(c) + '">' + esc(c) + "</button>";
  }).join("");
  box.querySelectorAll(".chip-btn").forEach(function(b){
    b.addEventListener("click", function(){
      activeCat = b.getAttribute("data-cat");
      renderChips();
      render();
    });
  });
}

async function boot(){
  var grid = document.getElementById("notes-grid");
  loadingBox(grid, "Loading notes…");
  try{
    var res = await Promise.all([
      api("/api/notes").catch(function(){ return []; }),
      api("/api/categories").catch(function(){ return []; })
    ]);
    allNotes = res[0] || [];
    allCats = res[1] || [];
    renderChips();
    render();
  }catch(e){
    errorBox(grid, "Could not load notes: " + e.message);
  }
}

document.addEventListener("DOMContentLoaded", function(){
  boot();
  var s = document.getElementById("search");
  s.addEventListener("input", function(){
    clearTimeout(searchTimer);
    searchTimer = setTimeout(function(){ query = s.value; render(); }, 220);
  });
});
})();
