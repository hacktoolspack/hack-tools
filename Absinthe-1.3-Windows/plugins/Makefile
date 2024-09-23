all: BlindMSSQL.dll BlindORASQL.dll BlindPGSQL.dll

BlindMSSQL.dll: BlindMSSQL.cs ../core/Absinthe.Core.dll
	mcs -g -warn:4 -r:../core/Absinthe.Core.dll,System.Data -t:library /out:Absinthe.BlindMSSQL.dll BlindMSSQL.cs

BlindORASQL.dll: BlindORASQL.cs ../core/Absinthe.Core.dll
	mcs -g -warn:4 -r:../core/Absinthe.Core.dll,System.Data -t:library /out:Absinthe.BlindORASQL.dll BlindORASQL.cs

BlindPGSQL.dll: BlindPGSQL.cs ../core/Absinthe.Core.dll
	mcs -g -warn:4 -r:../core/Absinthe.Core.dll,System.Data -t:library /out:Absinthe.BlindPGSQL.dll BlindPGSQL.cs
clean:
	rm -f *.dll
