<html>
	<head>
		<title>Log In</title>
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
					<a class="navbar-brand" href="/">Locked</a>
				</div>
			<div class="collapse navbar-collapse" id="main-navbar">
				<ul class="nav navbar-nav">
					<li><a href="/">Home</a></li>
				</ul>
			</div>
		</nav>
		
		<div class="container">
			<div class="row">
				<div class="col-md-6 col-md-offset-3 col-sm-10 col-sm-offset-1">
					<div class="panel panel-default">
						<div class="panel-heading">
							<h2 class="panel-title">Login</h2>
						</div>
						<div class="panel-body">
							<form class="form-horizontal" action="index.php" method="POST">
								<fieldset>
									<div id="login_msg">
										<?php
										include("stuff.php"); // get $email, $password, and $flag
										if (isset($_POST["email"]) && isset($_POST["password"])) {
											if ($_POST["email"] == $email && $_POST["password"] == $password) {
												?>
												<div class="alert alert-success">Nice. Here's the flag: <code><?php echo $flag ?></code></div>
												<?php
											} else {
												?>
												<div class="alert alert-danger">Sorry, wrong email or password.</div>
												<?php
											}
										}
										?>
									</div>
								</fieldset>
								<fieldset class="container-fluid">
									<div class="row">
										<div class="col-sm-12 form-group">
											<label class="col-sm-3 control-label" for="email">Email</label>
											<div class="col-sm-9">
												<input class="form-control" type="email" required name="email" id="email" placeholder="Email" autocomplete="off" />
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
												<input type="submit" class="btn btn-primary" value="Login!" />
												<a href="forgot_password.php" class="btn btn-default btn-sm">Forgot Password</a>
											</div>
										</div>
									</div>
								</fieldset>
							</form>
						</div>
					</div>
				</div>
			</div>
		</div>
		
		<script type="text/javascript" src="//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>
		<script type="text/javascript" src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script>
	</body>
</html>

<!-- SOURCE AT index.source.php -->