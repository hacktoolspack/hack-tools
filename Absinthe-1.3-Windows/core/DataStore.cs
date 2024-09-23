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
using System.IO;
using System.Xml;
using System.Collections;
using System.Collections.Specialized;

namespace Absinthe.Core
{
	public class DataStore 
	{

		private string _TargetURL = "";
		private string _ConnectionMethod = "";
		private bool _UseSSL = false;
		private Hashtable _ParamList = new Hashtable();
		private AttackVector _TargetAttackVector = null;
		private string _DatabaseVersion = "";
		private string _Username = "";
		private string _Filename = "";
		private GlobalDS.Table[] _DBTables = null;
		private StringDictionary _Cookies = null;
		private GlobalDS.OutputStatusDelegate _ParentOutput;
		private bool _TerminateQuery = false;
		private string _FilterDelimiter = Environment.NewLine;
		private int _ThrottleValue;
		private float _Tolerance = 0.01F;
		private PluginManager _Plugins;
		private bool _InjectAsString = false;

		///<summary>Sets the OutputStatusDelegate to communicate with the user</summary>
		///<param name="ParentOutput">The delegate used to bubble up messages</param>
		public DataStore(GlobalDS.OutputStatusDelegate ParentOutput)
		{
			_ParentOutput = ParentOutput;
			_Plugins = new PluginManager();
		}

		// {{{ InjectAsString Property
		public bool InjectAsString
		{
			get
			{
				return _InjectAsString;
			}
			set
			{
				_InjectAsString = value;
			}
		}
		// }}}

		// {{{ FilterTolerance Property
		public float FilterTolerance
		{
			get
			{
				return _Tolerance;
			}
			set
			{
				_Tolerance = 0;
				if (value >= 0) _Tolerance = value;
			}	
		}
		// }}}

		// {{{ TerminateQuery Property
		///<summary>
		///Indicates if a SQL statement is to be terminated with a comment
		///</summary>
		public bool TerminateQuery
		{
			get
			{
				return _TerminateQuery;
			}

			set
			{
				_TerminateQuery = value;
			}
		}
		// }}}

		// {{{ FilterDelimiter Property
		///<summary>
		///Used as the delimiter to create the linear signature
		///</summary>
		///<remarks>Defaults to Environment.NewLine</remarks>
		public string FilterDelimiter
		{
			get
			{
				return _FilterDelimiter;
			}
			set
			{
				if (value.Length == 0)
				{
					_FilterDelimiter = Environment.NewLine;
				}
				else
				{	
					_FilterDelimiter = value;
				}
			}
		}
		// }}}

		// {{{ ThrottleValue Property
		///<summary>The throttle value used to sleep (in msec) between requests</summary>
		///<remarks>If the value is negative, it is rounded to the nearest hundred 
		///which is used for multithreading (eg. -289 -> -300 -> 3 Threads)</remarks>
		public int ThrottleValue
		{
			get
			{
				return _ThrottleValue;
			}
			set
			{
				if(value < 0)
				{
					int Remainder;
					Math.DivRem(value, 100, out Remainder);
					
					if (Remainder < -50) Remainder = 100 + Remainder;

					_ThrottleValue = value - Remainder;
				}
				else
				{
					_ThrottleValue = value;
				}
			}
		}
		// }}}

		// {{{ OutputFile Property
		///<summary>
		///The filename in which to store the attack configuration
		///</summary>
		public string OutputFile
		{
			get
			{
				return _Filename;
			}

			set
			{
				_Filename = value;
			}
		}
		// }}}

		// {{{ TargetURL Property
		///<summary>
		///The URL of the attack target
		///</summary>
		public string TargetURL
		{
			get
			{
				return _TargetURL;
			}

			set
			{
				_TargetURL = value;
			}
		}
		// }}}

		// {{{ ConnectionMethod Property
		///<summary>
		///The connection method to be used. May be "GET" or "POST"
		///</summary>
		public string ConnectionMethod
		{
			get
			{
				return _ConnectionMethod;
			}

			set
			{
				if (value.ToUpper().Equals("POST") || value.ToUpper().Equals("GET"))
				{
					_ConnectionMethod = value.ToUpper();
				}
				else
				{
					_ConnectionMethod = "";
				}
			}
		}
		// }}}

		// {{{ Username Property
		///<summary>
		///The username the database connection operates as
		///</summary>
		public string Username
		{
			get
			{
				return _Username;
			}

			set
			{
				_Username = value;
			}
		}
		// }}}

		// {{{ DatabaseVersion Property
		///<summary>
		///The human readable version string from the database
		///</summary>
		public string DatabaseVersion 
		{
			get 
			{
				return _DatabaseVersion;
			}

			set
			{
				_DatabaseVersion = value;
			}
		}
		// }}}

		// {{{ AuthenticationMethod Property
		public GlobalDS.AuthType AuthenticationMethod
		{
			get
			{
				return _AuthenticationMethod;
			}
		}
		// }}}

		// {{{ AuthUser Property
		public string AuthUser
		{
			get
			{
				return _AuthUser;
			}
		}
		// }}}

		// {{{ AuthPassword Property
		public string AuthPassword
		{
			get
			{
				return _AuthPassword;
			}
		}
		// }}}

		// {{{ AuthDomain Property
		public string AuthDomain
		{
			get
			{
				return _AuthDomain;
			}
		}
		// }}}

		GlobalDS.AuthType _AuthenticationMethod = GlobalDS.AuthType.None;
		string _AuthUser;
		string _AuthPassword;
		string _AuthDomain;

		// {{{ Authdata
		public void Authdata(GlobalDS.AuthType AuthType)
		{
			_AuthUser = string.Empty;
			_AuthPassword = string.Empty;
			_AuthDomain = string.Empty;
			_AuthenticationMethod = GlobalDS.AuthType.None;
			if (AuthType != GlobalDS.AuthType.None)
			{ throw new Exception("Missing Information, AuthType set to 'None'"); }
			return;
		}

		public void Authdata(GlobalDS.AuthType AuthType, string Username, string Password)
		{
			_AuthUser = Username;
			_AuthPassword = Password;
			_AuthDomain = string.Empty;

			if (AuthType == GlobalDS.AuthType.None)
			{
				Authdata(AuthType); return;
			}

			_AuthenticationMethod = AuthType;

			if (AuthType == GlobalDS.AuthType.NTLM)
			{
				_AuthenticationMethod = GlobalDS.AuthType.Basic;
				throw new Exception("Missing Domain information, AuthType set to 'Basic'");
			}

		}

		public void Authdata(GlobalDS.AuthType AuthType, string Username, string Password, string Domain)
		{
			_AuthUser = Username;
			_AuthPassword = Password;
			_AuthDomain = Domain;

			if (AuthType == GlobalDS.AuthType.None)
			{
				Authdata(AuthType); return;
			}

			_AuthenticationMethod = AuthType;

			if (AuthType != GlobalDS.AuthType.NTLM)
				_AuthDomain = string.Empty;
		
		}
		// }}}

		// {{{ AddFormParameter
		///<summary>
		///Adds a form parameter for use during the attack
		///</summary>
		///<param name="value">The FormParam object containing the relevant parameter information</param>
		public void AddFormParameter(GlobalDS.FormParam value)
		{
			//_ParentOutput("There are {0} keys in the Parameter list!", _ParamList.Count);
			_ParamList[value.Name] =  value;
		}
		// }}}

		// {{{ Cookies Property
		///<summary>
		///The list of all the key/value pairs to be treated as cookies
		///</summary>
		public StringDictionary Cookies
		{
			get 
			{
				return _Cookies;
			}
			set
			{
				_Cookies = value;
			}
		}
		// }}}

		// {{{ ParameterTable Property
		///<summary>
		///A hashtable of the form parameters, keyed by the parameter name
		///</summary>
		public Hashtable ParameterTable
		{
			get
			{
				return _ParamList;
			}
		}
		// }}}

		// {{{ TargetAttackVector Property
		///<summary>
		///The AttackVector used against the target
		///</summary>
		public AttackVector TargetAttackVector
		{
			get
			{
				return _TargetAttackVector;
			}
			set
			{
				_TargetAttackVector = value;
			}
		}
		// }}}

		// {{{ TableList Property
		///<summary>
		///A list of all the tables recovered from the database
		///</summary>
		public Absinthe.Core.GlobalDS.Table[] TableList
		{
			get
			{
				return _DBTables;
			}
			set
			{
				_DBTables = value;
			}
		}
		// }}}

		// {{{ LoadedPluginName Property
		public string LoadedPluginName
		{
			get
			{
				return _LoadedPluginName;
			}
		}
		// }}}

		// {{{ PluginList Property
		public ArrayList PluginList
		{
			get
			{
				return _Plugins.PluginList;
			}
		}
		// }}}

		// {{{ GetTableFromName
		///<summary>
		///Used as a name based lookup for a table
		///</summary>
		///<param name="TableName">The human readable name of the table</param>
		///<returns>The table structure associated with the given name</returns>
		public GlobalDS.Table GetTableFromName(string TableName)
		{
			foreach(GlobalDS.Table tbl in _DBTables)
			{
				if (tbl.Name.Equals(TableName)) return tbl;
			}

			return new GlobalDS.Table();
		}
		// }}}

		// {{{ OutputToFile
		///<summary>
		///Save all known data to a file
		///</summary>
		public void OutputToFile(string PluginName)
		{

			// TODO: Define this exception better
			if (_Filename.Length == 0) throw new System.Exception(" No File Defined fucker ");

			XmlTextWriter xOutput = new XmlTextWriter(_Filename, System.Text.Encoding.UTF8);
			xOutput.Formatting = Formatting.Indented;
			xOutput.Indentation = 4;
			xOutput.WriteStartDocument();

			xOutput.WriteStartElement("Absinthedata");
			xOutput.WriteStartAttribute("version", null);
			xOutput.WriteString("1.0");
			xOutput.WriteEndAttribute();

			WriteTargetInfo(ref xOutput, PluginName);
			WriteAttackVector(ref xOutput);

			WriteDatabaseSchema(ref xOutput);

			xOutput.WriteEndElement();
			xOutput.WriteEndDocument();
			xOutput.Close();
		}
		// }}}

		// {{{ WriteDatabaseSchema
		private void WriteDatabaseSchema(ref XmlTextWriter xOutput)
		{
			if (_Username.Length > 0 || (_DBTables != null && _DBTables.Length > 0))
			{
				xOutput.WriteStartElement("DatabaseSchema");

				if (_Username.Length > 0)
				{
					xOutput.WriteStartAttribute("username", null);
					xOutput.WriteString(_Username);
					xOutput.WriteEndAttribute();
				}

				if (_DBTables != null && _DBTables.Length > 0) WriteTablesToXml(ref xOutput);

				xOutput.WriteEndElement();
			}
		}
		// }}}

		// {{{ WriteTablesToXml
		private void WriteTablesToXml(ref XmlTextWriter xOutput)
		{

			for (int i = 0; i < _DBTables.Length; i++)
			{
				xOutput.WriteStartElement("table");	

				xOutput.WriteStartAttribute("id", null);
				xOutput.WriteString(_DBTables[i].ObjectID.ToString());
				xOutput.WriteEndAttribute();

				xOutput.WriteStartAttribute("name", null);
				xOutput.WriteString(_DBTables[i].Name);
				xOutput.WriteEndAttribute();

				xOutput.WriteStartAttribute("recordcount", null);
				xOutput.WriteString(_DBTables[i].RecordCount.ToString());
				xOutput.WriteEndAttribute();

				if (_DBTables[i].FieldCount > 0) WriteFieldToXml(ref xOutput, _DBTables[i]);	

				xOutput.WriteEndElement();
			}
		}
		// }}}

		// {{{ WriteFieldToXml
		private void WriteFieldToXml(ref XmlTextWriter xOutput, GlobalDS.Table Tbl)
		{
			for (int i = 0; i < Tbl.FieldCount; i++)
			{
				xOutput.WriteStartElement("field");

				xOutput.WriteStartAttribute("id", null);
				xOutput.WriteString((i+1).ToString());
				xOutput.WriteEndAttribute();

				xOutput.WriteStartAttribute("name", null);
				xOutput.WriteString(Tbl.FieldList[i].FieldName);
				xOutput.WriteEndAttribute();

				xOutput.WriteStartAttribute("datatype", null);
				xOutput.WriteString(Tbl.FieldList[i].DataType.ToString());
				xOutput.WriteEndAttribute();

				if (Tbl.FieldList[i].IsPrimary)
				{
					xOutput.WriteStartAttribute("primary", null);
					xOutput.WriteString(true.ToString());
					xOutput.WriteEndAttribute();
				}
				
				xOutput.WriteEndElement();
			}
		}
		// }}}

		// {{{ WriteAttackVector
		private void WriteAttackVector(ref XmlTextWriter xOutput)
		{
			if (_TargetAttackVector != null)
			{
				_TargetAttackVector.ToXml(ref xOutput);
			}
		}
		// }}}

		// {{{ WriteTargetInfo
		private void WriteTargetInfo(ref XmlTextWriter xOutput, string PluginName)
		{
			if (_TargetURL.Length > 0 )
			{
				xOutput.WriteStartElement("target");

				xOutput.WriteStartAttribute("address", null);
				xOutput.WriteString(_TargetURL);
				xOutput.WriteEndAttribute();

				if (_ConnectionMethod.ToUpper().Equals("POST") || _ConnectionMethod.ToUpper().Equals("GET"))
				{
					xOutput.WriteStartAttribute("method", null);
					xOutput.WriteString(_ConnectionMethod.ToUpper());
					xOutput.WriteEndAttribute();
				}

				xOutput.WriteStartAttribute("ssl", null);
				xOutput.WriteString(_UseSSL.ToString());
				xOutput.WriteEndAttribute();

				xOutput.WriteStartAttribute("TerminateQuery", null);
				xOutput.WriteString(_TerminateQuery.ToString());
				xOutput.WriteEndAttribute();

				xOutput.WriteStartAttribute("Throttle", null);
				xOutput.WriteString(_ThrottleValue.ToString());
				xOutput.WriteEndAttribute();
				
				xOutput.WriteStartAttribute("Delimiter", null);
				xOutput.WriteString(_FilterDelimiter.ToString());				
				xOutput.WriteEndAttribute();                   

				xOutput.WriteStartAttribute("tolerance", null);
				xOutput.WriteString(_Tolerance.ToString());
				xOutput.WriteEndAttribute();                   

				xOutput.WriteStartAttribute("PluginName", null);
				xOutput.WriteString(PluginName);
				xOutput.WriteEndAttribute();

				WriteAuthenticationData(ref xOutput);
				WriteTargetParameters(ref xOutput);
				WriteCookieData(ref xOutput);

				xOutput.WriteEndElement();
			}
		}
		// }}}

		// {{{ WriteAuthenticationData
		private void WriteAuthenticationData(ref XmlTextWriter xOutput)
		{
			xOutput.WriteStartElement("authentication");
			
			xOutput.WriteStartAttribute("authtype", null);
			xOutput.WriteString(_AuthenticationMethod.ToString());
			xOutput.WriteEndAttribute();

			if (_AuthenticationMethod != GlobalDS.AuthType.None)
			{
				xOutput.WriteStartElement("username");
				xOutput.WriteStartAttribute("value", null);
				xOutput.WriteString(_AuthUser);
				xOutput.WriteEndAttribute();
				xOutput.WriteEndElement();

				xOutput.WriteStartElement("password");
				xOutput.WriteStartAttribute("value", null);
				xOutput.WriteString(_AuthPassword);
				xOutput.WriteEndAttribute();
				xOutput.WriteEndElement();

				if (_AuthenticationMethod == GlobalDS.AuthType.NTLM)
				{
					xOutput.WriteStartElement("domain");
					xOutput.WriteStartAttribute("value", null);
					xOutput.WriteString(_AuthDomain);
					xOutput.WriteEndAttribute();
					xOutput.WriteEndElement();
				}
			}
			xOutput.WriteEndElement();
		}
		// }}}

		// {{{ WriteTargetParameters
		private void WriteTargetParameters(ref XmlTextWriter xOutput)
		{
			foreach (object xp in _ParamList)
			{
				if (((DictionaryEntry) xp).Value.GetType() == typeof(GlobalDS.FormParam))
				{
					GlobalDS.FormParam fp= (GlobalDS.FormParam)((DictionaryEntry) xp).Value;
					xOutput.WriteStartElement("parameter");

					xOutput.WriteStartAttribute("name", null);
					xOutput.WriteString(fp.Name);
					xOutput.WriteEndAttribute();

					xOutput.WriteStartAttribute("value", null);
					xOutput.WriteString(fp.DefaultValue);
					xOutput.WriteEndAttribute();

					xOutput.WriteStartAttribute("injectable", null);
					xOutput.WriteString(fp.Injectable.ToString());
					xOutput.WriteEndAttribute();

					if (fp.AsString)
					{
						xOutput.WriteStartAttribute("string", null);
						xOutput.WriteString(fp.AsString.ToString());
						xOutput.WriteEndAttribute();
					}

					xOutput.WriteEndElement();
				}
				else
				{
					//_ParentOutput("Wtf?! We got a {0} down here!", ((DictionaryEntry)xp).Value.GetType().ToString());
				}
			}


		}
		// }}}

		// {{{ WriteCookieData
		private void WriteCookieData(ref XmlTextWriter xOutput)
		{
			if (_Cookies != null)
			{
				foreach (string CookieName in _Cookies.Keys)
				{
					xOutput.WriteStartElement("cookie");

					xOutput.WriteStartAttribute("name", null);
					xOutput.WriteString(CookieName);
					xOutput.WriteEndAttribute();

					xOutput.WriteStartAttribute("value", null);
					xOutput.WriteString(_Cookies[CookieName]);
					xOutput.WriteEndAttribute();

					xOutput.WriteEndElement();
				}
			}
		}
		// }}}

		private string _LoadedPluginName;

		// {{{ LoadXmlFile
		///<summary>Loads saved target information from an XML file</summary>
		///<param name="Filename">The name of the file to read information from</param>
		///<param name="ParentOutput">The OutputStatusDelegate used to feed information up to the user</param>
		///<param name="AnonProxies">The proxies to be using when the data is initialized</param>
		public void LoadXmlFile(string Filename, GlobalDS.OutputStatusDelegate ParentOutput, Queue AnonProxies)
		{
			FileStream InputStream = null;
			XmlDocument xInput = new XmlDocument();
			try
			{
				InputStream = File.OpenRead(Filename);
				xInput.Load(new XmlTextReader(InputStream));

				XmlNode docNode = xInput.DocumentElement;

				foreach (XmlNode n in docNode.ChildNodes)
				{
					switch (n.Name)
					{
						case "target": // Load General Target information
							DeserializeTargetXml(n);
							break;
						case "attackvector": // Initialize Attack Vector
							string FullUrl;
							if (!_UseSSL) FullUrl = "http://" + _TargetURL;
							else FullUrl = "https://" + _TargetURL;

							GlobalDS.InjectionOptions opts = new GlobalDS.InjectionOptions();
							opts.Delimiter = _FilterDelimiter;
							opts.Tolerance = _Tolerance;
							opts.TerminateQuery = _TerminateQuery;
							opts.WebProxies = AnonProxies;
							opts.Throttle = _ThrottleValue;
							AttackVectorFactory avf = new AttackVectorFactory(FullUrl, "", "", _ParamList, _ConnectionMethod, ParentOutput, opts);
							_TargetAttackVector = avf.BuildFromXml(n, opts, _Plugins);
							break;
						case "DatabaseSchema":
							DeserializeSchemaXml(n);
							break;	
						default:
							break;
					}
				}
				OutputFile = Filename;
			}
			catch (System.Xml.XmlException xe)
			{
				throw new InvalidDataFileException(Filename);
			}
			finally
			{
				InputStream.Close();
			}
		}
		// }}}

		// {{{ InvalidDataFileException Class
		///<summary>
		///An exception generated when the data file is malformed
		///</summary>
		public class InvalidDataFileException : System.Xml.XmlException
		{
			private string _Filename;
			public InvalidDataFileException(string Filename)
			{
				_Filename = Filename;
			}

			public new string Message()
			{
				return "The file: \"" + _Filename + "\" is not a valid Absinthe data file.";
			}

		}
		// }}}

		// {{{ DeserializeTargetXml
		private void DeserializeTargetXml(XmlNode TargetNode)
		{
			// Init member vars
			_TargetURL = ""; _ConnectionMethod = ""; _UseSSL = false;

			if (TargetNode.Attributes["address"] != null)
			{
				_TargetURL = TargetNode.Attributes["address"].InnerText;
			}

			if (TargetNode.Attributes["method"] != null)
			{
				_ConnectionMethod = TargetNode.Attributes["method"].InnerText.ToUpper();
				if (!_ConnectionMethod.ToUpper().Equals("POST") && !_ConnectionMethod.ToUpper().Equals("GET"))
				{
					_ConnectionMethod = "";
				}
			}

			if (TargetNode.Attributes["ssl"] != null)
			{
				_UseSSL = System.Boolean.Parse(TargetNode.Attributes["ssl"].InnerText);
			}

			if (TargetNode.Attributes["TerminateQuery"] != null)
			{
				_TerminateQuery = System.Boolean.Parse(TargetNode.Attributes["TerminateQuery"].InnerText);
			}

			if (TargetNode.Attributes["Throttle"] != null)
			{
				_ThrottleValue = Int32.Parse(TargetNode.Attributes["Throttle"].InnerText);
			}

			if (TargetNode.Attributes["PluginName"] != null)
			{
				_LoadedPluginName = TargetNode.Attributes["PluginName"].InnerText;
			}

			if (TargetNode.Attributes["tolerance"] != null)
			{
				FilterTolerance = (float) Convert.ToDouble(TargetNode.Attributes["tolerance"].InnerText);
			}

			if (TargetNode.Attributes["Delimiter"] != null)
			{
				FilterDelimiter = TargetNode.Attributes["Delimiter"].InnerText;
			}

			ExtractParametersFromXml(ref TargetNode);
			ExtractCookiesFromXml(ref TargetNode);
			ExtractAuthenticationDataFromXml(ref TargetNode);

		}
		// }}}

		// {{{ ExtractAuthenticationDataFromXml
		private void ExtractAuthenticationDataFromXml(ref XmlNode TargetNode)
		{
			XmlNode AuthDataNode = TargetNode.SelectSingleNode("authentication");

			if (AuthDataNode == null || AuthDataNode.Attributes["authtype"] == null || !System.Enum.IsDefined(typeof(GlobalDS.AuthType), AuthDataNode.Attributes["authtype"].InnerText)) // Older Data file
			{	
				_AuthenticationMethod = GlobalDS.AuthType.None;
				_AuthUser = string.Empty;
				_AuthPassword = string.Empty;
				_AuthDomain = string.Empty;
				return;
			}

			_AuthenticationMethod = (GlobalDS.AuthType) System.Enum.Parse(typeof(GlobalDS.AuthType), AuthDataNode.Attributes["authtype"].InnerText);
			
			XmlNode tmpnode = AuthDataNode.SelectSingleNode("username");
			if (tmpnode == null || tmpnode.Attributes["value"] == null)
				_AuthUser = string.Empty;
			else
				_AuthUser = tmpnode.Attributes["value"].InnerText;

			tmpnode = AuthDataNode.SelectSingleNode("password");
			if (tmpnode == null || tmpnode.Attributes["value"] == null)
				_AuthPassword = string.Empty;
			else
				_AuthPassword = tmpnode.Attributes["value"].InnerText;

			tmpnode = AuthDataNode.SelectSingleNode("domain");
			if (tmpnode == null || tmpnode.Attributes["value"] == null)
				_AuthDomain = string.Empty;
			else
				_AuthDomain = tmpnode.Attributes["value"].InnerText;
			
			return;
		}
		// }}}

		// {{{ ExtractParametersFromXml
		private void ExtractParametersFromXml(ref XmlNode TargetNode)
		{
			XmlNodeList Parameters = TargetNode.SelectNodes("parameter");

			if (Parameters.Count > 0)
			{
				_ParamList.Clear();

				foreach (XmlNode param in Parameters)
				{
					GlobalDS.FormParam NewParam = new GlobalDS.FormParam();

					if (param.Attributes["name"] != null)
					{
						NewParam.Name = param.Attributes["name"].InnerText;
					}

					if (param.Attributes["value"] != null)
					{
						NewParam.DefaultValue = param.Attributes["value"].InnerText;
					}

					if (param.Attributes["injectable"] != null)
					{
						NewParam.Injectable = System.Boolean.Parse(param.Attributes["injectable"].InnerText);

						if (param.Attributes["string"] != null)
						{
							NewParam.AsString = System.Boolean.Parse(param.Attributes["string"].InnerText);
						}
					}

					_ParamList.Add(NewParam.Name, NewParam);
				}
			}

		}
		// }}}

		// {{{ ExtractCookiesFromXml
		private void ExtractCookiesFromXml(ref XmlNode TargetNode)
		{
			XmlNodeList CookieElements = TargetNode.SelectNodes("cookie");

			_Cookies = new StringDictionary();

			if (CookieElements.Count > 0)
			{
				foreach (XmlNode cookie in CookieElements)
				{
					string CookieName, CookieValue;

					if (cookie.Attributes["name"] != null)
					{
						CookieName = cookie.Attributes["name"].InnerText;

						if (cookie.Attributes["value"] != null)
						{
							CookieValue = cookie.Attributes["value"].InnerText;
							_Cookies[CookieName] = CookieValue;
						}
					}
				}
			}
		}
		// }}}

		// {{{ DeserializeSchemaXml
		private void DeserializeSchemaXml(XmlNode TargetNode)
		{

			// Init member vars
			_Username = "";

			if (TargetNode.Attributes["username"] != null)
			{
				_Username = TargetNode.Attributes["username"].InnerText;
			}

			XmlNodeList Tables = TargetNode.SelectNodes("table");

			if (Tables.Count > 0)
			{
				ArrayList TableList = new ArrayList();
				// _DBTables.Clear();	This is an array.. use an arraylist

				foreach (XmlNode ExtractedTable in Tables)
				{
					GlobalDS.Table ThisTable = new GlobalDS.Table();

					if (ExtractedTable.Attributes["name"] != null && ExtractedTable.Attributes["id"] != null)
					{
						ThisTable.Name = ExtractedTable.Attributes["name"].InnerText;
						ThisTable.ObjectID = System.Int32.Parse(ExtractedTable.Attributes["id"].InnerText);
						
						if (ExtractedTable.Attributes["recordcount"] != null)
						{
							ThisTable.RecordCount = System.Int64.Parse(ExtractedTable.Attributes["recordcount"].InnerText);
						}

						XmlNodeList Fields = ExtractedTable.SelectNodes("field");
						foreach (XmlNode ExtractedField in Fields)
						{
							GlobalDS.Field ThisField = new GlobalDS.Field();
							
							if (ExtractedField.Attributes["name"] != null)
							{
								ThisField.FieldName = ExtractedField.Attributes["name"].InnerText;
							}
							
							if (ExtractedField.Attributes["datatype"] != null)
							{
								ThisField.DataType = (System.Data.SqlDbType) System.Enum.Parse(typeof(System.Data.SqlDbType),ExtractedField.Attributes["datatype"].InnerText);
							}
							
							if (ExtractedField.Attributes["primary"] != null)
							{
								try
								{
									ThisField.IsPrimary = bool.Parse(ExtractedField.Attributes["primary"].InnerText);
								}
								catch (System.FormatException sfe)
								{
									ThisField.IsPrimary = false;
								}
							}

							ThisTable.AddField(ThisField);
						}
						
						TableList.Add(ThisTable);
					}
				}
				_DBTables = (GlobalDS.Table[]) TableList.ToArray(typeof(GlobalDS.Table));
			}

		}
		// }}}

	}
}
