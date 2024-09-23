/*****************************************************************************
   Absinthe - Front End for the Absinthe Core Library
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
using System.Collections;
using System.Collections.Specialized;

using wx;
using Absinthe.Core;

public class TargetPanel : Panel
{
	private DataStore _SaveInfo;
	private string[] _PluginEntries;

	AbsintheForm.GuiControls _GuiActions;
	Absinthe.LocalSettings _AppSettings;

	private delegate void ThreadedSub();

	int _ParamIndex = -1;
	int _CookieIndex = -1;

	// {{{ Control Declarations
		private BoxSizer PanelSizer;
		private StaticBoxSizer sizExploitType;
		private StaticBoxSizer sizConnection;
		private StaticBoxSizer sizAuthentication;
		private StaticBoxSizer sizParameters;

		private RadioButton optConnectGet;
		private RadioButton optConnectPost;
		private StaticText lblConnectionMethod;
		private CheckBox chkUseSsl;
		private TextCtrl txtTargetURL;
		private StaticText lblTargetUrl;
		private CheckBox chkTerminateQuery;
		private CheckBox chkAppendTextToQuery;
		private TextCtrl txtAppendedText;
		
		private StaticText lblExploitType;
		private RadioButton optErrorBasedInjection;
		private RadioButton optBlindInjection;
		private StaticText lblPluginType;
		private ComboBox cboPlugins;

		private Panel pnlParams;
		private Panel pnlCookies;
		private Notebook ntbCookieParams;
		private ListView lstParams;
		private ListView lstCookies;
		private Button butRemoveParam;
		private Button butEditParam;
		private StaticText lblParamName;
		private TextCtrl txtParamName;
		private StaticText lblParamValue;
		private TextCtrl txtParamValue;
		private CheckBox chkInjectable;
		private CheckBox chkTreatAsString;
		private Button butAddCookie;
		private Button butAddParam;

		private CheckBox chkUseAuth;
		private RadioButton optBasicAuth;
		private RadioButton optDigestAuth;
		private RadioButton optNtlmAuth;
		private StaticText lblAuthUsername;
		private TextCtrl txtAuthUsername;
		private StaticText lblAuthPassword;
		private TextCtrl txtAuthPassword;
		private StaticText lblAuthDomain;
		private TextCtrl txtAuthDomain;

		private Button butInitialize;
	// }}}

	// {{{ Constructor
	public TargetPanel(Window Parent, ref DataStore SaveInfo, AbsintheForm.GuiControls ga, ref Absinthe.LocalSettings AppSettings) : base(Parent, -1)
	{
		_GuiActions = ga;
		_SaveInfo = SaveInfo;
		_AppSettings = AppSettings;
		PanelSizer = new BoxSizer(Orientation.wxVERTICAL);	
		
		SetupExploitType();
		SetupTargetInfo();
		SetupAuthenticationPanel();
		SetupFormParamsSection();

		PanelSizer.Add(sizExploitType, 0, (Direction.wxALL ^ Direction.wxTOP) | Stretch.wxEXPAND, 5);
		BoxSizer siz1 = new BoxSizer(Orientation.wxHORIZONTAL);
		PanelSizer.Add(sizConnection, 0, (Direction.wxALL ^ Direction.wxTOP) | Stretch.wxEXPAND, 5);
		PanelSizer.Add(sizAuthentication, 0, (Direction.wxALL ^ Direction.wxTOP) | Stretch.wxEXPAND, 5);
//		PanelSizer.Add(siz1, 0, (Direction.wxALL ^ Direction.wxTOP) | Stretch.wxEXPAND, 0);
		PanelSizer.Add(sizParameters, 0, (Direction.wxALL ^ Direction.wxTOP) | Stretch.wxEXPAND, 5);

		butInitialize = new wx.Button(this, "Initialize Injection", wxDefaultPosition, wxDefaultSize);

		PanelSizer.Add(butInitialize, 0, Direction.wxALL | Alignment.wxALIGN_CENTER, 8);
		PanelSizer.Add(5, 8, 0, Stretch.wxFIXED_MINSIZE | Alignment.wxALIGN_CENTER, 0);

		SetSizer(PanelSizer);

		BindEvents();
	}
	// }}}

	// {{{ Properties

	// {{{ TargetUrl Property
	public string TargetUrl
	{
		get
		{
			return txtTargetURL.Value;
		}
		set
		{
			txtTargetURL.Value = value;
		}
	}
	// }}}

	// {{{ PluginText Property
	public string PluginText
	{
		get
		{
			return cboPlugins.Value;
		}
	}
	// }}}	

	// }}}

	// {{{ BindEvents
	private void BindEvents()
	{
		EVT_BUTTON(butAddCookie.ID, new wx.EventListener(this.ButAddCookieClick));
		EVT_BUTTON(butRemoveParam.ID, new wx.EventListener(this.ButRemoveParamClick));
		EVT_BUTTON(butInitialize.ID, new wx.EventListener(this.ButInitializeClick));
		EVT_BUTTON(butEditParam.ID, new wx.EventListener(this.ButEditParamClick));
		EVT_BUTTON(butAddParam.ID, new wx.EventListener(this.AddParameter_Click));

		EVT_CHECKBOX(chkAppendTextToQuery.ID, new wx.EventListener(this.chkAppendTextToQuery_Click));
		EVT_CHECKBOX(chkInjectable.ID, new EventListener(chkInjectable_Click));

		EVT_CHECKBOX(chkUseAuth.ID, new EventListener(OnUseAuth_Click));

		EVT_RADIOBUTTON(optBasicAuth.ID, new EventListener(OnUseAuth_Click));
		EVT_RADIOBUTTON(optDigestAuth.ID, new EventListener(OnUseAuth_Click));
		EVT_RADIOBUTTON(optNtlmAuth.ID, new EventListener(OnUseAuth_Click));
		
		lstParams.ItemSelect += new EventListener( OnParamItemSelect );
		lstCookies.ItemSelect += new EventListener( OnCookieItemSelect );
	}
	// }}} 

	// {{{ OnParamItemSelect
	public void OnParamItemSelect( object sender, Event e )
	{
		ListEvent le = e as ListEvent;
		
		_ParamIndex = le.Index;
		
	}
	// }}}
	
	// {{{ OnCookieItemSelect
	public void OnCookieItemSelect( object sender, Event e )
	{
		ListEvent le = e as ListEvent;
		
		_CookieIndex = le.Index;
		
	}
	// }}}

	// {{{ MessageBoxWrite
	public void MessageBoxWrite(string Message)
	{

		if (Message != null && Message.Length > 0)
		{
			MessageDialog msg = new
				MessageDialog(this, Message, "Status", Dialog.wxOK | Dialog.wxICON_INFORMATION);

			msg.ShowModal();
		}

	}
	// }}}

	// {{{ Setup Internal Panels

	// {{{ SetupExploitType
	private void SetupExploitType()
	{

		StaticBox sbx = new wx.StaticBox(this, "Exploit Type:", wxDefaultPosition, wxDefaultSize, wx.Alignment.wxALIGN_TOP|wx.Alignment.wxALIGN_LEFT);

		sizExploitType = new StaticBoxSizer(sbx, Orientation.wxVERTICAL);

		BoxSizer siz = new BoxSizer(Orientation.wxHORIZONTAL);
		BoxSizer siz2 = new BoxSizer(Orientation.wxHORIZONTAL);

		lblExploitType = new wx.StaticText(this, "Select the type of injection:", wxDefaultPosition, wxDefaultSize, wx.Alignment.wxALIGN_TOP|wx.Alignment.wxALIGN_LEFT);

		optBlindInjection = new wx.RadioButton(this, "Blind Injection", wxDefaultPosition, wxDefaultSize, RadioButton.wxRB_GROUP);
		optBlindInjection.Value = true;

		optErrorBasedInjection = new wx.RadioButton(this, "Error Based", wxDefaultPosition, wxDefaultSize);
		optErrorBasedInjection.Value = false;
		optErrorBasedInjection.Enabled = false;

		siz.Add(lblExploitType, 0, Alignment.wxALIGN_CENTRE_VERTICAL | Direction.wxALL, 2);
		siz.Add(optBlindInjection, 0, wx.Stretch.wxEXPAND | Direction.wxALL, 2);
		siz.Add(optErrorBasedInjection, 0, wx.Stretch.wxEXPAND | Direction.wxALL, 2);

		// ----

		lblPluginType = new StaticText(this, "Select The Target Database:");

		LoadPluginList();
		cboPlugins = new ComboBox(this, String.Empty, wxDefaultPosition, new System.Drawing.Size(300, -1), _PluginEntries, ComboBox.wxCB_READONLY);

		siz2.Add(lblPluginType, 0, Alignment.wxALIGN_CENTRE_VERTICAL | Direction.wxALL, 2);
		siz2.Add(cboPlugins, 0, Stretch.wxEXPAND | Direction.wxALL, 2);

		sizExploitType.Add(siz, 0, 0, 0);
		sizExploitType.Add(siz2, 0, 0, 0);
	}
	// }}}

	// {{{ SetupAuthenticationPanel
	private void SetupAuthenticationPanel()
	{
		StaticBox sbx = new StaticBox(this, "Authentication", wxDefaultPosition, wxDefaultSize, Alignment.wxALIGN_TOP | Alignment.wxALIGN_LEFT);
		sizAuthentication = new StaticBoxSizer(sbx, Orientation.wxHORIZONTAL);
		BoxSizer siz2 = new BoxSizer(Orientation.wxHORIZONTAL);

		BoxSizer siz4 = new BoxSizer(Orientation.wxVERTICAL);

		chkUseAuth = new CheckBox(this, "Use Authentication");
		siz4.Add(chkUseAuth, 0, 0, 0);
		chkUseAuth.Value = false;
		
		BoxSizer siz1 = new BoxSizer(Orientation.wxHORIZONTAL);
		optBasicAuth = new RadioButton(this, "Basic");
		siz1.Add(optBasicAuth, 0, 0, 0);
		optBasicAuth.Enabled = false;
		
		optDigestAuth = new RadioButton(this, "Digest");
		siz1.Add(optDigestAuth, 0, 0, 0);
		optDigestAuth.Enabled = false;

		optNtlmAuth = new RadioButton(this, "NTLM");
		siz1.Add(optNtlmAuth, 0, 0, 0);
		optNtlmAuth.Enabled = false;

		siz4.Add(siz1, 0, 0, 0);
		sizAuthentication.Add(siz4, 0, 0, 0);

		sizAuthentication.Add(15, 15, 0, Stretch.wxFIXED_MINSIZE, 0); // Spacer

		GridSizer siz3 = new FlexGridSizer(3, 2, 2, 2);

		lblAuthUsername = new wx.StaticText(this, "Name:", wxDefaultPosition, wxDefaultSize, wx.Alignment.wxALIGN_TOP|wx.Alignment.wxALIGN_LEFT);
		siz3.Add(lblAuthUsername, 0, Direction.wxALL, 2);
		lblAuthUsername.Enabled = false;

		txtAuthUsername = new wx.TextCtrl(this, "", wxDefaultPosition, new System.Drawing.Size(128, 20), wx.Alignment.wxALIGN_TOP|wx.Alignment.wxALIGN_LEFT);
		siz3.Add(txtAuthUsername, 0, Direction.wxALL | Stretch.wxEXPAND, 2);
		txtAuthUsername.Enabled = false;

		lblAuthPassword = new wx.StaticText(this, "Password:", wxDefaultPosition, wxDefaultSize, wx.Alignment.wxALIGN_TOP|wx.Alignment.wxALIGN_LEFT);
		siz3.Add(lblAuthPassword, 0, Direction.wxALL, 2);
		lblAuthPassword.Enabled = false;

		txtAuthPassword = new wx.TextCtrl(this, "", wxDefaultPosition, new System.Drawing.Size(128, 20), wx.Alignment.wxALIGN_TOP|wx.Alignment.wxALIGN_LEFT);
		siz3.Add(txtAuthPassword, 0, Direction.wxALL | Stretch.wxEXPAND, 2);
		txtAuthPassword.Enabled = false;
		
		lblAuthDomain = new wx.StaticText(this, "Domain:", wxDefaultPosition, wxDefaultSize, wx.Alignment.wxALIGN_TOP|wx.Alignment.wxALIGN_LEFT);
		siz3.Add(lblAuthDomain, 0, Direction.wxALL, 2);
		lblAuthDomain.Enabled = false;

		txtAuthDomain = new wx.TextCtrl(this, "", wxDefaultPosition, new System.Drawing.Size(128, 20), wx.Alignment.wxALIGN_TOP|wx.Alignment.wxALIGN_LEFT);
		siz3.Add(txtAuthDomain, 0, Direction.wxALL | Stretch.wxEXPAND, 2);
		txtAuthDomain.Enabled = false;


		siz2.Add(siz3, 0, Alignment.wxALIGN_TOP, 0);
		
		sizAuthentication.Add(siz2, 0, 0, 0);

	}
	// }}}

	// {{{ SetupTargetInfo
	private void SetupTargetInfo()
	{
		StaticBox sbx;	
		sbx = new wx.StaticBox(this, "Connection:", wxDefaultPosition, wxDefaultSize, wx.Alignment.wxALIGN_TOP|wx.Alignment.wxALIGN_LEFT);
		sizConnection = new StaticBoxSizer(sbx, Orientation.wxVERTICAL);

		// ----
		BoxSizer siz1 = new BoxSizer(Orientation.wxHORIZONTAL);

		txtTargetURL = new wx.TextCtrl(this, "", wxDefaultPosition, new System.Drawing.Size(392, 20));

		lblTargetUrl = new wx.StaticText(this, "Target URL:  http://", wxDefaultPosition, wxDefaultSize, wx.Alignment.wxALIGN_TOP|wx.Alignment.wxALIGN_LEFT);

		siz1.Add(lblTargetUrl, 0, Alignment.wxALIGN_CENTRE_VERTICAL | Direction.wxALL, 2);
		siz1.Add(txtTargetURL, 0, Alignment.wxALIGN_CENTRE_VERTICAL | Direction.wxALL, 2);

		sizConnection.Add(siz1, 0, Stretch.wxEXPAND, 0);
		// ----

		BoxSizer siz2 = new BoxSizer(Orientation.wxHORIZONTAL);

		lblConnectionMethod = new wx.StaticText(this, "Connection Method:", wxDefaultPosition, wxDefaultSize, wx.Alignment.wxALIGN_TOP|wx.Alignment.wxALIGN_LEFT);

		optConnectGet = new wx.RadioButton(this, "Get", wxDefaultPosition, new System.Drawing.Size(56, 24), RadioButton.wxRB_GROUP);
		optConnectGet.Value = false;

		optConnectPost = new wx.RadioButton(this, "Post", wxDefaultPosition, new System.Drawing.Size(56, 24));
		optConnectPost.Value = false;

		chkUseSsl = new wx.CheckBox(this, "Use SSL", wxDefaultPosition, new System.Drawing.Size(72, 24));
		chkUseSsl.Value=false;

		siz2.Add(lblConnectionMethod, 0, wx.Stretch.wxEXPAND | Alignment.wxALIGN_BOTTOM | Direction.wxLEFT | Direction.wxBOTTOM, 1);
		siz2.Add(optConnectGet, 0, wx.Stretch.wxEXPAND | Direction.wxLEFT | Direction.wxBOTTOM, 1);
		siz2.Add(optConnectPost, 0, wx.Stretch.wxEXPAND | Direction.wxLEFT | Direction.wxBOTTOM, 1);
		siz2.Add(chkUseSsl, 0, wx.Stretch.wxEXPAND | Direction.wxALL ^ Direction.wxTOP, 1);

		sizConnection.Add(siz2, 0, 0, 0);
		// ----

		BoxSizer siz3 = new BoxSizer(Orientation.wxHORIZONTAL);
		
		chkTerminateQuery = new wx.CheckBox(this, "Comment End of Query", wxDefaultPosition, wxDefaultSize);
		chkTerminateQuery.Value = false;

		chkAppendTextToQuery = new CheckBox(this, "Append text to end of query", wxDefaultPosition, wxDefaultSize);
		chkAppendTextToQuery.Value = false;

		siz3.Add(chkTerminateQuery, 0, Stretch.wxEXPAND | Direction.wxLEFT | Direction.wxBOTTOM, 2);
		siz3.Add(chkAppendTextToQuery, 0, Stretch.wxEXPAND | Direction.wxALL ^ Direction.wxTOP, 2);

		sizConnection.Add(siz3, 0, 0, 0);

		txtAppendedText = new TextCtrl(this, "");
		sizConnection.Add(txtAppendedText, 0, Stretch.wxEXPAND | Direction.wxLEFT | Direction.wxRIGHT, 2);

		txtAppendedText.Enabled = false;
	}
	// }}}

	// {{{ SetupFormParamsSection
	private void SetupFormParamsSection()
	{
		StaticBox sbx1;

		sbx1 = new wx.StaticBox(this, "Form Parameters:", wxDefaultPosition, wxDefaultSize, wx.Alignment.wxALIGN_TOP|wx.Alignment.wxALIGN_LEFT);
		sizParameters = new StaticBoxSizer(sbx1, Orientation.wxHORIZONTAL);

		BoxSizer siz1 = new BoxSizer(Orientation.wxVERTICAL);
		siz1.Add(5, 20, 0, Stretch.wxFIXED_MINSIZE, 0);
		GridSizer siz2 = new FlexGridSizer(2, 2, 2, 2);

		lblParamName = new wx.StaticText(this, "Name:", wxDefaultPosition, wxDefaultSize, wx.Alignment.wxALIGN_TOP|wx.Alignment.wxALIGN_LEFT);
		siz2.Add(lblParamName, 0, Direction.wxALL, 2);

		txtParamName = new wx.TextCtrl(this, "", wxDefaultPosition, new System.Drawing.Size(128, 20), wx.Alignment.wxALIGN_TOP|wx.Alignment.wxALIGN_LEFT);
		siz2.Add(txtParamName, 0, Direction.wxALL, 2);

		lblParamValue = new wx.StaticText(this, "Default Value:", wxDefaultPosition, wxDefaultSize, wx.Alignment.wxALIGN_TOP|wx.Alignment.wxALIGN_LEFT);
		siz2.Add(lblParamValue, 0, Direction.wxALL, 2);

		txtParamValue=new wx.TextCtrl(this, "", wxDefaultPosition, new System.Drawing.Size(128, 20), wx.Alignment.wxALIGN_TOP|wx.Alignment.wxALIGN_LEFT);
		siz2.Add(txtParamValue, 0, Direction.wxALL, 2);

		siz1.Add(siz2, 0, 0, 0);

		chkInjectable = new wx.CheckBox(this, "Injectable Parameter", wxDefaultPosition, wxDefaultSize);
		chkInjectable.Value = false;

		siz1.Add(chkInjectable, 0, Direction.wxALL, 2);
		
		chkTreatAsString = new CheckBox(this, "Treat Value as String", wxDefaultPosition, wxDefaultSize);
		chkTreatAsString.Value = false;
		chkTreatAsString.Enabled = false;

		siz1.Add(chkTreatAsString, 0, Direction.wxALL, 2);
		
		GridSizer siz3 = new GridSizer(1,2,2,2);
		butAddParam = new wx.Button(this, "Add Parameter", wxDefaultPosition, wxDefaultSize);
		siz3.Add(butAddParam, 0, wx.Stretch.wxEXPAND, 0);

		butAddCookie = new wx.Button(this, "Add to Headers", wxDefaultPosition, wxDefaultSize);
		siz3.Add(butAddCookie, 0, Stretch.wxEXPAND, 0);
		siz1.Add(siz3, 0, 0, 0);

		sizParameters.Add(siz1, 0, Direction.wxALL, 2);

		// ----

		ntbCookieParams = new wx.Notebook(this, wxDefaultPosition, new System.Drawing.Size(216, 185));
		sizParameters.Add(ntbCookieParams, 0, wx.Stretch.wxEXPAND | Direction.wxALL, 2);

		pnlParams = new wx.Panel(ntbCookieParams);
		ntbCookieParams.AddPage(pnlParams, "Parameters");

		pnlCookies = new wx.Panel(ntbCookieParams);
		ntbCookieParams.AddPage(pnlCookies, "Additional Headers");

		lstCookies = new wx.ListView(pnlCookies, new System.Drawing.Point(8, 8), new System.Drawing.Size(192, 136), ListCtrl.wxLC_REPORT | ListCtrl.wxLC_SINGLE_SEL);

		lstParams = new wx.ListView(pnlParams, new System.Drawing.Point(8, 8), new System.Drawing.Size(192, 136), ListCtrl.wxLC_REPORT | ListCtrl.wxLC_SINGLE_SEL);

		// ----

		BoxSizer siz4 = new BoxSizer(Orientation.wxVERTICAL);
		siz4.Add(5, 24, 0, Stretch.wxFIXED_MINSIZE, 0);
		butEditParam = new wx.Button(this, "Edit", wxDefaultPosition, wxDefaultSize);
		siz4.Add(butEditParam, 0, Alignment.wxALIGN_CENTER | Direction.wxALL, 5);
		butRemoveParam = new wx.Button(this, "Remove", wxDefaultPosition, wxDefaultSize);
		siz4.Add(butRemoveParam, 0, Alignment.wxALIGN_CENTER | Direction.wxALL, 5);

		sizParameters.Add(siz4, 0, Direction.wxALL, 2);

		InitializeListViews();
	}
	// }}}

	// {{{ InitializeListViews
	private void InitializeListViews()
	{
		lstParams.InsertColumn(0, "Name");
		lstParams.InsertColumn(1, "Value");
		lstParams.InsertColumn(2, "Injectable");

		lstCookies.InsertColumn(0, "Name");
		lstCookies.InsertColumn(1, "Value");
	}
	// }}}

	// }}}

	// {{{ LoadPluginList
	private void LoadPluginList()
	{
		ArrayList al = _SaveInfo.PluginList;
		ArrayList NameList = new ArrayList();

		foreach (PluginTemplate pt in al)
		{
			if (!NameList.Contains(pt.PluginDisplayTargetName))
			{
				NameList.Add(pt.PluginDisplayTargetName);
			}
			else
			{
				string EntryName = pt.PluginDisplayTargetName;
				string Modifier = ""; int ModCounter = 0;
				while (NameList.Contains(EntryName + Modifier))
				{
					ModCounter++;
					Modifier = " {" + ModCounter + "}";
				}
				NameList.Add(EntryName + Modifier);
			}
		}

		_PluginEntries = (string[]) NameList.ToArray(typeof(string));
	}
	// }}}

	// {{{ ExtractFormParameters
	private StringDictionary ExtractFormParameters(ref string TargetName, ref string TargetField, out bool AsString)
	{
		bool FoundTarget = false;
		string Name, Val;
		bool Injectable;
		int cnt;
		StringDictionary retVal = new StringDictionary();
		AsString = false;

		for (cnt = 0; cnt < lstParams.ItemCount; cnt++)
		{
			ListItem li = new ListItem();
			li.Id = cnt;

			li.Column = 0;
			li.Mask = ListCtrl.wxLIST_MASK_TEXT;
			lstParams.GetItem(ref li);
			Name = li.Text;

			li.Column = 1;
			li.Mask = ListCtrl.wxLIST_MASK_TEXT;
			lstParams.GetItem(ref li);
			Val = li.Text;

			li.Column = 2;
			li.Mask = ListCtrl.wxLIST_MASK_TEXT;
			lstParams.GetItem(ref li);


			if (li.Text.Equals("Str"))
			{  Injectable = true; AsString = true;  }
			else
			{  Injectable = Convert.ToBoolean(li.Text); }
	
			if (!Injectable || FoundTarget)
			{
				retVal[Name] = Val;
			}
			else
			{
				TargetName = Name;
				TargetField = Val;
				FoundTarget = true;
			}
		}

		return retVal;
	}
	// }}}

	// {{{ ExtractCookies
	private StringDictionary ExtractCookies()
	{
		string Name, Val;
		int cnt;
		StringDictionary retVal = new StringDictionary();

		for (cnt = 0; cnt < lstCookies.ItemCount; cnt++)
		{
			ListItem li = new ListItem();

			li.Id = cnt;

			li.Column = 0;
			li.Mask = ListCtrl.wxLIST_MASK_TEXT;
			lstCookies.GetItem(ref li);
			Name = li.Text;

			li.Column = 1;
			li.Mask = ListCtrl.wxLIST_MASK_TEXT;
			lstCookies.GetItem(ref li);
			Val = li.Text;

			retVal[Name] = Val;
		}

		return retVal;
	}
	// }}}

	// {{{ ButAddCookieClick
	void ButAddCookieClick(object sender, wx.Event e)
	{
		// Create a list with the current Vector / Value
		if (txtParamName.Value == "" || txtParamName.Value == null)
		{
			wx.MessageDialog.MessageBox("A parameter name is required!");
			return;
		}

		if (txtParamValue.Value == "" || txtParamValue.Value == null)
		{
			wx.MessageDialog.MessageBox("A parameter value is required!");
			return;
		}

		_CookieIndex = -1;
		lstCookies.InsertItem(lstCookies.ItemCount, txtParamName.Value);
		lstCookies.SetItem(lstCookies.ItemCount - 1, 1, txtParamValue.Value);

		txtParamName.Value = "";
		txtParamValue.Value = "";
		chkInjectable.Value = false;
		chkTreatAsString.Value = false;
		chkTreatAsString.Enabled = false;
	}
	// }}}

	// {{{ ConnectMethod
	private string ConnectMethod()
	{
		string Method;

		if (optConnectPost.Value == true)
		{
			Method = "Post";
		}
		else if (optConnectGet.Value == true)
		{
			Method = "Get";
		}
		else
		{
			// default to get
			return "Get";
		}

		return Method;
	}
	// }}}

	// {{{ AddParameter_Click
	void AddParameter_Click(object sender, wx.Event e)
	{
		if (txtParamName.Value == "" || txtParamName.Value == null)
		{
			wx.MessageDialog.MessageBox("A parameter name is required!");
			return;
		}

		if (txtParamValue.Value == "" || txtParamValue.Value == null)
		{
			wx.MessageDialog.MessageBox("A parameter value is required!");
			return;
		}

		lstParams.InsertItem(lstParams.ItemCount, txtParamName.Value);
		lstParams.SetItem(lstParams.ItemCount - 1, 1, txtParamValue.Value);

		string Injectable = String.Empty;
		if (chkInjectable.Value && chkTreatAsString.Value) 
		{  Injectable = "Str";  }
		else
		{  Injectable = chkInjectable.Value.ToString();  }
		lstParams.SetItem(lstParams.ItemCount - 1, 2, Injectable);

		_ParamIndex = -1;
		txtParamName.Value = "";
		txtParamValue.Value = "";
		chkInjectable.Value = false;
		chkTreatAsString.Value = false;
		chkTreatAsString.Enabled = false;
	}			 
	// }}}

	// {{{ ButRemoveParamClick
	void ButRemoveParamClick(object sender, wx.Event e)
	{
		int SelectedIndex = -1;
		ListCtrl lstActive;

		if (ntbCookieParams.Selection == 0)
		{
			lstActive = lstParams;
			SelectedIndex = _ParamIndex;
		}
		else
		{
			lstActive = lstCookies;
			SelectedIndex = _CookieIndex;
		}

		//SelectedIndex = lstActive.GetNextItem(SelectedIndex, ListCtrl.wxLIST_NEXT_ALL, ListCtrl.wxLIST_STATE_SELECTED);

		if (SelectedIndex == -1)
		{
			MessageBoxWrite("Please select a parameter to remove.");
			return;
		}

		lstActive.DeleteItem(SelectedIndex);
	}
	// }}}

	// {{{ ButInitializeClick
	void ButInitializeClick(object sender, wx.Event e)
	{
		//InitializeAttackVectors();
		ThreadedSub a = new ThreadedSub(InitializeAttackVectors);
		a.BeginInvoke(null, new object());
	}
	// }}}

	// {{{ InitializeAttackVectors
	private void InitializeAttackVectors()
	{
		string URL;

		if (chkUseSsl.Value) URL = "https://";
		else URL = "http://";
		URL += txtTargetURL.Value;

		string Method = ConnectMethod();

		if (Method.Equals("")) return;

		Cursor = new Cursor(StockCursor.wxCURSOR_WAIT);

		// Generate StringDict
		string TargetName, TargetField;
		bool InjectAsString;
		TargetName = String.Empty; TargetField = String.Empty;

		StringDictionary Others = new StringDictionary();
		StringDictionary Cookies = new StringDictionary();

		Others = ExtractFormParameters(ref TargetName, ref TargetField, out InjectAsString);
		Cookies = ExtractCookies();

		if (TargetName.Equals(String.Empty))
		{
			_GuiActions.Status("No Injection Point Found");
			Cursor = new Cursor(StockCursor.wxCURSOR_ARROW);
			return;
		}

		_GuiActions.Status("Beginning Preliminary Scan");

		try
		{
			butInitialize.Enabled = false;

			AttackVectorFactory avf;
			GlobalDS.OutputStatusDelegate safeout = new GlobalDS.OutputStatusDelegate(_GuiActions.Output);

			//_GuiActions.Output(chkTerminateQuery.Value.ToString());

			GlobalDS.InjectionOptions opts = new GlobalDS.InjectionOptions();
			opts.Cookies = Cookies;
			opts.TerminateQuery = chkTerminateQuery.Value;
			opts.Tolerance = _SaveInfo.FilterTolerance;
			opts.WebProxies = _AppSettings.ProxyQueue();
			opts.InjectAsString = InjectAsString;
			opts.Delimiter = _SaveInfo.FilterDelimiter;
			if (chkUseAuth.Value) 
			{
				if (optNtlmAuth.Value)
				{
					opts.AuthCredentials = new NetworkCredential(txtAuthUsername.Value, txtAuthPassword.Value, txtAuthDomain.Value);
				}
				else
				{
					opts.AuthCredentials = new NetworkCredential(txtAuthUsername.Value, txtAuthPassword.Value);
				}
			}

			if (chkAppendTextToQuery.Value == true)
			{
				opts.AppendedQuery = txtAppendedText.Value;
			}
			//System.Console.WriteLine("Filter Delim: {0} && {1}", _SaveInfo.FilterDelimiter, opts.Delimiter);

			avf = new AttackVectorFactory(URL, TargetName, TargetField, Others, Method, safeout, opts);

			PluginTemplate pt = (PluginTemplate) _SaveInfo.PluginList[Array.IndexOf(_PluginEntries, cboPlugins.Value)];

			if (optBlindInjection.Value)
			{
				_SaveInfo.TargetAttackVector = avf.BuildBlindSqlAttackVector(_SaveInfo.FilterTolerance, pt);
			}
#if FULL_RELEASE
			else if(optErrorBasedInjection.Value)
			{
				_SaveInfo.TargetAttackVector = avf.BuildSqlErrorAttackVector();
			}
#endif
			_GuiActions.Status("Finished initial scan");
		}
		catch (Exception e)
		{
			_GuiActions.Output(e.ToString());
			_GuiActions.Status(e.Message);
		}
		finally
		{
			butInitialize.Enabled =  true;
			Cursor = new Cursor(StockCursor.wxCURSOR_ARROW);
		}

	}
	// }}}

	// {{{ ButEditParamClick
	private void ButEditParamClick(object sender, wx.Event e)
	{
		// Edit the selected parameter
		
		int SelectedIndex = -1;
		ListCtrl lstActive;

		if (ntbCookieParams.Selection == 0)
		{
			lstActive = lstParams;
			SelectedIndex = _ParamIndex;
		}
		else
		{
			lstActive = lstCookies;
			SelectedIndex = _CookieIndex;
		}

		//SelectedIndex = lstActive.GetNextItem(SelectedIndex, ListCtrl.wxLIST_NEXT_ALL, ListCtrl.wxLIST_STATE_SELECTED);
		
		if (SelectedIndex == -1)
		{
			MessageBoxWrite("Please select a parameter to edit.");
			return;
		}

		ListItem li = new ListItem();

		li.Id = SelectedIndex;

		li.Column = 0;
		li.Mask = ListCtrl.wxLIST_MASK_TEXT;
		lstActive.GetItem(ref li);
		txtParamName.Value = li.Text;

		li.Column = 1;
		li.Mask = ListCtrl.wxLIST_MASK_TEXT;
		lstActive.GetItem(ref li);
		txtParamValue.Value = li.Text;

		if (ntbCookieParams.Selection == 0)
		{
			li.Column = 2;
			li.Mask = ListCtrl.wxLIST_MASK_TEXT;
			lstActive.GetItem(ref li);
			if (li.Text.Equals("Str"))
			{  chkInjectable.Value = true; chkTreatAsString.Enabled = true; chkTreatAsString.Value = true;  }
			else
			{  chkInjectable.Value = Convert.ToBoolean(li.Text);  }
		}

		lstActive.DeleteItem(SelectedIndex);
	}
	// }}}

	// {{{ OnUseAuth_Click
	private void OnUseAuth_Click(object sender, Event e)
	{
		bool EnableVal = chkUseAuth.Value;
		optBasicAuth.Enabled = EnableVal;
		optDigestAuth.Enabled = EnableVal;
		optNtlmAuth.Enabled = EnableVal;
		lblAuthUsername.Enabled = EnableVal;
		txtAuthUsername.Enabled = EnableVal;
		lblAuthPassword.Enabled = EnableVal;
		txtAuthPassword.Enabled = EnableVal;
		lblAuthDomain.Enabled = EnableVal && optNtlmAuth.Value;
		txtAuthDomain.Enabled = EnableVal && optNtlmAuth.Value;
	}
	// }}}

	// {{{ chkAppendTextToQuery_Click
	private void chkAppendTextToQuery_Click(object sender, Event e)
	{
		txtAppendedText.Enabled = chkAppendTextToQuery.Value;
	}
	// }}}

	// {{{ chkInjectable_Click
	private void chkInjectable_Click(object sender, Event e)
	{
		chkTreatAsString.Enabled = chkInjectable.Value;
	}
	// }}}

	// {{{ PrepareForSave
	public void PrepareForSave()
	{
		//TODO: Verify all necessary info is being passed
		_SaveInfo.TargetURL = txtTargetURL.Value;
		SetParametersInDataStore();
		_SaveInfo.Cookies = ExtractCookies();
		if (!chkUseAuth.Value)
		{
			_SaveInfo.Authdata(GlobalDS.AuthType.None);
		}
		else
		{
			if (optNtlmAuth.Value)
			{
				_SaveInfo.Authdata(GlobalDS.AuthType.NTLM, txtAuthUsername.Value, txtAuthPassword.Value, txtAuthDomain.Value);
			}
			else
			{
				GlobalDS.AuthType at = GlobalDS.AuthType.None;

				if (optBasicAuth.Value)
					at = GlobalDS.AuthType.Basic;
				else if (optDigestAuth.Value)
					at = GlobalDS.AuthType.Digest;

				_SaveInfo.Authdata(at, txtAuthUsername.Value, txtAuthPassword.Value);
			}
		}
	}
	// }}}
	
	// {{{ SetParametersInDataStore
	private void SetParametersInDataStore()
	{
		int cnt;
		GlobalDS.FormParam fp = new GlobalDS.FormParam();

		for (cnt = 0; cnt < lstParams.ItemCount; cnt++)
		{
			ListItem li = new ListItem();
			li.Id = cnt;

			li.Column = 0;
			li.Mask = ListCtrl.wxLIST_MASK_TEXT;
			lstParams.GetItem(ref li);
			fp.Name = li.Text;

			li.Column = 1;
			li.Mask = ListCtrl.wxLIST_MASK_TEXT;
			lstParams.GetItem(ref li);
			fp.DefaultValue = li.Text;

			li.Column = 2;
			li.Mask = ListCtrl.wxLIST_MASK_TEXT;
			lstParams.GetItem(ref li);
			if (li.Text.Equals("Str"))
			{
				fp.Injectable = true;
				fp.AsString = true;
			}
			else
			{
				fp.Injectable = Convert.ToBoolean(li.Text);
			}

			_SaveInfo.AddFormParameter(fp);
		}
	}
	// }}}

	// {{{ LoadDataFromStore
	public void LoadDataFromStore(ref DataStore SaveInfo)
	{
		_SaveInfo = SaveInfo;

		if (_SaveInfo.ConnectionMethod.ToUpper().Equals("POST")) { optConnectPost.Value = true; }
		else { optConnectGet.Value = true; }

		txtTargetURL.Value = _SaveInfo.TargetURL;

		optBlindInjection.Value = false; optErrorBasedInjection.Value = false;
		chkTerminateQuery.Value = _SaveInfo.TerminateQuery;

		if (_SaveInfo.LoadedPluginName != null)
		{
			cboPlugins.SetSelection(cboPlugins.FindString(_SaveInfo.LoadedPluginName));
			cboPlugins.Value = _SaveInfo.LoadedPluginName;
		}

		if (_SaveInfo.TargetAttackVector != null)
		{
			switch(_SaveInfo.TargetAttackVector.ExploitType)
			{
				case GlobalDS.ExploitType.ErrorBasedTSQL:
					optErrorBasedInjection.Value = true;
					break;
				case GlobalDS.ExploitType.BlindTSQLInjection:
					optBlindInjection.Value = true;
					break;
			}
		}
		
		try
		{
			LoadParamsFromStore();
		}
		catch {}	
	
		try
		{
			LoadHeadersFromStore();
		}
		catch {}

		LoadAuthDataFromStore();
	}
	// }}}

	// {{{ LoadParamsFromStore
	private void LoadParamsFromStore()
	{
		foreach (DictionaryEntry den in _SaveInfo.ParameterTable)
		{
			GlobalDS.FormParam fp = (GlobalDS.FormParam) den.Value;

			lstParams.InsertItem(lstParams.ItemCount, fp.Name);
			lstParams.SetItem(lstParams.ItemCount - 1, 1, fp.DefaultValue);
			if (fp.Injectable && fp.AsString)
			{  lstParams.SetItem(lstParams.ItemCount - 1, 2, "Str");  }
			else
			{  lstParams.SetItem(lstParams.ItemCount - 1, 2, fp.Injectable.ToString());  }
		}
	}
	// }}}

	// {{{ LoadHeadersFromStore
	private void LoadHeadersFromStore()
	{
		foreach (DictionaryEntry den in _SaveInfo.Cookies)
		{
			lstCookies.InsertItem(lstCookies.ItemCount, den.Key.ToString());
			lstCookies.SetItem(lstCookies.ItemCount - 1, 1, den.Value.ToString());
		}
	}
	// }}}

	// {{{ LoadAuthDataFromStore
	private void LoadAuthDataFromStore()
	{
		switch(_SaveInfo.AuthenticationMethod)
		{
			case GlobalDS.AuthType.None:
				chkUseAuth.Value = false;
				optBasicAuth.Value = false; optDigestAuth.Value = false; optNtlmAuth.Value = false;
				txtAuthUsername.Value = string.Empty;
				txtAuthPassword.Value = string.Empty;
				txtAuthDomain.Value = string.Empty;
				break;
			case GlobalDS.AuthType.Basic:
				chkUseAuth.Value = true;
				optBasicAuth.Value = true; optDigestAuth.Value = false; optNtlmAuth.Value = false;
				txtAuthUsername.Value = _SaveInfo.AuthUser;
				txtAuthPassword.Value = _SaveInfo.AuthPassword;
				txtAuthDomain.Value = string.Empty;
				break;
			case GlobalDS.AuthType.Digest:
				chkUseAuth.Value = true;
				optBasicAuth.Value = false; optDigestAuth.Value = true; optNtlmAuth.Value = false;
				txtAuthUsername.Value = _SaveInfo.AuthUser;
				txtAuthPassword.Value = _SaveInfo.AuthPassword;
				txtAuthDomain.Value = string.Empty;
				break;
			case GlobalDS.AuthType.NTLM:
				chkUseAuth.Value = true;
				optBasicAuth.Value = false; optDigestAuth.Value = false; optNtlmAuth.Value = true;
				txtAuthUsername.Value = _SaveInfo.AuthUser;
				txtAuthPassword.Value = _SaveInfo.AuthPassword;
				txtAuthDomain.Value = _SaveInfo.AuthDomain;
				break;
		}

		OnUseAuth_Click(null, null);
	}
	// }}}
}
