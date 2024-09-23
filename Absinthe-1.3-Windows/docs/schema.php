<? include("absinthe-template-top.php"); ?>
	<tr>
		<td>

		<h1>Downloading the Schema</h1>

		After you have initialized the injection, you can proceed to the next tab to download the schema.
		<br /><br />
		<div align="center">
			<img src="fullwindow2.png" />
		</div>
		<br />
		When you first encounter this screen, there will be no information, but you will have the options to retrieve the username or download 
		the table information.
		
		</td>
		</tr>
		<tr>
		<td>

		<h1>Retrieving the Username</h1>
		Retrieving the connected username is not required to proceed with the injection, but it is a quick way to determine if the injection was
		initialized properly. It should only take a couple of seconds to download. Once again, this is not a required first step. All authentication
		against the database is done by the vulnerable web application, not by Absinthe. This is more for curiosity purposes.

		</td>
		</tr>

		<tr>
		<td>
		<h1>Retrieving the Schema</h1>

		<h2>Table Information</h2>
		The first set of information you will need is the table structure of the schema. Simply click on the <b><i>Load Table Info</i></b> button
		and wait as Absinthe communicates with the web application. Depending on the number of tables in the database, this may take some time. <br />
		When it has finished, There should be a list of table names, which can be expanded to display their internal ID number and the number of 
		records stored in each table.

		<h2>Field Information</h2>

		After you have gathered the table information, you can proceed to get the field information for each table individually. To do this, select
		the table name from the list of tables, and click the <b><i>Load Field Info</i></b> button. This will retrieve the name, order and data type of 
		all the fields for the table.

	</td>
	</tr>
<? include("absinthe-template-bottom.php"); ?>
