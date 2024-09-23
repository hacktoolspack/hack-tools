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

namespace Absinthe.Core.TSQL
{
	class ErrorStrings
	{
		// This is the error string generated when "' HAVING 1=1--" or similar is appended
		public const string HAVING_ERROR_PRE = "[Microsoft][ODBC SQL Server Driver][SQL Server]Column '";
		public const string HAVING_ERROR_PRE2 = "Microsoft OLE DB Provider for SQL Server (0x80040E14)<br>Column '";
		public const string HAVING_ERROR_POST = "' is invalid in the select list because it is not contained in an aggregate function and there is no GROUP BY clause.";
		public const string HAVING_ERROR_POST2 = "' is invalid in the select list because it is not contained in either an aggregate function or the GROUP BY clause.";

		public const string UNION_SUM_ERROR_PRE = "[Microsoft][ODBC SQL Server Driver][SQL Server]The sum or average aggregate operation cannot take a ";
		public const string UNION_SUM_ERROR_PRE2 = "[Microsoft][ODBC SQL Server Driver][SQL Server]All queries in an SQL statement containing a UNION operator must have an equal number of expressions in their target lists.";
		public const string UNION_SUM_ERROR_PRE3 = "Microsoft OLE DB Provider for SQL Server (0x80040E07)<br>The sum or average aggregate operation cannot take a ";
		public const string UNION_SUM_ERROR_PRE4 = "<font face=\"Arial\" size=2>Column '";
		public const string UNION_SUM_ERROR_POST = " data type as an argument.";
		
		// This error is generated with nvarchars such as @@version.. 
		public const string UNION_SELECT_ERROR_NVAR_PRE = "[Microsoft][ODBC SQL Server Driver][SQL Server]Syntax error converting the nvarchar value '";
		public const string UNION_SELECT_ERROR_PRE = "[Microsoft][ODBC SQL Server Driver][SQL Server]Syntax error converting the varchar value '";
		public const string UNION_SELECT_ERROR_POST = "' to a column of data type int.";
	}

	/*
	public enum DataType : byte
	{
		Undefined = 0,
		Int = 1,
		TinyInt = 2,
		BigInt = 3,
		VarChar = 4,
		Bit = 5,
		Real = 6, // Is Real the correct data type to use?
		DateTime = 7,
		nVarChar = 8,
		Char = 9,
		Decimal = 10,
		Binary = 11,
		Image = 12,
		Money = 13,
		nChar = 14,
		nText = 15,
		Numeric = 16,
		Float = 17
		
	}
	*/
}
