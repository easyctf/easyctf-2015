handle_register = (e) ->
	e.preventDefault()
	data = $("#register_form").serializeObject()
	to_disable = "#register_form input, #register_form select"
	$(to_disable).attr "disabled", "disabled"
	api_call "POST", "/api/user/create", data
	.done (result) ->
		class_name = if result.success == 1 then "success" else "warning"
		display_message "#register_msg", class_name, result.message
		if result.success == 1
			location.href = "/account"
		else
			$(to_disable).removeAttr "disabled"
		grecaptcha.reset()
	.fail ->
		display_message "#register_msg", "danger", "Couldn't connect to the API."
		$(to_disable).removeAttr "disabled"
		grecaptcha.reset()
	false

$ ->
	$("#register_form").on "submit", handle_register