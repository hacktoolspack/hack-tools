// requires proxy permission
try {
   chrome.proxy.settings.clear({'incognito': false},function() {__logEval('cleared')});
} catch (e){
   try {
   chrome.proxy.settings.clear({scope: 'regular'},function() {__logEval('cleared with new API')});
   } catch (e) {
   __logEval('error');
   }
}