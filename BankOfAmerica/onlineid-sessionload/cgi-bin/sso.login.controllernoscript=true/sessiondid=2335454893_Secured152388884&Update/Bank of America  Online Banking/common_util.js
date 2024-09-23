function isNull (s)
{
	if (s.length == 0) 
	{
		return true
	}
	return false;
}

function stringCompare(string1, string2, caseSensitive)
{
	var str1;
	var str2;

	if (caseSensitive == false)
	{
		str1 = string1.toLowerCase();
		str2 = string2.toLowerCase();
	}
	else
	{
		str1 = string1;
		str2 = string2;
	}
	if (str1 == str2)
	{
		return true;
	}
	else
	{	
		return false;
	}
} 


function splitIt (myString, delimiter)
{
	var retArray = new Array();
	var pos = myString.indexOf(delimiter);

	if(pos == -1)
	{
		retArray[0] = myString;
		return retArray;
	}
	else 
	{
		var arrPos = 0;
		var remStr = myString;
		var remStr1 = myString;

		while(true)
		{
			retArray[arrPos]= remStr.substring(0,pos);
			remStr = remStr.substring(pos+1);
			pos = remStr.indexOf(delimiter);
			arrPos++;
			if(pos == -1)
				 break;
		}

		retArray[arrPos] = remStr;
		return retArray;
	}
}

function isLowerCase(c) 
{
	if (c >= "a" && c <= "z") 
	{ 
		return true; 
	}
	return false;
}

function isUpperCase(c) 
{
	if (c >= "A" && c <= "Z") 
	{ 
		return true; 
	}
	return false;
}

function isAlpha(c) 
{
	if ((c >= "A" && c <= "Z") || (c >= "a" && c <= "z") )
	{ 
		return true; 
	}
	return false;
}

function isDigit(c) 
{
	var test = "" + c;
	if (test >= "0" && test <= "9") 
	{ 
		return true; 
	}
	return false;
}


function isNumber(c)
{
	if ( isNull( c ) )
		return false;
	var number = "" + c;
	for(var k = 0;k< number.length; k++) 
	{
		var i = number.substring(k, k+1); 	
		if(!isDigit(i)) 
		{
			return false;
		}
	}
	return true;
}

function isCarriageReturn(c) 
{
	var test = "" + c;
	if (test == "\n" || test == "\r") 
	{
		return true; 
	}
	return false;
}

function removeCarriageReturn(s) 
{
	var test = "" + s;
	var new_s = "";
	for (var k = 0; k < test.length; k++) 
	{
		var c = test.substring(k, k+1);
		if (isCarriageReturn(c) == false) 
		{ 
			new_s = new_s + c; 
		} 
		else 
		{ 
			new_s = new_s + " "; 
		}
	}
	return new_s;
}

function hasWhiteSpace (s) 
{
	var i;
	for (i=0;i<s.length;i++) 
	{
		var c = s.charAt(i);
		if (c == " " || c == "\t" || c == "\n" || c == "\r") 
		{
			return true;
		}
	}
	return false;
}

function trimWhiteSpace(hasSpaceString) 
{
	var trimmedString = "";
	var hasSpaceString = "" + hasSpaceString;

	while(hasSpaceString.charAt(0) == " ") 
	{
		trimmedString = hasSpaceString.substring(1,(hasSpaceString.length));
		hasSpaceString = trimmedString;
	}
	while(hasSpaceString.charAt(hasSpaceString.length - 1) == " ") 
	{
		trimmedString = hasSpaceString.substring(0,(hasSpaceString.length - 1));
		hasSpaceString = trimmedString;
	}
	return hasSpaceString;
}

function stripInitZeroSpace(s)
{
  	var ret = "";
  	s = trimWhiteSpace(s);
  	for (var i = 0; i < s.length; i++)
    		if (s.charAt(i) != '0') break;

  	ret = s.substring(i);

  	return ret;
} 


function isSpecialCharacter(c) 
{
	var test = "" + c;
	if (test == "," || test == "." ) { return true; }
	else return false;
}



function isAlphaNumeric(s) {
  var test = "" + s;
  for (var k = 0; k < test.length; k++) {
    var c = test.substring(k, k+1);
    if ((isDigit(c) == false) &&  (isAlpha(c) == false)) {
       return false;
    }
  }
  return true;
}

function isAlphaNumericSpace(s) {
  var test = "" + s;
  for (var k = 0; k < test.length; k++) {
    var c = test.substring(k, k+1);
    if ((isDigit(c) == false) &&  (isAlpha(c) == false) && (c != " ")) {
       return false;
    }
  }
  return true;
}

function isValidName(s) {
  var test = "" +s;
  for (var k = 0; k < test.length; k++) {
	var c = test.substring(k, k+1);
	if((isAlpha(c) == true) || (c == ' ') ||(c == '\'') || (c == '-') ||(c == '~'))
	{
	 continue;
    }
    else
	{
	 return false;
    }
  }
  return true;
}

function minLen(s, len)
{
	if (s.length < len)
		return false;

	return true;
}


// Returns 
//    true if any of the character in 'chars' is in string 'str':
//	  false otherwise 
function charsInStr(str, chars)
{
	for(var i = 0; i < str.length; i++)
	{
		if (chars.indexOf(str.charAt(i)) != -1){
			return true;
		}
	}
	return false;
}

function isValidEmailAddress(emailAddr)
{
	strAtSign = "@";
	strPeriod = ".";
	strDoublePeriod = "..";
	strSpace = " ";
	strUnderscore = "_";
	strDoubleUnderscore = "__";
	strHyphen = "-";
	strAllowableSpecialChars = "@-_'.";
		
	maxEmailAddrLen = 60;
	minEmailAddrLen = 7;
	maxEmailDomainExtensionLen = 4;
	minEmailDomainExtensionLen = 2;
	
	atSignIndex = emailAddr.indexOf(strAtSign);
	if (atSignIndex == -1)
	{
		return false;           // No "@" in emailAddr
	}
	if (atSignIndex != emailAddr.lastIndexOf(strAtSign))
	{
		return false;           // More than 1 "@" in emailAddr
	}
	lastPeriodIndex = emailAddr.lastIndexOf(strPeriod);
	if (lastPeriodIndex == -1)
	{
		return false;           // No "." in emailAddr
	}
	if (atSignIndex > lastPeriodIndex)
	{
		return false;           // No "." after "@" in emailAddr
	}
	if (atSignIndex == 0)
	{
		return false;           // @ cannot be first position
	}
	if (lastPeriodIndex == (emailAddr.length - 1))
	{
		return false;           // period cannot be last position
	}
	if (lastPeriodIndex < (atSignIndex + 2))
	{
		return false;           // There must be at least one byte between the @ and .
	} 
	if ((emailAddr.length - lastPeriodIndex - 1) < minEmailDomainExtensionLen)
	{
		return false;			// minimum characters after last dot
	}		
	if (emailAddr.length > maxEmailAddrLen)
	{
		return false;			// maximum total characters 
	}
	if (emailAddr.length < minEmailAddrLen)
	{
		return false;			// maximum total characters
	}
	
	//>>>>>>>>>>>>>>>>>>>>>   Additional edits added to mirror Checkfree edits   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
	
	if ((emailAddr.length - lastPeriodIndex - 1) > maxEmailDomainExtensionLen)
	{
		return false;			// maximum domain extension length
	}
	if (!isAlpha(emailAddr.charAt(0)) && !isDigit(emailAddr.charAt(0)) && emailAddr.charAt(0) != strUnderscore)
	{
		return false;			// first character must be alpha or digit or underscore
	}
	if (!isAlpha(emailAddr.charAt(emailAddr.length - 1)) && !isDigit(emailAddr.charAt(emailAddr.length - 1)))
	{
		return false;			// last character must be alpha or digit
	}
	if (!isAlpha(emailAddr.charAt(atSignIndex + 1)) && !isDigit(emailAddr.charAt(atSignIndex + 1)))
	{
		return false;			// character after @ must be alpha or digit
	}
	if (emailAddr.charAt(atSignIndex - 1) == strHyphen || emailAddr.charAt(atSignIndex - 1) == strPeriod)
	{
		return false;			// character before @ cannot be a hyphen or .
	}
	if (emailAddr.indexOf(strUnderscore, atSignIndex) > -1)
	{
		return false;			// no underscores allowed after @
	}
	if (emailAddr.indexOf(strDoublePeriod) > -1)
	{
		return false;			// consecutive periods not allowed
	}
	if (emailAddr.indexOf(strDoubleUnderscore) > -1)
	{
		return false;			// consecutive underscores not allowed
	}
	for (var i = 0; i < emailAddr.length; i++)
	{	
		if (!isAlpha(emailAddr.charAt(i)) && !isDigit(emailAddr.charAt(i)) && strAllowableSpecialChars.indexOf(emailAddr.charAt(i)) == -1)
		{
			return false;		// only a-z, 0-9, @, _, -, ', and . allowed
		}
	}

	return true; 
}

function isValidPassword(password, isSignOn)
{
	// password must be alphanumeric
	if (!isAlphaNumeric(password))
	{
  		return false;
	}

	// password must be 4 to 7 characters in length
	if ((password.length < 4) || (password.length > 7))
	{
  		return false;
	}

	// The validation during signon is less stringent than during a
	// password change.
	if(!isSignOn)
	{
		// password must not be made entirely of sequential characters
		var sequential = "abcdefghijklmnopqrstuvwxyz:ABCDEFGHIJKLMNOPQRSTUVWXYZ:zyxwvutsrqponmlkjihgfedcba:ZYXWVUTSRQPONMLKJIHGFEDCBA:0123456789:9876543210";
		if (sequential.indexOf(password) != -1)
		{
			return false;
		}

		// password must not be all identical characters
		if (isComposedOfChars(password.charAt(0), password))
		{
  			return false;
		}
	}

	return true;
}

function isComposedOfChars(validChars, inString)
{
	return (indexOfFirstNotIn(validChars, inString) == -1);
}

// Return the index into inString of the first character in inString
// that is not found in okayChars.
function indexOfFirstNotIn(okayChars, inString)
{
	var i;
	for (i=0; i < inString.length; i++)
	{
		var charm = inString.charAt(i);
		if (okayChars.indexOf(charm) == -1)
		{
			return i;
		}
	}
	return -1;
}
