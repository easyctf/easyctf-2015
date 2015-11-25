@forgot_password = () ->
	disable = "#forgot_password_form input, #forgot_password_form .btn"
	$(disable).attr "disabled", "disabled"
	api_call "POST", "/api/password_recovery/forgot", { "email": $("#email").val() }
	.done (result) ->
		if result["success"] == 1
			display_message "#forgot_msg", "success", result.message, () ->
				location.href = "/login"
		else
			$(disable).removeAttr "disabled"
			display_message "#forgot_msg", "danger", result.message

@reset_password = () ->
	disable = "#reset_password_form input, #reset_password_form .btn"
	$(disable).attr "disabled", "disabled"
	api_call "POST", "/api/password_recovery/reset", { "code": $("#code").val(), "password": $("#password").val(), "confirm": $("#confirm").val() }
	.done (result) ->
		if result["success"] == 1
			display_message "#reset_msg", "success", result.message, () ->
				location.href = "/login"
		else
			$(disable).removeAttr "disabled"
			display_message "#reset_msg", "danger", result.message

$ ->
	$("#code").val location.hash.replace "#", ""