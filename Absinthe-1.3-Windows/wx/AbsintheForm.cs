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

/*
	Authors: nummish
	Ported form the SWF implementation by Xeron
*/

// project created on 4/7/2004 at 12:33 AM
using System;
using System.Configuration;
using System.Threading;

using wx;

using System.Collections;
using System.Collections.Specialized;
using System.Text.RegularExpressions;
using System.Net;
using System.Security.Permissions;

using Absinthe.Core;


[assembly:PermissionSetAttribute(SecurityAction.RequestMinimum, Name = "FullTrust")]
public class AbsintheForm : wx.Frame
{
		private Notebook tabControl;
		private TargetPanel pnlInjection;
		private SchemaPanel pnlResults;
		private DownloadPanel pnlRecords;

		private Absinthe.LocalSettings _AppSettings = new Absinthe.LocalSettings();
		
		// {{{ Menus
		private wx.MenuItem mnuAbout;
		private wx.MenuItem mnuSaveAs;
		private wx.MenuItem mnuSave;
		private wx.MenuItem menuItem5;
		private wx.Menu mnuFile;
		private wx.Menu mnuHelp;
		private wx.MenuItem mnuQuit;
		private wx.MenuItem mnuOpen;
		private wx.MenuItem mnuNew;
		private wx.MenuBar mnuAbsinthe;
		private Menu mnuTools;	
		private MenuItem mnuInjOptions;
		private MenuItem mnuProxyConfig;
		// }}}

		private Hashtable InjectionFields = new Hashtable(); 

		Queue _ActionQueue;
		private int _GuiUiId;
			
		public delegate void StatusDelegate(string Message);
		public delegate void EnableDelegate(Window ctl, bool Enabled);
		public delegate void OutputDelegate(string Message);
		public delegate void CursorDelegate(StockCursor NewCursor);
		public delegate void InterformCall();
		
		public struct GuiControls
		{
			public StatusDelegate Status;
			public StatusDelegate MessageBox;
			public EnableDelegate Enable;
			public OutputDelegate Output;
			public CursorDelegate Cursor;
			public InterformCall ReloadAvailableFields;
		}

		private DataStore _SaveInfo;
		
		public AbsintheForm() : base("Absinthe", wx.Window.wxDefaultPosition, new System.Drawing.Size(585,675), wx.Window.wxCAPTION|wx.Window.wxCLIP_CHILDREN| wx.Window.wxRESIZE_BORDER| wx.Window.wxMAXIMIZE_BOX| wx.Window.wxSYSTEM_MENU|wx.Window.wxCLOSE_BOX|wx.Window.wxMINIMIZE_BOX)
		{
			_SaveInfo = new DataStore(new GlobalDS.OutputStatusDelegate(SafeOutput));
			InitializeComponent();			
		}

		// {{{ InitializeTabs
		private void InitializeTabs()
		{
			GuiControls ga;

			ga.Status = new StatusDelegate(SafeStatusBarWrite);
			ga.Enable = new EnableDelegate(SafeChangeSensitivity);
			ga.Output = new OutputDelegate(SafeOutput);
			ga.MessageBox = new StatusDelegate(SafeMessageBoxWrite);
			ga.Cursor = new CursorDelegate(SafeCursorChange);
			ga.ReloadAvailableFields = null;
			
			pnlInjection = new TargetPanel(tabControl, ref _SaveInfo, ga, ref _AppSettings);
			tabControl.AddPage(pnlInjection, "Host Information");

			pnlRecords = new DownloadPanel(tabControl, ref _SaveInfo, ga);

			ga.ReloadAvailableFields = new InterformCall(pnlRecords.ReloadAvailableFields);
			
			pnlResults = new SchemaPanel(tabControl, ref _SaveInfo, ga, ref _AppSettings);
			tabControl.AddPage(pnlResults, "DB Schema");

			tabControl.AddPage(pnlRecords, "Download Records");
		}
		// }}}

		// {{{ SetupFormComponents
		public void SetupFormComponents()
		{
			mnuAbsinthe = new wx.MenuBar();

			mnuFile = new Menu();
			mnuSave = new MenuItem();
			mnuSaveAs = new MenuItem();
			mnuQuit = new MenuItem();
			mnuNew = new MenuItem();
			mnuOpen = new MenuItem();

			mnuTools = new Menu();	
			mnuInjOptions = new MenuItem();
			mnuProxyConfig = new MenuItem();
			
			mnuHelp = new Menu();
			mnuAbout = new MenuItem();

			mnuAbsinthe.Append(mnuFile, "File");
			mnuFile.Append(mnuNew.ID, "New");
			mnuFile.Append(mnuOpen.ID, "Open");
			mnuFile.Append(mnuSave.ID, "Save");
			mnuFile.Append(mnuSaveAs.ID, "Save As...");
			mnuFile.AppendSeparator();
			mnuFile.Append(mnuQuit.ID, "Quit");

			mnuAbsinthe.Append(mnuTools, "Tools");
			mnuTools.Append(mnuInjOptions.ID, "Injection Options");
			mnuTools.Append(mnuProxyConfig.ID, "Proxy Config");

			mnuAbsinthe.Append(mnuHelp, "Help");
			mnuHelp.Append(mnuAbout.ID, "About");
			
			this.MenuBar = mnuAbsinthe;

			CreateStatusBar(2);
		}
		// }}}

		// {{{ InitializeComponent
		public void InitializeComponent()
		{
			tabControl = new wx.Notebook(this);			

			InitializeTabs();
			SetupFormComponents();
			
			this.CenterOnScreen();

			BindEvents();

			_ActionQueue = new Queue();
		}
		// }}}

		// {{{ BindEvents
		private void BindEvents()
		{
			EVT_MENU(mnuAbout.ID, new wx.EventListener(this.OnAbout_Click));
			EVT_MENU(mnuSave.ID, new wx.EventListener(this.OnSave_Click));
			EVT_MENU(mnuSaveAs.ID, new wx.EventListener(this.OnSaveAs_Click));
			EVT_MENU(mnuQuit.ID, new wx.EventListener(this.OnQuit_Click));
			EVT_MENU(mnuNew.ID, new wx.EventListener(this.OnNew_Click));
			EVT_MENU(mnuOpen.ID, new wx.EventListener(this.OnOpen_Click));

			EVT_MENU(mnuInjOptions.ID, new EventListener(this.OnInjectionOptions_Click));
			EVT_MENU(mnuProxyConfig.ID, new EventListener(this.OnProxyConfig_Click));

			_GuiUiId = Window.UniqueID;
			EVT_UPDATE_UI(_GuiUiId, new EventListener(this.GuiCallbackEvent));
		}
		// }}}

		// {{{ SafeChangeSensitivity
		private void SafeChangeSensitivity(Window ctl, bool Enabled)
		{
			lock(_ActionQueue)
			{
				_ActionQueue.Enqueue(GuiActions.ControlEnableSwitch);
				_ActionQueue.Enqueue(ctl);
				_ActionQueue.Enqueue(Enabled);
			}

			lock(this)
			{
				this.EventHandler.AddPendingEvent(new UpdateUIEvent(_GuiUiId));
			}
		}
		// }}}

		// {{{ SafeMessageBoxWrite
		public void SafeMessageBoxWrite(string Message)
		{

			if (Message != null)
			{
				lock (_ActionQueue)
				{
					_ActionQueue.Enqueue(GuiActions.DialogPopup);
					_ActionQueue.Enqueue(Message);
				}

				lock (this)
				{
					this.EventHandler.AddPendingEvent(new UpdateUIEvent(_GuiUiId));
				}
			}
		}
		// }}}

		// {{{ SafeCursorChange
		public void SafeCursorChange(StockCursor NewCursor)
		{

			lock (_ActionQueue)
			{
				_ActionQueue.Enqueue(GuiActions.SwitchCursor);
				_ActionQueue.Enqueue(NewCursor);
			}

			lock (this)
			{
				this.EventHandler.AddPendingEvent(new UpdateUIEvent(_GuiUiId));
			}
		}
		// }}}

		// {{{ SafeStatusBarWrite
		public void SafeStatusBarWrite(string Message)
		{

			if (Message != null)
			{
				lock (_ActionQueue)
				{
					_ActionQueue.Enqueue(GuiActions.StatusMessage);
					_ActionQueue.Enqueue(Message);
				}

				lock (this)
				{
					this.EventHandler.AddPendingEvent(new UpdateUIEvent(_GuiUiId));
				}
			}
		}
		// }}}

		// {{{ SafeOutput
		private void SafeOutput(string Message)
		{
			Console.WriteLine(Message);
		}
		// }}}

		// {{{ GuiActions Enum
		private enum GuiActions : byte
		{
			StatusMessage = 1,
			ProgressIncrease = 2,
			ProgressClear = 3,
			ControlEnableSwitch = 4,
			ControlVisibleSwitch = 5,
			DialogPopup = 6,
			SwitchCursor = 7
		}
		// }}}

		// {{{ GuiCallbackEvent
		private void GuiCallbackEvent(object sender, Event e)
		{
			Window tmp;
			string Msg;
			
			lock (_ActionQueue)
			{
				while (_ActionQueue.Count > 0)
				{
					switch ((GuiActions) _ActionQueue.Dequeue())
					{
						case GuiActions.StatusMessage:
							Console.WriteLine("one");
							Msg = _ActionQueue.Dequeue().ToString();
							Console.WriteLine("two : {0}", Msg);
							if (this.StatusBar == null) {
								Console.WriteLine("two and a half");
								return;
								}
							try
							{
								this.StatusBar.SetStatusText(Msg, 0);
							}
							catch (NullReferenceException nre)
							{
								Console.WriteLine("Status bar failure");
							}
							Console.WriteLine("three");
							break;
						case GuiActions.ProgressIncrease:
							break;
						case GuiActions.ProgressClear:
							break;
						case GuiActions.ControlEnableSwitch:
							tmp = (Window) _ActionQueue.Dequeue();
							tmp.Enabled = (bool) _ActionQueue.Dequeue();
							break;
						case GuiActions.ControlVisibleSwitch:
							tmp = (Window) _ActionQueue.Dequeue();
							tmp.Show((bool) _ActionQueue.Dequeue());
							break;
						case GuiActions.DialogPopup:
							Msg = _ActionQueue.Dequeue().ToString();
							MessageBoxWrite(Msg);
							break;
						case GuiActions.SwitchCursor:
							Cursor = new Cursor((StockCursor) _ActionQueue.Dequeue());
							break;
					}
				}
			}
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

		// {{{ OnOpen_Click
		void OnOpen_Click(object sender, wx.Event e)
		{
			OnNew_Click(sender, e);
			FileDialog openFile = new FileDialog(this, "Select a file to open...", "", "", "Xml Files (*.xml)|*.xml|All Files (*.*)|*.*", FileDialogStyle.wxOPEN | FileDialogStyle.wxFILE_MUST_EXIST);
			if (openFile.ShowModal() != Dialog.wxID_OK) return;

			string Filename = openFile.Path;

			GlobalDS.OutputStatusDelegate safeout = new GlobalDS.OutputStatusDelegate(SafeOutput);

			try
			{
				_SaveInfo.LoadXmlFile(Filename, safeout, _AppSettings.ProxyQueue());
			}
			catch (DataStore.InvalidDataFileException idfe)
			{
				MessageBoxWrite(idfe.Message());
			}
			catch (Exception ex)
			{
				System.Console.WriteLine(ex.ToString());
			}

			try
			{
				pnlInjection.LoadDataFromStore(ref _SaveInfo);
				pnlResults.LoadDataFromStore(ref _SaveInfo);
				pnlRecords.LoadDataFromStore(ref _SaveInfo);
			}
			catch (Exception ex)
			{
				System.Console.WriteLine(ex.ToString());
			}
			
			
		}
		// }}}

		// {{{ OnSave_Click
		void OnSave_Click(object sender, wx.Event e)
		{
			if (_SaveInfo.OutputFile.Length == 0)
			{
				OnSaveAs_Click(sender, e);
				return;
			}

			pnlInjection.PrepareForSave();
			pnlResults.PrepareForSave();

			try
			{
				_SaveInfo.OutputToFile(pnlInjection.PluginText);
			}
			catch (Exception ex)
			{
				System.Console.WriteLine(ex.ToString());
			}
		}
		// }}}

		// {{{ OnSaveAs_Click
		void OnSaveAs_Click(object sender, wx.Event e)
		{
			//FileDialog saveFile = new FileDialog(this, "Select a file to save...", "", "", "Xml Files (*.xml)|*.xml|All Files (*.*)|*.*", FileDialogStyle.wxSAVE );
			
			try
			{

				FileDialog saveFile = new FileDialog(this, "Select filename to save as...", "", "", "Absinthe Xml Files (*.xml)|*.xml|All Files (*.*)|*.*", FileDialogStyle.wxSAVE | FileDialogStyle.wxOVERWRITE_PROMPT);
				
				if (saveFile.ShowModal() != Dialog.wxID_OK) return;
	
				string Filename = saveFile.Path;
				if (Filename.Length > 0)
				{
					_SaveInfo.OutputFile = Filename;
	
					OnSave_Click(sender, e);
				}
			}
			catch (Exception ex)
			{
				System.Console.WriteLine("not good");
				System.Console.WriteLine(ex.ToString());
			}
		}
		// }}}

		// {{{ OnInjectionOptions_Click
		void OnInjectionOptions_Click(object sender, wx.Event e)
		{
			InjectionOptionsDialog iod = new InjectionOptionsDialog(this, ref _SaveInfo);
			iod.ShowModal();
		}
		// }}}

		// {{{ OnConfigProxy_Click
		void OnProxyConfig_Click(object sender, wx.Event e)
		{
			ProxyConfigDialog pcd = new ProxyConfigDialog(this, ref _AppSettings);
			pcd.ShowModal();
		}
		// }}}

		// {{{ OnNew_Click
		void OnNew_Click(object sender, wx.Event e)
		{
			// new
			/*
			   lstParams.Items.Clear();
			   lstCookies.Items.Clear();
			   lstAvailFields.Items.Clear();
			   lstSelectedFields.Items.Clear();*/
			/*
			   txtTargetURL.Value = null;


			   chkUseSsl.Value = false;

			   optConnectPost.Value = false;
			   optConnectGet.Value = false;
			   optBlindInjection.Value = true;
			   optErrorBasedInjection.Value = false;
			 */
			//tvDBSchema.Nodes.Clear();		
			/*tvDBSchema.Nodes.AddRange(new System.Windows.Forms.TreeNode[] {
			  new System.Windows.Forms.TreeNode("Database", new System.Windows.Forms.TreeNode[] {
			  new System.Windows.Forms.TreeNode("Username"),
			  new System.Windows.Forms.TreeNode("Tables")})});
			 */
			_SaveInfo = new DataStore(new GlobalDS.OutputStatusDelegate(SafeOutput));		
			//tvDBSchema.
		}
		// }}}

		// {{{ OnAbout_Click
		void OnAbout_Click(object sender, wx.Event e)
		{
			AboutDialog ad = new AboutDialog(this, (PluginTemplate[]) _SaveInfo.PluginList.ToArray(typeof(PluginTemplate)));
			ad.ShowModal();
		}
		// }}}

		private void OnQuit_Click(object Sender, Event evt)
		{
			this.Close();
		}

}

		// {{{ MyApp Class
		// Define a new	application	type, each program should derive a class from App
		public class MyApp : wx.App
		{

			public override bool OnInit()
			{
				AbsintheForm frame = new AbsintheForm();
				frame.Show(true);
				// Leave this out for now
				//frame.Icon = new wx.Icon("Absinthe.ico");
				return true;
			}

			[STAThread]
				static void Main()
				{
					MyApp app = new MyApp();
					app.Run();
				}
		}
		// }}}
