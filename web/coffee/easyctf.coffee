window.startDate = new Date("03 Nov 2015 20:00:00 GMT-0600")
window.endDate = new Date("11 Nov 2015 20:00:00 GMT-0600")

message_duration = 2500

@api_call = (method, url, data) ->
	if method == "POST" and $.cookie("token")
		data.token = $.cookie("token")
   
	$.ajax {url: url, type: method, data: data, dataType: "json", cache: false}
	.fail (jqXHR, text) ->
		$("#site-message").slideUp "fast", "swing", ->
			$("#site-message").html "<div class='alert alert-danger' style='margin:0;'>" + "<div class='container'>The EasyCTF API server is currently down. We're working on this to fix this error right away. Follow <a href='http://twitter.com/easyctf' target='_blank' style='color:#fff;'>@easyctf</a> for status updates.</div>" + "</div>"
			$("#site-message").slideDown "fast", "swing"

@display_message = (target, type, message, callback) ->
	window._callback = callback
	$(target).slideUp "fast", "swing", ->
		$(target).html "<div class='alert alert-" + type + "'" + ("#site-message" in target ? " style='margin:0'" : "") + ">" + message + "</div>"
		$(target).slideDown "fast", "swing", ->
			setTimeout (->
				$(target).slideUp "fast", "swing", ->
					$(target).html ""
					if window._callback
						window._callback()
			), message_duration

@display_message_permanent = (target, type, message, callback) ->
	window._callback = callback
	$(target).slideUp "fast", "swing", ->
		$(target).html "<div class='alert alert-" + type + "'" + ("#site-message" in target ? " style='margin:0'" : "") + ">" + message + "</div>"
		$(target).slideDown "fast", "swing", ->
			if window._callback
				window._callback()

@redirect_if_not_logged_in = (is_protected) ->
	api_call "GET", "/api/user/info", {}
	.done (result) ->
		if result.success == 0 or (result.data and result.data.logged_in != true)
			location.href = "/login"
		else
			if is_protected == true
				if not(result.data.type == 0 or new Date() > window.startDate)
					location.href = "/account"

@load_navbar = () ->
	api_call "GET", "/api/user/info", {}
	.done (result) ->
		if result.success == 0 or (result.data and result.data.logged_in != true)
			$("#nologin-nav").show()
		else
			$(".account_link").html("<img src='//www.gravatar.com/avatar/" + result.data.email_hash + "?size=20' class='navatar'>" + result.data.username)
			if result["data"]["team"] == false
				if result.data.type == 2
					$("#teacher-nav").show()
				else
					$("#noteam-nav").show()
			else
				if ((new Date()) > window.startDate and result.data.team and result.data.team.length > 0) or result.data.type == 0
					$("#competition-nav").show()
				else if result.data.type == 2
					$("#teacher-nav").show()
				else
					$("#login-nav").show()

@getQueryParams = (qs) ->
	qs = qs.split('+').join(' ')
	params = {}
	tokens = undefined
	re = /[?&]?([^=]+)=([^&]*)/g
	while tokens = re.exec(qs)
		params[decodeURIComponent(tokens[1])] = decodeURIComponent(tokens[2])
	params

@merge_options = (obj1, obj2) ->
	`var attrname`
	obj3 = {}
	for attrname of obj1
		obj3[attrname] = obj1[attrname]
	for attrname of obj2
		obj3[attrname] = obj2[attrname]
	obj3

@load_site_message = () ->
	""
	
@escape_ = (string) ->
	return string.replace(/ /g, "&nbsp;")

@htmlEntities = (str) ->
	String(str).replace(/&/g, '&amp;').replace(/\s/g, '&nbsp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace /"/g, '&quot;'
   
$.fn.serializeObject = ->
	o = {}
	a = this.serializeArray()
	$.each(a, ->
		if o[this.name]
			if !o[this.name].push
				o[this.name] = [o[this.name]]
			o[this.name].push(this.value || '')
		else
			o[this.name] = this.value || ''
	)
	return o

$ ->
	load_navbar()
	load_site_message()
	
	date = new Date()
	if date.getMonth() == 9 and date.getDate() == 11
		load_alt_stylesheet()