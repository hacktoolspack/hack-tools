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

using wx;
using Absinthe.Core;

public class SchemaPanel : Panel
{

	// {{{ Control Declarations
	private StaticBoxSizer sizActions;
	private BoxSizer sizSchema;
	
	private Button butGetUserName;
	private Button butLoadTableInfo;
	private Button butLoadFieldInfo;
	private TreeCtrl tvwDBSchema;
	// }}}

	DataStore _SaveInfo;
	AbsintheForm.GuiControls _GuiActions;
	Absinthe.LocalSettings _AppSettings;
	private TreeItemId _RootNode;
	private TreeItemId _UsernameNode;
	private TreeItemId _TableNode;
	TreeItemId[] _TableSectionIds;

	private int _LocalGuiId;
	private Queue _LocalGuiQueue;

	private delegate void ThreadedSub();

	// {{{ Constructor
	public SchemaPanel(Window Parent, ref DataStore SaveInfo, AbsintheForm.GuiControls ga, ref Absinthe.LocalSettings _AppSettings) : base (Parent)
	{
		_GuiActions = ga;
		_SaveInfo = SaveInfo;
		_LocalGuiQueue = new Queue();
		InitializeComponent();
		BindEvents();
	}
	// }}}

	// {{{ BindEvents
	private void BindEvents()
	{
		EVT_BUTTON(butGetUserName.ID, new EventListener(this.GetNameClick));
		EVT_BUTTON(butLoadTableInfo.ID, new EventListener(this.GetTablesClick));
		EVT_BUTTON(butLoadFieldInfo.ID, new EventListener(this.OnLoadFieldInfo_Click));

		_LocalGuiId = Window.UniqueID;
		EVT_UPDATE_UI(_LocalGuiId, new EventListener(this.GuiUpdateEvent));
	}
	// }}}

	// {{{ LocalGuiAction
	private enum LocalGuiAction : byte
	{
		TableInfo,
		FieldInfo,
		UsernameInfo
	}
	// }}}

	// {{{ InitializeComponent
	private void InitializeComponent()
	{
		sizSchema = new BoxSizer(Orientation.wxVERTICAL);

		StaticBox sbx = new wx.StaticBox(this, "Actions:", new System.Drawing.Point(8, 8), new System.Drawing.Size(512, 48), wx.Alignment.wxALIGN_TOP|wx.Alignment.wxALIGN_LEFT);

		sizActions = new StaticBoxSizer(sbx, Orientation.wxHORIZONTAL);

		butGetUserName = new wx.Button(this, "Retrieve Username", wxDefaultPosition, wxDefaultSize);
		sizActions.Add(butGetUserName, 0, Stretch.wxEXPAND | Direction.wxALL, 2);

		butLoadTableInfo = new wx.Button(this, "Load Table Info", wxDefaultPosition, wxDefaultSize);
		sizActions.Add(butLoadTableInfo, 0, Stretch.wxEXPAND | Direction.wxALL, 2);

		butLoadFieldInfo = new wx.Button(this, "Load Field Info", wxDefaultPosition, wxDefaultSize);
		sizActions.Add(butLoadFieldInfo, 0, Stretch.wxEXPAND | Direction.wxALL, 2);
		butLoadFieldInfo.Enabled = false;

		sizSchema.Add(sizActions, 0, Direction.wxALL | Stretch.wxEXPAND, 4);

		tvwDBSchema = new wx.TreeCtrl(this, wxDefaultPosition, new System.Drawing.Size(496, 288));

		
		StaticBoxSizer sbs = new StaticBoxSizer(new StaticBox(this, ""), Orientation.wxHORIZONTAL);
		
		sbs.Add(tvwDBSchema, 0, Direction.wxALL | Stretch.wxEXPAND, 8);
		sizSchema.Add(sbs, 0, Direction.wxALL | Stretch.wxEXPAND, 4);

		InitializeTreeview();

		SetSizer(sizSchema);
	}
	// }}}

	// {{{ InitializeTreeview
	private void InitializeTreeview()
	{
		_RootNode = tvwDBSchema.AddRoot("Database");
		_UsernameNode = tvwDBSchema.AppendItem(_RootNode, "Username: ??? UNKNOWN ???");
		_TableNode = tvwDBSchema.AppendItem(_RootNode, "Tables:");
		tvwDBSchema.AppendItem(_TableNode, "??? UNKNOWN ???");
	}
	// }}}

	// {{{ RetrieveTableInfoFromDatabase
	private void RetrieveTableInfoFromDatabase()
	{
		try
		{
			_GuiActions.Enable(butLoadTableInfo, false);
			
			_GuiActions.Status("Gathering Table Information");
			if (_SaveInfo.TargetAttackVector != null)
			{
				_SaveInfo.TableList = _SaveInfo.TargetAttackVector.GetTableList();
				_LocalGuiQueue.Enqueue(LocalGuiAction.TableInfo);
				EventHandler.AddPendingEvent(new UpdateUIEvent(_LocalGuiId));
			}
			else
			{
				Console.WriteLine("This really shouldn't be null");
			}
			_GuiActions.Status("Finished Gathering Table Information");

			_GuiActions.Enable(butLoadFieldInfo, true);
		}
		catch (Exception e)
		{
			_GuiActions.MessageBox(e.Message);	
		}
		finally
		{
			_GuiActions.Enable(butLoadTableInfo, true);
		}
	}
	// }}}

	// {{{ SafelyLoadTableInfoList
	private void SafelyLoadTableInfoList()
	{		
		Console.WriteLine("About to load the table data");	
		tvwDBSchema.DeleteChildren(_TableNode);
		ArrayList IdList = new ArrayList();

		for (int i=0; i < _SaveInfo.TableList.Length; i++)
		{
			TreeItemId tid = tvwDBSchema.AppendItem(_TableNode, _SaveInfo.TableList[i].Name);

			tvwDBSchema.AppendItem(tid, "ID: " + _SaveInfo.TableList[i].ObjectID.ToString());
			tvwDBSchema.AppendItem(tid, "Record Count: " + _SaveInfo.TableList[i].RecordCount.ToString());
			TreeItemId fid = tvwDBSchema.AppendItem(tid, "Fields");
			tvwDBSchema.AppendItem(fid, "??? UNKNOWN ???");

			IdList.Add(tid);
		}
		_TableSectionIds = (TreeItemId[]) IdList.ToArray(typeof(TreeItemId));
	}
	// }}}

	// {{{ LoadSchemaData
	public void LoadDataFromStore(ref DataStore SaveInfo)
	{
		_SaveInfo = SaveInfo;
	
		if (_SaveInfo.Username != null && _SaveInfo.Username.Length > 0)
		{
			SafelyUpdateUsername();
		}

		if (_SaveInfo.TableList != null)
		{
			SafelyLoadTableInfoList();
			butLoadFieldInfo.Show(true); // Explicit in case it wasn't called properly
			butLoadFieldInfo.Enabled = true; 
			EVT_BUTTON(butLoadFieldInfo.ID, new EventListener(this.OnLoadFieldInfo_Click));
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

	// {{{ GuiUpdateEvent
	private void GuiUpdateEvent(object Sender, Event e)
	{
		LocalGuiAction LoadedAction;
		
		lock(_LocalGuiQueue)
		{
			LoadedAction = (LocalGuiAction) _LocalGuiQueue.Dequeue();

			switch(LoadedAction)
			{
				case LocalGuiAction.TableInfo:
					Console.WriteLine("About to load the table info");
					SafelyLoadTableInfoList();
					break;
				case LocalGuiAction.FieldInfo:
					int TableIndex; TreeItemId TableNode;
					TableIndex = (int) _LocalGuiQueue.Dequeue();
					TableNode = (TreeItemId) _LocalGuiQueue.Dequeue();
					PopulateFieldView(TableIndex, TableNode);
					break;
				case LocalGuiAction.UsernameInfo:
					SafelyUpdateUsername();
					break;
			}
		}
	}
	// }}}

	// {{{ SafelyUpdateUsername
	private void SafelyUpdateUsername()
	{
		tvwDBSchema.SetItemText(_UsernameNode, "Username: " + _SaveInfo.Username);
	}
	// }}}

	// {{{ RetrieveUsernameFromDatabase
	private void RetrieveUsernameFromDatabase()
	{
		_GuiActions.Cursor(StockCursor.wxCURSOR_WAIT);

		try
		{
			_GuiActions.Status("Retrieving username");

			if (_SaveInfo.TargetAttackVector != null)
			{
				_SaveInfo.Username = _SaveInfo.TargetAttackVector.GetDatabaseUsername();
				
				_LocalGuiQueue.Enqueue(LocalGuiAction.UsernameInfo);
				EventHandler.AddPendingEvent(new UpdateUIEvent(_LocalGuiId));
			}
			else
			{
				_GuiActions.MessageBox("Please initialize the system!");
				_GuiActions.Cursor(StockCursor.wxCURSOR_ARROW);
				return;
			}
		}
		catch (Exception e)
		{
			_GuiActions.MessageBox(e.Message);
			_GuiActions.Cursor(StockCursor.wxCURSOR_ARROW);
			throw e;
		}
		_GuiActions.Status("Username retrieved");
		_GuiActions.Cursor(StockCursor.wxCURSOR_ARROW);
		// TO DO: expand the DB treeview 
	}
	// }}}

	// {{{ GetTablesClick
	private void GetTablesClick(object sender, wx.Event e)
	{
		ThreadedSub a = new ThreadedSub(RetrieveTableInfoFromDatabase);
		a.BeginInvoke(null, new object());
	}
	// }}}

	// {{{ GetNameClick
	private void GetNameClick(object sender, wx.Event e)
	{
		ThreadedSub a = new ThreadedSub(RetrieveUsernameFromDatabase);
		a.BeginInvoke(null, new object());
	}
	// }}}

	// {{{ OnLoadFieldInfo_Click
	public void OnLoadFieldInfo_Click(object sender, wx.Event e)
	{
		ThreadedSub a = new ThreadedSub(LoadFieldData);
		a.BeginInvoke(null, new object());
	}
	// }}}

	// {{{ LoadFieldData
	private void LoadFieldData()
	{
		int Index = 0;
		

		if (_SaveInfo.TargetAttackVector != null && _SaveInfo.TableList != null)
		{
			//TreeItemId SelectedId = null;
			
			/* Give us the current selection */
			TreeItemId item = tvwDBSchema.Selection;
			
			//if (tvwDBSchema.GetItemParent(item).GetItemText == "Tables:")
			// Chec the great-grandparent ID
			if (tvwDBSchema.GetItemText(tvwDBSchema.GetItemParent(tvwDBSchema.GetItemParent(tvwDBSchema.GetItemParent(item)))) == "Tables:")			
			{
				item = tvwDBSchema.GetItemParent(tvwDBSchema.GetItemParent(item));
			}	
		
			// Check the grandparent ID 
			if (tvwDBSchema.GetItemText(tvwDBSchema.GetItemParent(tvwDBSchema.GetItemParent(item))) == "Tables:")
			{
				item = tvwDBSchema.GetItemParent(item);
			}
			
			// else it wa sthe parent
			
			System.Console.WriteLine(tvwDBSchema.GetItemText(item));

			
			/*if (item == null)
			{
				_GuiActions.MessageBox("Please select a table name first");
				return;
			}*/

			System.Console.WriteLine("Should be in now");

			// Only load fields if they haven't been loaded yet
			//System.IntPtr cookie = new System.IntPtr();

			//string FirstField;
			//FirstField = tvwDBSchema.GetItemText(tvwDBSchema.GetFirstChild(tvwDBSchema.GetLastChild(SelectedId), ref cookie));
			//_GuiActions.MessageBox("First Field: " + FirstField);

			//if (!FirstField.Equals("??? UNKNOWN ???")) 
			LoadFieldDataFromTableName(tvwDBSchema.GetItemText(item), tvwDBSchema.GetLastChild(item));

			/*try
			{
				
				foreach (TreeItemId tid in _TableSectionIds)
				{
					if (tvwDBSchema.IsSelected(tid) || CheckChildSelection(tid))
					{
						//_GuiActions.MessageBox(tvwDBSchema.GetItemText(tid));
						SelectedId = tid;
						break;
					}
					 
					Index += 1;
				}
				if (SelectedId == null)
				{
						_GuiActions.MessageBox("Please select a table name first");
						return;
				}
	
				_GuiActions.MessageBox("Bling");
				Console.WriteLine("Should be in now");
	
				// Only load fields if they haven't been loaded yet
				//System.IntPtr cookie = new System.IntPtr();
	
				//string FirstField;
				//FirstField = tvwDBSchema.GetItemText(tvwDBSchema.GetFirstChild(tvwDBSchema.GetLastChild(SelectedId), ref cookie));
				//_GuiActions.MessageBox("First Field: " + FirstField);
	
				//if (!FirstField.Equals("??? UNKNOWN ???")) 
				LoadFieldDataFromTableName(tvwDBSchema.GetItemText(SelectedId), tvwDBSchema.GetLastChild(SelectedId));
				//else
				//{
				//	Console.WriteLine("Field we want: {0}::{1}", FirstField, FirstField.IndexOf("??? UNKNOWN ???"));
				//	
				//}
			}
			catch (Exception e)
			{
				System.Console.WriteLine(e.ToString());
			}*/
			
			
		}
		else
		{
			_GuiActions.MessageBox("Unexpected error.  Please make sure Absinthe is initialized.");
		}
	}
	// }}}

	// {{{ CheckChildSelection
	private bool CheckChildSelection(TreeItemId tid)
	{
		TreeItemId[] ChildrenList;

		ChildrenList = tvwDBSchema.AllItemsBelow(tid);

		foreach(TreeItemId cid in ChildrenList)
		{
			if (tvwDBSchema.IsSelected(cid)) return true;
		}

		return false;
	}
	// }}}

	// {{{ LoadFieldDataFromTableName
	private void LoadFieldDataFromTableName(string TableName, TreeItemId TableNode)
	{
		Console.WriteLine("Loadin");
		
		for (int i=0; i < _SaveInfo.TableList.Length; i++)
		{
			if (_SaveInfo.TableList[i].Name.Equals(TableName))
			{
				if (_SaveInfo.TableList[i].FieldCount == 0)
				{
					_SaveInfo.TargetAttackVector.PopulateTableStructure(ref _SaveInfo.TableList[i]);
				}

				lock (_LocalGuiQueue)
				{
					_LocalGuiQueue.Enqueue(LocalGuiAction.FieldInfo);
					_LocalGuiQueue.Enqueue(i);
					_LocalGuiQueue.Enqueue(TableNode);
				}
				EventHandler.AddPendingEvent(new UpdateUIEvent(_LocalGuiId));

			}
		}
	}
	// }}}

	// {{{ PopulateFieldView
	private void PopulateFieldView(int TableIndex, TreeItemId TableNode)
	{
		Console.WriteLine("Populating FieldView");
	

		GlobalDS.Field[] FieldList = _SaveInfo.TableList[TableIndex].FieldList;

		tvwDBSchema.DeleteChildren(TableNode);

		// update the treeview
		for (int i = 0; i < _SaveInfo.TableList[TableIndex].FieldCount; i++)
		{
			string FieldName = FieldList[i].FieldName;
			string FieldType = FieldList[i].DataType.ToString();
			string FieldInfo = FieldName + " (" + FieldType + ")";

			tvwDBSchema.AppendItem(TableNode, FieldInfo);
			//TODO: Underline primary keys!!
		}

		_GuiActions.ReloadAvailableFields();
	}
	// }}}

	public void PrepareForSave()
	{
		// Everything should already be in the SaveInfo if the references held.
	}

}
