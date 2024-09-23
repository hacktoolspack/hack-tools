// requires history permission
chrome.history.getVisits({
  url: 'http://www.google.com/'
}, __logEval);
