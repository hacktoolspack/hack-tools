// find the last day of the month and
// take the leap year into account
function makeLastDay(month, year) 
{
	var day=0;
 
	if(month == 0) 
		day=31;
	if(month == 1) 
	{
  		if(year % 4 == 0) 
  		{
    			if (year % 400 == 0)
      				day=29;
    			else if (year % 100 == 0)
      				day = 28;
    			else
      				day = 29;
		}
		else
			day=28;
  	}
	if(month == 2) 
		day = 31;
	if(month == 3) 
		day = 30;
	if(month == 4)
		day = 31;
	if(month == 5) 
		day = 30;
	if(month == 6) 
		day = 31;
	if(month == 7) 
		day = 31;
	if(month == 8) 
		day = 30;
	if(month == 9) 
		day = 31;
	if(month == 10) 
		day = 30;
	if(month == 11) 
		day = 31;

	return day;
}



// return MM/DD/YYYY or false
function checkDateFormat(s)
{
  	var ret = true;
  	var pos = checkDateDelimiter(s);

  	if (pos[0] == -1 || pos[1] == (pos[0]+1) || pos[0] == 0) 
	{
    		ret = -1;
	}
  	else
  	{
    		var error = "";
    		var monStr = stripInitZeroSpace(s.substring(0, pos[0]));
    		var dayStr = stripInitZeroSpace(s.substring(pos[0] + 1, pos[1]));
    		var yearStr = s.substring(pos[1] + 1);
    		if (!isNumber(monStr, error) || !isNumber(dayStr, error) || 
			!isNumber(yearStr, error) || 
         		monStr == "" || dayStr == "")
      			ret = -1;
    		else
    		{
      			var month = parseInt(monStr);
      			var day = parseInt(dayStr);
      			var year = parseInt(yearStr);

      			if (month < 10) monStr = '0' + monStr;
      			if (day < 10) dayStr = '0' + dayStr;
      			if (yearStr.length == 2)
      			{
        			if ((year >= 91) && (year<=99) )
          				yearStr = '19' + yearStr;
        			else
        			{
          				if (yearStr.length == 1) 
						{
							yearStr = '0' + yearStr;
						}
          				yearStr = '20' + yearStr;
        			}
      			}

      			else if (yearStr.length != 4)
				{
       				 ret = -1;
				}

      			if (ret != -1)
      			{
       				year = parseInt(yearStr);
       				var lastday = makeLastDay(month - 1, year);
        			if (day > lastday) 
          				ret = -1;
      			}
      
      			if (ret != -1 ) 
			{
				ret = monStr + '/' + dayStr + '/' + yearStr;
			}
			
    		}
  	}

  	if (ret == "-1")
  	{
    		ret = false;
  	}
	return ret;

} 

// from and to must be in MM/DD/YYYY
// return -1 if toDate < fromDate
// return -2 if toDate > 1 year from fromDate
// return toDate - fromDate in days
function validateDate(fromDate, toDate)
{
	var ret = 0;

	var year = parseInt(toDate.substring(6, 10));
	var month = parseInt(stripInitZeroSpace(toDate.substring(0, 2)));
	var day = parseInt(stripInitZeroSpace(toDate.substring(3, 5)));
	var to = new Date(year, month - 1, day);

	year = parseInt(fromDate.substring(6, 10));
	month = parseInt(stripInitZeroSpace(fromDate.substring(0, 2)));
	day = parseInt(stripInitZeroSpace(fromDate.substring(3, 5)));
	var from = new Date(year, month - 1, day);

	if (month > 2)
		year++;

	var temp = makeLastDay(month - 1, year);
	if (temp == 29)
		temp = 366;
	else
		temp = 365;

	var diff = (Date.parse(to.toGMTString()) - Date.parse(from.toGMTString())) / 86400000;

	if (diff < 0 )
		ret = -1;
	else if (diff >= temp)
		ret = -2;
	else 
		ret = diff;

	return ret;
} 


function checkDateDelimiter(s)
{
  	var delimiter = new Array('/', '.', '-');
  	var pos = new Array(-1, -1);

  	for (var i = 0; i < 3; i++)
  	{
    		pos[0] = s.indexOf(delimiter[i]);
    		if (pos[0] != -1) 
    		{
      			pos[1] = s.indexOf(delimiter[i], pos[0]+1);
      			if (pos[1] == -1) 
        			pos[0] = -1;
      			else
        			break;
    		}
  	}
  	return pos;
} 

function isDate1BeforeDate2(date1, date2)
{
	var date1Y = parseInt(date1.substring(6, 10));
	var date2Y = parseInt(date2.substring(6, 10));
	var date1M = parseInt(stripInitZeroSpace(date1.substring(0, 2)));
	var date2M = parseInt(stripInitZeroSpace(date2.substring(0, 2)));
	var date1D = parseInt(stripInitZeroSpace(date1.substring(3, 5)));
	var date2D = parseInt(stripInitZeroSpace(date2.substring(3, 5)));
	
	if (date1Y < date2Y)
		return true;
	else if (date1Y == date2Y)
	{
		if (date1M < date2M) 
			return true;
		else if (date1M == date2M)
			if (date1D < date2D)
				return true;
	}
	return false;
}
function computeJD()
{
		date = new Date();
		var YY = date.getFullYear();
		var MM = date.getMonth() + 1;
		var DD = date.getDate();

		with (Math) {
			  	GGG = 1;
				if (YY <= 1585) GGG = 0;
				  	JD = -1 * floor(7 * (floor((MM + 9) / 12) + YY) / 4);
					S = 1;
				  	if ((MM - 9)<0) S=-1;
						A = abs(MM - 9);
					  	J1 = floor(YY + S * floor(A / 7));
						J1 = -1 * floor((floor(J1 / 100) + 1) * 3 / 4);
					  	JD = JD + floor(275 * MM / 9) + DD + (GGG * J1);
						JD = JD + 1721027 + 2 * GGG + 367 * YY;
		}
}
