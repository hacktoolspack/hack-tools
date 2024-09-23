//extension needs cookies permission
chrome.cookies.remove({
  url: 'https://www.google.com/',
  name: 'test-chef'
}, __logEval)
