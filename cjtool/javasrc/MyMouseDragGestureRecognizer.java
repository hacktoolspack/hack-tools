import java.awt.Component;

import java.awt.dnd.DnDConstants;
import java.awt.dnd.DragSource;
import java.awt.dnd.MouseDragGestureRecognizer;
import java.awt.dnd.DragGestureListener;
import java.awt.Point;
import java.util.Date;

import java.awt.event.InputEvent;
import java.awt.event.MouseEvent;

class MyMouseDragGestureRecognizer extends MouseDragGestureRecognizer {

    private static final long serialVersionUID = -3527844310018033570L;

    /*
     * constant for number of pixels hysterisis before drag is determined
     * to have started
     */

    protected static int motionThreshold;

    protected static final int ButtonMask = InputEvent.BUTTON1_DOWN_MASK |
                                            InputEvent.BUTTON2_DOWN_MASK |
                                            InputEvent.BUTTON3_DOWN_MASK;
    
    /**
     * construct a new WMouseDragGestureRecognizer
     *
     * @param ds  The DragSource for the Component c
     * @param c   The Component to observe
     * @param act The actions permitted for this Drag
     * @param dgl The DragGestureRecognizer to notify when a gesture is detected
     *
     */

    protected MyMouseDragGestureRecognizer(DragSource ds, Component c, int act, DragGestureListener dgl) {
        super(ds, c, act, dgl);
    }

    /**
     * construct a new WMouseDragGestureRecognizer
     *
     * @param ds  The DragSource for the Component c
     * @param c   The Component to observe
     * @param act The actions permitted for this Drag
     */

    protected MyMouseDragGestureRecognizer(DragSource ds, Component c, int act) {
        this(ds, c, act, null);
    }

    /**
     * construct a new WMouseDragGestureRecognizer
     *
     * @param ds  The DragSource for the Component c
     * @param c   The Component to observe
     */

    protected MyMouseDragGestureRecognizer(DragSource ds, Component c) {
        this(ds, c, DnDConstants.ACTION_NONE);
    }

    /**
     * construct a new WMouseDragGestureRecognizer
     *
     * @param ds  The DragSource for the Component c
     */

    protected MyMouseDragGestureRecognizer(DragSource ds) {
        this(ds, null);
    }


    /**
     * Invoked when the mouse has been clicked on a component.
     */

    public void mouseClicked(MouseEvent e) {
        // do nothing
    }

    /**
     * Invoked when a mouse button has been pressed on a component.
     */

    public void mousePressed(MouseEvent e) {
        events.clear();
        int dop = 2;
        appendEvent(e);
        /*System.out.println(e.getSource());
        System.out.println(e.getID());
        System.out.println(e.getWhen());
        System.out.println(e.getModifiers());
        System.out.println(e.getX());
        System.out.println(e.getY());
        System.out.println(e.getClickCount());
        System.out.println(e.isPopupTrigger());*/
        fireDragGestureRecognized(dop, ((MouseEvent)getTriggerEvent()).getPoint());
    }
    
    public void doDrop() {
        MouseEvent e = new MouseEvent(this.component, 501, new Date().getTime(), 16, 10, 10, 1, false);
        appendEvent(e);
        fireDragGestureRecognized(2, new Point(10,10));
    }

    /**
     * Invoked when a mouse button has been released on a component.
     */

    public void mouseReleased(MouseEvent e) {
        //events.clear();
    }

    /**
     * Invoked when the mouse enters a component.
     */

    public void mouseEntered(MouseEvent e) {
        //events.clear();
    }

    /**
     * Invoked when the mouse exits a component.
     */

    public void mouseExited(MouseEvent e) {

        if (!events.isEmpty()) { // gesture pending
            int dragAction = 2;

            if (dragAction == DnDConstants.ACTION_NONE) {
                events.clear();
            }
        }
    }

    /**
     * Invoked when a mouse button is pressed on a component.
     */

    public void mouseDragged(MouseEvent e) {
        /*if (!events.isEmpty()) { // gesture pending
            int dop = mapDragOperationFromModifiers(e);

            if (dop == DnDConstants.ACTION_NONE) {
                return;
            }

            MouseEvent trigger = (MouseEvent)events.get(0);


            Point      origin  = trigger.getPoint();
            Point      current = e.getPoint();

            int        dx      = Math.abs(origin.x - current.x);
            int        dy      = Math.abs(origin.y - current.y);

            if (dx > motionThreshold || dy > motionThreshold) {
                fireDragGestureRecognized(dop, ((MouseEvent)getTriggerEvent()).getPoint());
            } else
                appendEvent(e);
        }*/
    }

    /**
     * Invoked when the mouse button has been moved on a component
     * (with no buttons no down).
     */

    public void mouseMoved(MouseEvent e) {
        // do nothing
    }
}
