var express = require("express");
var path = require("path");
var cookieParser = require("cookie-parser");
var bodyParser = require("body-parser");
var session = require("express-session");

var app = express();

app.set("views", path.join(__dirname, "views"));
app.set("view engine", "ejs");

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser("dpqgoiwphnipqiwmdpoihqpoieptoiqpweioht"));
app.use(express.static(path.join(__dirname, "public")));
app.use(session({
	secret: "ihptoihwponiurbnpqupehqtoihpgwinqpwoinpeqt"
}));

require("./api/api").route(app);
require("./router")(app);

app.use(function(req, res, next) {
	var err = new Error("Not Found");
	err.status = 404;
	res.send("404. Sucks to be you.");
});

module.exports = app;

var port = 10206;
app.listen(port);
console.log("Listening on port " + port + "...");
