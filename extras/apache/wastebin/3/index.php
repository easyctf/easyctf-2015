<!DOCTYPE html>
<html>

<head>
	<meta charset="utf-8">
	<title>Wastebin 3</title>
	<link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootswatch/3.3.4/spacelab/bootstrap.min.css" />
	<script type="text/javascript" src="//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>
	<script type="text/javascript" src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script>
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
				<a class="navbar-brand" href="/3/">Wastebin 3</a>
			</div>
		<div class="collapse navbar-collapse" id="main-navbar">
			<ul class="nav navbar-nav">
				<li><a href="/3/">Home</a></li>
			</ul>
			<ul class="nav navbar-nav navbar-right">
								<li><a href="/3/#login">Login</a></li>
					<li><a href="/3/#register">Register</a></li>
						</ul>
		</div>
	</nav>
	<div class="container">
		<?php
	
		error_reporting(0);
	
		if (isset($_POST['submit']) && isset($_POST['username']) && isset($_POST['password']) && $_POST['submit'] == "Login!") {
			$username = $_POST['username'];
			$password = $_POST['password'];
			include("functions.php"); // connect to mysql server
			
			$query = "SELECT * FROM `users` WHERE username='$username' AND password='$password'";
			$result = mysql_query($query);
			$rows = array();
			while($row = mysql_fetch_array($result)) {
				$rows[] = $row;
			}
			if (count($rows) != 1) {
				echo "<div class='alert alert-danger'>No accounts found with that username. <a href='index.php'>Try again?</a></div>";
			} else {
				$row = $rows[0];
				echo "<div class='alert alert-success'>Welcome, <code>" . $row['username'] . "</code>! ";
				if ($row['username'] == "admin") {
					echo "Your flag is <code>$flag</code>.";
				}
				echo "</div>";
			}
			
		} else {
			?>
			<div class="row">
				<div class="col-md-6 col-md-offset-3 col-sm-10 col-sm-offset-1">
					<div class="panel panel-default">
						<div class="panel-heading">
							<h2 class="panel-title">Login</h2>
						</div>
						<div class="panel-body">
							<form class="form-horizontal" action="index.php" method="post">
								<fieldset>
									<div id="login_msg"></div>
								</fieldset>
								<fieldset class="container-fluid">
									<div class="row">
										<div class="col-sm-12 form-group">
											<label class="col-sm-3 control-label" for="username">Username</label>
											<div class="col-sm-9">
												<input class="form-control" type="text" required name="username" id="username" placeholder="Username" autocomplete="off" />
											</div>
										</div>
									</div>
									<div class="row">
										<div class="col-sm-12 form-group">
											<label class="col-sm-3 control-label" for="password">Password</label>
											<div class="col-sm-9">
												<input class="form-control" type="password" required name="password" id="password" placeholder="Password" autocomplete="off" />
											</div>
										</div>
									</div>
									<div class="row">
										<div class="col-sm-12 form-group">
											<label class="col-sm-3 control-label"></label>
											<div class="col-sm-9">
												<input type="submit" class="btn btn-primary" name="submit" value="Login!" />
											</div>
										</div>
									</div>
								</fieldset>
							</form>
						</div>
					</div>
				</div>
			</div>
			<?php
		}
		?>
	</div>
</body>

</html>

<!-- source code at index.source.php -->