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
using System.Net;
using System.Text;
using System.Collections;
using System.Collections.Specialized;

namespace Absinthe.Core
{

	///<summary>All data structures universal to the Core Library</summary>
	public class GlobalDS
	{
		// {{{ FormParam Data Structure
		///<summary>The details of a parameter sent along with an HTTP request</summary>
		public struct FormParam
		{
			///<summary>The name of the parameter</summary>
			public string Name;
			///<summary>The default value of the parameter</summary>
			public string DefaultValue;
			///<summary>Indicates if the parameter is a valid injection point</summary>
			public bool Injectable;

			public bool AsString;
		}
		// }}}

		// {{{ PrimaryKey Data Structure
		///<summary>A primary key structure for enumerating table data</summary>
		public struct PrimaryKey
		{
			///<summary>The name of the column the primary key is located in</summary>
			public string Name;
			///<summary>The textual value of the primary key</summary>
			public string Value;
			///<summary>The value of the primary key escaped for use in queries</summary>
			public string OutputValue;
		}
		// }}}

		// {{{ InjectionOptions Class
		public class InjectionOptions
		{
			private float _Tolerance;
			private bool _TerminateQuery;
			private bool _InjectAsString;
			private Queue _WebProxies;
			private StringDictionary _Cookies;
			private string _Delimiter;
			private int _Throttle;
			private string _AppendedQuery;
			private NetworkCredential _AuthCredentials;

			public InjectionOptions()
			{
				_Tolerance = 0.01F;
				_TerminateQuery = false;
				_WebProxies = null;
				_Cookies = null;
				_Delimiter = Environment.NewLine;
				_Throttle = 0;
				_InjectAsString = false;
				_AppendedQuery = String.Empty;
				_AuthCredentials = null;
			}

			// {{{ AppendedQuery Propery
			public string AppendedQuery
			{
				get
				{
					return _AppendedQuery;
				}
				set
				{
					_AppendedQuery = value;
					if (value.Length > 0) TerminateQuery = false;
				}
			}
			// }}}

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

			// {{{ Tolerance Property
			public float Tolerance
			{
				get
				{
					return _Tolerance;
				}

				set
				{
					if (value > 0)
					{
						_Tolerance = value;
					}
					else
					{
						_Tolerance = 0;
					}
				}
			}
			// }}}

			// {{{ TerminateQuery Property
			public bool TerminateQuery
			{
				get
				{
					return _TerminateQuery;
				}
				set
				{
					_TerminateQuery = value;
					if (value) _AppendedQuery = String.Empty;
				}
			}
			// }}}

			// {{{ WebProxies Property
			public Queue WebProxies
			{
				get
				{
					return _WebProxies;
				}
				set
				{
					if (value != null && value.Count > 0)
					{
						_WebProxies = value;
					}
					else
					{
						_WebProxies = null;
					}
				}
			}
			// }}}

			// {{{ Cookies Property
			public StringDictionary Cookies
			{
				get
				{
					return _Cookies;
				}
				set
				{
					if (value != null && value.Count > 0)
					{ 
						_Cookies = value;
					}
					else
					{
						_Cookies = null;
					}
				}
			}
			// }}}

			// {{{ Delimiter Property
			public string Delimiter
			{
				get
				{
					return _Delimiter;
				}
				set
				{
					if (value.Length == 0)
					{
						_Delimiter = Environment.NewLine;
					}
					else
					{
						_Delimiter = value;
					}
				}
			}
			// }}}

			// {{{ Throttle Property
			public int Throttle
			{
				get
				{
					return _Throttle;
				}
				set
				{
					_Throttle = value;
				}
			}
			// }}}

			// {{{ AuthCredentials Property
			public NetworkCredential AuthCredentials
			{
				get
				{
					return _AuthCredentials;
				}
				set
				{
					_AuthCredentials = value;
				}
			}
			// }}}
		}
		// }}}

		// {{{ Field Data Structure
		///<summary>A field in the database being exploited</summary>
		public struct Field
		{
			private string _FieldName;
			private System.Data.SqlDbType _DataType;
			private string _TableName; // Generally will be empty, but could be used for detached fields
			private bool _IsPrimary;

			// {{{ FieldName Property
			///<summary>The human readable name of the field</summary>
			public string FieldName
			{
				get
				{
					return _FieldName;
				}

				set
				{
					if (value.LastIndexOf('.') >= 0)
					{
						_TableName = value.Substring(0, value.LastIndexOf('.'));
						_FieldName = value.Substring(value.LastIndexOf('.') + 1);
					}
					else
					{
						_FieldName = value;
					}
				}
			}
			// }}}

			// {{{ TableName Property
			///<summary>The human readable name of the table the field is located in</summary>
			public string TableName
			{
				get 
				{
					return _TableName;
				}
			}
			// }}}

			// {{{ FullName Property
			///<summary>The name of the table and field appended together</summary>
			public string FullName
			{
				get
				{
					StringBuilder retVal = new StringBuilder();

					if (_TableName.Length > 0)
					{
						retVal.Append(_TableName).Append(".");
					}

					retVal.Append(_FieldName);

					return retVal.ToString();
				}
			}
			// }}}

			// {{{ DataType Property
			///<summary>The datatype of the field</summary>
			public System.Data.SqlDbType DataType
			{
				get
				{
					return _DataType;
				}

				set
				{
					_DataType = value;
				}
			}
			// }}}

			// {{{ IsPrimary Property
			///<summary>Indicates if this field is a primary key for this table</summary>
			public bool IsPrimary
			{
				get
				{
					return _IsPrimary;
				}
				set
				{
					_IsPrimary = value;
				}
			}
			// }}}
		}
		// }}}

		// {{{ Table Struct
		///<summary>A table in the database being exploited</summary>
		public struct Table
		{
			private string _TableName;
			private long _TableID, _RecordCount;
			private ArrayList _FieldList;

			// {{{ Name Property
			///<summary>The human readable name of the table</summary>
			public string Name
			{
				get
				{
					return _TableName;
				}
				set
				{
					_TableName = value;
				}
			}
			// }}}

			// {{{ FieldCount Property
			///<summary>The number of fields (columns) in this table</summary>
			public int FieldCount
			{
				get
				{
					if (_FieldList == null) return 0;
					return _FieldList.Count;
				}
			}
			// }}}

			// {{{ ObjectID Property
			///<summary>The database recognizable numerical ID of this table</summary>
			public long ObjectID
			{
				get
				{
					return _TableID;
				}
				set
				{
					_TableID = value;
				}
			}
			// }}}

			// {{{ AddField
			///<summary>Add a field to this table</summary>
			///<param name="Value">The field to be added to this table</param>
			public void AddField(Field Value)
			{
				if (_FieldList == null) _FieldList = new ArrayList();
				_FieldList.Add(Value);
			}
			// }}}

			// {{{ FieldList Property
			///<summary>The list of fields stored in this table</summary>
			public GlobalDS.Field[] FieldList
			{
				get
				{	
					if (_FieldList == null) return null;

					return (GlobalDS.Field[]) _FieldList.ToArray(typeof(GlobalDS.Field));
				}
			}
			// }}}

			// {{{ RecordCount Property
			///<summary>The number of data records in this table</summary>
			public long RecordCount
			{
				get
				{
					return _RecordCount;
				}

				set
				{
					_RecordCount = value;
				}
			}
			// }}}
		}
		// }}}

		// {{{ ExploitType Enum
		public enum ExploitType : byte
		{
			Undefined = 255,
			BlindTSQLInjection = 0,
			ErrorBasedTSQL = 1
		}
		// }}}

		public enum AuthType : byte
		{
			None = 0,
			Basic = 1,
			Digest = 2,
			NTLM = 3
		}

		///<summary>Used as a delegate to bubble status messages up to the user</summary>
		///<param name="TextMsg">The text message to be passed up</param>
		public delegate void OutputStatusDelegate(string TextMsg);
	}
}
