import api
import sendgrid
import moment
from datetime import datetime

from api.exceptions import *
from api.user import hash_password

def send_email(params):
	if "email" not in params:
		raise WebException("Please enter an email >.>")
	
	db = api.common.db_conn()
	if db.users.count({ "email": params["email"].lower() }) != 1:
		raise WebException("That email was not found.")
	
	user = db.users.find_one({ "email": params["email"].lower() })
		
	db.password_recovery.update({
		"email": params["email"].lower()
	}, {
		"$set": { "active": False }
	}, multi=True)
	
	code = api.common.token()
	ticket = {
		"active": True,
		"code": code,
		"email": params["email"].lower(),
		"expire": datetime.utcnow().timestamp() + 60*60*24*2,
		"ip": params["ip"]
	}
	
	db.password_recovery.insert(ticket)
	sg = sendgrid.SendGridClient(api.config.sendgrid_apikey)
	
	message = sendgrid.Mail()
	message.add_to(params["email"])
	message.set_subject("Password Recovery")
	# please customize the message to change to your own domain
	message.set_html("<h1>Did you lose your password?</h1> <p>You requested a password change for the user <b>%s</b>. To continue, click this link:</p> <p><a href=\"https://www.yourctf.com/reset_password#%s\">https://www.yourctf.com/reset_password#%s</a></p> <p>and follow the directions on the page. If the link doesn't work, then try copy-pasting it into your browser. If the code doesn't show up, copy this code:</p> <p>%s</p> <p>If things still don't work out, shoot us an email at <a href=\"mailto:admin@yourctf.com\">admin@yourctf.com</a>.</p> <p>__<br /> YourCTF Team</p>" % (user["username"], code, code, code))
	# customize it to your own email
	message.set_from("Admin Team <admin@yourctf.com>")
	status, message = sg.send(message)
	
	return { "status": status, "message": message }

def reset_password(params):
	if not("code" in params and "password" in params and "confirm" in params):
		raise WebException("Please fill out all the fields.")
	
	if params["password"] != params["confirm"]:
		raise WebException("Your passwords don't match, silly!")
	
	db = api.common.db_conn()
	
	ticket = db.password_recovery.find_one({ "code": params["code"], "active": True })
	if ticket is None:
		raise WebException("That code doesn't seem to be right.")
	
	now = moment.utcnow().date.timestamp()
	expiredate = moment.unix(ticket["expire"], utc=True).date.timestamp()
	if now > expiredate:
		raise WebException("Your code expired!")
	
	db.password_recovery.update_one({ "code": params["code"], "active": True }, { "$set": { "active": False } })
	phash = hash_password(params["password"])
	db.users.update_one({ "email": ticket["email"].lower() }, { "$set": { "password": phash } })
	
	return