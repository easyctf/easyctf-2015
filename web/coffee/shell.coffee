@retrieve_credentials = () ->
	api_call "GET", "/api/team/shell"
	.done (result) ->
		if result.success == 1
			$("#credentials").html "username: <code>" + result.user + "</code> | password: <code>" + result.pass + "</code>. For SSH, <code>ssh " + result.user + "@ssh.easyctf.com</code>."
		else
			$("#credentials").html "Retrieving failed... <a href='javascript:retrieve_credentials();' class='btn btn-info'>try again?</a>"
			
$ ->
	redirect_if_not_logged_in(true)