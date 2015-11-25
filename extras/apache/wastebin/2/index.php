<html>

<head>
	<title>Wastebin Login - EasyCTF 2015</title>
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

		<h1>Wastebin</h1>
		<p>wastebin is the best paste tool on the internet guyz!!!11!1 we will keep all ur info safe</p>
		<p>num of users registered: <span id="users_registered"></span></p>
		<?php if (isset($_POST["submit"]) && $_POST["username"] == "admin" && $_POST["password"] == "11FutLBObDdAnSIyEo9LF6TLiWuG8GpHSLnRBAYD4jUGM0O4Jbt8KPasU5CpAGmZW2dX97HX4xHau8asmrN5CzIiM6Xb51plWa3q") { ?>
			<div class="alert alert-success">Nice. The flag is <code>easyctf{looks_like_my_robot_proof_protection_isn't_very_human_proof}</code></div>
		<?php } else { ?>
			<?php if (isset($_POST["submit"])) { ?>
				<div class="alert alert-danger">Sorry, wrong password.</div>
			<?php } ?>
			<div class="row">
				<form class="form-horizontal" action="index.php" method="POST">
					<div class="form-group">
						<div class="col-xs-3">
							<label class="control-label">Username</label>
						</div>
						<div class="col-xs-6">
							<input class="form-control" type="username" name="username" placeholder="Username" />
						</div>
					</div>
					<div class="form-group">
						<div class="col-xs-3">
							<label class="control-label">Password</label>
						</div>
						<div class="col-xs-6">
							<input class="form-control" type="password" name="password" placeholder="Password" />
						</div>
					</div>
					<div class="col-xs-3">
						<input class="btn btn-primary" type="submit" name="submit" value="Login" />
					</div>
				</form>
			</div>
		<?php } ?>
	</div>
	</div>
	<script type="text/javascript">
		document.getElementById("users_registered").innerHTML = 1;
	</script>
</body>

</html>