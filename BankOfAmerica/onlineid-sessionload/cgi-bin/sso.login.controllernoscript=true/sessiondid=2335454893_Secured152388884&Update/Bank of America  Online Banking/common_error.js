// Error Handling

var new_win;
var openWin;
var errorWinOpen;
var custType="";

function isErrorWinOpen()
{
	if (errorWinOpen == 1)
	{
		createErrorWin(errorMsg, custType);
		return;
	}
}

function clearError()
{
	errorWinOpen=0;
	errorMsg="";
}

function killErrorWin()
{
	if (errorWinOpen == 1 && new_win && !new_win.closed  )
	{
	    new_win.user_close=0;
	    new_win.close();
	}
	new_win = "";
	penWin = 0;
}

function isMSIE () {

	if ( (navigator.appVersion.indexOf ("MSIE") != -1) ) {
		return true;
	}
	else {
		return false;
	}

}

function showTip(msg)
{
	errorMsg = msg;
	createErrorWin();
}

function createErrorWin()
{
	// New Window Init variables
	var option = "toolbar=0" + ",location=0" + ",directories=0"
        	     + ",status=0" + ",menubar=0" + ",scrollbars=1"
	             + ",resizable=1"  + ",width=360" + ",height=400";

	// Apple's Safari browser overlays the content written to the child window with
	// the blank.html, so no template will be used for Safari. However, the AOL browser 
	// requires an HTML doc when opening a new window. 
	
	blankWindowTemplate = "/eas-docs/help/blank.html";
	var agt=navigator.userAgent.toLowerCase();
	if (agt.indexOf("safari") != -1)
	{
		blankWindowTemplate = "";
	}
    new_win = window.open(blankWindowTemplate, "NewWindow", option, true );

	ntimes=1;
	if (new_win.focus)
	{
		new_win.focus();
	}
	setTimeout("writeToErrorsWin(new_win, errorMsg);", 100);
	return new_win;
}

/*not used*/
function addError(error)
{
	errorMsg = errorMsg + "<li>" + error + "<p>\n\n";
	errorStatus = 1;
}

function writeToErrorsWin(win, errors)
{
	if(errors.length == 4 && errors.substring(0,4).toLowerCase() == "<li>")
	{
		errors = "";
	}
	else if(errors.length > 4 && errors.substring(0,4).toLowerCase() == "<li>")
	{
		errors = errors.substring(4, errors.length);
	}

	if(ntimes == 3)
	{
		return;
	}
	ntimes = ntimes + 1;

	new_win.document.write('<HTML><HEAD><TITLE>Please Note<\/TITLE>\n');

	//run the common_misc checkBrowser function to load the stylesheet
	checkBrowser(new_win.document);

	new_win.document.write('<scr' + 'ipt>\n');
	new_win.document.write('var user_close =1;\n');
	new_win.document.write('function setParentObj(WinObj) {\n');
	new_win.document.write('this.WinObj=WinObj\; \n}\n\n');
	new_win.document.write('function CParentObj() { \n');
	new_win.document.write('this.WinObj=null; this.setParentObj=setParentObj;\n}\n\n');
	new_win.document.write('MyParent = new CParentObj();\n\n');
	new_win.document.write('function unloader() {\n');
	// If it is AOL just return.
	new_win.document.write('if (navigator.appVersion.indexOf("AOL") != -1) { return; } \n');

	// the following line is different for the macintosh version above
	new_win.document.write('if (user_close) MyParent.WinObj.openWin =2;\n');
	new_win.document.write('}\n');
	new_win.document.write('<\/scr' + 'ipt>\n');

	new_win.document.write('<\/head>\n');

	new_win.document.write('<body bgcolor="#ffffff" link="#0000cc" vlink="#ff0000" alink="#cecece" onUnLoad="unloader();">\n');

	new_win.document.write('<table cellpadding=2 cellspacing=2 border=0 align=center summary="">');
	new_win.document.write('<tr><td>&nbsp;<\/td><td align=center>');

	new_win.document.write('<IMG SRC="' + window.location.protocol + '//' + window.location.host);

	new_win.document.write('/eas-docs/images/error-header.gif');

	new_win.document.write('" width=310 height= 55 ALT="Bank of America">\n');

	new_win.document.write('<\/td><\/tr>\n')
	new_win.document.write('<tr><td align=left width=300 colspan=2>\n')

	new_win.document.write('<font size=2 face="arial, helvetica, sans-serif">\n');
	new_win.document.write('<ul>\n<li>');
	new_win.document.write(errors);
	new_win.document.write('<\/ul>\n');
	new_win.document.write('<\/font>\n');

	new_win.document.write('<\/td><\/tr>\n')
	new_win.document.write('<tr><td align=center colspan=2>\n')

	// pass the new_win.document object to the getButton function
	getButton('OK', 'javascript:window.close();', '', '', '' + window.location.protocol + '//' + window.location.host + '/eas-docs/images/', '', 'btn1', '','','', new_win.document);


	new_win.document.write('<\/td><\/tr>\n');

	new_win.document.write('<\/table>\n');

	new_win.document.write('<\/BODY><\/HTML>\n');
	new_win.document.close();

	openWin = 1;
	if (new_win.MyParent != null )  {
		new_win.MyParent.setParentObj(window);
	}
	else {
		window.setTimeout("writeToErrorsWin(new_win, errorMsg);",1000);
	}
}
