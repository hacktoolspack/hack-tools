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


using System;
using System.Collections;
using System.Net;

using wx;

public class ProxyConfigDialog : Dialog
{
	int _ProxyIndex = -1;
	// {{{ Control Declarations
	CheckBox chkUseProxy;
	
	StaticText lblHostname;
	TextCtrl txtHostname;
	StaticText lblPort;
	TextCtrl txtPort;

	Button butAdd;
	Button butRemove;

	ListCtrl lstProxies;

	Button butOk;
	Button butCancel;
	// }}}

	private Absinthe.LocalSettings _AppSettings;

	// {{{ Constructor
	public ProxyConfigDialog(Window Parent, ref Absinthe.LocalSettings AppSettings) : base(Parent, "Proxy Configuration", wxDefaultPosition, wxDefaultSize, wxDEFAULT_FRAME_STYLE | wxFRAME_FLOAT_ON_PARENT)
	{
		_AppSettings = AppSettings;
		InitializeComponent();
	}
	// }}}

	// {{{ InitializeComponent
	private void InitializeComponent()
	{
		BoxSizer sizProxyConfig = new BoxSizer(Orientation.wxVERTICAL);

		chkUseProxy = new CheckBox(this, "Use HTTP Proxies");

		sizProxyConfig.Add(chkUseProxy, 0, Direction.wxALL, 5);

		lblHostname = new StaticText(this, "IP/Hostname:");
		txtHostname = new TextCtrl(this, string.Empty);

		lblPort = new StaticText(this, "Port:");
		txtPort = new TextCtrl(this, string.Empty);

		BoxSizer siz1 = new BoxSizer(Orientation.wxHORIZONTAL);

		siz1.Add(lblHostname, 0, Direction.wxALL | Alignment.wxALIGN_CENTRE_VERTICAL, 2);
		siz1.Add(txtHostname, 0, Direction.wxALL, 2);
		siz1.Add(lblPort, 0, Direction.wxALL | Alignment.wxALIGN_CENTRE_VERTICAL, 2);
		siz1.Add(txtPort, 0, Direction.wxALL, 2);

		sizProxyConfig.Add(siz1, 0, Direction.wxALL, 5);

		butAdd = new Button(this, "Add");
		butRemove = new Button(this, "Remove");
		
		BoxSizer siz2 = new BoxSizer(Orientation.wxHORIZONTAL);
		
		siz2.Add(butAdd, 0, Direction.wxALL, 5);
		siz2.Add(butRemove, 0, Direction.wxALL, 5);

		sizProxyConfig.Add(siz2, 0, Direction.wxALL | Alignment.wxALIGN_CENTER, 5);

		lstProxies = new ListCtrl(this, wxDefaultPosition, new System.Drawing.Size(250, 200), ListCtrl.wxLC_REPORT | ListCtrl.wxLC_SINGLE_SEL);
		sizProxyConfig.Add(lstProxies, 0, Direction.wxALL, 5);

		butOk = new Button(this, "OK");
		butCancel = new Button(this, "Cancel");

		BoxSizer siz3 = new BoxSizer(Orientation.wxHORIZONTAL);
		siz3.Add(butOk, 0, Direction.wxALL, 5);
		siz3.Add(butCancel, 0, Direction.wxALL, 5);
		sizProxyConfig.Add(siz3, 0, Alignment.wxALIGN_CENTER | Direction.wxALL, 5);

		SetSizerAndFit(sizProxyConfig, true);

		SetupProxyList();

		BindEvents();
	}
	// }}}

	// {{{ BindEvents
	private void BindEvents()
	{
		EVT_BUTTON(butAdd.ID, new wx.EventListener(this.AddProxy_Click));
		EVT_BUTTON(butRemove.ID, new wx.EventListener(this.RemoveProxy_Click));

		EVT_BUTTON(butOk.ID, new EventListener(this.butOk_Click));
		EVT_BUTTON(butCancel.ID, new EventListener(this.butCancel_Click));
		
		lstProxies.ItemSelect += new EventListener( OnProxy_Click );
	}
	// }}}
	
	// {{{ OnProxy_Click
	private void OnProxy_Click(object sender, wx.Event e)
	{
		ListEvent le = e as ListEvent;
		
		_ProxyIndex = le.Index;			
	}
	// }}}

	// {{{ SetupProxyList
	private void SetupProxyList()
	{
		lstProxies.InsertColumn(0, "Hostname");
		lstProxies.InsertColumn(1, "Port");

		Queue ProxyList = _AppSettings.ProxyQueue(true);

		if (ProxyList != null)
		{
			foreach (WebProxy wp in ProxyList)
			{
				lstProxies.InsertItem(lstProxies.ItemCount, wp.Address.Host);
				lstProxies.SetItem(lstProxies.ItemCount - 1, 1, wp.Address.Port.ToString());
			}
		}

		chkUseProxy.Value = _AppSettings.ProxyInUse;

	}
	// }}}

	// {{{ AddProxy_Click
	void AddProxy_Click(object sender, Event e)
	{
		if(txtHostname.Value == "") //TODO: Verify valid hostname
		{
			wx.MessageDialog.MessageBox("A hostname or IP address name is required!");
			return;
		}

		if(txtPort.Value == "") //TODO: Verify valid portname
		{
			wx.MessageDialog.MessageBox("A proxy port is required!");
			return;
		}

		try
		{
			Int32.Parse(txtPort.Value);
		}
		catch (System.FormatException)
		{
			wx.MessageDialog.MessageBox("Invalid proxy port.", "Error!");
			return;
		}
		catch (Exception ex)
		{
			wx.MessageDialog.MessageBox(ex.ToString(), "Error!");
			return;
		}

		lstProxies.InsertItem(lstProxies.ItemCount, txtHostname.Value);
		lstProxies.SetItem(lstProxies.ItemCount - 1, 1, txtPort.Value);

		txtHostname.Value = "";
		txtPort.Value = "";

	}
	// }}}

	// {{{ RemoveProxy_Click
	void RemoveProxy_Click(object sender, Event e)
	{
		string ProxyHostName;
		int SelectedIndex = _ProxyIndex;
		//SelectedIndex = lstProxies.GetNextItem(SelectedIndex, ListCtrl.wxLIST_NEXT_ALL, ListCtrl.wxLIST_STATE_SELECTED);

		if (SelectedIndex == -1)
		{
			MessageDialog.MessageBox("Please select a proxy to remove");
			return;
		}

		ListItem li = new ListItem();
		
		li.Id = SelectedIndex;
		li.Column = 0;
		li.Mask = ListCtrl.wxLIST_MASK_TEXT;
		lstProxies.GetItem(ref li);
		ProxyHostName = li.Text;

		lstProxies.DeleteItem(SelectedIndex);
		
	}
	// }}}

	void butOk_Click(object sender, Event e)
	{
		string ProxyHostName;
		int ProxyPort;

		_AppSettings.ClearProxies();

		for (int cnt = 0; cnt < lstProxies.ItemCount; cnt++)
		{
			ListItem li = new ListItem();
			li.Id = cnt;

			li.Column = 0;
			li.Mask = ListCtrl.wxLIST_MASK_TEXT;
			lstProxies.GetItem(ref li);
			ProxyHostName = li.Text;

			li.Column = 1;
			li.Mask = ListCtrl.wxLIST_MASK_TEXT;
			lstProxies.GetItem(ref li);
			ProxyPort = Convert.ToInt32(li.Text);

			_AppSettings.AddProxy(ProxyHostName, ProxyPort);
		}

		_AppSettings.ProxyInUse = chkUseProxy.Value;

		this.Close();
	}

	// {{{ butCancel_Click
	void butCancel_Click(object sender, Event e)
	{
		this.Close();	
	}
	// }}}
}
