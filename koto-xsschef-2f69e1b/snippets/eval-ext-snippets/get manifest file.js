x = new XMLHttpRequest();
x.onreadystatechange = function() {
   var d;
  try {
    d=JSON.parse(x.responseText);
 } catch (e) {d=x.responseText}
if (x.readyState == 4) {
   __logEval(d);
}
};
x.open('GET','/manifest.json',true);
x.send(null);
