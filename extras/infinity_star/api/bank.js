var common = require("./common");

exports.transfer = function(req, res) {
	common.is_logged_in(req, function(logged_in) {
		if (logged_in) {
			common.user_info(unescape(req.signedCookies["username"]), function(user) {
				var amount = parseInt(req.query.amount);
				var recipient_username = req.query.recipient;
				common.db.collection("users").find({
					username: recipient_username
				}).toArray(function(err, users) {
					if (err) { return res.send({ success: 0, message: "Internal error (8)." }); }
					if (users.length != 1) {
						return res.send({ success: 0, message: "Recipient doesn't exist. Check the username you entered and try again." });
					}
					var recipient = users[0];
					if (amount == 420) {
						return res.send({ success: 0, message: "egg{blaze_it_4_infinity_dayz}" });
					}
					if (recipient["username"] == user["username"]) {
						return res.send({ success: 0, message: "You can't send money to yourself, silly!" });
					}
					if (amount <= 0) { // || amount > 150) {
						return res.send({ success: 0, message: "You can only send positive amounts." });
					}
					if (user["username"] == "michael") {
						if (recipient["purchased"] == true) {
							return res.send({ success: 0, message: "You've already purchased the premium service!" });
						}
						common.db.collection("users").update({
							username: recipient["username"]
						}, {
							$set: {
								balance: user["balance"] + amount
							}
						}, function(err2) {
							if (err2) { return res.send({ success: 0, message: "Internal error (9)." }); }
							return res.send({ success: 1, message: "Funds were transferred." });
						});
					} else {
						return res.send({ success: 0, message: "You're not allowed to send transfers (feature under testing)." });
					}
				});
			});
		} else {
			return res.send({ success: 0, message: "You're not logged in." });
		}
	});
};

exports.premium = function(req, res) {
	common.is_logged_in(req, function(logged_in) {
		if (logged_in) {
			common.user_info(unescape(req.signedCookies["username"]), function(user) {
				if (user["balance"] >= 100 && user["purchased"] == false) {
					common.db.collection("users").update({
						username: user["username"]
					}, {
						$set: {
							balance: user["balance"] - 100,
							purchased: true
						}
					}, function(err) {
						if (err) { return res.send({ success: 0, message: "Internal error (10)." }); }
						return res.send({ success: 1, message: "Congrats for purchasing premium. Page is reloading..." });
					});
				} else {
					return res.send({ success: 0, message: "You don't have enough money to buy this." });
				}
			});
		} else {
			return res.send({ success: 0, message: "You're not logged in." });
		}
	});
};