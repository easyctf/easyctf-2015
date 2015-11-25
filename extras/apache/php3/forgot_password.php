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
							<h2 class="panel-title">Forgot Password</h2>
						</div>
						<div class="panel-body">
							<form class="form-horizontal" action="forgot_password.php" method="POST">
								<fieldset>
									<div id="login_msg">
										<?php
											include("stuff.php"); // get $email and $password
											if (isset($_POST["email"])) {
												if (strpos($_POST["email"], $email) !== FALSE) {
													$to = $email;
													$subject = "Password Recovery";
													$message = "Hi. You requested the password for the account with the email " . $_POST["email"] . ". Here it is: " . $password;
													
													$headers = "From: " . $_POST["email"]; // who requested the email
													$mail_sent = mail($to, $subject, $message, $headers);
													
													if ($mail_sent) {
														?>
														<div class="alert alert-success">The email was sent!</div>
														<?php
													} else {
														?>
														<div class="alert alert-danger">Sorry, the email failed to send.</div>
														<?php
													}
												} else {
													?>
													<div class="alert alert-danger">Sorry, only <code><?php echo $email; ?></code> can recover his account password.</div>
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
											<label class="col-sm-3 control-label"></label>
											<div class="col-sm-9">
												<input type="submit" class="btn btn-primary" value="Recover!" />
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

<!-- SOURCE AT forgot_password.source.php -->