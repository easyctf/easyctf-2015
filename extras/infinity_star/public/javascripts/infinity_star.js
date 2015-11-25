var message_duration = 2500,
	 indexOf = [].indexOf || function(item) { for (var i = 0, l = this.length; i < l; i++) { if (i in this && this[i] === item) return i; } return -1; };

window.display_message = function(target, type, message, callback) {
	window._callback = callback;
	return $(target).slideUp("fast", "swing", function() {
		var ref;
		$(target).html("<div class='alert alert-" + type + "'" + ((ref = indexOf.call(target, "#site-message") >= 0) != null ? ref : {
			" style='margin:0'": ""
		}) + ">" + message + "</div>");
		return $(target).slideDown("fast", "swing", function() {
			return setTimeout((function() {
				return $(target).slideUp("fast", "swing", function() {
					$(target).html("");
					if (window._callback) {
						return window._callback();
					}
				});
			}), message_duration);
		});
	});
};