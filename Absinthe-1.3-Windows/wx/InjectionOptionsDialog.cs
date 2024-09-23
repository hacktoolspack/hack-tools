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
using System.Text.RegularExpressions;

using wx;

public class InjectionOptionsDialog : Dialog
{

	// {{{ Control Declarations
	StaticText lblTolerance;
	TextCtrl txtTolerance;
	StaticText lblTolerancePct;

	StaticText lblDelimiter;
	TextCtrl txtDelimiter;
	StaticText lblDelimiterInfo;

	StaticText lblThrottle;
	TextCtrl txtThrottle;

	StaticText lblSpeedup;
	Slider sldSpeedup;

	Button butOk;
	Button butCancel;
	// }}}

	private Absinthe.Core.DataStore _Storage;

	// {{{ Constructor
	public InjectionOptionsDialog(Window Parent, ref Absinthe.Core.DataStore Storage) : base(Parent, "Injection Options", wxDefaultPosition, wxDefaultSize, wxDEFAULT_FRAME_STYLE | wxFRAME_FLOAT_ON_PARENT)
	{
		_Storage = Storage;
		InitializeComponent();
		LoadValuesFromStorage();
		BindEvents();
	}
	// }}}

	// {{{ LoadValuesFromStorage
	private void LoadValuesFromStorage()
	{
		txtTolerance.Value = (_Storage.FilterTolerance * 100).ToString();
		if (_Storage.FilterDelimiter.Equals(System.Environment.NewLine))
		{
			txtDelimiter.Value = String.Empty;
		}
		else
		{
			txtDelimiter.Value = _Storage.FilterDelimiter;
		}
		txtThrottle.Value = _Storage.ThrottleValue.ToString();
		sldSpeedup.Value = _Storage.ThrottleValue;
	}
	// }}}

	// {{{ InitializeComponent
	private void InitializeComponent()
	{
		BoxSizer sizMain = new BoxSizer(Orientation.wxVERTICAL);

		BoxSizer siz1 = new BoxSizer(Orientation.wxHORIZONTAL);

		lblTolerance = new StaticText(this, "Compared Tolerance:");
		txtTolerance = new TextCtrl(this, String.Empty);
		lblTolerancePct = new StaticText(this, "%");

		siz1.Add(lblTolerance, 0, Direction.wxALL | Alignment.wxALIGN_CENTRE_VERTICAL, 2);
		siz1.Add(txtTolerance, 0, Direction.wxALL, 2);
		siz1.Add(lblTolerancePct, 0, Direction.wxALL | Alignment.wxALIGN_CENTRE_VERTICAL, 2);

		sizMain.Add(siz1, 0, 0, 0);

		lblDelimiter = new StaticText(this, "Filter Delimiter:");
		txtDelimiter = new TextCtrl(this, String.Empty);
		lblDelimiterInfo = new StaticText(this, "(Leave blank for linebreak)");

		BoxSizer siz2 = new BoxSizer(Orientation.wxHORIZONTAL);

		siz2.Add(lblDelimiter, 0, Direction.wxALL | Alignment.wxALIGN_CENTRE_VERTICAL, 2);
		siz2.Add(txtDelimiter, 0, Direction.wxALL, 2);
		siz2.Add(lblDelimiterInfo, 0, Direction.wxALL | Alignment.wxALIGN_CENTRE_VERTICAL, 2);

		sizMain.Add(siz2, 0, 0, 0);

		lblThrottle = new StaticText(this, "Attack Throttle:");
		txtThrottle = new TextCtrl(this, String.Empty);

		BoxSizer siz3 = new BoxSizer(Orientation.wxHORIZONTAL);

		siz3.Add(lblThrottle, 0, Direction.wxALL | Alignment.wxALIGN_CENTRE_VERTICAL, 2);
		siz3.Add(txtThrottle, 0, Direction.wxALL, 2);

		sizMain.Add(siz3, 0, 0, 0);

		lblSpeedup = new StaticText(this, "Attack Speedup:");
		sldSpeedup = new Slider(this, 1, 1, 2, wxDefaultPosition, new System.Drawing.Size(50, -1));

		BoxSizer siz4 = new BoxSizer(Orientation.wxHORIZONTAL);

		siz4.Add(lblSpeedup, 0, Direction.wxALL | Alignment.wxALIGN_CENTRE_VERTICAL, 2);
		siz4.Add(sldSpeedup, 0, Direction.wxALL, 2);

		sizMain.Add(siz4, 0, 0, 0);

		butOk = new Button(this, "OK");
		butCancel = new Button(this, "Cancel");

		BoxSizer siz5 = new BoxSizer(Orientation.wxHORIZONTAL);

		siz5.Add(butOk, 0, Direction.wxALL | Alignment.wxALIGN_CENTRE_VERTICAL, 4);
		siz5.Add(butCancel, 0, Direction.wxALL | Alignment.wxALIGN_CENTRE_VERTICAL, 4);

		sizMain.Add(siz5, 0, Alignment.wxALIGN_CENTRE, 0);

		SetSizerAndFit(sizMain, true);
	}
	// }}}

	// {{{ BindEvents
	private void BindEvents()
	{
		EVT_BUTTON(butOk.ID, new EventListener(this.butOK_Click));
		EVT_BUTTON(butCancel.ID, new EventListener(this.butCancel_Click));
	}
	// }}}

	// {{{ ErrorBoxWrite
	public void ErrorBoxWrite(string Message)
	{
		if (Message != null && Message.Length > 0)
		{
			MessageDialog msg = new
				MessageDialog(this, Message, "Status", Dialog.wxOK | Dialog.wxICON_ERROR);

			msg.ShowModal();
		}
	}
	// }}}

	// {{{ butCancel_Click
	public void butCancel_Click(object sender, wx.Event e)
	{
		this.Close();
	}
	// }}}

	// {{{ butOK_Click
	public void butOK_Click(object sender, wx.Event e)
	{
		// this should allow decimals too
		//if (Regex.IsMatch(txtTolerance.Text, @"^\d*[\.\d*]?$")) 
		if (Regex.IsMatch(txtTolerance.Value, @"^[+]?\d+(\.\d+)?$") == false)
		{
			ErrorBoxWrite("You have entered an invalid tolerance.");
			return;
		}

		_Storage.FilterTolerance = Single.Parse(txtTolerance.Value) / 100;
		_Storage.FilterDelimiter = txtDelimiter.Value;

		int ThrottleValue;
		ThrottleValue = Convert.ToInt32(sldSpeedup.Value);

		if (ThrottleValue == 0)
		{
			ThrottleValue = Int32.Parse(txtThrottle.Value);
		}
		else
		{
			ThrottleValue *= -100;
		}

		_Storage.ThrottleValue = ThrottleValue;

		this.Close();
	}
	// }}}

}
