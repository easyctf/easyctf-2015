types = [ "Administrator", "Student", "Instructor", "Observer" ]

@load_account_page = () ->
	api_call "GET", "/api/user/info", {}
	.done (result) ->
		if result.success == 1
			account = result.data
			$("#name").html account.name
			$("#account-name").val account.name
			$("#avatar").attr "src", "//www.gravatar.com/avatar/" + account.email_hash + "?size=512"
			$("#email").html account.email
			$("#-account-email").val account.email
			$("#email_container").attr "href", "mailto:" + account.email
			$("#type").html types[account.type]
			
			$("#" + panel).slideDown "fast" for panel in result.data.panels
			if "_team" in result.data.panels and (account.type != 2)
				$("#leave_form").attr "action", "javascript:remove_user('" + account.uid + "');"
				$("#leave_form").attr "onsubmit", "remove_user('" + account.uid + "');return false;"
				api_call "GET", "/api/team/info", {}
				.done (result2) ->
					team = result2.data
					$("#team_name").html team.teamname
					$("#team-name").val team.teamname
					if team.school
						$("#team-school").val team.school
					$("#public_profile_link").attr "href", "/team?" + team.teamname
					$("#leave_confirm").attr "placeholder", team.teamname
					if account.teamowner == true
						$("#team-school").removeAttr "disabled"
						api_call "GET", "/api/team/schools", {}
						.done (result3) ->
							$("#team-school").typeahead { items: 10, minLength: 2, source: result3.data }
						$("#team-name").removeAttr "disabled"
						$("#team-help").slideDown "fast"
						api_call "GET", "/api/team/join_code", {}
						.done (result3) ->
							if result3.success == 1
								$("#team-join-code").val result3.data
								$("#join_code_row").slideDown "fast"
				api_call "GET", "/api/team/members", {}
				.done (result2) ->
					if result2.success == 1
						html = ""
						for member in result2.data
							you = member.uid == account.uid;
							html += "<li class='list-group-item' id='remove_" + member.uid + "' style='display:none;'></li>"
							html += "<li class='list-group-item' id='member_" + member.uid + "'>"
							html += "<span style='font-weight: " + (you ? "bold" : "normal") + ";'>" + member.name + "</span><br />"
							html += "<small><a href='mailto:" + member.email + "' class='NO_HOVER_UNDERLINE_DAMMIT'><span class='fa fa-envelope'></span> &nbsp; " + member.email + "</a></small>"
							if account.teamowner == true and member.uid != account.uid
								html += "<a href='javascript:remove_user(\"" + member.uid + "\");' class='badge'>REMOVE</a>"
						$("#team-members").html html
		else
			location.href = "/login"

@remove_user = (uid) ->
	api_call "POST", "api/team/remove", { uid: uid, confirm: $("#leave_confirm").val() }
	.done (result) ->
		if result.success == 1
			$("#member_" + uid).slideUp "fast"
		display_message "#remove_" + uid, (if result.success == 1 then 'success' else 'danger'), result.message, () ->
			if result.success == 1
				window.location.reload true

@join_team = () ->
	$("[id^=join-]").attr "disabled", "disabled"
	api_call "POST", "/api/team/join", { join_code: $("#join-code").val() }
	.done (result) ->
		if result.success != 1
			$("[id^=join-]").removeAttr "disabled"
		display_message "#join_msg", (if result.success == 1 then 'success' else 'danger'), result.message, () ->
			if result.success == 1
				window.location.reload true

@create_team = () ->
	$("[id^=create-]").attr "disabled", "disabled"
	api_call "POST", "/api/team/create", { teamname: $("#create-name").val() }
	.done (result) ->
		if result.success == 1
			display_message "#create_msg", "success", result.message, () ->
				window.location.reload true
		else
			display_message "#create_msg", "danger", result.message
			$("[id^=create-]").removeAttr "disabled"

@toggle_join_code = () ->
	if $('#team-join-code').attr('type') == 'text'
		$('#team-join-code').attr 'type', 'password'
	else if $('#team-join-code').attr('type') == 'password'
		$('#team-join-code').attr 'type', 'text'

@generate_join_code = () ->
	api_call "POST", "/api/team/join_code/new", {}
	.done (result) ->
		if result.success == 1
			$('#team-join-code').val result.data
			$('#team-join-code').attr 'type', 'text'

@update_team = () ->
	api_call "POST", "/api/team/update", { teamname: $("#team-name").val(), school: $("#team-school").val() }
	.done (result) ->
		if result.success == 1
			$("#saved_msg").css "display", "inline"
			$("#saved_msg").fadeOut "slow"

@update_info = () ->
	to_disable = "#update_info_form input[id^=account-]"
	($ to_disable).attr "disabled", "disabled"
	api_call "POST", "/api/user/update", { name: $("#account-name").val(), nPassword: $("#account-password").val(), cPassword: $("#account-confirm").val() }
	.done (result) ->
		if result.success == 1
			display_message "#update_user_msg", "success", result.message, () ->
				location.reload true
		else
			display_message "#update_user_msg", "danger", result.message
			($ to_disable).removeAttr "disabled"

@post_update = () ->
	content = CKEDITOR.instances["update-content"].getData()
	api_call "POST", "/api/updates/post", { title: $("#update-title").val(), content: content }
	.done (result) ->
		if result.success == 1
			console.log result
		display_message "#update_msg", (if result.success == 1 then 'success' else 'danger'), result.message, () ->
			if result.success == 1
				window.location.reload true

$ ->
	redirect_if_not_logged_in()
	load_account_page()