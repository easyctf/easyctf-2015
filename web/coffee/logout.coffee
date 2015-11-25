$ ->
	api_call "POST", "/api/user/logout", {}
	.done (result) ->
		location.href = "/"