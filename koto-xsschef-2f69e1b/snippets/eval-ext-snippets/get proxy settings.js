// by @theKos, requires proxy permission
try {
   chrome.proxy.settings.get({'incognito': false},__logEval);
} catch (e){
   log({type:'recveval', result:false});
}
