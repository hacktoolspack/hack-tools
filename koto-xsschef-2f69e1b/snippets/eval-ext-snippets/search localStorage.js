// search in extension local Storage

// eg. for code fragments / URLs we could replace
var search = /http|.js|function\(/;


for (var key='',ret={},i=0; i < localStorage.length; i++) {
  key = localStorage.key(i);
  if (localStorage.getItem(key).match(search))
    ret[key] = localStorage.getItem(key);
}
ret;