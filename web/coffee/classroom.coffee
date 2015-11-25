@create_group = () ->
	$("#create_group_form input, #create_group_form .btn").attr "disabled", "disabled"
	api_call "POST", "/api/group/create", { "groupname": $("#group_name").val() }
	.done (result) ->
		if result["success"] == 1
			display_message "#create_group_msg", "success", result.message, () ->
				location.reload true
		else
			$("#create_group_form input, #create_group_form .btn").removeAttr "disabled"
			display_message "#create_group_msg", "danger", result.message

@remove_group = (gid) ->
	if confirm("Are you sure you want to remove this class? This action is irreversible.")
		api_call "POST", "/api/group/delete", { "gid": gid }
		.done (result) ->
			if result["success"] == 1
				display_message "#msg_" + gid, "success", result.message, () ->
					location.reload true

@add_team = (gid, jc_box) ->
	$(".add_team_form input").attr "disabled", "disabled"
	api_call "POST", "/api/group/add_team", { "gid": gid, "join_code": $(jc_box).val() }
	.done (result) ->
		if result["success"] == 1
			display_message "#msg_" + gid, "success", result.message, () ->
				location.reload true
		else
			$(".add_team_form input").removeAttr "disabled"
			display_message "#msg_" + gid, "danger", result.message

@remove_team = (gid, tid) ->
	if confirm("Are you sure you want to remove this team? This action is irreversible.")
		api_call "POST", "/api/group/remove_team", { "gid": gid, "tid": tid }
		.done (result) ->
			if result["success"] == 1
				($ "#grouppanel" + gid + tid).slideUp "fast"
				display_message "#msg_" + gid, "success", result.message, () ->
					location.reload true

@load_group_info = (show_first_tab, callback) ->
	api_call "GET", "/api/group/list", {}
	.done (result) ->
		if result["success"] == 1
			window.groupListCache = result["data"]
			window.teamCache = { }
			for group in result["data"]
				for team in group["members"]
					window.teamCache[team["tid"]] = team
			load_group_management result["data"], show_first_tab, callback
		
@load_graph = (gid, tid) ->
	google.load "visualization", "1", {
		packages: ["corechart"]
		callback: ->
			team = window.teamCache[tid]
			data = [
			]
			members = [ "Members" ]
			uids = [ ]
			for member in (Object.keys team["members"])
				members.push team["members"][member]["name"]
				uids.push team["members"][member]["uid"]
			members.push "Unsolved"
			data.push members
			for category in (Object.keys team["category_breakdown"])
				cdata = [ category ]
				for member in uids
					cdata.push 0
				cdata.push 0
				for problem in team["category_breakdown"][category]
					if problem["solved"] == true
						cdata[(uids.indexOf problem["by"]) + 1] += 1
					else
						cdata[cdata.length - 1] += 1
				data.push cdata
			console.log data
			gdata = google.visualization.arrayToDataTable data
			colors = ["#2FA4F0", "#B9F9D0", "#2E5CC0", "#8BADE0", "#E6BF70", "#CECFF0", "#30A0B0", "#0c6aa6"]
			colors[members.length - 2] = "#000000"
			options = {
		        title: "Problem Overview for " + team["teamname"]
		        height: 400
		        legend: { position: 'top', maxLines: 3 }
		        isStacked: true
		        bar: { groupWidth: '75%' }
		        colors: colors
		        series: { }
			}
			options.series[members.length - 2] = {
				color: "black"
				visibleInLegend: false
		    };
			chart = new google.visualization.ColumnChart (document.getElementById "graph" + gid + team["tid"])
			chart.draw gdata, options
	}

@load_group_management = (groups, show_first_tab, callback) ->
	render_class_list = _.template $("#template_class_list").remove().text()
	render_team = _.template $("#template_team").remove().text()
	if groups.length > 0
		groups[0].active = true
	$("#class_container").html render_class_list {
		groups: groups,
		render_team: render_team
	}
	if callback
		callback()

$ ->
	api_call "GET", "/api/user/info", {}
	.done (result) ->
		if result.success == 0 or (result.data and result.data.logged_in != true)
			location.href = "/login"
		else
			if not(result.data.type == 2)
				location.href = "/account"
	load_group_info true
	$('#group_tabs a').click (e) ->
		e.preventDefault()
		$(this).tab "show"