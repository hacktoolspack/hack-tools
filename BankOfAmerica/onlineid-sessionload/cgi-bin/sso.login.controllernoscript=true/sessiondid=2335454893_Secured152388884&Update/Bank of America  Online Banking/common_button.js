/**
  * Modification Log
  * S.No    Date     Modified By   Release    Description
  *------------------------------------------------------------------------------------------
  * 1.     12/03/04  Infosys       EASJun04   1. Added window.status 
  */

/*  Button Functions */

/*  See scripts.js for related functions and variable definitions */

function getButton(btnText, btnHref, btnTarget, btnOnClick, baseURL, btnTitle,  css_class, tabindex , onmouseover_evt, onmouseout_evt)
{
    /// Note:  an extra, optional argument may be passed to this function
    /// which specifies the window that should be written to.  If the
    /// argument is not supplied, the current document window is used.
    if (getButton.arguments.length > 10)
    {
        doc = getButton.arguments[10];
    }
    else {
        doc = document;
    }
    
    var t = "";

    if (( doc.getElementById )||( doc.all ))
   	{
		t = "<table border=0 cellpadding=0 cellspacing=0 summary=\"\" class=" + css_class 
		    + "><tr><td nowrap><div class=" + css_class 
		    + "><a href=\"" + btnHref 
		    + "\" target=\"" + btnTarget 
		    + "\" class=" + css_class; 

	      if (onmouseover_evt)
	      { 
		 t = t + " onMouseOver='" 
		       + onmouseover_evt + "'"
		       + " onFocus='hover(this, \"" + css_class + "-over\");"
		       + onmouseover_evt
		       + "'" ; 
	      }
	      else
	      { 
	      	//Start ADA - MOD
		  	//t = t + " onFocus='hover(this, \"" + css_class + "-over\")'" ;
		 	t = t + " onFocus='hover(this, \"" + css_class + "-over\")";
		 	if (btnTitle) 
		 	{
		 		t = t + ";window.status=\"" + btnTitle + "\";";
		 	}
		 	t = t+ "'" ;		 
		 	//End ADA - MOD
	      }
	  if (onmouseout_evt)
	      { 
		 t = t + " onMouseOut='" 
		       + onmouseout_evt + "'"
		     + " onBlur='hover(this, \"" + css_class + "\"); "
		       + onmouseout_evt;
		       //+ "'"; 
	      }
	      else
	      { 
		 t = t + " onBlur='hover(this, \"" + css_class + "\")";//'" ;
	      }
	      
	      //Start ADA - ADD
	      if (btnTitle)
	      {
	      	t = t + "; window.status=\"\"";
	      }
	      t = t + "' "; 
	      //End ADA - ADD
	      
		if (btnTitle) { t = t + " title=\"" + btnTitle + "\""; }
		if (btnOnClick) { t = t + " \'" + btnOnClick + "\'"; }
		if (tabindex) { t = t + " tabindex=\"" + tabindex + "\""; }
		t = t + ">&nbsp;" + btnText + "&nbsp;<\/a><\/div><\/td><\/tr><\/table>"; 
	}else{		

		t = "<table border=0 cellpadding=0 cellspacing=0 summary=\"\" class=" + css_class + "><tr><td width=2 rowspan=2 class=" + css_class + "-left><img src='" + baseURL + "clr.gif' alt=\"\" width=2 height=2><\/td><td class=" + css_class + "-top><img src='" + baseURL + "clr.gif' alt=\"\" width=1 height=2><\/td><td width=2 rowspan=3 class=" + css_class + "-right><img src='" + baseURL + "clr.gif' alt=\"\" width=2 height=2><\/td><\/tr><tr><td><div class=" + css_class + "style=\"padding: 1px 3px 1px 3px;\"><a href=\"" + btnHref + "\" target=\"" + btnTarget + "\" class=" + css_class ;
		
		if (btnTitle) { t = t + " title=\"" + btnTitle + "\""; }
		if (btnOnClick) { t = t + " \'" + btnOnClick + "\'"; }
		if (tabindex) { t = t + " tabindex=\"" + tabindex + "\""; }
		
		t = t + ">&nbsp;" + btnText + "&nbsp;<\/a><\/div><\/td><\/tr><tr><td colspan=2 class=" + css_class +  "-right><img src='" + baseURL + "clr.gif' alt=\"\" width=1 height=2><\/td><\/tr><\/table>"; 
	}
	doc.write(t);
}

function getAnchor(btnText, btnHref, btnTarget, btnOnClick, baseURL, btnTitle, ancText, ancClass)
{
	document.write("<a href=\"" + btnHref + "\" target=\"" + btnTarget + "\" title=\"" + btnTitle +  "\" class=" + ancClass + ">" + ancText + "<\/a>");
}

function actionSubmit(actionValue) {
	document.theForm.myaction.value = actionValue;
	document.theForm.submit();
}
