Absinthe.Core.dll: AttackVector.cs BlindSqlAttackVector.cs DataStore.cs GlobalDS.cs ParsePage.cs SqlErrorAttackVector.cs TSQL.cs httpConnect.cs PluginTemplate.cs PluginManager.cs Absinthe-core.key
	mcs -g -warn:4 -t:library -r:System.Web,System.Data /out:Absinthe.Core.dll /doc:Absinthe.Core.xml *.cs

Absinthe-core.key:
	sn -k Absinthe-core.key

clean: 
	rm -f *.dll
