var common = require("./api/common");

var router = function(app) {
	var pages = [
		{ url: "/", view: "index", "vars": { title: "" } },
		{ url: "/register", view: "register", "vars": { title: "Register" } },
		{ url: "/login", view: "login", "vars": { title: "Login" } },
		{ url: "/account", view: "account", "vars": { title: "Account" } }
	];
	for(var i=0; i<pages.length; i++) {
		(function(page) {
			app.get(page.url, function(req, res, next) {
				console.log("[router.js] GET " + page.url);
				console.log("[router.js] " + JSON.stringify(req.cookies));
				var vars = { };
				common.is_logged_in(req, function(logged_in) {
					if (logged_in) {
						common.user_info(req.signedCookies["username"], function(user_info) {
							vars.extend({ user_info: user_info, logged_in: logged_in });
							res.render(page.view, { page: vars.extend(page.vars) });
						});
					} else {
						vars.extend({ logged_in: logged_in });
						res.render(page.view, { page: vars.extend(page.vars) });
					}
				});
			});
		})(pages[i]);
	}
};

module.exports = router;