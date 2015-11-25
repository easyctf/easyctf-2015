var bank = require("./bank");
// var childProcess = require('child_process');
var user = require("./user");

var cp = require('child_process');

var api = { };

api.route = function(app) {
	app.post("/api/user/login", user.login);
	app.get("/logout", user.logout);
	app.post("/api/user/register", user.register);
	app.get("/api/bank/transfer", bank.transfer);
	app.post("/api/bank/premium", bank.premium);
	app.post("/api/report", report);
};

var report = function(req, res) {
	var page_url = req.body.page;
	console.log(__dirname);
	
	var child = cp.spawn('node', ['api/horseman', page_url]);
	child.stdout.on('data', function(data) {
	    console.log('stdout: ' + data);
	});
	child.stderr.on('data', function(data) {
	    console.log('stdout: ' + data);
	});
	child.on('error', function (err) {
	  console.log('Failed to start child process.');
	  console.dir(err);
	});
	res.send({ success: 1, message: "Reported." });
	/*
	var x = childProcess.spawn("phantomjs", [ __dirname + "/admin.phantom.js", page_url ]);
	x.stdout.pipe(process.stdout);
	*/
		/*.on("resourceReceived", function(response) {
			console.dir(response);
		});*/
};
	
module.exports = api;