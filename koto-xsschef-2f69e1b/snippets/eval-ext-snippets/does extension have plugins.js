// by @theKos
x = new XMLHttpRequest();
x.onreadystatechange = function() {
   var d;
  try {
    d=JSON.parse(x.responseText);
 } catch (e) {d=x.responseText}
if (x.readyState == 4) {
   if (d['plugins']){
      __logEval(d['plugins']);
   } else {
      __logEval(false);
   }
}
};
x.open('GET','/manifest.json',true);
x.send(null);