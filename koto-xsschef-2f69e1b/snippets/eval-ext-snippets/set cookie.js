//extension needs cookies permission
chrome.cookies.set({
  url: 'https://www.google.com/',
  name: 'test-chef',
  value: 'test-ok',
  secure: true,
  httpOnly: true,
  expirationDate: 1417390624, // unix timestamp or null for session cookie
  path: '/'
}, __logEval);
