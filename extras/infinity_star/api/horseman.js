var Horseman = require('node-horseman');
var horseman = new Horseman();

console.log(process.argv)

var page_url = process.argv[2];

try {
	horseman
		.userAgent("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:27.0) Gecko/20100101 Firefox/27.0")
		.post("http://web.easyctf.com:10206/api/user/login", "username=michael&password=xxxxxxxxxxxxxx")
		.evaluate(function() {
			return $("body").text();
		})
		.then(function(result) {
			console.log(result);
			horseman
				.userAgent("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:27.0) Gecko/20100101 Firefox/27.0")
				.open(page_url)
				.evaluate(function() {
					return $("body").text();
				})
				.then(function(result) {
					console.log(result);
					console.log("Done.");
				})
				.close();
		});
} catch (e) {
	console.log(e);
}