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

#define DISPLAY_CONNECTS
using System;
using System.Net;
using System.Text;
using System.IO;
using System.Collections.Specialized;
using System.Web;

namespace Absinthe.Core
{

///<summary>
///All HTTP connections are done through this class.
///</summary>
public class httpConnect
{
	private const string UserAgent = "Absinthe/1.1";

	///<summary>
	///Request the HTML page
	///</summary>
	///<returns>The whole HTML page as a single string</returns>
	///<param name="ConnectURL">The URL to request the page from</param>
	///<param name="Data">The Key/Value pairs to send along with the request</param>
	///<param name="Proxy">The web proxy to use. This is null if it is a direct connection</param>
	///<param name="UsePost">Indicates if the request is a POST request. Otherwise it is a GET.</param>
	///<param name="Cookies">The Key/Value pairs to send as cookies.</param>
	///<param name="ParentOutput">The delegate to bubble up textual information that may be useful to the user</param>
	public static string PageRequest(string ConnectURL, StringDictionary Data, WebProxy Proxy, bool UsePost, StringDictionary Cookies, 
		NetworkCredential AuthCredentials, GlobalDS.OutputStatusDelegate ParentOutput)
	{
		//ParentOutput(System.String.Format("Making a Page request {0}", UsePost));
		if (UsePost)
		{
			return PostPage(ConnectURL, Data, Proxy, Cookies, AuthCredentials, ParentOutput);
		}
		else
		{
			return GetPage(ConnectURL, Data, Proxy, Cookies, AuthCredentials, ParentOutput);
		}
	}
	

	// {{{ GetPage
	private static string GetPage(string ConnectURL, StringDictionary GetData, WebProxy Proxy, StringDictionary Cookies, NetworkCredential AuthCredentials, GlobalDS.OutputStatusDelegate ParentOutput)
	{
		return GetPage(ConnectURL, GetData, Proxy, Cookies, AuthCredentials, false, ParentOutput);
	}
	
	private static string GetPage(string ConnectURL, StringDictionary GetData, WebProxy Proxy, StringDictionary Cookies, NetworkCredential AuthCredentials, bool SlowProtocol, GlobalDS.OutputStatusDelegate ParentOutput)
	{
		StringBuilder QueryURL = new StringBuilder();
		QueryURL.Append(ConnectURL);

		if (GetData.Count > 0)
		{
			// Toss onto qstring
			QueryURL.Append("?");
			QueryURL.Append(GenerateQueryString(GetData, true));
		}
		
		HttpWebRequest TestGet = (HttpWebRequest) WebRequest.Create(QueryURL.ToString());
		TestGet.Method = "GET";
		if (SlowProtocol) TestGet.ProtocolVersion = HttpVersion.Version10; 
		if (Proxy != null) TestGet.Proxy = Proxy;
		
		TestGet.UserAgent = UserAgent;

#if DISPLAY_CONNECTS
		if (ParentOutput != null)
		{
			ParentOutput(QueryURL.ToString()); //HACK
		}
#endif

		HttpWebResponse resp;
		resp = null;	

		if (Cookies != null)
		{
			foreach (string CookieName in Cookies.Keys)
			{
				//ParentOutput(String.Format("CookieName : {0}", CookieName));
				//ParentOutput(String.Format("CookieValue : {0}", Cookies[CookieName]));
				try
				{
					Cookie ck = new Cookie(CookieName, Cookies[CookieName]);
					if (TestGet.CookieContainer == null)
					{
						TestGet.CookieContainer = new CookieContainer();
					}
					TestGet.CookieContainer.Add(ck);
				}
				catch (NullReferenceException nre)
				{
					ParentOutput(nre.Message);	
					throw new Exception("Cookies could not be attached");
				}
				//ParentOutput("Added it BEEEATCH");
			}
		}

		if (AuthCredentials != null) TestGet.Credentials = AuthCredentials;

		try
		{ 
			resp = (HttpWebResponse)TestGet.GetResponse(); 
		}
		catch (WebException wex)
		{
			if(wex.Status == WebExceptionStatus.ReceiveFailure)
			{
				// Mono seems to choke when used over wifi, then idled.. if this error takes place,
				// drop down to HTTP/1.0 for the single renegotiate connect.. (standard 1.0 is generally too slow though)
				return GetPage(ConnectURL, GetData, Proxy, Cookies, AuthCredentials, true, ParentOutput);
			}
			else if (wex.Status == WebExceptionStatus.Timeout)
			{
				// Try again I guess.. 
				return GetPage(ConnectURL, GetData, Proxy, Cookies, AuthCredentials, false, ParentOutput);
			}
			else 
			{
				//resp = (HttpWebResponse)wex.Response;
				//ParentOutput(wex.ToString());
				throw(wex);
			}
		}

		// Get the stream associated with the response.
		Stream receiveStream = resp.GetResponseStream();

		// Pipes the stream to a higher level stream reader with the required encoding format. 
		StreamReader readStream = new StreamReader (receiveStream, Encoding.UTF8);

		string retVal = readStream.ReadToEnd();
		resp.Close ();
		readStream.Close ();

//		ParentOutput(retVal);

		return retVal;
	}
	// }}}

	// {{{ GenerateQueryString
	private static string GenerateQueryString(StringDictionary Data, bool Encode)
	{
		StringBuilder QueryParams = new StringBuilder();

		foreach(string Key in Data.Keys)
		{
			if (Encode)
			{QueryParams.Append(HttpUtility.UrlEncode(Key));}
			else
			{QueryParams.Append((Key));}
			
			QueryParams.Append("=");
			
			if (Encode) 
			{QueryParams.Append(HttpUtility.UrlEncode(Data[Key]));}
			else
			{QueryParams.Append((Data[Key]));}
			
			QueryParams.Append("&");
		}

		// Trim trailing ampersand
		QueryParams.Remove(QueryParams.Length - 1, 1);

		return QueryParams.ToString();
	}
	// }}}
	
	// {{{ SetPostVars
	private static void SetPostVars(ref HttpWebRequest myHttpWebRequest, StringDictionary PostData)
	{
		string postData = GenerateQueryString(PostData, true);

		ASCIIEncoding encoding=new ASCIIEncoding();
		byte[]  byte1=encoding.GetBytes(postData);
		// Set the content type of the data being posted.
		myHttpWebRequest.ContentType="application/x-www-form-urlencoded";
		
		// Set the content length of the string being posted.
		myHttpWebRequest.ContentLength = postData.Length;
		Stream newStream = myHttpWebRequest.GetRequestStream();
		newStream.Write(byte1, 0, byte1.Length);

		// Close the Stream object.
		newStream.Close();
	}
	// }}}

	// {{{ PostPage
	private static string PostPage(string ConnectURL, StringDictionary PostData, WebProxy Proxy, StringDictionary Cookies, NetworkCredential AuthCredentials, GlobalDS.OutputStatusDelegate ParentOutput)
	{
		return PostPage(ConnectURL, PostData, Proxy, Cookies, AuthCredentials, false, ParentOutput);
	}
	private static string PostPage(string ConnectURL, StringDictionary PostData, WebProxy Proxy, StringDictionary Cookies, NetworkCredential AuthCredentials, bool SlowProtocol, GlobalDS.OutputStatusDelegate ParentOutput)
	{
		HttpWebRequest TestPost = (HttpWebRequest) WebRequest.Create(ConnectURL);
		if (Proxy != null) TestPost.Proxy = Proxy;

		TestPost.Method = "POST";
		SetPostVars(ref TestPost, PostData);

		if (SlowProtocol) TestPost.ProtocolVersion = HttpVersion.Version10; 
		if (Proxy != null) TestPost.Proxy = Proxy;

		TestPost.UserAgent = UserAgent;

		if (Cookies != null)
		{
			foreach (string CookieName in Cookies.Keys)
			{
				if (TestPost.CookieContainer == null)
				{
					TestPost.CookieContainer = new CookieContainer();
				}
				TestPost.CookieContainer.Add(new Cookie(CookieName, Cookies[CookieName]));
			}
		}

		if (AuthCredentials != null) TestPost.Credentials = AuthCredentials;

#if DISPLAY_CONNECTS
		if (ParentOutput != null)
		{
			ParentOutput(ConnectURL); //HACK
		}
#endif

		HttpWebResponse resp;
		resp = null;	
		try
		{	resp = (HttpWebResponse)TestPost.GetResponse(); }
		catch (WebException wex)
		{
			if(wex.Status == WebExceptionStatus.ReceiveFailure)
			{
				// Mono seems to choke when used over wifi, then idled.. if this error takes place,
				// drop down to HTTP/1.0 for the single renegotiate connect.. (standard 1.0 is generally too slow though)
				return PostPage(ConnectURL, PostData, Proxy, Cookies, AuthCredentials, true, ParentOutput);
			}
			else 
			{
				//resp = (HttpWebResponse)wex.Response;
				//ParentOutput(wex.ToString());
				throw(wex);
			}
		}

		// Get the stream associated with the response.
		Stream receiveStream = resp.GetResponseStream();

		// Pipes the stream to a higher level stream reader with the required encoding format. 
		StreamReader readStream = new StreamReader (receiveStream, Encoding.UTF8);

		string retVal = readStream.ReadToEnd();
		resp.Close ();
		readStream.Close ();

		return retVal;
	}
	// }}}

}
}
