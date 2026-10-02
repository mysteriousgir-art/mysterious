/* Mysterious quiz list */
(function(){
"use strict";

async function boot(){
  var grid = document.getElementById("quiz-grid");
  loadingBox(grid, "Loading quizzes…");
  try{
    var quizzes = await api("/api/quizzes");
    if(!quizzes || !quizzes.length){
      grid.innerHTML = '<p class="small">No quizzes yet — check back soon.</p>';
      return;
    }
    grid.innerHTML = quizzes.map(function(q){
      return '<a class="card hoverable" href="quiz.html?slug=' + encodeURIComponent(q.slug) + '">' +
        "<h3>" + esc(q.title) + "</h3>" +
        '<p class="small">' + esc(q.questionCount || 0) + ' questions · ' + esc(q.playCount || 0) + " plays" + "</p>" +
        (q.noteSlug ? '<a href="note.html?slug=' + encodeURIComponent(q.noteSlug) + '" class="small">📖 Read the note first →</a><br>' : "") +
        '<span class="btn btn-primary btn-sm" style="margin-top:.6rem">Start quiz</span>' +
      "</a>";
    }).join("");
  }catch(e){
    errorBox(grid, "Could not load quizzes: " + e.message);
  }
}

document.addEventListener("DOMContentLoaded", boot);
})();
