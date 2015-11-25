from flask import request, session
from flask import Blueprint

import api
import json
import mimetypes
import os.path
import api.auth
import api.team

import api.problem

from api.annotations import *
from api.common import flat_multi
from api.exceptions import *

blueprint = Blueprint("problem_api", __name__)

@blueprint.route("/get_unlocked", methods=["GET"])
@api_wrapper
@require_login
@require_team
@block_before_competition("You can't view problems before the competition starts!")
def problem_get_unlocked_hook():
	problems = api.problem.get_unlocked()
	result = { "success": 1, "data": problems, "unlocked": len(problems), "total": api.problem.get_total_count() }
	user = api.user.get_user()
	if not("show_rules" in user and user["show_rules"] == True):
		result["show_rules"] = True
		db = api.common.db_conn()
		db.users.update_one({ "uid": user["uid"] }, { "$set": { "show_rules": True } })
	return result

@blueprint.route("/submit", methods=["POST"])
@api_wrapper
@require_login
@require_team
@block_before_competition("You can't submit problems before the competition starts!")
def problem_submit_hook():
	team = api.team.get_team()
	if team is None:
		raise WebException("You must be logged in to submit problems!")
	pid = request.form.get("pid")
	answer = request.form.get("answer")
	result = api.problem.submit(team["tid"], pid, answer, ip=request.remote_addr)
	return { "success": 1, "data": result }

@blueprint.route("/e_submit", methods=["POST"])
@api_wrapper
@require_login
@require_team
@block_before_competition("You can't submit easter eggs before the competition starts!")
def easter_egg_submit_hook():
	team = api.team.get_team()
	if team is None:
		raise WebException("You must be logged in to submit easter eggs!")
	answer = request.form.get("answer")
	result = api.problem.e_submit(team["tid"], answer, ip=request.remote_addr)
	return { "success": 1, "data": result }

@blueprint.route("/e_solved", methods=["GET"])
@api_wrapper
@require_login
@require_team
@block_before_competition("You can't view easter eggs before the competition starts!")
def easter_egg_solved_hook():
	solved = api.problem.e_solved_names()
	return { "success": 1, "data": solved }