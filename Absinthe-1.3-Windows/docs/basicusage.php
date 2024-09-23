<? include("absinthe-template-top.php"); ?>
<tr><td>
		<h1>Basic Usage</h1>

		Absinthe does not discover injections, so it requires the user to enter all relevant information about the target host. Once Absinthe is loaded,
		you should be presented with a screen like this:<br />
		<br />
		<div align="center">
			<img src="fullwindow1.png" />
		</div>
		<br />
		Here you can enter the relevant information about the vulnerable target. The URL should contain the hostname, the port and the specific page, but not the 
		parameters to be sent and manipulated during the injection.<br /><br />
		<div align="center">
			<img border=1 src="connection.png" />
		</div>

	
</td></tr>
<tr><td>

		<h1>Entering Parameters</h1>

		Parameters for the web application are entered in a separate box on the main tab. If more than one parameter is marked as injectable, Absinthe will only
		use the first one listed. If the injectable parameter is to be treated as a string, check the appropriate box. If the default value is not numeric, it 
		will assume it is supposed to be a string.
		<br /><br />
		<div align="center">
			<img border=1 src="parameters.png" />
		</div>

	</p>
	
</td></tr>
<tr><td>

<h1>Adding Cookies</h1>

		Sometimes, HTTP Headers or Cookies are required to send injection parameters to the web application. These can be added in the same area as the 
		parameters. Once the information is in the boxes, simply click the <b><i>Additional Headers</i></b> button.


	
</td></tr>
<tr><td>

		<h1>Saving Target Information</h1>
		At any point, you can save the information about this injection by selecting <b><i>File->Save</i></b> from the top menu. This will save all information
		entered about the host to an XML file for later use.

	
</td></tr>
<tr><td>

		<h1>Initializing the Injection</h1>
		Once all of the information has been entered, click the <b><i>Initialize Injection</i></b> button on the bottom of the screen. This will gather the 
		base cases required to automated the process of data retrieval. After the base cases have been successfully gathered, you can save these so you won't
		have to initialize again during another session.
</td></tr>
<? include("absinthe-template-bottom.php"); ?>
