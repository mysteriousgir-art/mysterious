/* Mysterious auth page — login / signup tabs */
(function(){
"use strict";

var COUNTRIES = [
  "Afghanistan","Australia","Austria","Bahrain","Bangladesh","Belgium","Brazil","Canada",
  "China","Denmark","Egypt","Finland","France","Germany","Greece","India","Indonesia",
  "Iran","Iraq","Ireland","Italy","Japan","Jordan","Kenya","Kuwait","Malaysia","Mexico",
  "Netherlands","New Zealand","Nigeria","Norway","Oman","Pakistan","Philippines",
  "Poland","Portugal","Qatar","Russia","Saudi Arabia","Singapore","South Africa",
  "South Korea","Spain","Sri Lanka","Sweden","Switzerland","Thailand","Turkey",
  "Ukraine","United Arab Emirates","United Kingdom","United States","Vietnam","Other"
];

function fillCountries(){
  var sel = document.getElementById("su-country");
  sel.innerHTML = '<option value="">Select country…</option>' +
    COUNTRIES.map(function(c){
      return '<option value="' + esc(c) + '">' + esc(c) + "</option>";
    }).join("");
}

function showTab(which){
  var login = which === "login";
  document.getElementById("tab-login").classList.toggle("active", login);
  document.getElementById("tab-signup").classList.toggle("active", !login);
  document.getElementById("form-login").style.display = login ? "" : "none";
  document.getElementById("form-signup").style.display = login ? "none" : "";
  document.getElementById("auth-error").innerHTML = "";
}

function fieldOk(id, ok){
  document.getElementById(id).closest(".field").classList.toggle("invalid", !ok);
  return ok;
}
var emailRe = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function fail(msg){
  document.getElementById("auth-error").innerHTML =
    '<div class="alert alert-err">' + esc(msg) + "</div>";
}

function afterAuth(user){
  window.zehenUser = user;
  var next = qp("next");
  window.location.href = (next && next.charAt(0) === "/") ? next : "index.html";
}

document.addEventListener("DOMContentLoaded", function(){
  fillCountries();
  showTab("login");
  document.getElementById("tab-login").addEventListener("click", function(){ showTab("login"); });
  document.getElementById("tab-signup").addEventListener("click", function(){ showTab("signup"); });

  // If already logged in, go home
  if(window.zehenUserLoaded && window.zehenUser){ afterAuth(window.zehenUser); return; }
  document.addEventListener("zehen:user", function(){
    if(window.zehenUser) afterAuth(window.zehenUser);
  }, {once:true});

  document.getElementById("form-login").addEventListener("submit", async function(e){
    e.preventDefault();
    var email = document.getElementById("login-email").value.trim();
    var pass = document.getElementById("login-password").value;
    var ok = fieldOk("login-email", emailRe.test(email)) &
             fieldOk("login-password", pass.length > 0);
    if(!ok) return;
    var btn = document.getElementById("login-btn");
    btn.disabled = true; btn.innerHTML = '<span class="spinner"></span> Logging in…';
    try{
      var d = await api("/api/auth/login", {method:"POST", body:{email:email, password:pass}});
      toast("Welcome back! 🌱", "ok");
      afterAuth(d.user);
    }catch(err){ fail(err.message); }
    btn.disabled = false; btn.textContent = "Log in";
  });

  document.getElementById("form-signup").addEventListener("submit", async function(e){
    e.preventDefault();
    var name = document.getElementById("su-name").value.trim();
    var email = document.getElementById("su-email").value.trim();
    var pass = document.getElementById("su-pass").value;
    var country = document.getElementById("su-country").value;
    var ok = fieldOk("su-name", name.length >= 2 && name.length <= 40) &
             fieldOk("su-email", emailRe.test(email)) &
             fieldOk("su-pass", pass.length >= 6) &
             fieldOk("su-country", country.length > 0);
    if(!ok) return;
    var btn = document.getElementById("signup-btn");
    btn.disabled = true; btn.innerHTML = '<span class="spinner"></span> Creating account…';
    try{
      var d = await api("/api/auth/signup", {
        method:"POST",
        body:{email:email, password:pass, displayName:name, country:country}
      });
      toast("Account created — welcome to Mysterious! 🎉", "ok");
      afterAuth(d.user);
    }catch(err){ fail(err.message); }
    btn.disabled = false; btn.textContent = "Create account";
  });
});
})();
