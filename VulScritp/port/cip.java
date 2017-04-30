package com.port.scan;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.InputStreamReader;
import java.io.PrintWriter;

public class IP {
	public static void main(String[] args) throws Exception {
		String DbPath=System.getProperty("user.dir")+"\\ip.txt";
        String encoding="utf-8";
        File file=new File(DbPath);
        if(file.isFile() && file.exists()){ //判断文件是否存在
            InputStreamReader read = new InputStreamReader(
            new FileInputStream(file),encoding);//考虑到编码格式
            BufferedReader bufferedReader = new BufferedReader(read);
            String lineTxt = null;
            while((lineTxt = bufferedReader.readLine()) != null){
            for (int i = 1; i <=255; i++) {
                System.out.println(lineTxt+"."+i);
                writeurl(lineTxt+"."+i+"\r\n");
			}
            }
        }
		
	}
	
	 public static void writeurl(String resulturl) throws Exception{
		 String DbPath=System.getProperty("user.dir")+"\\result.txt";
    	 PrintWriter pw = new PrintWriter( new FileWriter( "result.txt",true ) );
         pw.print(resulturl);
         pw.close();
    }
}
