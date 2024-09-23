// Timeout functions
var pdfWin;
var opt="toolbar=no,directories=no,location=no,status=no,scrollbars=yes,resizable=yes,copyhistory=no";
var opt480=opt + ",width=600,height=480";
var opt500=opt + ",width=636,height=370";
var opt507=opt + ",width=650,height=507";
var optAcct=opt + ",width=550,height=507";

function openHelp(url,custType)
{
 open(url, "helpwindow_" + custType, opt480 );
}

function openHelpUrl(url)
{
 open(url, "helpwindow_", opt480);
}

function openAcctHelpUrl(url)
{
 open(url, "helpwindow_", optAcct);
 }

function openNonBofAHelp(url)
{
 open(url, "helpwindow_", opt480);
}

function openHelpUrlCustom(url, iWidth, iHeight)
{
	var optCustom = opt + ",width=" + iWidth + ",height=" + iHeight;

	open(url, "helpwindow_", openForPrintWindowPosition(optCustom));
}

function openForPrint(url)
{
	open(url, "pintwindow_", openForPrintWindowPosition(opt500));
}

function openForPrintWindowPosition(winOpt)
{
	var new_x = 0;
	var new_y = 0;

	if(document.all)
	{
		new_x = window.screenLeft + 35;
		new_y = window.screenTop + 47;
	}
	else
	{
		new_x = window.screenX + 35;
		new_y = window.screenY + 47 + 112;
	}

	winOpt += ",left=" + new_x + ",top=" + new_y + ",screenX=" + new_x + ",screenY=" + new_y;
	return winOpt;
}

var defaultTimeOutMilliseconds = 480000; // 8 Minutes
var TimeOutWaitMilliseconds = 120000; // 2 minutes
var curTimeOut=defaultTimeOutMilliseconds;
var timerID, timerWarnID, timeoutUrl, resetTimeoutURL="";
var timeoutWarningMsg;
var timeoutMsg;

function LoadPage()
{
 customaryLoadPage();
}
function customaryLoadPage()
{
 isErrorWinOpen();
 if (this["extendbody"]!=null)
  extendbody.action();
 if(this["myTimeoutMilliseconds"] != null)
 {
  curTimeOut=myTimeoutMilliseconds;
  setupTimeout(curTimeOut);
 }
    else if(this["UITimeoutMilliseconds"] != null)
 {
  curTimeOut=UITimeoutMilliseconds;
  setupTimeout(curTimeOut);
  }

  if (this["timeOutURL"] != null)
  timeoutUrl=timeOutURL;
 else
  timeoutUrl=baseURL + "bofa/ibd/IAS/presentation/TimeoutControl";

 resetTimeoutURL=baseURL + "bofa/ibd/IAS/presentation/GotoResetTimeout?navigation=true";
}

function loadPageWithoutTimeout()
{
 isErrorWinOpen();
 if (this["extendbody"]!=null)
 {
  extendbody.action();
 }
}

function unLoadPage()
{
 killErrorWin();
}

function writeToTimeoutWin(curTimeOut)
{
  var timeout_option = "toolbar=0" + ",location=0" + ",directories=0"
 + ",status=0" + ",menubar=0" + ",scrollbars=0"
 + ",resizable=0" + ",width=320" + ",height=210";

	// AOL browser requires a blank HTML when opening a new window, but Safari overlays 
	// all the data written to the window with the html doc if provided in the window.open  
	// statement
	
	blankWindowTemplate = "/eas-docs/help/blank.html";
	var agt=navigator.userAgent.toLowerCase();
	if (agt.indexOf("safari") != -1)
	{
		blankWindowTemplate = "";
	}
	
    var timeout_win = window.open(blankWindowTemplate, "NewWindow", timeout_option, true );

    timeout_win.document.write('<HTML><HEAD><TITLE>Please - Note<\/TITLE>\n');

    checkBrowser(timeout_win.document);

    timeout_win.document.write('<scr' + 'ipt language="JavaScript" type="text/javascript">');
    timeout_win.document.write('function submitForm() { window.opener.clearGoToTimeout(); document.frmTimeout.submit(); }\n');
    timeout_win.document.write( 'function hover(ref, classRef) { eval(ref).className = classRef; }');
    timeout_win.document.write('<\/scr' + 'ipt>');

    timeout_win.document.write('<\/head>\n');
    timeout_win.document.write('<body bgcolor="#ffffff" link="#0000cc" vlink="#ff0000" alink="#cecece" onload=\'window.setTimeout("this.close()",' + (TimeOutWaitMilliseconds-2000).toString() + ');\'>\n');

    timeout_win.document.write('<FORM METHOD=GET name=frmTimeout ACTION="' + resetTimeoutURL + '">\n');
    if ( tmOutID != null )
    {
        timeout_win.document.write('<input type=hidden name=tmOutID value="' + tmOutID + '">\n' );
    }
    timeout_win.document.write('<input type=hidden name=timerreset value=yes>\n' );
    timeout_win.document.write('<\/form>\n');

    timeout_win.document.write('<table cellpadding=0 cellspacing=0 border=0 width=300 align=center summary="">');

    timeout_win.document.write('<tr><td align=center width="100%" colspan=3>');
    timeout_win.document.write('<img alt="" src="' + window.location.protocol + '//' + window.location.host + '/eas-docs/images/timeout-header.gif" border=0 width=310 height=55>\n');
    timeout_win.document.write('<\/td><\/tr>\n')

    timeout_win.document.write('<tr><td align=center width="100%" colspan=3>');
    timeout_win.document.write('<img alt="" src="' + window.location.protocol + '//' + window.location.host + '/eas-docs/images/clr.gif" border=0 width=1 height=5>\n');
    timeout_win.document.write('<\/td><\/tr>\n')

    timeout_win.document.write('<tr><td>&nbsp;<\/td><td align=left>\n');

    timeout_win.document.write('<p class="text2">\n');
    timeout_win.document.write('Your Online Banking session is about to be timed out. As a security precaution, sessions end after ' + (curTimeOut+TimeOutWaitMilliseconds)/60000 + ' minutes of inactivity. Click OK to continue your current session.');
    timeout_win.document.write('<\/p>\n');

    timeout_win.document.write('<\/td><td>&nbsp;<\/td><\/tr>\n')

    timeout_win.document.write('<tr><td align=center width="100%" colspan=3>');
    timeout_win.document.write('<img alt="" src="' + window.location.protocol + '//' + window.location.host + '/eas-docs/images/clr.gif" border=0 width=1 height=5>\n');
    timeout_win.document.write('<\/td><\/tr>\n')

    timeout_win.document.write('<tr><td>&nbsp;<\/td><td align=center>\n')

    getButton('OK', 'javascript: void submitForm();', '', '', '' + window.location.protocol + '//' + window.location.host + '/eas-docs/images/', '', 'btn1', '','','', timeout_win.document);

    timeout_win.document.write('<\/td><td>&nbsp;<\/td><\/tr>\n');

    timeout_win.document.write('<\/table>\n');

    timeout_win.document.write('<\/body>\n');
    timeout_win.document.write('<\/html>\n');
    timeout_win.document.close();
}

function clearGoToTimeout()
{
  clearTimeout(timerID);

  if(this["UITimeoutMilliseconds"] != null)
 {
  curTimeOut=UITimeoutMilliseconds;
 }

  setupTimeout(curTimeOut);
}

function resetTimeoutValues(timeoutValue)
{
// For clearing the timeout for timeout window AND timeout-warning window
  clearTimeout(timerID);
  clearTimeout(timerWarnID);
  setupTimeout(timeoutValue);
}

function goToTimeout(curTimeOut)
{
 // pdfWin is used by PaperStatementLandingPage to popup
 // new window. It must be closed when session times out.
 if(pdfWin && !pdfWin.closed)
 {
        pdfWin.close();
 }


 var timeoutMsg="Your Online Banking session has been timed out. \n\nAs a security precaution, sessions are ended after "+ (curTimeOut+TimeOutWaitMilliseconds)/60000 + " minutes of inactivity. \n\nYou can sign in again to resume using Online Banking.";

 alert(timeoutMsg);
 self.status ="Redirect now...";
 self.location=timeoutUrl;
 return;
}


function setupTimeout(curTimeOut)
{
 timerWarnID=window.setTimeout('writeToTimeoutWin(curTimeOut)', curTimeOut);
 timerID=window.setTimeout('goToTimeout(curTimeOut)', curTimeOut+TimeOutWaitMilliseconds);
}

var clickedAlready = 0;
function GotoCFAndPause(ctrl)
{
 if ( clickedAlready != 1 )
 {
 window.setTimeout( "clickedAlready=0;", 5000);
 clickedAlready = 1;
 window.location=baseURL + "bofa/ibd/IAS/presentation/" + ctrl;
 }
}

var platform= navigator.platform.toLowerCase(); // Operating system
var appName = navigator.appName;                // Browser name
var appVer= parseInt(navigator.appVersion);     // Browser versionnumber

// set the correct style sheet for the browser
function checkBrowser(doc)
{
    if (platform.indexOf("win") != -1)  // Windows platform
    {
        if (appName == "Netscape" && appVer >= 5) // Netscape 6.x
        {
            doc.writeln('<link rel="stylesheet" type="text/css" href="/eas-docs/images/win_ns6.css">');
        }
        else if (appName == "Netscape" && appVer >= 4) // Netscape 4
        {
            doc.writeln('<link rel="stylesheet" type="text/css" href="/eas-docs/images/win_ns4.css">');
        }
        else if (appName == "Microsoft Internet Explorer" && appVer >= 4 &&  navigator.appVersion .indexOf("MSIE 4") != -1) // IE 4.x
        {
            doc.writeln('<link rel="stylesheet" type="text/css" href="/eas-docs/images/win_ie4.css">');
        }
        else if (appName == "Microsoft Internet Explorer" && appVer >= 4) // IE 4.x +
        {
            doc.writeln('<link rel="stylesheet" type="text/css" href="/eas-docs/images/win_ie.css">');
        }
        else if (appName == "Opera")  // Opera 5.x, 6.x
        {
            doc.writeln('<link rel="stylesheet" type="text/css" href="/eas-docs/images/win_opera.css">');
        }
        else  // All other win browsers
        {
            doc.writeln('<link rel="stylesheet" type="text/css" href="/eas-docs/images/win_ie.css">');
        }
    }
    else if (platform.indexOf("mac") != -1)    // Mac platform
    {
        if (appName == "Netscape" && appVer >= 5) // Netscape 6.x
        {
            doc.writeln('<link rel="stylesheet" type="text/css" href="/eas-docs/images/mac_ns6.css">');
        }
        else if (appName == "Netscape" && appVer >= 4) // Netscape 4
        {
            doc.writeln('<link rel="stylesheet" type="text/css" href="/eas-docs/images/mac_ns4.css">');
        }
        else if (appName == "Microsoft Internet Explorer" && appVer >= 4) // IE 4.x
        {
            doc.writeln('<link rel="stylesheet" type="text/css" href="/eas-docs/images/mac_ie.css">');
        }
        else if (appName == "Opera")  // Opera 5.x, 6.x
        {
            doc.writeln('<link rel="stylesheet" type="text/css" href="/eas-docs/images/mac_ie.css">');
        }
        else  // All other browsers
        {
            doc.writeln('<link rel="stylesheet" type="text/css" href="/eas-docs/images/mac_ie.css">');
        }
    }
    else if (platform.indexOf("os2") != -1)    // os2 platform
    {
        if (appName == "Netscape" && appVer >= 4) // Netscape 4
        {
            doc.writeln('<link rel="stylesheet" type="text/css" href="/eas-docs/images/os2_ns4.css">');
        }
        else
        {
            doc.writeln('<link rel="stylesheet" type="text/css" href="/eas-docs/images/win_ie.css">');
        }
    }
    else    // all other platforms
    {
        if (appName == "Netscape" && appVer >= 4) // Netscape 4
        {
            doc.writeln('<link rel="stylesheet" type="text/css" href="/eas-docs/images/mac_ns4.css">');
        }
        else
        {
            doc.writeln('<link rel="stylesheet" type="text/css" href="/eas-docs/images/win_ie.css">');
        }
    }
}
/* Multiply the size of the font for each style sheet rule
   for all linked and embedded style sheets.
*/
function multipleFontSize(factor)
{
    var styleSheet;
    var i;
    var done;

    for(i=0;i<document.styleSheets.length;i++)
    {
        styleSheet = document.styleSheets[i].cssText;
        styleSheet = styleSheet.toLowerCase();

        var pattern = /font-size\s*:\s*([\d\.]+)((em)|%)+/g;
        pattern.multiline = true;
        var result;
        done = false;

        while (!done)
        {
            var result = pattern.exec(styleSheet);
            if (result == null)
            {
                done = true;
            }
            else
            {
                strLeft = styleSheet.substring(0, result.index-1);
                strMid = result[0];
                strRight = styleSheet.substring(result.index +  result[0].length);
                size = result[1];
                size *= factor;
                var number_pattern = /(\d*.?\d{0,2})\d*/;
                var number_result = number_pattern.exec(size);
                strMid = strMid.replace(result[1], number_result[1]);
                styleSheet = strLeft + strMid + strRight;
            }
        }
        document.styleSheets[i].cssText= styleSheet;
    }
}

/* Examine the default page font.  If too small,
   increase by a percent factor
*/
function examineFontSize(ref)
{
    if (document.getElementById)
    {
        if (document.getElementById(ref).currentStyle)
        {
            var size = document.getElementById(ref).currentStyle.fontSize;
            var index = size.indexOf("pt");
            var newstr = parseInt(size.substr(0,index));

            if (newstr < 10)
            {
                multipleFontSize(1.3);
            }
            else if (newstr < 12)
            {
                multipleFontSize(1.2);
            }
        }
    }
}
