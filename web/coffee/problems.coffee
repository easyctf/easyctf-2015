@load_problems = () ->
	api_call "GET", "/api/user/info", { }
	.done (result) ->
		if result["success"] == 1 and result["data"]["team"].length > 0
			render_problem_list = _.template $("#template_problem_list").remove().text()
			render_problem = _.template $("#template_problem").remove().text()
			api_call "GET", "/api/problem/get_unlocked", {}
			.done (result) ->
				if result.success == 1
					if result["show_rules"]
						$("#rules").slideDown "fast"
					if result["unlocked"] == result["total"]
						$("#problems_count").html "<div class='alert alert-success'>You've unlocked all <b>" + result["total"] + "</b> problems!</div>"
					else
						$("#problems_count").html "" # <div class='alert alert-info'>You've unlocked <b>" + result["unlocked"] + "</b> out of <b>" + result["total"] + "</b> problems!</div>"
					$("#problems_container").html render_problem_list {
						problems: result.data,
						render_problem: render_problem,
						cardinal: ["1st", "2nd", "3rd"]
					}
					$('.solved').parent().parent().next().hide()
				else
					display_message_permanent "#problems_msg", "danger", result.message
		else
			display_message_permanent "#problems_msg", "warning", "You must be in a team to view problems! Click <a href='/account' class='text-danger'>here</a> to join or create a team!"

@show_hint = (id) ->
	$('#hint_' + id).slideToggle 120, "swing"
	return

@handle_submit = (id) ->
	api_call "POST", "/api/problem/submit", { pid: id, answer: $("#" + id).val() }
	.done (result) ->
		if result.success == 1
			display_message "#msg_" + id, (if result.data.correct == true then 'success' else 'danger'), result.data.message, () ->
				if result.data.correct == true
					location.reload true
		else
			display_message "#msg_" + id, "danger", result.message

$ ->
	load_problems()
	redirect_if_not_logged_in(true)