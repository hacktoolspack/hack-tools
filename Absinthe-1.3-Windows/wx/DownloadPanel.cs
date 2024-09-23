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
using System.Threading;

using wx;
using Absinthe.Core;

public class DownloadPanel : Panel
{

		// {{{ Control Declarations
		private Button butFileBrowse;
		private Button butRemoveDlField;
		private Button butPullData;
		private Button butAddDlField;
		private ListCtrl lstSelectedFields;
		private StaticText lblFilename;
		private ListCtrl lstAvailFields;
		private TextCtrl txtPullDataXml;
		private BoxSizer PanelSizer;
		// }}}


		int _AvailFieldsIndex = -1;
		int _DlFieldsIndex = -1;
		DataStore _SaveInfo;
		AbsintheForm.GuiControls _GuiActions;
		private delegate void ThreadedSub();

      	// {{{ Constructor
		public DownloadPanel(Window Parent, ref DataStore SaveInfo, AbsintheForm.GuiControls ga) : base (Parent, -1)
		{
			_SaveInfo = SaveInfo;
			_GuiActions = ga;
			InitializeComponent();
		}
		// }}}

		// {{{ SetupFieldLists
		private BoxSizer SetupFieldLists()
		{
			BoxSizer FieldListSizer = new BoxSizer(Orientation.wxHORIZONTAL);
		
			StaticBox sbx2 = new wx.StaticBox(this, "Available Fields:", wxDefaultPosition, wxDefaultSize, wx.Alignment.wxALIGN_TOP|wx.Alignment.wxALIGN_LEFT);
			StaticBoxSizer sizSbx2 = new StaticBoxSizer(sbx2, Orientation.wxVERTICAL);
			
			lstAvailFields = new wx.ListView(this, wxDefaultPosition, new System.Drawing.Size(192, 256));
			sizSbx2.Add(lstAvailFields, 0, Stretch.wxEXPAND, 0);
			
			StaticBox sbx3 = new wx.StaticBox(this, "Selected Fields", wxDefaultPosition, wxDefaultSize, wx.Alignment.wxALIGN_TOP|wx.Alignment.wxALIGN_LEFT);
			StaticBoxSizer sizSbx3 = new StaticBoxSizer(sbx3, Orientation.wxVERTICAL);

			lstSelectedFields = new wx.ListView(this, wxDefaultPosition, new System.Drawing.Size(192, 256));
			sizSbx3.Add(lstSelectedFields, 0, Stretch.wxEXPAND, 0);
			
			BoxSizer bx = new BoxSizer(Orientation.wxVERTICAL);
			butAddDlField = new wx.Button(this, "Add", wxDefaultPosition, new System.Drawing.Size(72, 23));
			butRemoveDlField = new wx.Button(this, "Remove", wxDefaultPosition, new System.Drawing.Size(72, 23));
			bx.Add(butAddDlField, 0, Direction.wxALL | Alignment.wxALIGN_CENTRE_VERTICAL, 4);
			bx.Add(butRemoveDlField, 0, Direction.wxALL | Alignment.wxALIGN_CENTRE_VERTICAL, 4);

			FieldListSizer.Add(sizSbx2, 0, Direction.wxALL, 4);
			FieldListSizer.Add(bx, 0, Direction.wxALL | Alignment.wxALIGN_CENTRE_VERTICAL, 4);
			FieldListSizer.Add(sizSbx3, 0, Direction.wxALL, 4);

			lstAvailFields.InsertColumn(0, "Table");
			lstAvailFields.InsertColumn(1, "Field");
			lstAvailFields.InsertColumn(2, "Field Id");
							
			lstSelectedFields.InsertColumn(0, "Table");
			lstSelectedFields.InsertColumn(1, "Field");
			lstSelectedFields.InsertColumn(2, "Field Id");

			return FieldListSizer;
		}
		// }}}

		// {{{ InitializeComponent
		private void InitializeComponent()
		{
			PanelSizer = new BoxSizer(Orientation.wxVERTICAL);

			StaticBox sbx1 = new wx.StaticBox(this, "Output:", new System.Drawing.Point(8, 64), wxDefaultSize, wx.Alignment.wxALIGN_TOP|wx.Alignment.wxALIGN_LEFT);
			StaticBoxSizer sizSchema = new StaticBoxSizer(sbx1, Orientation.wxHORIZONTAL);
			
			lblFilename = new wx.StaticText(this, "Filename:", wxDefaultPosition, wxDefaultSize, wx.Alignment.wxALIGN_TOP|wx.Alignment.wxALIGN_LEFT);
			sizSchema.Add(lblFilename, 0, Direction.wxALL, 4);
			
			txtPullDataXml = new wx.TextCtrl(this, "", wxDefaultPosition, new System.Drawing.Size(360, 20), wx.Alignment.wxALIGN_TOP|wx.Alignment.wxALIGN_LEFT);
			sizSchema.Add(txtPullDataXml, 0, Direction.wxALL, 4);
			
			butFileBrowse = new wx.Button(this, "Browse ...", wxDefaultPosition, wxDefaultSize);
			sizSchema.Add(butFileBrowse, 0, Direction.wxALL, 4);

			PanelSizer.Add(sizSchema, 0, Stretch.wxEXPAND | Direction.wxALL | Alignment.wxALIGN_CENTER, 4);

			PanelSizer.Add(SetupFieldLists(), 0, Direction.wxALL | Alignment.wxALIGN_CENTER, 4);

			butPullData = new wx.Button(this, "Download Fields to XML", new System.Drawing.Point(184, 360), wxDefaultSize);
			PanelSizer.Add(butPullData, 0, Direction.wxALL | Alignment.wxALIGN_CENTER, 4);

			SetSizer(PanelSizer);

			BindEvents();
		}
		// }}}

		// {{{ BindEvents
		private void BindEvents()
		{
			EVT_BUTTON(butFileBrowse.ID, new EventListener(OnBrowseDatapull_Click));
			EVT_BUTTON(butPullData.ID, new EventListener(OnPullData_Click));
			EVT_BUTTON(butAddDlField.ID, new EventListener(OnAddDlField_Click));
			EVT_BUTTON(butRemoveDlField.ID, new EventListener(OnRemoveDlField_Click));
			
			lstSelectedFields.ItemSelect += new EventListener( OnSelectedField_Click );
			lstAvailFields.ItemSelect += new EventListener( OnAvailField_Click );
		}
		// }}}

		// {{{ OnPullData_Click
		private void OnPullData_Click(object sender, wx.Event e)
		{

			Console.WriteLine("boo");
			if (txtPullDataXml.Value.Length > 0)
			{
				ThreadedSub a = new ThreadedSub(PullDataFromTables);
				a.BeginInvoke(null, new object());
			}
			else
			{
				_GuiActions.MessageBox("Please select a file!");			
			}
		}
		// }}}

		// {{{ PullDataFromTables
		private void PullDataFromTables()
		{
			Hashtable TableSet = new Hashtable();
			string TableName, FieldName;
			long FieldID;
			ArrayList al;


			for (int cnt = 0; cnt < lstSelectedFields.ItemCount; cnt++)
			{
				ListItem li = new ListItem();
				li.Id = cnt;

				li.Column = 0;
				li.Mask = ListCtrl.wxLIST_MASK_TEXT;
				lstSelectedFields.GetItem(ref li);
				TableName = li.Text;
				
				li.Column = 1;
				li.Mask = ListCtrl.wxLIST_MASK_TEXT;
				lstSelectedFields.GetItem(ref li);
				FieldName = li.Text;

				// Do we need this?
				li.Column = 2;
				li.Mask = ListCtrl.wxLIST_MASK_TEXT;
				lstSelectedFields.GetItem(ref li);
				FieldID = Int64.Parse(li.Text) + 1L;
				
				// add fieldid to stuff.
				if (!TableSet.ContainsKey(TableName))
				{
					al = new ArrayList();
					TableSet.Add(TableName, al);
				}

				al = (ArrayList) TableSet[TableName];
				al.Add(FieldID);
				TableSet[TableName] = al;

			}

			int TabCount = 0;
			ArrayList ColAl, TblAl;
			ColAl = new ArrayList();
			TblAl = new ArrayList();

			foreach (string tab in TableSet.Keys)
			{
				long[] ColumnList = (long[]) ((ArrayList) TableSet[tab]).ToArray(typeof(long));
				TblAl.Add(_SaveInfo.GetTableFromName(tab));
				ColAl.Add( (long[]) ((ArrayList) TableSet[tab]).ToArray(typeof(long)));

				TabCount++;	
			}

			_SaveInfo.TargetAttackVector.PullDataFromTable((GlobalDS.Table[]) TblAl.ToArray(typeof(GlobalDS.Table)), (long[][]) ColAl.ToArray(typeof(long[])), txtPullDataXml.Value);

			_GuiActions.MessageBox("Data Retrieved");
		}
		// }}}

		// {{{ OnBrowseDatapull_Click
		private void OnBrowseDatapull_Click(object sender, wx.Event e)
		{
			FileDialog saveFile = new FileDialog(this, "Select filename to save as...", "", "", "Absinthe Xml Files (*.xml)|*.xml|All Files (*.*)|*.*", FileDialogStyle.wxSAVE | FileDialogStyle.wxOVERWRITE_PROMPT);

			if (saveFile.ShowModal() != Dialog.wxID_OK) return;

			txtPullDataXml.Value = saveFile.Path;
		}
		// }}}

		// {{{ ReloadAvailableFields
		public void ReloadAvailableFields()
		{	
			lstAvailFields.DeleteAllItems();
			lstSelectedFields.DeleteAllItems();
			if (_SaveInfo.TableList == null) return;
			for (int i = 0; i < _SaveInfo.TableList.Length; i++)
			{
				if (_SaveInfo.TableList[i].FieldCount > 0)
				{
					GlobalDS.Field[] FieldList = _SaveInfo.TableList[i].FieldList;
					for (int j = 0; j < _SaveInfo.TableList[i].FieldCount; j++)
					{
						string FieldName = FieldList[j].FieldName;
						int FieldId = j;
						lstAvailFields.InsertItem(lstAvailFields.ItemCount, _SaveInfo.TableList[i].Name);
						lstAvailFields.SetItem(lstAvailFields.ItemCount - 1, 1, FieldName);
						lstAvailFields.SetItem(lstAvailFields.ItemCount - 1, 2, FieldId.ToString());
					}
				}
			}
		}
		// }}}

		// {{{ OnAddDlField_Click
		private void OnAddDlField_Click(object sender, wx.Event e)
		{
			MoveForDownload(ref lstAvailFields, ref lstSelectedFields);
			//SwapFieldEntries(ref lstAvailFields, ref lstSelectedFields);
		}
		// }}}
		
		// {{{ OnAvailField_Click
		private void OnAvailField_Click(object sender, wx.Event e)
		{
			ListEvent le = e as ListEvent;
			
			if ((lstAvailFields.ItemCount > 0) && (le.Index <= lstAvailFields.ItemCount))
			{
				_AvailFieldsIndex = le.Index;
			}
			else
			{
				_AvailFieldsIndex = -1;
			}
		}
		// }}}
		
		// {{{ OnSelectedField_Click
		private void OnSelectedField_Click(object sender, wx.Event e)
		{
			ListEvent le = e as ListEvent;
			
			if ((lstSelectedFields.ItemCount > 0) && (le.Index <= lstSelectedFields.ItemCount))
			{
				_DlFieldsIndex = le.Index;
			}
			else
			{
				_DlFieldsIndex = -1;
			}
		}
		// }}}
		
		// {{{ MoveForDownload
		private void MoveForDownload(ref ListCtrl Source, ref ListCtrl Target)
		{
			int SelectedIndex = -1;
			
			SelectedIndex = _AvailFieldsIndex;

			if ((SelectedIndex == -1) || (Source.ItemCount == 0) || (SelectedIndex > Source.ItemCount))
			{
				_GuiActions.MessageBox("Please select a field.");
				return;
			}

			ListItem li = new ListItem();

			li.Id = SelectedIndex;
			li.Mask = ListCtrl.wxLIST_MASK_TEXT;
			li.Column = 0;
			Source.GetItem(ref li);
			if (li.Text != null)
			{
				Target.InsertItem(Target.ItemCount, li.Text);
	
				li.Column = 1;
				li.Mask = ListCtrl.wxLIST_MASK_TEXT;
				Source.GetItem(ref li);
				Target.SetItem(Target.ItemCount -1, 1, li.Text);
	
				li.Column = 2;
				li.Mask = ListCtrl.wxLIST_MASK_TEXT;
				Source.GetItem(ref li);
				Target.SetItem(Target.ItemCount -1, 2, li.Text);
	
				Source.DeleteItem(SelectedIndex);
			}
			
			
		}
		// }}}

		// {{{ MoveFromDownload
		private void MoveFromDownload(ref ListCtrl Source, ref ListCtrl Target)
		{
			int SelectedIndex = -1;
			
			SelectedIndex = _DlFieldsIndex;

			if (SelectedIndex == -1 || (Source.ItemCount == 0) || SelectedIndex > Source.ItemCount)
			{
				_GuiActions.MessageBox("Please select a field.");
				return;
			}

			ListItem li = new ListItem();

			li.Id = SelectedIndex;
			li.Mask = ListCtrl.wxLIST_MASK_TEXT;
			li.Column = 0;
			Source.GetItem(ref li);
			Target.InsertItem(Target.ItemCount, li.Text);

			li.Column = 1;
			li.Mask = ListCtrl.wxLIST_MASK_TEXT;
			Source.GetItem(ref li);
			Target.SetItem(Target.ItemCount -1, 1, li.Text);

			li.Column = 2;
			li.Mask = ListCtrl.wxLIST_MASK_TEXT;
			Source.GetItem(ref li);
			Target.SetItem(Target.ItemCount -1, 2, li.Text);

			Source.DeleteItem(SelectedIndex);
			
			
		}
		// }}}

		// {{{ SwapFieldEntries
		private void SwapFieldEntries(ref ListCtrl Source, ref ListCtrl Target)
		{
			int SelectedIndex = -1;
			
			SelectedIndex = _AvailFieldsIndex;
			//SelectedIndex = Source.GetNextItem(SelectedIndex, ListCtrl.wxLIST_NEXT_ALL, ListCtrl.wxLIST_STATE_SELECTED);

			if (SelectedIndex == -1)
			{
				_GuiActions.MessageBox("Please select a field.");
				return;
			}

			ListItem li = new ListItem();

			li.Id = SelectedIndex;
			li.Mask = ListCtrl.wxLIST_MASK_TEXT;
			li.Column = 0;
			Source.GetItem(ref li);
			Target.InsertItem(Target.ItemCount, li.Text);

			li.Column = 1;
			li.Mask = ListCtrl.wxLIST_MASK_TEXT;
			Source.GetItem(ref li);
			Target.SetItem(Target.ItemCount -1, 1, li.Text);

			li.Column = 2;
			li.Mask = ListCtrl.wxLIST_MASK_TEXT;
			Source.GetItem(ref li);
			Target.SetItem(Target.ItemCount -1, 2, li.Text);

			Source.DeleteItem(SelectedIndex);
		}
		// }}}

		// {{{ OnRemoveDlField_Click
		private void OnRemoveDlField_Click(object sender, wx.Event e)
		{
			MoveFromDownload(ref lstSelectedFields, ref lstAvailFields);
		}
		// }}}

		// {{{ LoadDataFromStore
		public void LoadDataFromStore(ref DataStore SaveInfo)
		{	
			_SaveInfo = SaveInfo;
			ReloadAvailableFields();
		}
		// }}}
}
