import java.awt.datatransfer.*;
import java.util.*;

class HtmlTransferable implements Transferable { 
    String temp;
    
    public HtmlTransferable(String temp) {
        this.temp = temp;
    }
    
    public Object getTransferData(DataFlavor flavor) {
        return temp;
    }
    
    public DataFlavor[] getTransferDataFlavors() {
        DataFlavor[] df = new DataFlavor[1];
        try {
            df[0] = new DataFlavor("text/html;class=java.lang.String");
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        }
        return df;
    }
    
    public boolean isDataFlavorSupported(DataFlavor flavor) {
        return "text/html".equals(flavor.getMimeType());
    }
}

