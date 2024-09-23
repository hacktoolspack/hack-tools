// return a string with thousand separator
// eg, 1234.1 becomes 1,234.10
function formatAmount(s)
{
  	var ret = "";
  	var amtStr = "" + s;
  	var dot = amtStr.indexOf('.');
	if (dot == -1)
		dot = amtStr.length;
  	var intStr = amtStr.substring(0, dot);
  	var amt = parseInt(intStr);

  	var l = intStr.length;
  	var pos = l % 3;
  	if (pos != 0) 
    		ret = amtStr.substring(0, pos) + ',';
  
  	while(pos < l)
  	{
    		ret += amtStr.substring(pos, pos+3) + ',';
    		pos += 3;
  	}

	if (ret.length > 1)
	  	ret = ret.substring(0, ret.length - 1);

	if (amtStr.length == l || amtStr.charAt(amtStr.length - 1) == '.')
		ret += ".00";
	else
	{
		ret += ".";
		var dec = amtStr.substring(dot + 1);
		if (dec.length == 1)
			dec += "0";
  		ret += dec;
	}
  	return ret;
} 

// check if it is in amount format
function isAmountFormat(c) 
{
	var number = "" + c;
	var specialChar = " ";
	var commaCount = 0;
	var digitsAfterDot = 0;
	var digitsAfterComma = 0;
	var specialCharCount = 0;
	var digitFlag = false;
	var digitCount = 0;
	for(var k = 0;k< number.length; k++) 
	{
	        var i = number.substring(k, k+1);
		if(isDigit(i) && digitsAfterDot < 2  && digitsAfterComma <= 3 ) 
		{
			digitFlag = true;
			digitCount++;
			if(specialChar == ".")
			{
				digitsAfterDot++;
			}
			if(specialChar == ",")
			{
				digitsAfterComma++;
			}
		}
		else if (isSpecialCharacter(i) && digitsAfterDot < 2 && digitsAfterComma <= 3) 
		{
			if(digitFlag == true) 
			{
				digitFlag = false;
				specialChar = i;
				if(i == ",")
				{
					commaCount ++; 
					digitsAfterComma = 0;
				}
				specialCharCount++;
			}	
			else 
			{
				return false;
			}
		}
		else 
		{
			return false;
		}
	 }
	// cents must be 2 digits
	if((specialChar == "." ) && (digitsAfterDot < 2))
	{
		return false;
	}
	// make sure number does not end in dot or comma
	if(isSpecialCharacter(i))
	{
		return false;
	}
	return true;	
}

function amountOnly(amt)
{
	var amount = "";
	var amtStr = "" + amt;
	var start = 0;
	var pos = amtStr.indexOf(',');
	while (pos != -1)
	{
		amount += amtStr.substring(start, pos);
		start = pos + 1;
		pos = amtStr.indexOf(',', start);
	}
	amount += amtStr.substring(start);
	return amount;
}

function checkAmtRange(amt, min, max)
{
	if (amt > max || amt < min)
	{
		return false;
	}

	return true;
} 

