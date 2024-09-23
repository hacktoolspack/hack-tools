@ECHO OFF

SET JAVA_HOME=C:\AppSecWorkbench\jdk16\jre
SET PATH=%PATH%;%JAVA_HOME%\bin

java -classpath .;lib/concurrent.jar;OWASP-CSRFTester-1.0.jar org.owasp.csrftester.CSRFTester
