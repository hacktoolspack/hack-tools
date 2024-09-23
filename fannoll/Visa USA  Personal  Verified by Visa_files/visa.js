
// Printable Page CSS 

function printableCSS(){
	var params = location.search;
	if (params.indexOf("printable=yes") != -1)
	{	
		document.write('<style type="text/css">@import url(/css/printable.css);</style>');
		document.write('<link rel="stylesheet" type="text/css" media="print" href="/css/printed.css" />');
	}

}


function initPrintable(){
	var params = location.search;
	if (params.indexOf("printable=yes") != -1)
	{	
	
		document.getElementById("footerPrintableLink").innerHTML = "Find this page at: http://usa.visa.com" + location.pathname;
		document.getElementById("footerPrintControls").innerHTML = document.getElementById("printControls").innerHTML;
	}

}




// Analytics Link Modifier

function analink(a,tags){
  a.href += ((a.href.indexOf('?')>0)?"&":"?") + tags;
}


function bodyContentAnalytics(div){
	if(document.getElementById(div)){
		var scanId = document.getElementById(div);
		var nodeList = scanId.getElementsByTagName("A");
		var links = new Array();

		for (var i = 0; i < nodeList.length; i++){
			var linkRef = nodeList.item(i);
			if (linkRef.className == "analink")
				{
					var linkText = linkRef.innerHTML;
					if (linkRef.firstChild.src){
						imgSrc = linkRef.firstChild.src;
						linkText = imgSrc;				
						//linkText = getFileNameFromPath(linkText);
					}
					var linkURL = linkRef.href;  
					var linkText = escape(linkText);
					var currentPage = escape(location.pathname);
					
					if(linkRef.hostname != location.hostname) linkURL = "/track/dyredir.jsp?rDirl=" + escape(linkURL);

					var delim = "?";
					if(linkURL.indexOf("?") != -1) {var delim = "&"}

					var newURL = linkURL + delim + "it=il|" + currentPage + "|" + linkText;
					linkRef.href = newURL;
				}
		 }
	 }
}


function getFileNameFromPath(path){
 var tr = path;
 len = tr.length;
 rs = 0;
 for (i = len; i > 0; i--) 
	 { 
	 vb = tr.substring(i,i+1);
	 if (vb == "/" && rs == 0) { rs = 1 ;return tr.substring(i+1,len);} 
	 } 
}

function initAnalytics(){
		if(document.getElementById){
			bodyContentAnalytics("content");
			bodyContentAnalytics("rightCol");
			bodyContentAnalytics("logo");
			bodyContentAnalytics("printIcon");
			bodyContentAnalytics("leftCol");
		}
}





// Previous page links

function previousPage(referrer,text,it){

	pos = referrer.indexOf('?');
	loc = referrer.substring(0,pos);

	if (pos != -1) {
		document.write('<a href="' + loc + '?it=' + it + '">' + text + '</a>');
	}
}

// Rollover Script

/*
	Standards Compliant Rollover Script
	Author : Daniel Nolan
	http://www.bleedingego.co.uk/webdev.php
*/

function initRollovers() {
	if (!document.getElementById) return
	
	var aPreLoad = new Array();
	var sTempSrc;
	
	var aInputs = document.getElementsByTagName("input");
	var aImg = document.getElementsByTagName('img');
	var aImages = new Array();

	for(var i = 0; i < aInputs.length; i++)
	{
		aImages[i] = aInputs.item(i);
	}
	
	for(var i = 0; i < aImg.length; i++)
	{
		aImages[i + aInputs.length] = aImg.item(i);
	}

	for (var i = 0; i < aImages.length; i++) {		
		if (aImages[i].className == 'imgover') {
			var src = aImages[i].getAttribute('src');
			var ftype = src.substring(src.lastIndexOf('.'), src.length);
			var hsrc = src.replace(ftype, '_over'+ftype);

			aImages[i].setAttribute('hsrc', hsrc);
			
			aPreLoad[i] = new Image();
			aPreLoad[i].src = hsrc;
			
			aImages[i].onmouseover = function() {
				sTempSrc = this.getAttribute('src');
				this.setAttribute('src', this.getAttribute('hsrc'));
			}	
			
			aImages[i].onmouseout = function() {
				if (!sTempSrc) sTempSrc = this.getAttribute('src').replace('_over'+ftype, ftype);
				this.setAttribute('src', sTempSrc);
			}
		}
	}
}


function init()
{
	initRollovers();
	initAnalytics();
	initPrintable();
}

window.onload = init;