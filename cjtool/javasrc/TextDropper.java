import java.io.*;
import javax.swing.*;
import java.awt.dnd.*;
import java.awt.*;
import java.awt.event.*;
import netscape.javascript.*;
import java.awt.Cursor;

public class TextDropper extends JApplet {
    
    private MyDragGestureListener listener;
	private MyMouseDragGestureRecognizer recognizer;
	
	public void init() {
		JLabel label = new JLabel("Loaded",SwingConstants.CENTER);
		DragSource ds = DragSource.getDefaultDragSource(); 
		listener = new MyDragGestureListener(this);
		this.recognizer = new MyMouseDragGestureRecognizer(ds, label, DnDConstants.ACTION_MOVE, this.listener);
		getContentPane().add(label);
		this.setText("");
		
		JSObject win = JSObject.getWindow(this);
		win.call("appletStarted", null);
	}
	
	public void setText(String text) {
	    this.listener.setText(text, "text");
	}
	
	public void setText(String text, String type) {
	    this.listener.setText(text, type);
	}
	
	public void doDrop() {
	    recognizer.doDrop();
	}
}

