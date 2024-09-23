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
using System.Reflection;
using System.Collections;

namespace Absinthe.Core
{
	public class PluginManager
	{

		private ArrayList _Plugins = new ArrayList();

		public PluginManager()
		{
			LoadAllPlugins();
		}

		public ArrayList PluginList
		{
			get
			{
				return _Plugins;
			}
		}
		
		public PluginTemplate GetPluginByName(string PluginName)
		{
			foreach (PluginTemplate pt in _Plugins)
			{
				if (pt.PluginDisplayTargetName.Equals(PluginName)) return pt;
			}

			throw new UnsupportedPluginException("No plugin matching \""+ PluginName +"\" was found.");
		}

		private void LoadAllPlugins()
		{
			Assembly asm = Assembly.GetAssembly(this.GetType());

			string PluginPath = asm.Location.Substring(0, 1+asm.Location.LastIndexOf(System.IO.Path.DirectorySeparatorChar));
			PluginPath += "plugins" + System.IO.Path.DirectorySeparatorChar;

			if (!System.IO.Directory.Exists(PluginPath)) 
			{
				Console.WriteLine(PluginPath + " not found.");
			}

			System.IO.DirectoryInfo d411 = new System.IO.DirectoryInfo(PluginPath);
			System.IO.FileInfo[] f411 = d411.GetFiles("*.dll");

			foreach (System.IO.FileInfo fi in f411)
			{
				Assembly a = Assembly.LoadFile(PluginPath + fi.Name);
				Type type = a.GetType("AbsinthePlugin");

				if (type != null) 
				{
					Object obj = Activator.CreateInstance(type);
					PluginTemplate pt = (PluginTemplate) obj;

					_Plugins.Add(pt);
				}
			}
		}
	}
}
