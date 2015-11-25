var express = require('express');
var app = express();

for(var i=0; i<100; i++) {
	var path = Array(i+1).join("/ubuntu");
	app.get(path, function(req, res) {
		res.sendfile(__dirname + "/ubuntu.html")
	});
}

var path = Array(101).join("/ubuntu");
app.get(path, function(req, res) {
	res.send({ "Easter Egg Hunt": "egg{ubuntus_on_ubuntus_on_ubuntus}" });
});

var server = app.listen(8001, function () {
	var host = server.address().address;
	var port = server.address().port;
	
	console.log('Example app listening at http://%s:%s', host, port);
});