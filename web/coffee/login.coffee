handle_login = (e) ->
	e.preventDefault()
	data = $("#login_form").serializeObject()
	to_disable = "#login_form input, #login_form select"
	$(to_disable).attr "disabled", "disabled"
	api_call "POST", "/api/user/login", data
	.done (result) ->
		class_name = if result.success == 1 then "success" else "warning"
		display_message "#login_msg", class_name, result.message, () ->
			if result.success == 1
				location.href = "/account"
		$(to_disable).removeAttr "disabled"
		grecaptcha.reset()
	.fail ->
		display_message "#login_msg", "danger", "Couldn't connect to the API."
		$(to_disable).removeAttr "disabled"
		grecaptcha.reset()
	false

$ ->
	$("#login_form").on "submit", handle_login