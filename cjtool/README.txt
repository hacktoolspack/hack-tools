Clickjacking Tool version 0.8
=============================
Written by Paul Stone, Context Information Security, please see the 
enclosed LICENSE.txt for terms and conditions of use.

This tool can be used to craft and replay various clickjacking techniques 
against web sites that have not yet implemented clickjacking protection. 

This tool has been tested in Firefox 3.6 and Internet Explorer 8.

Tools
=====

Load URL:
    URL: The URL to load. Click the Go button to actually load the page.
    Frame size: The size of the page. You'll normally want to leave this at
    default, but it can be changed if the default size is too small (e.g a
    long page)
    Fragment Check: Check for the presence of a particular ID on the page 
    before proceeding with the following steps.
    Loaded from User Click: Tick this if the page is loaded as the result 
    of the user clicking on a link or button. Instead of explicitly loading
    the page, the tool will wait for the iframe's onload event before
    continuting with the following steps.
    Drop IDs: Use this to display an overlay of the IDs in the page. To use
    this do the following:
        1. Click the 'Get Fragments' button. The overlay will be removed.
        2. Click in the iframe to focus it, then press Ctrl-A to select all
        the text on the page.
        3. Drag the text onto the little white square next to the button
    Any IDs on the page will be displayed as little labels. To use these to
    place a marker, first focus a marker input field, then click on a
    label. A marker will appear, which can be moved to get relative
    positioning.
    
Click:
    A basic click. Drag the marker onto the page to place it.
    
Enter Text:
    The same as a click, but should be placed over a text field. It uses 
    the 'Java applet forced drag' method to enter text into a field.
    
Drag:
    Use this to select some text on the page. There are two markers, one
    for the start position and another for the end position. Can also be
    used in some other situations, e.g dropdown menus on webpages that
    disappear when the page loses focus.
    
Extract:
    Extract a link, image or selection from a page. Place the marker to
    designate where the drag should start from.
    
    
Other Buttons:
==============
Replay Steps/Replay from Current Step: Replay the steps so that everything
is visible. You should click or drag over the target page, as neccessary. 

Hide/Show Overlay: Use this to hide the page overlay so that you can
interact directly with the framed page.

Save: Click this to display a saveable representation of the steps. This
can later be reloaded using the Load function.

Load: Paste previously saved steps into here, then click OK.

Known Bugs
==========

* Things go strange after clicking the 'Cancel Replay' button while 
  replaying steps.
* Extract HTML doesn't work in Chrome/Safari (ondrop event doesn't trigger
yet)
