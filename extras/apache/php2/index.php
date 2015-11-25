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
					<a class="navbar-brand" href="/">Super Secret Content</a>
				</div>
			<div class="collapse navbar-collapse" id="main-navbar">
				<ul class="nav navbar-nav">
					<li><a href="/">Home</a></li>
				</ul>
			</div>
		</nav>
		
		<div class="container">
		<?php
			include("stuff.php"); // get $pass and $flag
			
			$auth = false;
			if (isset($_GET["password"])) {
				if (strcmp($_GET["password"], $pass) == 0) {
					$auth = true;
				}
			}
			if ($auth) {
				echo "Wow! You guessed my password! Here's my super secret content: " . $flag;
			} else { ?>
				<p>Sorry, but you'll have to enter the password to see my super secret content. And it's not "password"!</p>
				<div class="row"><form class="form-horizontal" action="index.php" method="GET">
					<div class="col-xs-9">
						<input class="form-control" type="password" name="password" placeholder="Password" />
					</div>
					<div class="col-xs-3">
						<input class="btn btn-primary" type="submit" value="View Super Secret Content" />
					</div>
				</form></div>
			<?php }
		?>
		</div>
		
		<script type="text/javascript" src="//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>
		<script type="text/javascript" src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script>
	</body>
</html>

<!-- SOURCE AT index.source.php -->