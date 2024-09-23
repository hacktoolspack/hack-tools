/*****************************************************************************
   Absinthe - Front End for the Absinthe Core Library
   This software is Copyright (C) 2004 nummish, 0x90.org

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

using wx;

using System;
using System.IO;
using System.Text;
using System.Reflection;
using System.Drawing;

using Absinthe.Core;

public class AboutDialog : Dialog
{
	Button butOk;

	public AboutDialog(Window Parent, PluginTemplate[] PluginList) : base(Parent, "About Absinthe", wxDefaultPosition, new Size(425, 400), wxDEFAULT_FRAME_STYLE | wxFRAME_FLOAT_ON_PARENT)
	{
		InitializeComponent(PluginList);
	}

	private void InitializeComponent(PluginTemplate[] PluginList)
	{
		BoxSizer sizMain = new BoxSizer(Orientation.wxVERTICAL);

		/*
		Image img0x90Logo = new Image();
		Image imgAbsintheLogo = new Image();

		DC dc0x90Logo = new DC();
		DC dcAbsintheLogo = new DC();

		sizMain.Add(dc0x90Logo, 0, 0, 0);
		sizMain.Add(dcAbsintheLogo, 0, 0, 0);
		*/
		Assembly asm = Assembly.GetExecutingAssembly();

		StaticText lblTitle = new StaticText(this, 
			((AssemblyTitleAttribute)AssemblyTitleAttribute.GetCustomAttribute(asm, typeof (AssemblyTitleAttribute))).Title);
		sizMain.Add(lblTitle, 0, Alignment.wxALIGN_CENTRE | Direction.wxALL, 4);

		StaticText lblDescription = new StaticText(this,
			((AssemblyDescriptionAttribute)AssemblyDescriptionAttribute.GetCustomAttribute(asm, typeof (AssemblyDescriptionAttribute))).Description);
		sizMain.Add(lblDescription, 0, Alignment.wxALIGN_CENTRE | Direction.wxALL, 4);
		
		StaticText lblCopyright = new StaticText(this,
			((AssemblyCopyrightAttribute)AssemblyCopyrightAttribute.GetCustomAttribute(asm, typeof(AssemblyCopyrightAttribute))).Copyright);
		sizMain.Add(lblCopyright, 0, Alignment.wxALIGN_CENTRE | Direction.wxALL, 4);

		StaticText lblAuthors = new StaticText(this, "Authors: nummish, Xeron");
		sizMain.Add(lblAuthors, 0, Alignment.wxALIGN_CENTRE | Direction.wxALL, 4);

		StaticText lblLicense = new StaticText(this, "License:");
		sizMain.Add(lblLicense, 0, Direction.wxLEFT, 4);

		TextCtrl txtLicense = new TextCtrl(this, "", wxDefaultPosition, new Size(-1,100), TextCtrl.wxTE_MULTILINE);

		//Visual Studio requires the namespace to be applied to the resource name, otherwise it can't find it.
		Stream LicenseStream = asm.GetManifestResourceStream("LICENSE");
		if (LicenseStream == null) LicenseStream = asm.GetManifestResourceStream("Absinthe.LICENSE");
		StreamReader str = new StreamReader(LicenseStream); 

		txtLicense.Value = str.ReadToEnd(); 
		sizMain.Add(txtLicense, 0, Stretch.wxEXPAND | Direction.wxALL, 4);
		txtLicense.SetEditable(false);

		StaticText lblPlugins = new StaticText(this, "Plugin Information:");
		sizMain.Add(lblPlugins, 0, Direction.wxLEFT, 4);

		TextCtrl txtPluginInfo = new TextCtrl(this, "", wxDefaultPosition, new Size(-1, 100), TextCtrl.wxTE_MULTILINE);
		sizMain.Add(txtPluginInfo, 0, Stretch.wxEXPAND | Direction.wxALL, 4);
		txtPluginInfo.Value = PluginInfo(PluginList);

		Button butOk = new Button(this, "OK");
		sizMain.Add(butOk, 0, Alignment.wxALIGN_CENTRE | Direction.wxALL, 4);

		SetSizer(sizMain);
		

		EVT_BUTTON(butOk.ID, new EventListener(OK_Click));
	}

	private string PluginInfo(PluginTemplate[] PluginList)
	{
		StringBuilder retVal = new StringBuilder();

		foreach (PluginTemplate pt in PluginList)
		{
			retVal.Append(pt.PluginDisplayTargetName);
			retVal.Append(" - Author: ").Append(pt.AuthorName);
			retVal.Append(Environment.NewLine);
		}

		return retVal.ToString();
	}

	private void OK_Click(object Sender, Event evt)
	{
		this.Close();
	}
}

