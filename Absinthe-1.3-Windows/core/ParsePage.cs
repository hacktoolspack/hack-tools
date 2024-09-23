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
using System.Collections;
using System.Data;

namespace Absinthe.Core
{

	///<summary>This class handles anything related to page comparisons</summary>
	public class ParsePage
	{

		// {{{ Error Based Stuff
/* Not going to worry about Error Based SQL Injection for now */
#if FULL_RELEASE
		// {{{ ParseUnionSumError
		/*
		public static System.Data.SqlDbType ParseUnionSumError(string HTMLCode, GlobalDS.OutputStatusDelegate ParentOutput)
		{
			SqlDbType retVal = new System.Data.SqlDbType();
			retVal = SqlDbType.Variant;

			int StartError, StartData, EndError, StartSize;
			string ErrorData;

			// Check for the first half of the error
			StartError = HTMLCode.IndexOf(TSQL.ErrorStrings.UNION_SUM_ERROR_PRE);
			StartSize = TSQL.ErrorStrings.UNION_SUM_ERROR_PRE.Length;
			if (StartError < 0)
			{
				StartError = HTMLCode.IndexOf(TSQL.ErrorStrings.UNION_SUM_ERROR_PRE3);
				StartSize = TSQL.ErrorStrings.UNION_SUM_ERROR_PRE3.Length;
			}
			if (StartError < 0)
			{
				StartError = HTMLCode.IndexOf(TSQL.ErrorStrings.UNION_SUM_ERROR_PRE4);
				StartSize = TSQL.ErrorStrings.UNION_SUM_ERROR_PRE4.Length;
			}


			if (StartError >= 0)
			{
				// Now check for the second half of the error
				EndError = HTMLCode.IndexOf(TSQL.ErrorStrings.UNION_SUM_ERROR_POST);
				if (EndError > StartError)
				{
					StartData = StartError + StartSize;
					ErrorData = HTMLCode.Substring(StartData, EndError - StartData);

					switch (ErrorData)
					{
						case "datetime":
							retVal = SqlDbType.Int;
						break;
						case "varchar":
							retVal = SqlDbType.VarChar;
						break;
						case "nvarchar":
							retVal = SqlDbType.NVarChar;
						break;
						case "bit":
							retVal = SqlDbType.Bit;
						break;
						case "char":
							retVal = SqlDbType.Char;
						break;
						default:
						ParentOutput(String.Format("Unknown Data Type of type: {0}", ErrorData));
						break;
					}
				}

			}
			else
			{
				// If this error shows up, then we know it's an Int of some kind (may be a Big or Tiny though)
				if (HTMLCode.IndexOf(TSQL.ErrorStrings.UNION_SUM_ERROR_PRE2) >= 0)
				{
					retVal = SqlDbType.Int;
				}
				else
				{
					ParentOutput(String.Format("Error: {0}", HTMLCode));
				}
			}

			return retVal;
		}
		*/
		// }}}

		// {{{ ParseUnionSelectForIntegerRefinement
		/*
		public static System.Data.SqlDbType ParseUnionSelectForIntegerRefinement(string HTMLCode, GlobalDS.OutputStatusDelegate ParentOutput)
		{
			System.Data.SqlDbType retVal = new System.Data.SqlDbType();
			//retVal = TSQL.DataType.Undefined;

			int StartError, EndError;

			// Check for the first half of the error
			StartError = HTMLCode.IndexOf(TSQL.ErrorStrings.UNION_SELECT_ERROR_PRE);
			if (StartError >= 0)
			{
				// Now check for the second half of the error
				EndError = HTMLCode.IndexOf(TSQL.ErrorStrings.UNION_SELECT_ERROR_POST);
				if (EndError > StartError)
				{
					retVal = SqlDbType.Int;
				}
				else 
				{
					ParentOutput(HTMLCode);
					throw new Exception("Unknown Int");
				}

			}
			else
			{
				ParentOutput(HTMLCode);
				throw new Exception("Unknown Int");
			}

			return retVal;
		}
		*/
		// }}}

		// {{{ ParseGroupedHaving
		/*
		public static GlobalDS.Field ParseGroupedHaving(string HTMLCode)
		{
			GlobalDS.Field retVal = new GlobalDS.Field();
			int StartError, StartData, EndError, StartSize;
			string ErrorData;

			// Initialize retVal
			retVal.DataType = SqlDbType.Variant;
			retVal.FieldName = String.Empty;

			// Check for first half of the error
			StartError = HTMLCode.IndexOf(TSQL.ErrorStrings.HAVING_ERROR_PRE);
			StartSize = TSQL.ErrorStrings.HAVING_ERROR_PRE.Length;

			if (StartError < 0 )
			{
				StartError = HTMLCode.IndexOf(TSQL.ErrorStrings.HAVING_ERROR_PRE2);
				StartSize = TSQL.ErrorStrings.HAVING_ERROR_PRE2.Length;
			}

			if (StartError >= 0)
			{

				// Now check for the second half of the error
				EndError = HTMLCode.IndexOf(TSQL.ErrorStrings.HAVING_ERROR_POST);
				if (EndError == -1)
				{ EndError = HTMLCode.IndexOf(TSQL.ErrorStrings.HAVING_ERROR_POST2); }

				if (EndError > StartError)
				{
					StartData = StartError + StartSize;
					ErrorData = HTMLCode.Substring(StartData, EndError - StartData);

					retVal.FieldName = ErrorData;
				}

			}

			// Return the information
			return retVal;
		}
		*/
		// }}}
#endif
		// }}}

		// {{{ CompareSignatures
		///<summary>Compares a known value signature set to an unknown value signature set</summary>
		///<returns>A value indicating if the two signatures match</returns>
		///<param name="KnownCase">The signature of the known value</param>
		///<param name="UnknownCase">The signature of the unknown value</param>
		///<param name="Tolerance">The tolerance band to use during comparison</param>
		///<param name="ParentOutput">The delegate used to bubble messages up to the user</param>
		public static bool CompareSignatures(double[] KnownCase, double[] UnknownCase, float Tolerance, GlobalDS.OutputStatusDelegate ParentOutput)
		{
			if (KnownCase.Length != UnknownCase.Length)
			{
				// Should it be extended? I say no for now.. 
				//ParentOutput("Page Lengths don't match.. I'm outta here {0} vs Unknown: {1}", KnownCase.Length, UnknownCase.Length);
				//return false;
			}

			int MaxIter = KnownCase.Length > UnknownCase.Length ? UnknownCase.Length : KnownCase.Length;

			for (int i=0; i < MaxIter; i++)
			{
				double Known, Unknown;
				Known = KnownCase[i];
				Unknown = UnknownCase[i];

				ParentOutput(String.Format("Known Value: [{0}] Unknown Value [{1}]", Known, Unknown));

				// Compare the difference to the tolerance for this value
				if ((Math.Abs(Known - Unknown)/Known) > (Tolerance * Known))
				{
					return false;
				}
			}

			// No breaks encountered
			return true;
		}
		// }}}

		// {{{ CompareSignatures w/ Filter
		public static bool CompareSignatures(double[] KnownCase, double[] UnknownCase, int[] Filter, float Tolerance)
		{
			bool retVal = true;
			for (int i=0; i < Filter.Length; i++)
			{
				int CompareIndex = Filter[i];

				if (CompareIndex < UnknownCase.Length)
				{
					double Known, Unknown;
					Known = KnownCase[CompareIndex];
					Unknown = UnknownCase[CompareIndex];

					// Compare the difference to the tolerance for this value
					if ((Math.Abs(Known - Unknown)/Known) > (Tolerance * Known))
					{
						retVal = false;
					}
				}
			}

			// No breaks encountered
			return retVal;
		}
		// }}}

		// {{{ GetHtmlPageSignature
		///<summary>Generate the Page Signature for use in blind SQL Injections</summary>
		///<param name="HtmlPage">The source HTML to generate a signature from</param>
		///<returns>The ASCII-Sum signature for the given page</returns>
		public static double[] GetHtmlPageSignature(string HtmlPage, string Delimiter)
		{
			string[] PageStringArray;
			ArrayList SumArray = new ArrayList();
			int Sum;

			PageStringArray = SplitByString(HtmlPage, Delimiter);

			for (int i = 0; i < PageStringArray.Length; i++)
			{
				int j = 0;
				char[] LineArray = PageStringArray[i].ToCharArray();

				Sum = 0;
				while (j < PageStringArray[i].Length)
				{
					Sum += LineArray[j];
					j++;
				}
				SumArray.Add(double.Parse(Sum.ToString()));
			}

			return (double [])SumArray.ToArray(typeof(double));
		}
		// }}}

		// {{{ SplitByString
		private static string[] SplitByString(string Value, string Delimiter)
		{
			ArrayList retVal = new ArrayList();
			string Shrinker = Value;

			while (Shrinker.IndexOf(Delimiter) >= 0)
			{
				int pos = Shrinker.IndexOf(Delimiter);
				if (pos > 0)
				{
					string s = Shrinker.Substring(0, pos);
					retVal.Add(s);
				}
				Shrinker = Shrinker.Substring(pos + Delimiter.Length);
			}

			if (Shrinker.Length > 0) retVal.Add(Shrinker); 
			
			return (string []) retVal.ToArray(typeof(string));
		}
		// }}}

		// {{{ GenerateAdaptiveFilter
		///<summary>Generate the adaptive filter from a set of signatures that embody the same boolean value</summary>
		///<param name="Signatures">An array of signatures that represent the same result value</param>
		///<returns>An array of indices that do not change indepedently of the desired page results</returns>
		public static int[] GenerateAdaptiveFilter(double[][] Signatures, float Tolerance)
		{
			int SignatureCount = Signatures.Length;
			int MinSignatureCount = 0;

			for (int i=0; i < SignatureCount; i++)
			{
				if (MinSignatureCount == 0 || MinSignatureCount > Signatures[i].Length)
				{
					MinSignatureCount = Signatures[i].Length;
				}
			}

			ArrayList RetVal = new ArrayList();
			double TempVal;

			/* Previous incarnations took an average, but this was not mathematically sound */
			for (int i=0; i < MinSignatureCount; i++)
			{
				bool NoAdd = false;
				TempVal = 0;

				for(int j=0; j < SignatureCount; j++)
				{
					if (j > 0 && Math.Abs(Signatures[j][i] - Signatures[j-1][i]) > Tolerance) NoAdd = true;
				}

				if (NoAdd == false) RetVal.Add(i);
			}

			return (int[]) RetVal.ToArray(typeof(int));
		}
		// }}}

		// {{{ GenerateSubtractiveFilter
		///<summary>Generate the subtractive filter from a set of opposing signatures</summary>
		///<param name="Signature1">The first signature to generate the filter against</param>
		///<param name="Signature2">The second signature to generate the filter against. This should represent a 
		///different value than the first signature</param>
		///<returns>An array of indices that contain values unique to each signature</returns>
		public static int[] GenerateSubtractiveFilter(double[] Signature1, double[] Signature2, float Tolerance)
		{
			int MinLength = (Signature1.Length > Signature2.Length) ? Signature2.Length : Signature1.Length;
			ArrayList RetVal = new ArrayList();

			for (int i = 0; i < MinLength; i++)
			{
				if (Math.Abs(Signature1[i] - Signature2[i]) > Tolerance)
				{
					RetVal.Add(i);
				}
			}

			return (int[]) RetVal.ToArray(typeof(int));
		}
		// }}}
	}
}
