var http = require('http');
http.createServer(function (req, res) {
	res.writeHead(200, {'Content-Type': 'text/plain'});
	res.end('Easter Egg Hunt: egg{9_much_h4kking}\n');
}).listen(1337, '0.0.0.0');