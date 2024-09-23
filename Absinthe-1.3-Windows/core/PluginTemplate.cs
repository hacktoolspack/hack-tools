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

namespace Absinthe.Core
{
	
	// {{{ PluginTemplate Class
	public abstract class PluginTemplate
	{
		// I think these should be static, but it can't be both abstract and static
		public abstract string AndEqualWrapper(string Value);

		public abstract string AndGreaterThanWrapper(string Value);
		
		public abstract string AndGreaterThanEqualWrapper(string Value);

		public abstract string AndIsNullWrapper(string Value);

		public abstract string NextLowestTableID(long PrevTableID);
		
		public abstract string NextLowestFieldID(long TableID, long PrevFieldID);

		public abstract string TableNameLength(long TableID);
		
		public abstract string TableNameCharacterValue(long Index, long TableID);

		public abstract string NumberOfRecords(string TableName);

		public abstract string PrimaryKeyColumn(long TableID);

		public abstract string FieldDataType(long FieldID, long TableID);

		public abstract string FieldNameLength(long FieldID, long TableID);

		public abstract string FieldNameCharacterValue(long Index, long FieldID, long TableID);

		public abstract string NumberOfTables();

		public abstract string NumberOfFieldsInTable(long TableID);

		public abstract string LengthOfConvertedPrimaryKeyValue(string KeyName, string TableName);

		public abstract string LengthOfConvertedPrimaryKeyValue(string KeyName, string TableName, string PrevKeyValue);

		public abstract string ConvertedPrimaryKeyValueCharacter(long Index, string KeyName, string TableName);

		public abstract string ConvertedPrimaryKeyValueCharacter(long Index, string KeyName, string TableName, string PrevKeyValue);

		public abstract string IntegerPrimaryKeyValue(string KeyName, string TableName);

		public abstract string IntegerPrimaryKeyValue(string KeyName, string TableName, string PrevKeyValue);

//		public abstract string CheckRecordForNull(string Value);

		public abstract string PluginDisplayTargetName{ get; }

		public abstract string AuthorName{ get; }

		public abstract string SelectValueForGivenPrimaryKey( string FieldName, string TableName, GlobalDS.PrimaryKey pk);
		
		public abstract string SelectLengthOfValueForGivenPrimaryKey(string FieldName, string TableName, GlobalDS.PrimaryKey pk);
		
		public abstract string SelectCharacterValueForGivenPrimaryKey(long Index, string FieldName, string TableName, GlobalDS.PrimaryKey pk);

		public abstract string SelectLengthOfConvertedRecordValue(string FieldName, string TableName, GlobalDS.PrimaryKey pk);

		public abstract string SelectCharacterValueForConvertedRecordValue(long Index, string FieldName, string TableName, GlobalDS.PrimaryKey pk);

		public abstract string ConcatenationCharacter
		{
			get;
		}

		public abstract string CharConversionFunction(long DecimalValue);

		public abstract System.Data.SqlDbType ConvertNativeDataType(long DataType);

		public abstract string SelectDatabaseUsernameLength();

		public abstract string SelectCharacterFromDatabaseUsername(long Index);
	}
	// }}}

	public class UnsupportedPluginException : Exception
	{
		private string _Message;

		public UnsupportedPluginException(string Message)
		{
			_Message = Message;
		}

		public override string Message
		{
			get
			{
				return _Message;
			}
		}
	}
}
