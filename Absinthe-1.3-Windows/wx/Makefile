WX_NET = ../bin/wx.NET.dll

Absinthe.exe: AbsintheForm.cs AssemblyInfo.cs TargetPanel.cs SchemaPanel.cs DownloadPanel.cs ProxyConfigDialog.cs InjectionOptionsDialog.cs AboutDialog.cs
	mcs -g AbsintheForm.cs AssemblyInfo.cs TargetPanel.cs SchemaPanel.cs DownloadPanel.cs ProxyConfigDialog.cs InjectionOptionsDialog.cs LocalSettings.cs AboutDialog.cs -o Absinthe.exe -r:$(WX_NET),../core/Absinthe.Core.dll,System.Drawing -resource:../LICENSE

clean:
	rm -f Absinthe.exe
