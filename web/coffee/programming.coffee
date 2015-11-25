window.editor = undefined
ctrl = false

@runCode = () ->
	data = new FormData()
	data.append "language", $("#language").val()
	data.append "pid", $("#pid").val()
	data.append "program", window.editor.getValue()
	to_disable = "#upload_form input, #upload_form select"
	$(to_disable).attr "disabled", "disabled"
	$.ajax { type: "POST", url: "/api/programming/run_code", dataType: "json", data: data, processData: false, contentType: false }
	.done (result) ->
		class_name = if result.success == 1 then "success" else "warning"
		display_message "#upload_msg", class_name, result.message, () ->
			if result.success == 1
				$(to_disable).removeAttr "disabled"
				fetch_submissions()
		if result.success != 1
			$(to_disable).removeAttr "disabled"

@handle_upload = (e) ->
	e.preventDefault()
	data = new FormData()
	file = (document.getElementById "file").files[0]
	if file and file.name
		data.append "file", file, file.name
	data.append "language", $("#language").val()
	data.append "pid", $("#pid").val()
	# data = $("#upload_form").serializeObject()
	to_disable = "#upload_form input, #upload_form select"
	$(to_disable).attr "disabled", "disabled"
	$.ajax { type: "POST", url: "/api/programming/upload", dataType: "json", data: data, processData: false, contentType: false }
	.done (result) ->
		class_name = if result.success == 1 then "success" else "warning"
		display_message "#upload_msg", class_name, result.message, () ->
			if result.success == 1
				$(to_disable).removeAttr "disabled"
				fetch_submissions()
		if result.success != 1
			$(to_disable).removeAttr "disabled"

@viewLog = (token) ->
	api_call "GET", "/api/programming/stdout", { token: token }
	.done (result) ->
		if result.success == 1
			$("#stdoutModalLabel").html ("Output for " + result.pid + " <small>" + ((new Date(result.timestamp * 1000)).toISOString()) + "</small>")
			$("#stdoutModalBody").html ("<pre>" + result.data + "</pre>")
			$('#stdoutModal').modal {}
		

@fetch_problems = () ->
	api_call "GET", "/api/problem/get_unlocked", {}
	.done (result) ->
		if result.success == 1
			names = []
			for problem in result.data
				if problem["programming"] == true
					names.push { pid: problem["pid"], title: problem["title"] }
			namesOptions = ''
			for name in names
				namesOptions += '<option value=\'' + name["pid"] + '\'>' + name["title"] + '</option>'
			$('#pid').html namesOptions
			$('#pid').selectpicker("refresh")
	
@deleteRun = (p_token) ->
	if confirm("Are you sure you want to remove this program? This action is irreversible.")
		api_call "POST", "/api/programming/delete_run", { "p_token": p_token }
		.done (result) ->
			if result["success"] == 1
				display_message "#rr" + token + " td", "success", result["message"], () ->
					($("#r" + token)).slideUp "fast"
			else
				display_message "#rr" + token + " td", "danger", result["message"]

@fetch_submissions = () ->
	api_call "GET", "/api/programming/all", {}
	.done (result) ->
		if result.success == 1
			html = ""
			count = result.data.length
			for row in result.data
				html += "<tr id='rr" + row["token"] + "'><td colspan='5'></div></tr>"
				html += "<tr id='r" + row["token"] + "'>"
				html += "<td>" + '<div class=\'dropdown\'><a class=\'btn btn-default\' id=\'optbtn' + row['token'] + '\' data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false" data-target="#">' + count + '</a><ul class=\'dropdown-menu\' aria-labelledby=\'optbtn' + row['token'] + '\'><li><a href=\'javascript:void(0);\' onclick=\'javascript:viewLog("' + row['token'] + '");\'><i class=\'fa fa-eye fa-fw\'></i> View Log</a></li><li><a href=\'javascript:void(0);\' onclick=\'javascript:deleteRun("' + row['token'] + '");\'><i class=\'fa fa-trash fa-fw\'></i> Remove This Run</a></li></ul></div>' + "</td>"
				html += "<td>" + (if row["timestamp"] then "<span class='timeago' title='" + ((new Date(row["timestamp"] * 1000)).toISOString()) + "'></span>" else "<img src='/images/loading.gif' />") + "</td>"
				html += "<td>" + (if row["pid"] then row["pid"] else "<img src='/images/loading.gif' />") + "</td>"
				# html += "<td>" + (if row["signal"] then "<code>" + row["signal"] + "</code>" else "<img src='/images/loading.gif' />") + "</td>"
				html += "<td style='max-width:40vh;'>" + (if row["message"] then row["message"] else "<img src='/images/loading.gif' />") + "</td>"
				html += "<td>" + (if row["flag"] then "<span class='flag_hide'>" + row["flag"] + "</span>" else "<span class='no_flag'></span>") + "</td>"
				html += "</tr>"
				count -= 1
			$("#submissions_container").html html
			$(".flag_hide").each () ->
				flag = $(this).html()
				flag = flag.replace "'", "\'"
				$(this).html("<input type='password' class='form-control' value=\"" + flag + "\" onfocus=\"javascript:this.type='text';\" onblur=\"javascript:this.type='password';\" size='3' />")
			$(".no_flag").each () ->
				$(this).html("<input type='password' class='form-control' size='3' placeholder='No flag!' disabled />")
			$(".timeago").timeago()
			0
			
@loadCSS = (path) ->
	link = document.createElement "link"
	link.href = path
	link.type = "text/css"
	link.rel = "stylesheet"
	
	(document.getElementsByTagName "head")[0].appendChild link

$ ->
	redirect_if_not_logged_in(true)
	$("#upload_btn").on "click", handle_upload
	fetch_problems()
	si = setInterval fetch_submissions, 10000
	fetch_submissions()
	window.editor = CodeMirror (document.getElementById "editor-container"), {
		mode: "python",
		theme: "eclipse",
		lineNumbers: true,
	}
	
	$(document).keydown (e) ->
		if e.keyCode == 17
			ctrl = true
		return
	$(document).keyup (e) ->
		if e.keyCode == 13 and ctrl and window.editor.getValue().trim().length > 0
			runCode()
		else if e.keyCode == 17
			ctrl = false
		return
	
	$("#theme").on "change", (e) ->
		theme = e.target.value
		window.editor.setOption "theme", theme