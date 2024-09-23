var imageArray    = new Array();                      // Array for images
var nrImages      = new Number(0);                    // number of images
var outState      = new String("_off");               // the "out" state - tab not selected or highlighted
var onState       = new String("_on");                // the "on" state - tab is selected
var overState     = new String("_over");              // the "over" state - tab is highlighted

/* Current link on focus for keyboard, if any */
//var current_onfocus_obj =  new String("");
var current_onfocus_obj =  new String("");
/* Class name for current link on focus for keyboard, if any */
var current_onfocus_obj_defocus_src =  new String("");
var current_onfocus_obj_classname =  new String("");

// preload images
function preLoadImages(imageName, subdir, nrStates)
{  
   // Parameters:
   //    imageName - an array of objects such that imageName[i].name is a file name
   //                without extension or postfix,
   //                and imageName.ext is the file extension
   //    subdir    - the subdirectory where the image files reside
   //    nrStates  - either 2 ("off" and "over") or 3 ("off", "on", and "odver")

   if (document.images)   // if image processing is OK
   {  
     // create image array
      for (i = 0; i < imageName.length; i++)
      {   
         var j = imageArray.length; 
         imageArray[j] = new Object();
         imageArray[j].name = imageName[i].name;
         
			if (nrStates == "2")
          {
            imageArray[j].outImage = new Image();
            nrImages++;
            imageArray[j].outImage.src = new String(subdir + imageName[i].name + outState + "." + imageName[i].ext); 
     
            imageArray[j].overImage = new Image();
            nrImages++;             
            imageArray[j].overImage.src = new String(subdir + imageName[i].name + overState + "." + imageName[i].ext);  
          }
         
          else if  (nrStates == "3")
          {
            imageArray[j].outImage = new Image();
            nrImages++;            
            imageArray[j].outImage.src = new String(subdir + imageName[i].name + outState + "." + imageName[i].ext); 

           
            imageArray[j].onImage = new Image();
            nrImages++;
            imageArray[j].onImage.src = new String(subdir + imageName[i].name + onState + "." + imageName[i].ext);

            imageArray[j].overImage = new Image();
            nrImages++;
            imageArray[j].overImage.src = new String(subdir + imageName[i].name + overState + "." + imageName[i].ext); 
         }
            
      }  // end for
   }  // end if

}  // end function

// set the source of an image to the "out or "over" state
function setImage(ref, ImgName, state)
{
   // Parameters
   //    nrImg       - the number of the image
   //    state       - the image state to convert to

    if (document.images)    // if image processing is OK
   {     	
      for (i = 0; i < imageArray.length; i++)
      { 
         if (imageArray[i].name == ImgName)
         {
	         if (state == "over")
            { 
             document[ImgName].src = imageArray[i].overImage.src; 
            }
            else if (state == "out")
            { 
             document[ImgName].src = imageArray[i].outImage.src;
            }
            else
            ;
         }
						
      }

   }
}

// set the source of an image to the "out or "over" state
// set this tab as the one in focus (it has been tabbed to)
function setImage_focus(ref, ImgName, state)
{
   // Parameters
   //    nrImg       - the number of the image
   //    state       - the image state to convert to

    if (document.images)    // if image processing is OK
   {     	
      for (i = 0; i < imageArray.length; i++)
      { 
         if (imageArray[i].name == ImgName)
         {
	         if (state == "over")
            { 
             document[ImgName].src = imageArray[i].overImage.src; 
				 current_onfocus_obj = ImgName;
				 current_onfocus_obj_defocus_src = imageArray[i].outImage.src;
            }
            else if (state == "out")
            { 
             document[ImgName].src = imageArray[i].outImage.src;
				 current_onfocus_obj = "";
             }
            else
            ;
         }
      }
   }
}

// set the source of an image to the "out or "over" state
// defocus any image that has been tabbed to
function setImage_defocus(ref, ImgName, state)
{
   // Parameters
   //    nrImg       - the number of the image
   //    state       - the image state to convert to
   // Parameters
   //    nrImg       - the number of the image
   //    state       - the image state to convert to

    if (document.images)    // if image processing is OK
   {     	
      for (i = 0; i < imageArray.length; i++)
      { 
         if (imageArray[i].name == ImgName)
         {
	         if (state == "over")
            { 
             document[ImgName].src = imageArray[i].overImage.src; 
            }
            else if (state == "out")
            { 
             document[ImgName].src = imageArray[i].outImage.src;
             }
            else
            ;
         }
			 if (current_onfocus_obj != "")
			 { 
			   document[current_onfocus_obj].src = current_onfocus_obj_defocus_src;
				current_onfocus_obj = "";
			 } // end if
      }
   }
}


// Parameters - ref is a reference to the element (this)
//	classRef is a new class attribute value
function rollover(ref, classRef)
{
 	if ((classRef.indexOf("over") != -1) || (classRef.indexOf("on") != -1) || (classRef.indexOf("hover") != -1))
		{current_onfocus_obj = ref;}
	else
		{current_onfocus_obj = ""; }
	
	eval(ref).className = classRef;
	current_onfocus_obj_classname = classRef;
}	// end function

function rollover_defocus(ref, classRef)
{
	// defocus the current link - disallows 2 links to both be highlighted
	// exception - if you highlight and item and tab through other items, then 
	// both items will be highlighted, due to CSS
	var strIndex = -1;
	if (current_onfocus_obj != "")
	{ 
		if ((current_onfocus_obj_classname.indexOf("navg") != -1))
		{
			strIndex = current_onfocus_obj_classname.indexOf("-over");
			eval(current_onfocus_obj).className = current_onfocus_obj_classname.substr(0,strIndex) + "-out";
		}
      else if ((current_onfocus_obj_classname.indexOf("nav1-sel") != -1))
		{
			strIndex = current_onfocus_obj_classname.indexOf("-over");
			eval(current_onfocus_obj).className = current_onfocus_obj_classname.substr(0,strIndex) + "-out";
		}
		else if ((current_onfocus_obj_classname.indexOf("nav1") != -1))
		{
			strIndex = current_onfocus_obj_classname.indexOf("-over");
			eval(current_onfocus_obj).className = current_onfocus_obj_classname.substr(0,strIndex) + "-out";
		}
   	else if (current_onfocus_obj_classname.indexOf("nav2") != -1)
		{
			strIndex = current_onfocus_obj_classname.indexOf("-over");
			eval(current_onfocus_obj).className = current_onfocus_obj_classname.substr(0,strIndex) + "-out";
      }
   	else if (current_onfocus_obj_classname.indexOf("footer") != -1)
		{ 
			/* footer links */
			eval(current_onfocus_obj).className = "footer2-housinglink";
		}
	} // end if
	
	if (classRef.indexOf("-over") != -1 || classRef.indexOf("-hover") != -1 || classRef.indexOf("-on") != -1)
		{current_onfocus_obj = ref;}
	else
		{current_onfocus_obj = ""; }
	
	eval(ref).className = classRef;
	current_onfocus_obj_classname = classRef;

}	// end function


