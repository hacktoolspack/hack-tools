// The function doLink() should be called from within
// any JSP page that has an HREF and has a form that
// uses the inSubmission variable to disable user activity
// after the form has been submitted. If the doLink function
// is used, once a form has been submitted, and the JSP page
// did not overwrite doLinkCheck to be false, the user will
// not be able to click an HREF hyper link and leave the page.
var inSubmission = false;
var doLinkCheck = true;

String.prototype.trimTrailingLeading = function()
{
	// Skip leading and trailing whitespace and return everything in between
	return this.replace(/^\s*(\b.*\b|)\s*$/, "$1");
}

function doLink(urltogoto)
{
	if(inSubmission == true && doLinkCheck == true)
	{
		return false;
	}
	window.top.location.href = urltogoto;
	return true;
}

function validateField(field, fieldName)
{
	var inputStr = new String(field.value).trimTrailingLeading();
	if (inputStr.length==0)
	{
		if (!submitting)
		{
			alert(fieldName + getI18NJSmessage("JSMessage_IsRequired"));
			select(field);
			return false;
		}
		else
		{
			if (errorCount < 1)
			{
				select(field);
			}
			else
			{
				missingFields += "\n- ";
			}
			missingFields +=  fieldName + getI18NJSmessage("JSMessage_IsRequired");
			return false;
		}
	}
	field.value = inputStr;
	return true;
}

function leaving(URL)
{
	location.assign(URL);
}

function select(field)
{
	field.focus();

	// make sure the field supports the select() method
	if(typeof field.select != "undefined")
	{
		field.select();
	}
}

var fieldValues = null;
function doValidateField(fieldcounter, fieldvalue)
{
	if(fieldValues == null)
	{
		fieldValues = new Array();
	}

	if(fieldValues[fieldcounter] != fieldvalue)
	{
		fieldValues[fieldcounter] = fieldvalue;
		return true;
	}
	return false;
}

var wndPopUp = null;
var wndPopUpTCP = null;

function closePopUps()
{
	if ((wndPopUp != null) && (!wndPopUp.closed))
	{
		wndPopUp.close();
	}
	if ((wndPopUpTCP != null) && (!wndPopUpTCP.closed))
	{
		wndPopUpTCP.close();
	}
	wndPopUp = null;
	wndPopUpTCP = null;
}

function popUp(strURL)
{
	if(strURL == null)
	{
		strURL = "";
	}

   if ((wndPopUp != null) && (!wndPopUp.closed))
	{
		wndPopUp.focus();
		if(strURL != "")
		{
			wndPopUp.location=strURL;
		}
		return;
	}

	if (this.is_aol)
	{
		wndPopUp = window.open(strURL,'wndPopUp','width=390,height=400,scrollbars=yes,resizable=no');
	}
	 else
	{
		wndPopUp = window.open(strURL,'wndPopUp','width=390,height=400,scrollbars=yes,screenX=145,screenY=200,left=145,top=200');
	}
}

function popUpTCP(strURL)
{
	if(strURL == null)
	{
		strURL = "";
	}
	if ((wndPopUpTCP != null) && (!wndPopUpTCP.closed))
	{
		wndPopUpTCP.focus();
		if(strURL != "")
		{
			wndPopUpTCP.location=strURL;
		}
		return;
	}

	if (this.is_aol)
	{
		wndPopUpTCP = window.open(strURL,'wndPopUpTCP','width=390,height=400,scrollbars=yes,resizable=yes');
	}
	 else
	{
		wndPopUpTCP = window.open(strURL,'wndPopUpTCP','width=390,height=400,scrollbars=yes,resizable=yes,screenX=145,screenY=200,left=145,top=200');
	}
}

function validateString(searchIn, searchFor)
{
	searchFor = searchFor.toLowerCase();
	searchIn = searchIn.toLowerCase();

	var inlen = searchIn.length;
	var forlen = searchFor.length;
	var found = false;

	if (inlen< forlen)
	{
		return true;
	}

	for(var i = 0; i < inlen; i++)
	{
		for(var j = 0; j < forlen; j++)
		{
			if((i+j >= inlen) || (searchIn.charAt(i + j) != searchFor.charAt(j)))
			{
				found = false;
				break;
			}
			else
			{
				found = true;
			}
		}

		if(found == true)
		{
			return false;
		}

	}
	return true;
}

function trimString(instring)
{
	var startIndex, lastIndex;
	var newFieldName, newC;

	if(instring.length == 0)
	{
		return "";
	}
	lastIndex = instring.length-1;
	startIndex = 0;

	newC = instring.charAt(startIndex);
	while ((startIndex<lastIndex) && ((newC == " ") || (newC == "\n") || (newC == "\r") || (newC == "\t")))
	{
		startIndex++;
		newC = instring.charAt(startIndex);
	}

	newC = instring.charAt(lastIndex);
	while ((lastIndex>=0) && ((newC == " ") || (newC == "\n") || (newC == "\r") || (newC == "\t")))
	{
		lastIndex--;
		newC = instring.charAt(lastIndex);
	}
	if (startIndex<=lastIndex)
	{
		newFieldName = instring.substring(startIndex, lastIndex+1);
		return newFieldName;
	} else {
		return fieldName;
	}
} 