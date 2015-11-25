from flask import request, session
from flask import Blueprint

import api
import json
import mimetypes
import os.path

import api.auth
import api.team

from api.annotations import *
from api.common import flat_multi
from api.exceptions import *

blueprint = Blueprint("team_api", __name__)

@blueprint.route("/public_info", methods=["GET"])
@api_wrapper
def team_public_info_hook():
	teamname = request.args.get("teamname")
	if api.team.get_team(teamname=teamname) is None:
		raise WebException("No team found under that name.")
	data = api.team.public_info(teamname=teamname)
	data["max_score"] = api.problem.get_max_points()
	return { "success": 1, "data": data }

@blueprint.route("/create", methods=["POST"])
@api_wrapper
@require_login
def team_create_hook():
	tid = api.team.create(api.common.flat_multi(request.form))
	return { "success": 1, "message": "Your team was successfully created!" }

@blueprint.route("/members", methods=["GET"])
@api_wrapper
def team_members_hook():
	members = api.team.members()
	return { "success": 1, "data": members }

@blueprint.route("/join", methods=["POST"])
@api_wrapper
@require_login
def team_join_hook():
	if request.form.get("join_code") is None or len(request.form.get("join_code")) < 1:
		raise WebException("Please provide a join code.")
	join_code = request.form.get("join_code")
	message = api.team.join(join_code)
	return { "success": 1, "message": message }

@blueprint.route("/join_code", methods=["GET"])
@api_wrapper
@require_login
@require_team
def team_join_code_hook():
	code = api.team.join_code()
	return { "success": 1, "data": code }

@blueprint.route("/join_code/new", methods=["POST"])
@api_wrapper
@require_login
@require_team
def team_join_code_new_hook():
	code = api.team.join_code(force=True)
	return { "success": 1, "data": code }

@blueprint.route("/remove", methods=["POST"])
@api_wrapper
@require_login
@require_team
def team_remove_hook():
	if api.auth.is_logged_in() and api.user.in_team():
		uid = request.form.get("uid")
		user = api.user.get_user()
		if uid == user["uid"]:
			confirm = request.form.get("confirm")
			team = api.team.get_team()
			if confirm != team["teamname"]:
				raise WebException("Please confirm your name.")
		message = api.team.remove(uid)
		return { "success": 1, "message": message }
	else:
		raise WebException("Stop. Just stop.")

@blueprint.route("/info", methods=["GET"])
@api_wrapper
@require_login
def team_info_hook():
	team = api.team.get_team()
	team_info = {
		"tid": team['tid'],
		"teamname": team['teamname'],
		"members": api.team.members(),
	}
	if "school" in team: team_info["school"] = team["school"]
	return { "success": 1, "data": team_info }
	
@blueprint.route("/update", methods=["POST"])
@api_wrapper
@require_login
def team_update_hook():
	updated = api.team.update(api.common.flat_multi(request.form))
	if updated: return { "success": 1, "message": "saved!" }
	else: return { "success": 0, "message": "nothing updated." }

@blueprint.route("/schools", methods=["GET"])
@api_wrapper
@require_login
def team_schools_hook():
	schools = api.team.get_schools()
	return { "success": 1, "data": schools }
	
@blueprint.route("/shell", methods=["GET"])
@api_wrapper
@require_login
def team_shell_hook():
	team = api.team.get_team()
	if "shell_user" in team and "shell_pass" in team:
		return {
			"success": 1,
			"user": team["shell_user"],
			"pass": team["shell_pass"]
		}
	else:
		shell_account = api.team.assign_shell_account(team["tid"])
		print(shell_account)
		return {
			"success": 1,
			"user": shell_account["username"],
			"pass": shell_account["password"]
		}