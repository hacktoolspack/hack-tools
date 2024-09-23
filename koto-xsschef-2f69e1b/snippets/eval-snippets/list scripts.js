var s = [];
for (i=0;i<document.scripts.length;i++) {
s.push(document.scripts[i].src || document.scripts[i].textContent);
}
s;