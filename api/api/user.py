import bcrypt, re, urllib, flask, requests
import api
import api.auth

import mailchimp

from voluptuous import Schema, Length, Required
from api.schemas import verify_to_schema, check
from api.exceptions import *
from flask import request

__check_email_format = lambda email: re.match(r".+@.+\..{2,}", email) is not None
__check_ascii = lambda s: all(ord(c) < 128 for c in s)
__check_username = lambda username: get_user(username_lower=username.lower()) is None
__check_email = lambda email: get_user_by_email(email) is None

UserSchema = Schema({
	Required("email"): check(
		([str, Length(min=4, max=128)], "Your email should be between 4 and 128 characters long."),
		([__check_email], "Someone already registered this email."),
		([__check_email_format], "Please enter a legit email.")
	),
	Required("name"): check(
		([str, Length(min=4, max=128)], "Your name should be between 4 and 128 characters long.")
	),
	Required("username"): check(
		([str, Length(min=4, max=32)], "Your username should be between 4 and 32 characters long."),
		([__check_ascii], "Please only use ASCII characters in your username."),
		([__check_username], "This username is taken, did you forget your password?")
	),
	Required("password"): check(
		([str, Length(min=4, max=64)], "Your password should be between 4 and 64 characters long."),
		([__check_ascii], "Please only use ASCII characters in your password."),
	),
	Required("type"): int,
	"notify": str
}, extra=True)

""" /api/user/create """

def create(params):
	if "g-recaptcha-response" not in params:
		raise WebException("Please do the captcha.")
	captcha_response = params["g-recaptcha-response"]
	del params["g-recaptcha-response"]
	if "type" in params:
		params["type"] = int(params["type"])
	r = requests.post("https://www.google.com/recaptcha/api/siteverify", data={
		"secret": api.config.recaptcha_secret,
		"response": captcha_response,
		"remoteip": request.remote_addr
	})
	if not r.json()["success"] == True: raise WebException("Please do the captcha.")
	verify_to_schema(UserSchema, params)
	db = api.common.db_conn()
	uid = "user_" + api.common.token()
	if "notify" in params and params["notify"] == "on":
		r = requests.post("https://us11.api.mailchimp.com/2.0/lists/subscribe", data={
			"apikey": api.config.mailchimp_secret,
			"id": api.config.mailchimp_subscriber_list,
			"email[email]": params["email"]
		})
	user = {
		"uid": uid,
		"name": params["name"],
		"username": params["username"],
		"username_lower": params["username"].lower(),
		"email": params["email"].lower(),
		"password": hash_password(params["password"]),
		"type": int(params["type"])
	}
	db.users.insert(user)
	return uid

def is_teacher():
	user = get_user()
	return user["type"] == 2

def update_user(user, name, nPassword, cPassword):
	db = api.common.db_conn()
	if not(cPassword is not None and api.auth.confirm_password(cPassword, user["password"])):
		raise WebException("Please enter your current password.")
	update = {
		"name": name,
		"password": hash_password(nPassword) if (nPassword is not None and len(nPassword) > 0) else user["password"],
	}
	db.users.update_one({ "uid": user["uid"] }, {
		"$set": update
	})
	return True
	
""" Helper functions """

def get_user(username=None, username_lower=None, uid=None):
	db = api.common.db_conn()
	match = {}
	if username != None:
		match.update({ "username": username })
	elif username_lower != None:
		match.update({ "username_lower": username_lower })
	elif uid != None:
		match.update({ "uid": uid })
	elif api.auth.is_logged_in():
		match.update({ "uid": api.auth.get_uid() })
	else:
		return None
	result = db.users.find_one(match)
	return result

def get_user_by_email(email):
	db = api.common.db_conn()
	match = {}
	if email != None:
		match.update({ "email": email.lower() })
	else:
		raise InternalException("Please provide an email.")
	result = db.users.find_one(match)
	return result

def in_team():
	user = get_user()
	return "team" in user and len(user["team"]) > 1
	
def hash_password(password):
	return bcrypt.hashpw(password, bcrypt.gensalt(8))