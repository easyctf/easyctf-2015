$ ->
	redirect_if_not_logged_in(true)
	api_call "GET", "/api/problem/e_solved", {}
	.done (result) ->
		if result.success == 1
			html = ""
			for egg in result.data
				html += "<li class='list-group-item'>" + egg + "</li>"
			$("#collected_eggs").html html

@submit_egg = () ->
	api_call "POST", "/api/problem/e_submit", { answer: $("#egg").val() }
	.done (result) ->
		if result.success == 1
			display_message "#egg_msg", (if result.data.correct == 1 then 'success' else 'danger'), result.data.message, () ->
				if result.data.correct == true
					location.reload true
		else
			display_message "#egg_msg", "danger", result.message