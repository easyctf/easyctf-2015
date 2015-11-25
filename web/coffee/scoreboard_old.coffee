@scoreboard_name = ""

@load_graph = ->
	api_call "GET", "/api/stats/scoregraph"
	.done (result) ->
		if result["success"] == 1
			window._points = result["data"]["points"]
			window._options = result["data"]["options"]
			google.load "visualization", "1", {
				packages: ["corechart"]
				callback: ->
					data = google.visualization.arrayToDataTable window._points
					options = window._options
					#options["width"] = window.innerWidth/2
					chart = new google.visualization.LineChart (document.getElementById "graph_container")
					chart.draw data, options
					console.log "Done drawing graph."
					$("#graph_well").show "fast"
			}

@load_scoreboard = (name, query) ->
	window.scoreboard_name = name
	if name == "ranked"
		location.hash = ""
	else
		location.hash = "#" + name
	$("#scoreboardtable").slideUp "fast", "swing", () ->
		# $.ajax { url: "/static/scoreboard.json", "type": "GET", "dataType": "json", "cache": false }
		# $.getJSON "/static/scoreboard.json"
		api_call "GET", "/api/stats/scoreboard", {}
		.done (result) ->
			if result["success"] == 1
				tabs = [
					{ href: "ranked", title: "US Teams", active: name == "ranked" }
					{ href: "all", title: "All Teams", active: name == "all" }
				]
				_group = null
				if "groups" in (Object.keys result["data"])
					for group in result["data"]["groups"]
						tabs.push {
							href: group["gid"]
							title: group["name"]
							active: name == group["gid"]
						}
						if name == group["gid"]
							_group = group
				$("#scoreboard_list").html window.render_tab { tabs: tabs }
				scores = result["data"]["scores"]
				html = ""
				searchq = []
				rank = 1
				html += "<!-- <tr><td>0</td><td><a href='/team?EasyCTF'>EasyCTF</a></td><td>Various Schools</td><td>Infinity</td></tr> -->"
				for team in scores
					show = true
					if name == "ranked"
						show = team.observer == false
					else if name == "all"
						show = true
					else
						gmembers = _group["members"].map (obj) ->
							return obj["tid"]
						show = team["tid"] in gmembers
					if show
						if (query and query.length > 0 and ((team.teamname.toLowerCase().indexOf query.toLowerCase()) > -1 or (team.school and (team.school.toLowerCase().indexOf query.toLowerCase()) > -1))) or not(query and query.length > 0)
							html += "<tr" + (if team["my_team"] == true then " class='success'" else "") + ">"
							html += "<td>" + (if team.observer then '<span class="badge">' + rank + '</i></span>' else rank) + "</td>"
							html += "<td><a href=\"/team?" + encodeURIComponent(team.teamname) + "\">" + htmlEntities(team.teamname) + "</a></td>"
							html += "<td>" + (if team.school then htmlEntities(team.school) else '') + "</td>"
							html += "<td><span class='on_hover'>" + (Math.round team.points) + "<span class='decimal' style='display:none;color:#999;'>" + (team.points - (Math.round team.points)) + "</span></span></td>"
							html += "</tr>"
						if not(team.school in searchq)
							searchq.push team.teamname
						if team.school
							if not(team.school in searchq)
								searchq.push team.school
						rank += 1
				$("#scoreboardtable_body").html html
				$("#scoreboardtable").slideDown "fast", "swing"
				$("#team_query").typeahead "destroy"
				$("#team_query").typeahead { items: 10, minLength: 2, source: searchq }

@search_teams = () ->
	load_scoreboard window.scoreboard_name, $("#team_query").val()

$ ->
	initial = "ranked"
	if location.hash.length > 1
		initial = location.hash.substr 1
	window.render_tab = _.template $("#template_tab").remove().text()
	if (new Date()) > startDate
		load_graph()
	load_scoreboard initial, ""
	$(".on_hover").hover () ->
		$(this).child(".decimal").toggleClass "hidden_decimal"
		false
	false