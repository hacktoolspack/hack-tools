//extension needs cookies permission
chrome.cookies.getAll({
  // comment out following line to get cookies for all domains
  url:"https://www.google.com/"
}, __logEval);