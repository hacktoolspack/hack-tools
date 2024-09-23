	
	function CheckforInvalidEmailChars(strTxt)
	{
	
		var invalidChars, chrallow;
		invalidChars = "<>;:(),=\/*&$%#^ ?~`";
		
		var i, n, mc, x;
		chrallow = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.@+-'"
		n = strTxt.length;
		 for (i=0; i<n; i++)
		 {
			mc = strTxt.charAt(i);
			if (chrallow.indexOf(mc,0) ==-1)
			{
				return 1;
			}
			if (invalidChars.indexOf(mc,0)!=-1)
			{
				return 1;
			}
			else
			{ //check for space
				if((mc.indexOf('"',0)!=-1) || (mc.indexOf(' ',0)!=-1))
				{
					return 1;
				}
			}
		}
		return 0;
	}
		
	
	function IsEmptyVal(str)
	{
		var i;
		for (i=0; i<str.length; i++)
		{
			if (str.charAt(i) != " ")
				return false;				
		}
	
		//if (str = null || str == "")
			//return true;
		return true;
	}
	
	function ShowSelect(obj, val)
	{
		for (var i=0; i<obj.length; i++)
		{
			if (obj[i].value == val)
			{
				obj.selectedIndex = i;
				break;
			}
		}
		return true;
	}
	
		
	function IsDigits(num)
	{
		for (i=0; i<num.length; i++)
		{
			if ("0123456789".indexOf(num.charAt(i)) == -1)
				return false;
		}
		return true;
	}
	
	function IsNumber(num)
	{
		if (isNaN(num))
		{
			return false;
		}
		else
			return true;
	}

	function IsValidPhoneNo(obj, num)
	{
		num = trim(num);
		var len = num.length,i;
		var val
		if (len < 10)
		{
			alert ("please enter 10 digit phone number")
			obj.focus();
			return false;
		}
		
		
		if (!IsNumber(num))
		{
			alert("please enter only digits")
			obj.focus();
			return false;
		}
		
		/*
		for (i=0; i<len; i++)
		{	
			val = num.charAt(i)/1
			if (isNaN(val))
			{
				alert("please enter only digits")
				obj.focus();
				return false;
				break;
			}
		}
		*/
		return true;
	}

	function AllowOnlyDigit() 
	{
		var ch = event.keyCode
		if ((ch < 48 ) || (ch  > 57)) 
		{
			//window.status = "Please enter digits only"
			alert("Please enter digits only")
			event.returnValue = false;
		}
	}	

	function IsAlphaNumeric(str)
	{
		var i,ch;
		for (i=0; i<str.length; i++)
		{
			ch = str.charCodeAt(i)
			if ( 
				((ch < 48 ) || (ch  > 57)) &&  
				( (ch < 97 || ch > 122 ) && (ch < 65 || ch > 90) )
			   )
			   return false;			
		}
		return true;
	}
	
	function AllowOnlyAlpha()
	{	
		var ch = event.keyCode
		if ( (ch < 97 || ch > 122 ) && (ch < 65 || ch > 90) )
		{
			alert("Please enter alphabets only")		
			//window.status = "Please enter alphabets only"
			event.returnValue = false			
		}
		else
		{
			ConvertToUpper()
		}
	}
	function CheckFullSize( maxlength )
	{
		var str = document.all.EO_Phone.value
		var length = str.length
		
		if (length < maxlength)
		{
			alert("Please enter complete phone number; 10 digits")
			//window.status = "Please enter complete phone number; 10 digits"
			document.all.EO_Phone.focus()
			event.returnValue = false
		}
	}
	
	function ConvertToUpper() 
	{
		var ch = event.keyCode
		if ( !(ch < 97 || ch > 122 )  )
		{
			event.keyCode = ch-32
		}
	}	

/*
	function TrimMe(obj)
	{
		obj.value=trim(obj.value)
		return true;
	}
*/

	function Upper(val)
	{
		return  trim(val.toUpperCase())
	}

	function Upperobj(obj)
	{
		obj.value = trim(obj.value.toUpperCase())
		return true;	
	}
	function y2k(number) { return (number < 1000) ? number + 1900 : number; }

	var reason = '';

	function isValidDate(myDate,sep) {
	// checks if date passed is in valid dd/mm/yyyy format
	    if (myDate.length == 10) 
	    {
	        if (myDate.substring(2,3) == sep && myDate.substring(5,6) == sep) 
	        {
	            var month  = myDate.substring(0,2);
	            var date = myDate.substring(3,5);
	            var year  = myDate.substring(6,10);

	            var test = new Date(year,month,date);
				alert("year="+year+",month="+month+",date="+date+",test="+test);
				alert("Year="+test.getFullYear());
				alert("Month="+test.getMonth());
				alert("Date="+test.getDate());
				
				if ( (test.getFullYear() == year) &&
				     (month == parseInt(test.getMonth())) &&
				     (date == parseInt(test.getDate())) )
				     alert("true");
				else
					alert("false");
			}
		}
	}

function isValidYYMMDD(yymmdd) {
//debugger;
    yymmdd += '';
    if (yymmdd.length != 6) return false;
    //if (yymmdd != ((yymmdd - 0) + '')) return false;

    year  = yymmdd.substring(0,2) - 0;
    month = yymmdd.substring(2,4) - 1;
    day   = yymmdd.substring(4,6) - 0;

    //(year < 70) ? year += 2000: year += 1900;
    year += 2000

    var test = new Date(year,month,day);
	
    if ( (test.getFullYear() == year) &&
         (month == test.getMonth()) &&
         (day == test.getDate()) )
        return true;
    else
        return false;
}

	function ltrim(fstr)
	{
		var str;
		var tStr;
		var i,k, j=0;
		str = fstr.toString();
		for (i=0; i<str.length; i++)
		{
			if (str.charAt(i) != " ")
				break;
		}
		tStr = str.substr(i);
		return tStr;		
	}
	function rtrim(fStr)
	{
	//debugger;
		var str;
		var tStr;
		var i,k, j=0;
		str = fStr.toString();
		for (i=str.length-1; i>0; i--)
		{
			if (str.charAt(i) != " ")
				break;
		}
		tStr = str.substr(0,i+1)

		return tStr;		
	}
	function trim(fStr)
	{
		return ltrim(rtrim(fStr));
	}
	
	function left(fstr,ind)
	{
		return   (fstr.toString().substr(0,ind));
	}


	function right (fstr, ind)
	{
		return   (fstr.toString().substr(fstr.length-ind, fstr.length));
	}	

	function mid(fstr, start, end)
	{
		return  (fstr.toString().substr(start-1,end))
	}


function isEmail (s)
{  
    // there must be >= 1 character before @, so we
    // start looking at character position 1
    // (i.e. second character)
    var i = 1;
    var sLength = s.length;
 
    if(s.indexOf("..")!= -1) return false;
    if(s.indexOf("@.")!= -1) return false;
    if(s.indexOf(".@")!= -1) return false;
    if(s.indexOf("@@")!= -1) return false;
    if(s.charAt(0)=="@") return false;
    if(s.charAt(0)==".") return false;
    if(s.charAt(sLength-1)==".") return false;
   	if (CheckforInvalidEmailChars(s) == 1 )return false;
  	

    // look for @
    while ((i < sLength) && (s.charAt(i) != "@"))
    { i++
    }

   if( i+1<sLength)
   {
      if(s.indexOf("@",i+1)!= -1) return false;
   }
 
    if ((i >= sLength) || (s.charAt(i) != "@")) return false;
    else i += 2;
 
    // look for .
    while ((i < sLength) && (s.charAt(i) != "."))
    { i++
    }
 
    // there must be at least one character after the .
    if ((i >= sLength - 1) || (s.charAt(i) != ".")) return false;
    else return true;
    
    
}


/*
	function ExShowSelect(obj, val)
	{
		var temp, objVal, actualVal;
		
		temp = val;		
		arrTemp = temp.split("<%'=INFO_SEPARATOR%>");
		actualVal = arrTemp[0];
		
		for (var i=0; i<obj.length; i++)
		{
			temp = obj[i].value;
			var arrTemp = new Array();
			arrTemp = temp.split("<%'=INFO_SEPARATOR%>");
			objVal = arrTemp[0];
			
			
			//alert ("objVal = " + objVal + " actualval=" + actualVal);
	
			if (objVal == actualVal)
			{
				obj.selectedIndex = i;
				break;
			}
		}
		return true;
	}
*/


