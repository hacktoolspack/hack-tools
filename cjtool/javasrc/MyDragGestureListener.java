import java.awt.dnd.*;
import java.awt.datatransfer.*;
import javax.swing.*;
import netscape.javascript.*;
import java.awt.Cursor;

class MyDragGestureListener extends DragSourceAdapter implements DragGestureListener 
{
    JSObject win;
    String text;
    String type;
    
    public MyDragGestureListener(JApplet applet) {
        win = JSObject.getWindow(applet);
        this.type = "text";
    }

    public void dragGestureRecognized(DragGestureEvent evt) {
        Transferable t;
        
        if (this.type.equals("html"))
            t = new HtmlTransferable(this.text);
        else
            t = new StringSelection(this.text);
        
		try {
            evt.startDrag(Cursor.getDefaultCursor(), t, this);
            win.call("dragStarted", null);
		} catch (Exception e) {
		     System.out.println(e);   
		}
	}
	
	public void setText(String text, String type) {
	    this.text = text;
	    this.type = type;
	}
	
	public void dragDropEnd(DragSourceDropEvent dsde) {
	    win.call("dragEnded", null); 
	}   
}

