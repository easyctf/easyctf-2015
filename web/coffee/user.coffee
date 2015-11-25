$ ->
	username = decodeURIComponent (location.search.substring 1)
	$(".username").html htmlEntities(username)
	document.title = "User " + htmlEntities(username) + " - EasyCTF 2015"