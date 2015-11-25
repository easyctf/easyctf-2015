<html>
	<head>
		<title>Welcome to my awesome site!</title>
		<link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootswatch/3.3.4/cerulean/bootstrap.min.css" />
	</head>
	<body>
		<nav class="navbar navbar-default">
			<div class="container">
				<div class="navbar-header">
					<button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#main-navbar">
						<span class="sr-only">Toggle navigation</span>
						<span class="icon-bar"></span>
						<span class="icon-bar"></span>
						<span class="icon-bar"></span>
					</button>
					<a class="navbar-brand" href="?page=pages/index.html">Awesome Site</a>
				</div>
			<div class="collapse navbar-collapse" id="main-navbar">
				<ul class="nav navbar-nav">
					<li><a href="?page=pages/index.html">Home</a></li>
					<li><a href="?page=pages/about.html">About</a></li>
				</ul>
			</div>
		</nav>
		
		<div class="container">
		<?php
			$url = realpath(isset($_GET["page"]) ? $_GET["page"] : "pages/index.html");
			$basepath = getcwd();
			if (strpos($url, $basepath) !== 0) {
				echo "Are you trying to hack me?";
			} else {
				echo file_get_contents($url);
			}
		?>
		</div>
		<script type="text/javascript" src="//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>
		<script type="text/javascript" src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script>
	</body>
</html>