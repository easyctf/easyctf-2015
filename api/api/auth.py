import api.user
import bcrypt

from api.exceptions import *
from api.schemas import check, verify_to_schema

from flask import session
from voluptuous import Schema, Required, Length

UserLoginSchema = Schema({
	Required('username'): check(
		([str, Length(min=3, max=50)], "Usernames must be between 3 and 50 characters."),
	),
	Required('password'): check(
		([str, Length(min=3, max=50)], "Passwords must be between 3 and 50 characters.")
	)
})

def confirm_password(attempt, actual):
	return bcrypt.hashpw(attempt, actual) == actual

def login(username, password):
	verify_to_schema(UserLoginSchema, { "username": username, "password": password })
	user = api.user.get_user(username_lower=username.lower())
	if user is None:
		raise WebException("No user with that username exists!")
	if user.get("disabled", False):
		raise WebException("This account is disabled.")
	if confirm_password(password, user["password"]):
		if user["uid"] is not None:
			session["uid"] = user["uid"]
			if user["type"] == 0:
				session["admin"] = True
			session.permanent = True
		else:
			raise WebException("Login error. Error code: 1.")
	else:
		raise WebException("Wrong password.")

def logout():
	session.permanent = False
	if "uid" in session: session.pop("uid")
	session["admin"] = False
	if "uid" in session: del session["uid"]
	session.clear()

def is_logged_in():
	logged_in = "uid" in session
	if logged_in and not api.user.get_user(uid=session["uid"]):
		logout()
		return False
	return logged_in
	
def get_uid():
	if is_logged_in():
		return session['uid']
	else:
		return None