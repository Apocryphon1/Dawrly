console.log("script.js Loaded");


var form = document.querySelector("form");

form.addEventListener("submit", function (e) {
    e.preventDefault();
    form.submit();
});