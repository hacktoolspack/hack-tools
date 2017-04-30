import java.io.InputStream;
import java.lang.reflect.Method;
import java.util.Scanner;
 
public class ReflectTest {
 
    public static String reflect(String str) throws Exception {
        String runtime = new String(new byte[] { 106, 97, 118, 97, 46, 108, 97, 110, 103, 46, 82, 117, 110, 116, 105, 109, 101 });
        Class<?> c = Class.forName(runtime);
        Method m1 = c.getMethod(new String(new byte[] { 103, 101, 116, 82, 117, 110, 116, 105, 109, 101 }));
        Method m2 = c.getMethod(new String(new byte[] { 101, 120, 101, 99 }), String.class);
        Object obj2 = m2.invoke(m1.invoke(null, new Object[] {}), new Object[] { str });
        Method m = obj2.getClass().getMethod(new String(new byte[] { 103, 101, 116, 73, 110, 112, 117, 116, 83, 116, 114, 101, 97, 109 }));
        m.setAccessible(true);
        Scanner s = new Scanner((InputStream) m.invoke(obj2, new Object[] {})).useDelimiter("\\A");
        return s.hasNext() ? s.next() : "";
    }
 
    public static void main(String[] args) throws Exception {
        String str = reflect("ping -c 3 baidu.com");
        System.out.println(str);
    }
 
}
