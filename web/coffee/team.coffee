$ ->
	teamname = decodeURIComponent (location.search.substring 1)
	$(".teamname").html htmlEntities(teamname)
	document.title = "Team " + teamname + " - EasyCTF 2015"
	
	api_call "GET", "/api/team/public_info", { teamname: teamname }
	.done (result) ->
		$.getJSON "/api/stats/scoreboard"
		.done (sc_result) ->
			if result.success == 1 and sc_result.success == 1
				team = result.data
				scoreboard = sc_result["data"]["scores"]
				for team_entry in scoreboard
					if team_entry["tid"] == team["tid"]
						team = merge_options team, team_entry
						break
				console.log team
				if team["school"]
					$("#school").html team["school"]
				$("#num_members").html team["members"].length
				html = "<ul>"
				for member in team["members"]
					html += "<li><a href='/user?" + encodeURIComponent(member["username"]) + "'>" + htmlEntities(member["name"]) + "</a></li>"
				html += "</ul>"
				$("#members").html html
				if team["rank"]
					$("#rank").html team["rank"]
				if team["score"]
					$("#score").html team["score"]
				if team["points"] > 0 and "category_breakdown" in Object.keys(team)
					html = ""
					
					google.load "visualization", "1", {
						packages: ["corechart"]
						callback: ->
							data = google.visualization.arrayToDataTable result["data"]["score_progression"]["points"]
							options = result["data"]["score_progression"]["options"]
							chart = new google.visualization.LineChart (document.getElementById "graph_container")
							chart.draw data, options
							console.log "Done drawing graph."	
							$("#graph_container").show "fast"
					}
					
					solved = []
					for category in (Object.keys team["category_breakdown"])
						for problem in team["category_breakdown"][category]
							if problem["solved"] == true
								solved.push problem
					solved.sort ((x, y) ->
						if x["timestamp"] < y["timestamp"]
							return 1
						if x["timestamp"] > y["timestamp"]
							return -1
						return 0
					)
					for problem in solved
						newDate = new Date()
						newDate.setTime problem["timestamp"] * 1000
						html += "<tr>"
						html += "<td>" + problem["problem"] + "</td>"
						html += "<td>" + problem["category"] + "</td>"
						html += "<td>" + ((Math.round ((parseFloat problem["points"]) * 100)) / 100) + "</td>"
						html += "<td><span class='timeago' title='" + (newDate.toISOString()) + "'></span></td>"
						html += "</tr>"
					$("#teaminfo_body").html html
					$(".timeago").timeago()
					$("#teaminfo_score").slideDown "fast"
					false
				$("#teaminfo").slideDown "fast"
			else
				$("#comments_section").hide()
				$("#error_1").slideDown "fast"