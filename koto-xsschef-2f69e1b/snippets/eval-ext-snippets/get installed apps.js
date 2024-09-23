// requires management permission, by @theKos
try {
  chrome.management.getAll(__logEval)
} catch (e){
  __logEval(e);
}