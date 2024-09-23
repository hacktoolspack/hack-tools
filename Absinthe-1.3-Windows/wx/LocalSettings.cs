/*****************************************************************************
   Absinthe - The Automated Blind SQL Injection Tool
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
using System.Net;

namespace Absinthe
{
	public class LocalSettings
	{

		private const string _SettingsFile = "/Absinthe-config.xml";
		private string _SettingsFullPath;

		private Hashtable _ProxyTable = new Hashtable();
		private bool _ProxyInUse = false;

		// {{{ Constructor
		public LocalSettings()
		{
			_SettingsFullPath = System.Environment.GetFolderPath(System.Environment.SpecialFolder.LocalApplicationData) + _SettingsFile;
			LoadSettings();
		}
		// }}}
		
		// {{{ LoadSettings
		private void LoadSettings()
		{
			if (!System.IO.File.Exists(_SettingsFullPath)) return;		
		
			FileStream InputStream = null;
			
			XmlDocument xInput = new XmlDocument();
			try
			{
				InputStream = File.OpenRead(_SettingsFullPath);
				xInput.Load(new XmlTextReader(InputStream));
				XmlNode docNode = xInput.DocumentElement;

				_ProxyTable = new Hashtable();
				foreach (XmlNode n in docNode.ChildNodes)
				{
					if (n.Name.Equals("proxy")) ReadProxyXml(n);
					else if (n.Name.Equals("proxies"))
					{
						foreach (XmlNode nd in n.ChildNodes)
							if (nd.Name.Equals("proxy")) ReadProxyXml(nd);
					}
				}
			}
			catch (System.Exception e)
			{
				// Ignore any exceptions here, the file will be overwritten if necessary
			}
			finally
			{
				InputStream.Close();
			}
		}
		// }}}

		// {{{ ReadProxyXml
		private void ReadProxyXml(XmlNode n)
		{
			string ProxyAddress;
			int ProxyPort;
			
			if ((n.Attributes["address"] != null) && (n.Attributes["port"] != null))
			{
				ProxyAddress = n.Attributes["address"].InnerText;
				ProxyPort = Int32.Parse(n.Attributes["port"].InnerText);
				if (n.Attributes["active"] != null) 
				{
					if (Boolean.Parse(n.Attributes["active"].InnerText))
					{
						_ProxyInUse = true;
						_ProxyTable.Add(ProxyAddress, ProxyPort);
					}
				}
				else
				{
					_ProxyInUse = true;
					_ProxyTable.Add(ProxyAddress, ProxyPort);
				}

			}
		}
		// }}}

		// {{{ ProxyQueue Method [like a property, but with a force value]
		public Queue ProxyQueue()
		{
			return ProxyQueue(false);
		}
		
		public Queue ProxyQueue(bool RegardlessOfUse)
		{
			if (_ProxyInUse || RegardlessOfUse)
			{
				Queue ProxyQ = new Queue();

				if (_ProxyTable == null) _ProxyTable = new Hashtable();

				foreach (string HostKey in _ProxyTable.Keys)
				{
					WebProxy wp = new WebProxy(HostKey, (int) _ProxyTable[HostKey]);
					ProxyQ.Enqueue(wp);
				}
				return ProxyQ;
			}

			return null;
		}
		// }}}

		// {{{ ProxyInUse Property
		public bool ProxyInUse
		{
			get
			{
				return _ProxyInUse;
			}
			set
			{
				_ProxyInUse = value;
			}
		}
		// }}}

		// {{{ AddProxy
		public void AddProxy(string ProxyAddress, int ProxyPort)
		{
			if (_ProxyTable == null) _ProxyTable = new Hashtable();
			_ProxyTable.Add(ProxyAddress, ProxyPort);
			SaveSettings();
		}
		// }}}
		
		/*
		public void DelProxy(string ProxyAddress)
		{
			if (_ProxyTable == null) return;
			
			_ProxyTable.Remove(ProxyAddress);
			SaveSettings();
		}
		*/

		// {{{ ClearProxies
		public void ClearProxies()
		{
			if (_ProxyTable != null) _ProxyTable.Clear();
			SaveSettings();
		}
		// }}}

		// {{{ GeneratePath
		private void GeneratePath()
		{
			if (!System.IO.Directory.Exists(System.Environment.GetFolderPath(System.Environment.SpecialFolder.LocalApplicationData)))
			{
				System.IO.Directory.CreateDirectory(System.Environment.GetFolderPath(System.Environment.SpecialFolder.LocalApplicationData));
			}
		}
		// }}}

		// {{{ SaveSettings
		private void SaveSettings()
		{
			GeneratePath();

			XmlTextWriter xOutput = new XmlTextWriter(_SettingsFullPath, System.Text.Encoding.UTF8);
			xOutput.Formatting = Formatting.Indented;
			xOutput.Indentation = 4;
			xOutput.WriteStartDocument();

			xOutput.WriteStartElement("absinthe-settings");

			xOutput.WriteStartElement("proxies");
			xOutput.WriteStartAttribute("active", null);
			xOutput.WriteString(_ProxyInUse.ToString());
			xOutput.WriteEndAttribute();

			if (_ProxyTable != null && _ProxyTable.Count > 0)
			{
				foreach (string HostKey in _ProxyTable.Keys)
				{
					string ProxyAddress = HostKey;
					int ProxyPort = (int) _ProxyTable[HostKey];

					xOutput.WriteStartElement("proxy");

					xOutput.WriteStartAttribute("address", null);
					xOutput.WriteString(ProxyAddress);
					xOutput.WriteEndAttribute();

					xOutput.WriteStartAttribute("port", null);
					xOutput.WriteString(ProxyPort.ToString());
					xOutput.WriteEndAttribute();

					xOutput.WriteEndElement();
				}
			}
			xOutput.WriteEndElement();

			xOutput.WriteEndElement();
			xOutput.WriteEndDocument();
			xOutput.Close();
		}
		// }}}
	}
}
