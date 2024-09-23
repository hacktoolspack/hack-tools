// DCSC - TrojanForge.com

library ioX_getWebSRC;

uses Windows, Wininet;

function getWebSRC(sURL: String): String;
var
  hOpen, hURL: HINTERNET;
  dwBytesRead: DWORD;
  Buf : array[0..2048] of Char;
  htmlContent : String;
begin
  result := ''; htmlContent := '';
  hOpen := InternetOpen('TrojanForge', INTERNET_OPEN_TYPE_PRECONFIG, nil, nil, 0);
  if NOT Assigned(hOpen) then exit;
  try
    hURL := InternetOpenUrl(hOpen,
                            PChar(sURL),
                            nil,
                            0,
                            INTERNET_FLAG_RELOAD or INTERNET_SERVICE_HTTP, // Fuck off cache
                            0
                            );

    if NOT Assigned(hURL) then exit;
    try

      repeat
        ZeroMemory(@Buf, sizeof(buf));
        InternetReadFile(hURL, @Buf, SizeOf(Buf), dwBytesRead); // read 2KiB
        if dwBytesRead = 0 then break;
        htmlContent := htmlContent + Buf;
      until dwBytesRead = 0;

      // return the whole shit
      result := htmlContent;
    finally
      InternetCloseHandle(hURL);
    end;
  finally
    InternetCloseHandle(hOpen);
  end;
end;


begin
  MessageBox(0, PChar(getWebSRC('http://google.com/')), 'google.com SRC', 0);

end.