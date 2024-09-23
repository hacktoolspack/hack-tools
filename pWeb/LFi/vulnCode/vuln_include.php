<html>
<head>
<title>INCLUDE FILE GOES HERE!</title>
<style>
.boxen {
	background: #ccc;
	color: red;
}
</style>
</head>
<body>
<h1>Hello World, Include a file?</h1>

<div class="boxen">
	<?php
		# include a file:
		include($_GET['filename']);
	?>
</div>

</body>
<footer>
</footer>	
