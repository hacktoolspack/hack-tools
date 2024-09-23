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
using System.Collections;
using System.Collections.Specialized;

namespace Absinthe.Core
{
	// {{{ AttackVector Class
	///<summary>
	///The general interface denoting the style of injection taking place
	///</summary>
	public interface AttackVector
	{
		GlobalDS.ExploitType ExploitType {get;}
		Queue Proxies {set;}

		void ToXml(ref XmlTextWriter xOutput);
		string GetDatabaseUsername();
		GlobalDS.Table[] GetTableList();
		void PopulateTableStructure(ref Absinthe.Core.GlobalDS.Table TableData);
		void PullDataFromTable(GlobalDS.Table[] SrcTable, long[][] ColumnIDLists, string xmlFilename);
	}
	// }}}

	// {{{ AttackVectorFactory
	///<summary>
	///Used as a factory class to generate an attack vector object
	///</summary>
	public class AttackVectorFactory
	{
		private string _Method;
		private string _TargetURL;
		private string _VectorName;
		private string _VectorBuffer;
		private StringDictionary _AttackParams;
		//private StringDictionary _Cookies;
		//private WebProxy _Proxy;
		//private Queue _Proxies;
		//private bool _TerminateQuery;
		private GlobalDS.InjectionOptions _Options;
		private GlobalDS.OutputStatusDelegate _ParentOutput;

		// {{{ Constructors
		///<summary>
		///Public Constructor for instantiation
		///</summary>
		///<param name="URL">The URL of the attack target</param>
		///<param name="VectorName">The name of the injectable parameter</param>
		///<param name="VectorBuffer">The default value of the injectable parameter</param>
		///<param name="AdditionalParams">Any additional parameters to be sent but not used as part of the injection</param>
		///<param name="Method">The form action method to use during the injection</param>
		///<param name="ParentOutput">The OutputStatusDelegate used to bubble messages up to the user</param>
		///<param name="Options">The InjectionOptions to be used during the attack</param>
		public AttackVectorFactory(string URL, string VectorName, string VectorBuffer, StringDictionary AdditionalParams, string Method, 
				GlobalDS.OutputStatusDelegate ParentOutput, GlobalDS.InjectionOptions Options)
		{
			//_Cookies = Options.Cookies;
			//_Proxies = Options.WebProxies;
			_Options = Options;
			_ParentOutput = ParentOutput;
			Initialize(URL, VectorName, VectorBuffer, AdditionalParams, Method, Options.TerminateQuery);
		}

		///<summary>
		///Public Constructor for instantiation
		///</summary>
		///<param name="URL">The URL of the attack target</param>
		///<param name="VectorName">The name of the injectable parameter</param>
		///<param name="VectorBuffer">The default value of the injectable parameter</param>
		///<param name="FormParams">Any additional parameters to be sent but not used as part of the injection</param>
		///<param name="Method">The form action method to use during the injection</param>
		///<param name="ParentOutput">The OutputStatusDelegate used to bubble messages up to the user</param>
		///<param name="Options">The InjectionOptions to be used during the attack</param>
		public AttackVectorFactory(string URL, string VectorName, string VectorBuffer, Hashtable FormParams, string Method,
				GlobalDS.OutputStatusDelegate ParentOutput, GlobalDS.InjectionOptions Options)
		{
			StringDictionary AdditionalParams = PrepAdditionalParams(FormParams);
			_ParentOutput = ParentOutput;
			//_Proxies = Options.WebProxies;
			//_Cookies = Options.Cookies;
			_Options = Options;
			Initialize(URL, VectorName, VectorBuffer, AdditionalParams, Method, Options.TerminateQuery);
		}

		private StringDictionary PrepAdditionalParams(Hashtable FormParams)
		{
			StringDictionary retVal = new StringDictionary();

			foreach (object Key in FormParams.Keys)
			{
				GlobalDS.FormParam Param = (GlobalDS.FormParam) FormParams[Key];
				retVal.Add(Param.Name, Param.DefaultValue);	
			}
			return retVal;
		}
		// }}}

		// {{{ Initialize
		private void Initialize(string URL, string VectorName, string VectorBuffer, StringDictionary AdditionalParams, string Method, bool TerminateQuery)
		{
			_Method = Method.ToUpper();
			_TargetURL = URL;
			_VectorName = VectorName;
			_VectorBuffer = VectorBuffer;
			_AttackParams = AdditionalParams;
//			_TerminateQuery = TerminateQuery;
		}
		// }}}

#if FULL_RELEASE
		// {{{ BuildSqlErrorAttackVector
		public SqlErrorAttackVector BuildSqlErrorAttackVector()
		{
			if (_Proxy != null)
			{
				return new SqlErrorAttackVector(_TargetURL, _VectorName, _VectorBuffer, _AttackParams, _Method, _ParentOutput, _Proxy);
			}
			return new SqlErrorAttackVector(_TargetURL, _VectorName, _VectorBuffer, _AttackParams, _Method, _ParentOutput);
		}
		// }}}
#endif

		// {{{ BuildBlindSqlAttackVector
		///<summary>
		///Creates a BlindSqlAttackVector object
		///</summary>
		///<param name="Tolerance">The percentage tolerance band to use for comparing signatures</param>
		///<param name="PluginUsed">The plugin being used for this injection</param>
		///<returns>An initialized BlindSqlAttackVector</returns>
		public BlindSqlAttackVector BuildBlindSqlAttackVector(float Tolerance, PluginTemplate PluginUsed)
		{
			_Options.Tolerance = Tolerance;
			return new BlindSqlAttackVector(_TargetURL, _VectorName, _VectorBuffer, _AttackParams, _Method, PluginUsed, _ParentOutput, _Options);
		}
		// }}}

		// {{{ BuildFromXml
		///<summary>
		///Rebuilds an AttackVector from it's saved XML format
		///</summary>
		///<param name="VectorNode">The root node of the Attack Vector information</param>
		///<returns>An initialized AttackVector</returns>
		public AttackVector BuildFromXml(XmlNode VectorNode, GlobalDS.InjectionOptions opts, PluginManager PlM)
		{
			string VectorType;
			if (VectorNode.Attributes["type"] != null)
			{
				VectorType = VectorNode.Attributes["type"].InnerText;
				if (!System.Enum.IsDefined(typeof(GlobalDS.ExploitType), VectorType)) VectorType = GlobalDS.ExploitType.Undefined.ToString();
				
				opts.Cookies = _Options.Cookies;
				opts.WebProxies = _Options.WebProxies;

				//if (VectorNode.Attributes["TerminateQuery"] != null) opts.TerminateQuery = System.Boolean.Parse(VectorNode.Attributes["TerminateQuery"].InnerText);
				if (VectorNode.Attributes["PostBuffer"] != null)  opts.AppendedQuery = VectorNode.Attributes["PostBuffer"].InnerText;
				//if (VectorNode.Attributes["Throttle"] != null) opts.Throttle = Int32.Parse(VectorNode.Attributes["Throttle"].InnerText);
				if (VectorNode.Attributes["Delimiter"] != null) opts.Delimiter = VectorNode.Attributes["Delimiter"].InnerText;


				switch((GlobalDS.ExploitType) System.Enum.Parse(typeof(GlobalDS.ExploitType), VectorType))
				{
#if FULL_RELEASE
					case GlobalDS.ExploitType.ErrorBasedTSQL:
						//_ParentOutput("Deserializing Sql Error");
						return DeserializeSqlErrorAttackVectorXml(VectorNode);
#endif
					case GlobalDS.ExploitType.BlindTSQLInjection:
						//_ParentOutput("Deserializing Blind.. ");
						return DeserializeBlindTSqlAttackVectorXml(VectorNode, opts, PlM);
					default:
						// During Dev I'll use Blind MS Sql
						return DeserializeBlindTSqlAttackVectorXml(VectorNode, opts, PlM);
				}
			}

			return null;
		}
		// }}}

		// {{{ DeserializeBlindTSqlAttackVectorXml
		private BlindSqlAttackVector DeserializeBlindTSqlAttackVectorXml(XmlNode VectorNode, GlobalDS.InjectionOptions opts, PluginManager PlM)
		{
			double[] TrueSig = null, FalseSig = null;
			int[] TrueFilter = null, FalseFilter = null;

			foreach (XmlNode n in VectorNode.ChildNodes)
			{
				switch (n.Name)
				{
					case "truepage":
						//_ParentOutput("Deserializing True signature.. ");
						TrueSig = ExtractSignatureFromXml(n);
						break;
					case "falsepage":
						//_ParentOutput("Deserializing False signature.. ");
						FalseSig = ExtractSignatureFromXml(n);
						break;
					case "truefilter":
						//_ParentOutput("Deserializing True Filter.. ");
						TrueFilter = ExtractFilterFromXml(n);
						break;
					case "falsefilter":
						//_ParentOutput("Deserializing False filter.. ");
						FalseFilter = ExtractFilterFromXml(n);
						break;
				}
			}

			if (TrueSig == null || FalseSig == null || TrueFilter == null || FalseFilter == null) return null;
			
			string Name = String.Empty;
			string Buffer = String.Empty;

			if (VectorNode.Attributes["tolerance"] != null) opts.Tolerance = System.Single.Parse(VectorNode.Attributes["tolerance"].InnerText);
			if (VectorNode.Attributes["name"] != null){Name = VectorNode.Attributes["name"].InnerText;}
			if (VectorNode.Attributes["buffer"] != null){Buffer = VectorNode.Attributes["buffer"].InnerText;}
			if (VectorNode.Attributes["InjectAsString"] != null)  opts.InjectAsString = System.Boolean.Parse(VectorNode.Attributes["InjectAsString"].InnerText);

			PluginTemplate DBPlugin = ChoosePluginFromXml(VectorNode, PlM);	
			_ParentOutput("Read the buffer: [" + Buffer + "] from xml");

			return new BlindSqlAttackVector(_TargetURL, Name, Buffer, _AttackParams, _Method, DBPlugin, _ParentOutput, TrueSig, FalseSig, TrueFilter, FalseFilter, opts);
		}
		// }}}

		private PluginTemplate ChoosePluginFromXml(XmlNode VectorNode, PluginManager PlM)
		{
			/* Choose plugin of best fit */
			string PluginName = null;
			if (VectorNode.Attributes["PluginName"] != null)
			{
				PluginName = VectorNode.Attributes["PluginName"].InnerText;
			}
			else
			{
				throw new UnsupportedPluginException("No plugin listed for this data file");
			}

			return PlM.GetPluginByName(PluginName);
		}

		// {{{ ExtractFilterFromXml
		private int[] ExtractFilterFromXml(XmlNode FilterNode)
		{
			ArrayList RetVal = new ArrayList();
			
			XmlNodeList FilterElements = FilterNode.SelectNodes("filter-item");	

			if (FilterElements.Count > 0)
			{
				foreach (XmlNode ele in FilterElements)
				{
					RetVal.Add(System.Int32.Parse(ele.InnerText));
				}
			}
			return (int[]) RetVal.ToArray(typeof(int));
		}
		// }}}

		// {{{ ExtractSignatureFromXml
		private double[] ExtractSignatureFromXml(XmlNode SigNode)
		{
			ArrayList RetVal = new ArrayList();

			XmlNodeList SignatureElements = SigNode.SelectNodes("signature-item");
			
			if (SignatureElements.Count > 0)
			{
				foreach (XmlNode ele in SignatureElements)
				{
					RetVal.Add(System.Double.Parse(ele.InnerText));
				}
			}

			return (double[]) RetVal.ToArray(typeof(double));
		}
		// }}}

#if FULL_RELEASE
		// {{{ DeserializeSqlErrorAttackVectorXml
		private SqlErrorAttackVector DeserializeSqlErrorAttackVectorXml(XmlNode VectorNode)
		{
			ArrayList ElementList = new ArrayList();

			XmlNodeList AttackElements = VectorNode.SelectNodes("entry");

			if (AttackElements.Count > 0)
			{
				foreach (XmlNode ele in AttackElements)
				{
					GlobalDS.Field NewField = new GlobalDS.Field();
					string fieldname = "";

					if (ele.Attributes["field"] != null)
					{
						fieldname = ele.Attributes["field"].InnerText;
						if (ele.Attributes["table"] != null)
						{
							fieldname += ele.Attributes["table"].InnerText;
						}

						NewField.FieldName = fieldname;
					}

					if (ele.Attributes["datatype"] != null)
					{
						NewField.DataType = (SqlDbType) System.Enum.Parse(typeof(SqlDbType), ele.Attributes["datatype"].InnerText);
					}

					ElementList.Add(NewField);

				}
			}

			string Name = "";
			string Buffer = "";

			if (VectorNode.Attributes["name"] != null){Name = VectorNode.Attributes["name"].InnerText;}
			if (VectorNode.Attributes["buffer"] != null){Buffer = VectorNode.Attributes["buffer"].InnerText;}

			return new SqlErrorAttackVector(_TargetURL, _Method, ElementList, Name, Buffer, _AttackParams);
		}
		// }}}
#endif 

	}
	// }}}

}
