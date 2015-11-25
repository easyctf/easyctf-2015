from flask import request, session, redirect
from flask import Blueprint

import api
import json
import mimetypes
import os.path
import api.auth
import hashlib

from api.annotations import api_wrapper
from api.common import flat_multi
from api.exceptions import *

blueprint = Blueprint("user_api", __name__)

@blueprint.route("/create", methods=["POST"])
@api_wrapper
def user_create_hook():
	uid = api.user.create(api.common.flat_multi(request.form))
	session["uid"] = uid
	return { "success": 1, "message": "You've successfully registered!" }

@blueprint.route("/login", methods=["POST"])
@api_wrapper
def user_login_hook():
	username, password = request.form.get('username'), request.form.get('password')
	api.auth.login(username, password)
	return { "success": 1, "message": "Successfully logged in!" }
	
@blueprint.route("/logout", methods=["GET", "POST"])
def user_logout_hook():
	api.auth.logout()
	return redirect("/")

@blueprint.route("/update", methods=["POST"])
@api_wrapper
def user_update_hook():
	user = api.user.get_user()
	if user is None:
		raise WebException("You must be logged in.")
	name, nPassword, cPassword = request.form.get("name"), request.form.get("nPassword"), request.form.get("cPassword")
	api.user.update_user(user, name, nPassword, cPassword)
	return { "success": 1, "message": "Successfully updated your settings." }
	
@blueprint.route("/info", methods=["GET"])
@api_wrapper
def user_info_hook():
	logged_in = api.auth.is_logged_in()
	if logged_in:
		user = api.user.get_user()
		in_team = api.user.in_team()
		team = None
		if in_team:
			team = api.team.get_team()
		req = api.common.flat_multi(request.form)
		user_info = { "success": 1, "data": {
			"logged_in": logged_in,
			"type": user['type'],
			"username": user['username'] if logged_in else "",
			"team": user['team'] if in_team else False,
			"teamowner": user['uid'] == team['owner'] if in_team else False,
			"name": user['name'],
			"email": user['email'],
			"email_hash": hashlib.md5(user['email'].encode('utf-8')).hexdigest(),
			"uid": user['uid']
		} }
		panels = ["_settings"]
		if user["type"] == 0:
			panels.append("_updates")
		if in_team:
			panels.append("_team")
		else:
			panels.append("_noteam")
		# else:
			# panels.append("_groups")
		user_info["data"]["panels"] = panels
		return user_info
	else:
		raise WebException("You must be logged in.")