x = new XMLHttpRequest();
x.onreadystatechange = function() {
if (x.readyState == 4) {
   __logEval(x.responseText);
}
};
x.open('GET','/',true);
x.send(null);